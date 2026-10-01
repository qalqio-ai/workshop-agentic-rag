# Feature Specification: API Readiness Probe

**Feature Branch**: `004-api-readiness`

**Created**: 2026-10-01

**Status**: Draft

**Input**: User description: "Add GET /ready as a readiness probe for the vector store. Preserve /health behavior, make no LLM calls, and meet the acceptance criteria above. Use slug=api-readiness."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Verify service readiness (Priority: P1)

As a deployment operator, I can call `GET /ready` to determine whether the API can access its vector
store, so that traffic is sent only to an instance able to serve retrieval requests.

**Why this priority**: A readiness signal prevents routing requests to an instance whose required
retrieval dependency is unavailable.

**Independent Test**: Call `GET /ready` when the vector store is available and confirm a successful,
machine-readable readiness response without submitting a query.

**Acceptance Scenarios**:

1. **Given** a running API whose vector store is reachable, **When** an operator requests `GET /ready`,
   **Then** the API returns a successful response that states the service is ready.
2. **Given** a running API whose vector store cannot be reached, **When** an operator requests
   `GET /ready`, **Then** the API returns a non-success response that states the service is not ready
   and does not disclose secrets or internal connection details.

---

### User Story 2 - Retain liveness compatibility (Priority: P2)

As an operator of an existing deployment, I can continue to use `GET /health` exactly as before, so
that existing liveness checks remain valid while readiness is added separately.

**Why this priority**: Existing deployment automation relies on the current liveness contract.

**Independent Test**: Call `GET /health` before and after this feature and compare its status code and
response body.

**Acceptance Scenarios**:

1. **Given** an API instance, **When** an operator requests `GET /health`, **Then** it returns the
   existing successful response unchanged, regardless of vector-store readiness.

### Edge Cases

- If the vector store becomes unavailable after startup, the next readiness request reports not ready.
- A readiness request does not require a use-case identifier, document, question, session, or user data.
- A readiness request does not generate an answer or invoke any language-model provider.
- Dependency failure responses remain safe for an unauthenticated local-development API and do not expose
  credentials, file paths, or provider internals.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The API MUST expose `GET /ready` as a readiness probe for vector-store availability.
- **FR-002**: When the vector store is available, `GET /ready` MUST return a successful, machine-readable
  response that identifies the API as ready.
- **FR-003**: When the vector store is unavailable or cannot be checked, `GET /ready` MUST return a
  non-success response that identifies the API as not ready without exposing sensitive dependency details.
- **FR-004**: `GET /ready` MUST check only the availability required to serve retrieval requests; it MUST
  NOT create, modify, or delete indexed content or session data.
- **FR-005**: Handling `GET /ready` MUST NOT invoke a language-model provider or generate a response to a
  user question.
- **FR-006**: The existing `GET /health` status code and response body MUST remain unchanged and MUST NOT
  become dependent on vector-store availability.
- **FR-007**: Both the readiness and unchanged liveness contracts MUST be included in the API's published
  interface documentation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In automated checks, 100% of readiness requests against an available vector store return a
  successful ready response.
- **SC-002**: In automated checks, 100% of readiness requests against an unavailable vector store return
  a non-success not-ready response without sensitive details.
- **SC-003**: In automated checks, 100% of `GET /health` requests retain the pre-feature status code and
  response body when the vector store is both available and unavailable.
- **SC-004**: In automated checks, 0 readiness requests invoke a language-model provider, generate an
  answer, or change indexed or session data.

## Assumptions

- The existing vector-store connection is the only dependency whose availability this readiness probe
  assesses; model-provider availability is outside this feature's scope.
- This feature retains the service's existing local-development security posture and does not introduce
  authentication, authorization, rate limiting, or public deployment support.
- Readiness is evaluated for each request so operators can observe a vector-store outage that occurs after
  application startup.
