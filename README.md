# QALQIO AI-Native Repo + Agentic RAG Demo

A local-first, API-first Agentic RAG starter with isolated knowledge profiles, evidence-grounded answers, short-lived session memory, deterministic tests, Docker packaging, and GitHub Actions CI.

## GitHub description

AI-native repository starter and Agentic RAG workshop demo: reusable project specs, agent guidance, and a staged path from repo setup to GitHub Spec Kit and Superpowers.

## Purpose

Demonstrate an AI-native software workflow and a bounded Agentic RAG application. This first implementation provides three isolated use-case profiles, a FastAPI interface, Qdrant local storage, SQLite session memory, an OpenAI Responses API adapter, and a mock mode for offline development.

The service is intended for local workshops and development. It has no authentication and must not be exposed to the public internet as-is. Use fictional or approved public materials only.

## Starter contents

| Path | Purpose |
|---|---|
| AGENTS.md | Shared instructions for coding agents |
| agents/roles.md | Suggested roles for the RAG demo |
| .specify/memory/constitution.md | Project principles and decision boundaries |
| docs/templates/prompt-requirements.md | Turn a prompt into testable requirements |
| .specify/templates/spec-template.md | Feature specification template |
| .specify/templates/plan-template.md | Lightweight implementation plan |
| .specify/templates/tasks-template.md | Implementation task breakdown |
| specs/001-agentic-rag-demo/spec.md | Initial scope and open decisions |
| .env.example | Configuration names only; no secrets |
| LICENSE | MIT text with rights-holder placeholder |
| src/agentic_rag | FastAPI, profile registry, retrieval, memory, and model adapters |
| tests | API and behavior tests using in-memory Qdrant and mock generation |
| Dockerfile / compose.yaml | Local container build and run configuration |
| .github/workflows/ci.yml | Pull request and main-branch CI, including a container API smoke test |
| sample_data | Fictional documents for the three isolated demo profiles |

## First steps

1. Replace [COPYRIGHT HOLDER] in LICENSE with the correct rights holder before publishing.
2. Review AGENTS.md and the constitution; make them match the team's actual rules.
3. Complete the initial spec. Select the demo scenario and approved sources before choosing implementation details.
4. Create a numbered feature directory and copy the spec template there.
5. Commit the starter baseline before adding workflow tools.

## Evolution path

### 1. Start with this spec pack

Use the constitution, prompt requirements, feature spec, plan, and tasks to make intent and acceptance criteria reviewable. These are project-owned starting points, not a replacement for a full methodology.

### 2. Add GitHub Spec Kit

Follow the current instructions in the [official GitHub Spec Kit documentation](https://github.github.com/spec-kit/). Spec Kit can set up agent-specific command files and guide a structured flow from specification through implementation and convergence.

Review generated files before committing. Keep one authoritative version of each rule and template. Spec Kit evolves, so use its current setup guide rather than pinning an old command here.

### 3. Add Superpowers

When the team wants reusable agent skills for design, planning, implementation, testing, review, debugging, and branch completion, install [Superpowers](https://github.com/obra/superpowers) for the coding-agent harness in use. Installation differs by harness; follow its current official README.

Treat Superpowers as the workflow layer. Keep QALQIO domain rules, privacy constraints, architecture decisions, tool permissions, and acceptance criteria in this repository. Extend the workflow only for recurring needs; do not copy upstream skills without a maintenance reason.

See the [Spec Kit + Superpowers workflow guide](docs/Superpowers_Workflow_Guide.md) for the ownership map, per-agent setup notes, and a sample feature to take through prep, build, test, and ship. The sample spec is not implemented yet.

## RAG evidence path

1. A user asks a question.
2. The system identifies needed information and chooses permitted retrieval tools.
3. Retrieval returns passages and source metadata.
4. The system checks evidence sufficiency and relevance.
5. The response cites supporting sources or states uncertainty.
6. The agent may refine the query or ask a bounded follow-up; it must not invent evidence.
7. Evaluation checks retrieval, citations, groundedness, and safe handling of missing evidence.

Specify memory separately from document retrieval. Do not silently persist user content or treat conversation memory as an authoritative source.

## Local setup

~~~bash
git clone https://github.com/qalqio-ai/workshop-agentic-rag.git
cd workshop-agentic-rag
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install --no-deps -e .
cp .env.example .env
uvicorn agentic_rag.main:app --reload
~~~

The default mock model and hash embedder require no API key. Visit http://127.0.0.1:8000/docs for interactive API docs. Set MODEL_PROVIDER=openai and provide OPENAI_API_KEY in .env to use the configured OpenAI Responses API model. The model name defaults to gpt-4.1-mini and can be changed with MODEL_NAME.

### Run tests locally

~~~bash
./scripts/test.sh
~~~

The test suite uses a temporary in-memory Qdrant collection and a SQLite file under pytest's temporary directory. It does not call an LLM API.

### Run with Docker Compose

~~~bash
docker compose up --build -d
docker compose ps
python scripts/api_smoke.py
docker compose down
~~~

The container defaults to mock mode and persists Qdrant and session data in named Docker volumes. To keep data only for one run, use docker compose down --volumes.

After the API is running, load one synthetic document for each profile with:

~~~bash
python scripts/seed_samples.py
~~~

### API request examples

Ingest a document:

~~~bash
curl -sS http://127.0.0.1:8000/v1/documents \
  -H 'Content-Type: application/json' \
  -d '{"use_case_id":"workshop-knowledge","source_id":"quickstart","title":"Quickstart","text":"Start the API with Docker Compose."}'
~~~

Ask a question:

~~~bash
curl -sS http://127.0.0.1:8000/v1/query \
  -H 'Content-Type: application/json' \
  -d '{"use_case_id":"workshop-knowledge","question":"How do I start the API with Docker?"}'
~~~

The query response includes an evidence status, citations, session ID, and trace ID. An unsupported question returns an insufficient-evidence response with no citations.

## CI and Docker verification

Pull requests and pushes to main run Python compile, Ruff, and pytest checks, then build the Docker image, start the API container, and perform black-box health, profile, ingestion, query, and citation checks. Run the same Python checks locally with ./scripts/test.sh.

## Runtime boundaries

- Each configured use case has a separate Qdrant collection; requests never search across profiles.
- Session memory is stored in SQLite, scoped to a session and use case, and expires after the configured TTL.
- Retrieved documents are untrusted evidence. Instructions in a document cannot replace the system policy.
- The mock model is the default. The OpenAI adapter is optional and reads its key from the environment.
- This demonstration has no authentication, rate limiting, tenant management, or production hardening.

Never commit .env, API keys, private corpora, local Qdrant data, SQLite files, or real user data.

## Public repository checklist

- [ ] Confirm the rights holder in LICENSE.
- [ ] Remove internal, private, and customer material before committing.
- [ ] Add only synthetic or approved demo documents.
- [ ] Review repository visibility and organization policy.
- [ ] Record the scenario and data-handling rules in a feature spec.

## Upstream references

- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Spec Kit documentation](https://github.github.com/spec-kit/)
- [Superpowers](https://github.com/obra/superpowers)
