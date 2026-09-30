from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request

from .agent import get_model
from .config import settings
from .memory import SessionMemory
from .models import Citation, DocumentIn, QueryIn, QueryOut
from .profiles import USE_CASES
from .retrieval import ProfileStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.store = ProfileStore(settings.qdrant_path)
    app.state.memory = SessionMemory(settings.session_db_path, settings.session_ttl_seconds)
    yield
    app.state.store.close()


app = FastAPI(
    title="Workshop Agentic RAG API",
    version="0.1.0",
    description="Local-first, profile-scoped retrieval with evidence-backed answers.",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/v1/use-cases")
def list_use_cases():
    return [{"id": item.id, "name": item.name, "description": item.description} for item in USE_CASES.values()]


@app.post("/v1/documents")
def ingest_document(body: DocumentIn, request: Request):
    if body.use_case_id not in USE_CASES:
        raise HTTPException(status_code=404, detail={"code": "unknown_use_case"})
    first_chunk = request.app.state.store.add(body.use_case_id, body.source_id, body.title, body.text)
    return {"status": "ingested", "source_id": body.source_id, "first_chunk_id": first_chunk}


@app.post("/v1/query", response_model=QueryOut)
def query(body: QueryIn, request: Request):
    if body.use_case_id not in USE_CASES:
        raise HTTPException(status_code=404, detail={"code": "unknown_use_case"})
    trace_id = str(uuid4())
    session_id = body.session_id or str(uuid4())
    memory: SessionMemory = request.app.state.memory
    context = memory.get(session_id, body.use_case_id)
    store: ProfileStore = request.app.state.store
    evidence = store.search(body.use_case_id, body.question, limit=5)

    # Retry retrieval at most once with normalized text if the first evidence is weak.
    if evidence and max(item.score for item in evidence) < settings.evidence_threshold:
        refined = " ".join(dict.fromkeys(body.question.lower().split()))
        if refined != body.question:
            evidence = store.search(body.use_case_id, refined, limit=5)

    grounded = bool(evidence) and max(item.score for item in evidence) >= settings.evidence_threshold
    answer = get_model().answer(body.question, evidence if grounded else [], context)
    citations = (
        [Citation(source_id=item.source_id, title=item.title, chunk_id=item.chunk_id) for item in evidence]
        if grounded
        else []
    )
    memory.put(session_id, body.use_case_id, f"Q: {body.question}\nA: {answer}")
    return QueryOut(
        answer=answer,
        evidence_status="grounded" if grounded else "insufficient",
        citations=citations,
        session_id=session_id,
        trace_id=trace_id,
    )


@app.delete("/v1/sessions/{session_id}")
def delete_session(session_id: str, request: Request):
    request.app.state.memory.delete(session_id)
    return {"status": "deleted", "session_id": session_id}

@app.get("/v1/use-cases/{use_case_id}")
def get_use_case(use_case_id: str):
    item = USE_CASES.get(use_case_id)
    if item is None:
        raise HTTPException(status_code=404, detail={"code": "unknown_use_case"})
    return {"id": item.id, "name": item.name, "description": item.description}