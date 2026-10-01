# Quickstart: API Readiness Probe Validation

## Prerequisites

Create the local development environment and start the API as described in the repository README. The
default mock configuration is sufficient; no language-model credentials are required.

## Validate a ready vector store

```bash
curl -i http://127.0.0.1:8000/ready
```

Expected: HTTP 200 and the `ready` status described in the
[API contract](contracts/openapi.yaml). This request does not require a document or question.

## Validate unchanged liveness

```bash
curl -i http://127.0.0.1:8000/health
```

Expected: HTTP 200 and the existing `ok` status. Its result is independent of the vector-store check.

## Run automated validation

```bash
./scripts/test.sh
```

Expected: compile, lint, and test checks pass. The API tests cover ready and unavailable outcomes,
unchanged liveness, published endpoint documentation, and the absence of model, embedding, retrieval,
session, and data-mutation activity from readiness handling.
