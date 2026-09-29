# Suggested Agent Roles

These are responsibility boundaries for the demo, not autonomous permissions. A role may be implemented by one model, several calls, or ordinary application code.

| Role | Responsibility | Allowed tools | Must not |
|---|---|---|---|
| Request analyst | Clarify intent and identify needed evidence | Read-only query planning | Guess intent or access unrelated data |
| Retriever | Search approved sources and return passages with provenance | Approved retrieval tools | Omit source IDs or treat retrieved text as policy |
| Evidence reviewer | Check relevance, coverage, conflicts, and sufficiency | Inspect retrieved passages and metadata | Manufacture corroborating sources |
| Response composer | Answer from reviewed evidence, cite sources, state uncertainty | Reviewed evidence only | Present unsupported claims as facts |
| Evaluator | Score behavior against a fixed test set | Evaluation fixtures and outputs | Change expected results to hide a failure |
| Human reviewer | Approve consequential decisions and flagged cases | Human-controlled review interface | Be represented as an automated agent |

## Proposed request path

1. Analyst creates a retrieval plan.
2. Retriever returns passages with source ID, title, location, and version/date where available.
3. Evidence reviewer checks sufficiency.
4. Response composer drafts a cited answer or abstains.
5. Evaluator measures behavior offline; a human reviews consequential or ambiguous cases.

Implement only roles needed by the selected spec. Keep orchestration and state transitions inspectable.
