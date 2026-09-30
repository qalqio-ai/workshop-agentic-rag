# Feature Specification: Profile-Scoped Source Catalog

**Feature ID:** 003-source-catalog  
**Status:** Walkthrough seed; not implemented  
**Workflow:** Spec Kit + Superpowers practice feature  

## Outcome

Allow a workshop developer to list which sources have been ingested for one configured use-case profile without retrieving document contents.

## User story

As a developer inspecting a knowledge profile, I want to see its ingested source IDs and titles so I can confirm which synthetic materials are available before querying the assistant.

## API behavior

Add `GET /v1/use-cases/{use_case_id}/sources`.

For a configured profile, return HTTP 200 with a JSON array. Each entry contains only:

- `source_id`: the source identifier provided during ingestion
- `title`: the source title provided during ingestion

Return one entry per distinct source ID, sorted by `source_id` in ascending order. An empty profile returns an empty array. Do not return chunk text, embeddings, internal Qdrant point IDs, or session data.

An unknown profile returns HTTP 404 with the existing error shape:

```json
{"detail":{"code":"unknown_use_case"}}
```

## Acceptance criteria

- **AC-001:** An ingested source appears in the listing for its own use-case profile.
- **AC-002:** Multiple chunks for one source produce one catalog entry.
- **AC-003:** Distinct sources are returned in deterministic ascending `source_id` order.
- **AC-004:** A profile with no ingested documents returns HTTP 200 and `[]`.
- **AC-005:** A source ingested into one profile never appears in another profile's listing.
- **AC-006:** Unknown profile IDs return HTTP 404 with `unknown_use_case`.
- **AC-007:** Catalog entries contain only `source_id` and `title`; document text and internal vector-store data are not exposed.
- **AC-008:** Tests use in-memory Qdrant and mock mode; no live model or network access is needed.
- **AC-009:** The OpenAPI schema documents the endpoint and response.
- **AC-010:** Existing API behavior, local checks, Docker build, and black-box smoke tests continue to pass.

## Boundaries

- Read-only endpoint; it does not ingest, delete, or update sources.
- Use the selected profile's existing isolated collection only.
- No authentication, public deployment, new persistence layer, dependencies, or LLM calls.
- Do not change the existing behavior for repeated ingestion or stale chunks; that is a separate feature decision.

## Verification notes

Add API tests for one source, multiple chunks, deterministic ordering, empty profile, unknown profile, and profile isolation. Assert that returned objects have exactly the two public fields. Keep fixture data synthetic.

This file is an exercise seed. Generate and review `plan.md` and `tasks.md` with the installed Spec Kit integration before implementing the feature.
