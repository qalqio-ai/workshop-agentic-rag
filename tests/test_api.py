from fastapi.testclient import TestClient
import pytest
from dataclasses import replace

from agentic_rag import main
from agentic_rag.memory import SessionMemory
from agentic_rag.retrieval import ProfileStore


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "ProfileStore", lambda _path: ProfileStore(":memory:", in_memory=True))
    monkeypatch.setattr(
        main,
        "settings",
        replace(main.settings, session_db_path=str(tmp_path / "sessions.sqlite3")),
    )
    with TestClient(main.app) as test_client:
        yield test_client


def ingest(client, profile="workshop-knowledge", text="Run the API with Docker Compose."):
    return client.post(
        "/v1/documents",
        json={
            "use_case_id": profile,
            "source_id": "quickstart",
            "title": "Workshop Quickstart",
            "text": text,
        },
    )


def test_health_profiles_and_openapi(client):
    assert client.get("/health").json() == {"status": "ok"}
    profiles = client.get("/v1/use-cases").json()
    assert {profile["id"] for profile in profiles} == {
        "workshop-knowledge",
        "policy-handbook",
        "technical-troubleshooting",
    }
    assert client.get("/openapi.json").status_code == 200


def test_ready_reports_available_store_without_using_query_paths(client, monkeypatch):
    store = client.app.state.store

    def forbidden(*args, **kwargs):
        raise AssertionError("readiness must not use query or mutation paths")

    monkeypatch.setattr(main, "get_model", forbidden)
    monkeypatch.setattr(store, "add", forbidden)
    monkeypatch.setattr(store, "search", forbidden)
    monkeypatch.setattr(store.embedder, "embed", forbidden)
    monkeypatch.setattr(client.app.state.memory, "get", forbidden)
    monkeypatch.setattr(client.app.state.memory, "put", forbidden)

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_ready_reports_unavailable_store_without_error_details(client, monkeypatch):
    monkeypatch.setattr(client.app.state.store, "is_available", lambda: False)

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "not_ready"}


def test_openapi_publishes_ready_contract(client):
    responses = client.get("/openapi.json").json()["paths"]["/ready"]["get"]["responses"]

    assert set(responses) == {"200", "503"}


def test_ingest_and_grounded_query_return_valid_citation(client):
    assert ingest(client).status_code == 200
    result = client.post(
        "/v1/query",
        json={"use_case_id": "workshop-knowledge", "question": "How do I run the API with Docker?"},
    )
    assert result.status_code == 200
    body = result.json()
    assert body["evidence_status"] == "grounded"
    assert body["citations"] == [
        {"source_id": "quickstart", "title": "Workshop Quickstart", "chunk_id": "quickstart-001"}
    ]
    assert body["trace_id"]


def test_unsupported_question_abstains_without_citations(client):
    ingest(client)
    result = client.post(
        "/v1/query",
        json={
            "use_case_id": "workshop-knowledge",
            "question": "What is the reimbursement deadline for overseas travel?",
        },
    )
    assert result.status_code == 200
    assert result.json()["evidence_status"] == "insufficient"
    assert result.json()["citations"] == []
    assert "not have enough evidence" in result.json()["answer"]


def test_use_case_isolation_and_unknown_profile(client):
    ingest(client)
    result = client.post(
        "/v1/query",
        json={
            "use_case_id": "policy-handbook",
            "question": "How do I run the API with Docker?",
            "session_id": "shared-session",
        },
    )
    assert result.json()["evidence_status"] == "insufficient"
    assert result.json()["citations"] == []
    assert client.post(
        "/v1/documents",
        json={"use_case_id": "not-configured", "source_id": "x", "title": "x", "text": "x"},
    ).status_code == 404


def test_validation_and_session_delete(client):
    response = client.post(
        "/v1/query",
        json={"use_case_id": "workshop-knowledge", "question": " "},
    )
    assert response.status_code == 422
    session = "session-to-delete"
    client.app.state.memory.put(session, "workshop-knowledge", "private turn")
    assert client.app.state.memory.get(session, "workshop-knowledge") == "private turn"
    assert client.delete(f"/v1/sessions/{session}").json()["status"] == "deleted"
    assert client.app.state.memory.get(session, "workshop-knowledge") is None


def test_session_memory_expires(tmp_path, monkeypatch):
    clock = [100.0]
    monkeypatch.setattr("agentic_rag.memory.time.time", lambda: clock[0])
    memory = SessionMemory(str(tmp_path / "ttl.sqlite3"), ttl_seconds=5)
    memory.put("s1", "workshop-knowledge", "context")
    assert memory.get("s1", "workshop-knowledge") == "context"
    clock[0] += 6
    assert memory.get("s1", "workshop-knowledge") is None

def test_get_use_case_detail(client):
    response = client.get("/v1/use-cases/workshop-knowledge")
    assert response.status_code == 200
    assert response.json() == {
        "id": "workshop-knowledge",
        "name": "Workshop knowledge assistant",
        "description": "Answers from the workshop guide corpus.",
    }

    missing = client.get("/v1/use-cases/not-configured")
    assert missing.status_code == 404
    assert missing.json()["detail"]["code"] == "unknown_use_case"
