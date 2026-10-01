# Data Model: API Readiness Probe

This feature adds no persisted entity and changes no vector or session schema.

## Transient response: Readiness status

| Field | Type | Rules |
|---|---|---|
| `status` | string | `ready` when the vector store is available; `not_ready` when it is unavailable or cannot be checked. |

The status is computed for each readiness request. It has no identifier, retention period, relationship
to a use case, or lifecycle beyond the response. Failure details are intentionally excluded.
