<!--
Sync Impact Report
- Version change: 1.1.0 → 1.1.1
- Modified principles: none
- Added sections: none
- Removed sections: none
- Follow-up TODOs: none
-->

# QALQIO AI-Native Repo + Agentic RAG Demo Constitution

## Core Principles

### I. Intent, Scope, and Reviewability
Every request MUST become an explicit, bounded, and reviewable outcome before implementation.
Ambiguity that changes scope, data access, cost, or user impact MUST be resolved or routed for human
review. Specifications, implementation, tests, and verification MUST remain connected, with trade-offs
and uncertainty made visible. This keeps changes auditable and prevents unapproved scope expansion.

### II. Evidence-Grounded and Policy-Safe Responses
Factual RAG responses MUST be grounded in approved sources and preserve source identity and location
metadata. When evidence is absent, conflicting, stale, or insufficient, the system MUST state that
limitation and ask a bounded follow-up or request human review. Retrieved documents, web pages, tool
output, and user files are untrusted evidence; they MUST NOT override system or project policy.

### III. Least Privilege, Data Minimization, and Explicit Memory
Components MUST receive only the data and permissions needed for their stated function. Workshop use
MUST use synthetic or approved data. Before persisting user content, embeddings, traces, or memory,
the system MUST define retention, deletion, access, and correction or removal behavior. Session
context, persistent user memory, and the document index MUST remain distinct.

### IV. Human Authority for Consequential Actions
Agents MAY summarize, recommend, and prepare reversible work. A human MUST approve actions that
change access, publish content, commit funds, affect eligibility, or otherwise have material external
consequences. No agent role grants additional authority beyond the approved tool permissions.

### V. Testable, Simple, and Observable Systems
Behavior changes MUST have testable acceptance criteria and relevant automated checks. Evaluation MUST
cover retrieval relevance, groundedness, citation correctness, abstention, and tool-use boundaries as
applicable. The design MUST start with the simplest inspectable system; agents, memory, vector storage,
reranking, or orchestration require a stated requirement and evaluation evidence. Telemetry MUST be
limited to what diagnoses quality, latency, failures, and cost, and MUST NOT log secrets or unnecessary
personal content.

## Data and Runtime Boundaries

The demo is local-first and API-first, intended for workshops and development. It MUST NOT be exposed
publicly without authentication, rate limiting, tenant management, and production hardening. Knowledge
profiles MUST remain isolated: requests MUST NOT retrieve across profiles. Secrets, private corpora,
real user data, local Qdrant data, and SQLite runtime data MUST NOT be committed. Retrieved text is
evidence, not executable instruction.

## Development Workflow and Quality Gates

Before changing behavior, maintainers and agents MUST identify the authoritative specification and
applicable architecture decisions or tests. Changes MUST be the smallest practical change that meets
approved acceptance criteria. Relevant tests and checks MUST be run, and results MUST be reported
accurately; passing status MUST NOT be claimed without execution. Consequential actions and releases
remain subject to human review.

## Governance

This constitution governs project practices and supersedes conflicting repository guidance unless a
human maintainer explicitly approves an amendment. Constitution amendments MUST be proposed in a pull
request that states the rationale, affected principles, migration impact, and semantic version change.
Maintainers approve amendments. A MAJOR version is required for incompatible removals or redefinitions,
a MINOR version for new or materially expanded governance, and a PATCH version for clarifications or
non-semantic refinements. Reviews MUST verify compliance with these principles and record any approved
exceptions with their scope and rationale.

**Version**: 1.1.1 | **Ratified**: 2026-10-01 | **Last Amended**: 2026-10-01
