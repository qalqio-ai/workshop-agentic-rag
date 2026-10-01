# Implementation Plan: API Readiness Probe

**Branch**: `004-api-readiness` | **Date**: 2026-10-01 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/004-api-readiness/spec.md`

## Summary

Add a read-only `GET /ready` contract that confirms the vector store is available to serve retrieval
requests. Keep `GET /health` as an independent, static liveness contract. The readiness path delegates
the availability check to the existing profile-store boundary, returns a sanitized unavailable response
when that check fails, and never reaches embedding, retrieval, session, or model-generation code.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: FastAPI 0.115.12; Qdrant client 1.14.2

**Storage**: Local Qdrant vector store; existing SQLite session memory is out of scope

**Testing**: pytest 8.3.5 with FastAPI TestClient; Ruff and compileall via `scripts/test.sh`

**Target Platform**: Local development API and Docker container

**Project Type**: Web service

**Performance Goals**: A readiness request performs one read-only vector-store availability check and
returns without embedding text or invoking a language-model provider.

**Constraints**: Preserve the exact existing `/health` response; no vector or session mutation; return
no exception details, credentials, file paths, or provider internals on a failed readiness check.

**Scale/Scope**: One new API endpoint, one profile-store availability seam, focused API tests, and
published interface documentation; no authentication, remote-store configuration, or model-health check.

## Constitution Check

*GATE: Passed before Phase 0 research. Re-checked after Phase 1 design: passed.*

- Intent and scope: The plan is limited to readiness of the existing vector store and explicitly retains
  liveness behavior.
- Evidence and policy safety: The endpoint produces operational status only and does not retrieve,
  interpret, or expose untrusted content.
- Least privilege and explicit memory: The check is read-only, receives no request data, and does not
  access session memory or stored content.
- Human authority: No consequential external action is introduced.
- Testability and observability: Success, dependency failure, unchanged liveness, OpenAPI visibility,
  and absence of model or data-path calls are covered by automated checks.

## Project Structure

### Documentation (this feature)

```text
specs/004-api-readiness/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/openapi.yaml
└── tasks.md             # Created later by $speckit-tasks
```

### Source Code (repository root)

```text
src/agentic_rag/
├── main.py              # HTTP routes and response mapping
└── retrieval.py         # ProfileStore and read-only availability boundary

tests/
└── test_api.py          # API contract and isolation tests
```

**Structure Decision**: Extend the existing single FastAPI service. Keep the vector-store operation at
`ProfileStore` so the route does not depend on the Qdrant client directly; extend the existing API test
module because it owns health and OpenAPI contract checks.

## Complexity Tracking

No constitution violations or complexity exceptions require tracking.
