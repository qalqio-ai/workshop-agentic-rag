# Research: API Readiness Probe

## Decision: Use a read-only profile-store availability method

The readiness route will ask the existing `ProfileStore` whether its vector-store client is available.
That method will perform one read-only collection-listing operation and report availability to the route.

**Rationale**: The store already owns the Qdrant client. A collection-listing operation proves the
client is usable without requiring a profile, document, vector, embedding, retrieval query, session, or
language-model call. Keeping the client operation behind `ProfileStore` gives tests a focused failure
seam.

**Alternatives considered**:

- Return a static ready response: rejected because it cannot distinguish an unavailable vector store.
- Run a retrieval query: rejected because it requires embedding and can make readiness depend on indexed
  content.
- Check a named profile collection: rejected because an empty store can still be available and no profile
  is required by the readiness contract.

## Decision: Return a sanitized service-unavailable response on check failure

If the store check raises an availability-related error, the route will return HTTP 503 with a stable,
machine-readable not-ready response and no error text.

**Rationale**: Operators need an unambiguous non-success result for traffic routing. Suppressing raw
exceptions protects local paths, connection details, and other operational internals.

**Alternatives considered**:

- Propagate the raw exception: rejected because it leaks implementation details and produces an unstable
  contract.
- Reuse `/health` for the dependency check: rejected because it would break the existing liveness
  contract.

## Decision: Verify the no-model and no-mutation boundary with isolated tests

Tests will make model generation, embedding, retrieval, document mutation, and session access fail if
called during a readiness request.

**Rationale**: A successful HTTP response alone does not prove the endpoint avoided costly or mutating
paths. Isolated failure seams make the scope boundary executable.

**Alternatives considered**:

- Rely on manual code review: rejected because the requirement is testable and susceptible to regression.
