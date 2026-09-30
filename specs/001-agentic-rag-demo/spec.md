# Feature Specification: Multi Use Case Agentic RAG API

**Feature ID:** 001-agentic-rag-demo  
**Status:** Implementation baseline  
**Owner:** QALQIO workshop team  
**Last updated:** 2026-09-29

## Outcome
Provide a local-first, API-first starter that answers questions from one selected knowledge profile, returns source citations, abstains when evidence is inadequate, and keeps short-lived session context separate from indexed documents.

The full implementation brief is [Agentic RAG Multi Use Case API Starter PRD](../../docs/Agentic_RAG_Multi_Use_Case_API_Starter_PRD.md). This feature spec and its acceptance criteria remain the implementation source of truth for this thin slice.

## Included profiles

- `workshop-knowledge`: fictional workshop quickstart material
- `policy-handbook`: synthetic policy examples
- `technical-troubleshooting`: synthetic troubleshooting guidance

Each profile uses an isolated Qdrant collection and session scope. The sample data is fictional. The application is for localhost workshops and development; it has no authentication and is not internet-ready.

## Selected implementation baseline

- Python 3.12+, FastAPI, and OpenAPI documentation
- Qdrant local mode with a replaceable embedding adapter; deterministic hash embeddings in mock mode and FastEmbed when using the live provider
- SQLite session memory with configurable TTL and explicit deletion
- Mock answer generation by default; optional OpenAI Responses API adapter with configurable model name
- Dockerfile and Docker Compose for local container execution
- GitHub Actions on pull requests and pushes to `main`, including Python checks, Docker image build, and container API smoke tests

The live-model default is `gpt-4.1-mini`; change `MODEL_NAME` through environment configuration. Automated tests must remain offline and must not call a paid model API.

## API contract

- `GET /health`
- `GET /v1/use-cases`
- `POST /v1/documents` for plain text and Markdown content with profile and source metadata
- `POST /v1/query` with profile ID, question, and optional session ID
- `DELETE /v1/sessions/{session_id}`

Query responses include answer, evidence status, citations, session ID, and trace ID. Citations are generated from retrieved chunk metadata and must never be invented by the model.

## Safety and data requirements

- A request searches only the selected profile.
- Retrieved documents are untrusted evidence and cannot override system or project instructions.
- Insufficient evidence produces an explicit abstention and no citations.
- No consequential actions, arbitrary code tools, public network exposure, private customer data, or real credentials.
- Session state is scoped to both session and profile, expires by TTL, and supports deletion.
- Provider errors and secrets are not returned to callers or written to logs.

## Acceptance criteria

- **AC-001:** A clean environment can install dependencies and run the API using the README.
- **AC-002:** Health, use-case listing, ingestion, query, and session deletion endpoints are documented in OpenAPI.
- **AC-003:** A supported question returns evidence-backed text and citations that map to retrieved source/chunk IDs.
- **AC-004:** An unsupported question returns `insufficient` status and an empty citation list.
- **AC-005:** Retrieval and session context do not cross use-case boundaries.
- **AC-006:** Empty or whitespace-only questions, malformed requests, and unknown profiles are rejected safely.
- **AC-007:** Session TTL and deletion behavior are covered by tests.
- **AC-008:** The local CI command runs compile, lint, and tests without provider credentials or model network calls.
- **AC-009:** GitHub Actions installs dependencies, runs the same checks, builds the Docker image, launches a mock-mode container, and passes health/profile/ingestion/query/citation smoke checks.
- **AC-010:** No secrets, private documents, local vector data, or SQLite database files are committed.

## Deferred

- Production authentication, authorization, rate limits, tenant provisioning, public hosting, persistent cross-user memory, document upload formats beyond text/Markdown, and autonomous write tools.
- Superpowers integration and installation. Add it only after this starter's local checks, remote CI, Docker build, and API tests are green; design that integration through a separate PRD.
