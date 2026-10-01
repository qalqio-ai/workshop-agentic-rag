# Tasks: API Readiness Probe

**Input**: Design documents from `specs/004-api-readiness/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/openapi.yaml`, and
`quickstart.md`

**Tests**: Required. The feature specification requires automated verification of ready and unavailable
outcomes, unchanged liveness, published API documentation, and the no-model/no-mutation boundary.

**Organization**: Tasks are grouped by user story so each outcome is independently testable.

## Phase 1: Setup

**Purpose**: No project initialization is required; the existing FastAPI service, Qdrant client, pytest
fixture, and local test command are reused.

---

## Phase 2: Foundational - Vector-store Availability Boundary

**Purpose**: Create the focused, read-only store seam that the readiness route and its tests use.

- [X] T001 Add availability and closed-client failure tests for `ProfileStore` in `tests/test_retrieval.py`
- [X] T002 Implement the read-only `ProfileStore` availability check in `src/agentic_rag/retrieval.py` without embedding text, querying documents, or mutating collections

**Checkpoint**: The profile store can report available or unavailable through a testable read-only
boundary; no route contract has changed yet.

---

## Phase 3: User Story 1 - Verify Service Readiness (Priority: P1) 🎯 MVP

**Goal**: An operator can determine whether the API can access the vector store before routing retrieval
traffic to it.

**Independent Test**: With the existing in-memory test store, `GET /ready` returns the documented ready
response; when the store availability seam fails, it returns a sanitized HTTP 503 not-ready response;
all prohibited model, embedding, retrieval, session, and mutation seams remain unused.

- [X] T003 [US1] Add `GET /ready` ready, unavailable, sanitized-error, and no-model/no-mutation API tests in `tests/test_api.py`
- [X] T004 [US1] Implement the `GET /ready` route and its ready/HTTP-503 response mapping in `src/agentic_rag/main.py`, using only the `ProfileStore` availability boundary
- [X] T005 [US1] Extend the published endpoint assertions for the `GET /ready` contract in `tests/test_api.py`

**Checkpoint**: The readiness contract is independently functional and proves vector-store availability
without accepting user data or traversing query-generation paths.

---

## Phase 4: User Story 2 - Retain Liveness Compatibility (Priority: P2)

**Goal**: Existing operators can continue to rely on the unchanged `GET /health` liveness contract.

**Independent Test**: When the vector-store availability seam succeeds or fails, `GET /health` remains
HTTP 200 with exactly `{"status": "ok"}` and does not invoke the readiness check.

- [X] T006 [US2] Add liveness-regression tests covering ready and unavailable store states in `tests/test_api.py`

**Checkpoint**: Liveness stays independent of the vector store while readiness reports dependency status.

---

## Phase 5: Polish and Cross-Cutting Validation

**Purpose**: Exercise the new public contract in the repository's black-box smoke path and run all
documented checks.

- [X] T007 [P] Add `GET /ready` black-box readiness verification to `scripts/api_smoke.py`
- [X] T008 Validate the feature scenarios and full local test command from `specs/004-api-readiness/quickstart.md`

---

## Dependencies & Execution Order

```text
T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008
```

- Phase 2 blocks User Story 1 because the route uses the profile-store availability boundary.
- User Story 2 can be authored after the route design is known; it validates that the new readiness path
  did not alter existing liveness behavior.
- Polish begins after both stories are complete.

## Parallel Opportunities

- T007 can begin after the readiness response contract is fixed by T004 and does not modify the API or
  unit-test files.
- No other implementation tasks are marked parallel: they deliberately share `src/agentic_rag/main.py`
  or `tests/test_api.py`, and sequential execution keeps the contract and its tests coherent.

## Implementation Strategy

### MVP First

1. Complete T001–T005.
2. Run the independent User Story 1 tests.
3. Demonstrate a ready store and a simulated unavailable store before proceeding.

### Incremental Delivery

1. Add the read-only availability boundary.
2. Deliver the readiness contract and its isolation guarantees.
3. Verify the unchanged liveness contract.
4. Add the black-box smoke check and run the quickstart validation.

## Phase 6: Convergence

- [X] T009 CRITICAL Integrate the read-only `ProfileStore` availability check, `GET /ready` ready/not-ready response mapping, and isolation tests per FR-001–FR-005 and US1 (missing)
- [X] T010 Publish and verify the `GET /ready` OpenAPI contract, including its HTTP 503 response, in `src/agentic_rag/main.py` and `tests/test_api.py` per FR-007 (missing)
- [X] T011 Add the `/health` vector-store-independence regression test in `tests/test_api.py` per FR-006 and US2 (missing)
- [X] T012 Add `GET /ready` verification to `scripts/api_smoke.py` per plan validation and T007 (missing)
