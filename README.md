# QALQIO AI-Native Repo + Agentic RAG Demo

A starter repository for the QALQIO workshop build: establish a small, readable AI-native project foundation, then add spec-driven development and agent workflow tooling as the project grows.

## GitHub description

AI-native repository starter and Agentic RAG workshop demo: reusable project specs, agent guidance, and a staged path from repo setup to GitHub Spec Kit and Superpowers.

## Purpose

Demonstrate an AI-native software workflow and a bounded Agentic RAG application. Start with requirements, evidence, and constraints before implementation.

The RAG scenario, source corpus, runtime, vector store, and deployment target remain open until selected in a reviewed feature specification. Do not treat examples in templates as approved product decisions.

## Starter contents

| Path | Purpose |
|---|---|
| AGENTS.md | Shared instructions for coding agents |
| agents/roles.md | Suggested roles for the RAG demo |
| .specify/memory/constitution.md | Project principles and decision boundaries |
| docs/templates/prompt-requirements.md | Turn a prompt into testable requirements |
| .specify/templates/spec-template.md | Feature specification template |
| .specify/templates/plan-template.md | Lightweight implementation plan |
| .specify/templates/tasks-template.md | Implementation task breakdown |
| specs/001-agentic-rag-demo/spec.md | Initial scope and open decisions |
| .env.example | Configuration names only; no secrets |
| LICENSE | MIT text with rights-holder placeholder |

## First steps

1. Replace [COPYRIGHT HOLDER] in LICENSE with the correct rights holder before publishing.
2. Review AGENTS.md and the constitution; make them match the team's actual rules.
3. Complete the initial spec. Select the demo scenario and approved sources before choosing implementation details.
4. Create a numbered feature directory and copy the spec template there.
5. Commit the starter baseline before adding workflow tools.

## Evolution path

### 1. Start with this spec pack

Use the constitution, prompt requirements, feature spec, plan, and tasks to make intent and acceptance criteria reviewable. These are project-owned starting points, not a replacement for a full methodology.

### 2. Add GitHub Spec Kit

Follow the current instructions in the [official GitHub Spec Kit documentation](https://github.github.com/spec-kit/). Spec Kit can set up agent-specific command files and guide a structured flow from specification through implementation and convergence.

Review generated files before committing. Keep one authoritative version of each rule and template. Spec Kit evolves, so use its current setup guide rather than pinning an old command here.

### 3. Add Superpowers

When the team wants reusable agent skills for design, planning, implementation, testing, review, debugging, and branch completion, install [Superpowers](https://github.com/obra/superpowers) for the coding-agent harness in use. Installation differs by harness; follow its current official README.

Treat Superpowers as the workflow layer. Keep QALQIO domain rules, privacy constraints, architecture decisions, tool permissions, and acceptance criteria in this repository. Extend the workflow only for recurring needs; do not copy upstream skills without a maintenance reason.

## RAG evidence path

1. A user asks a question.
2. The system identifies needed information and chooses permitted retrieval tools.
3. Retrieval returns passages and source metadata.
4. The system checks evidence sufficiency and relevance.
5. The response cites supporting sources or states uncertainty.
6. The agent may refine the query or ask a bounded follow-up; it must not invent evidence.
7. Evaluation checks retrieval, citations, groundedness, and safe handling of missing evidence.

Specify memory separately from document retrieval. Do not silently persist user content or treat conversation memory as an authoritative source.

## Local setup

This starter contains documentation and examples; it does not require a runtime or API key.

~~~bash
git clone https://github.com/qalqio-ai/workshop-agentic-rag.git
cd workshop-agentic-rag
git status
~~~

Copy .env.example to .env only when an implementation needs configuration. Never commit .env, credentials, private documents, or real user data.

## Public repository checklist

- [ ] Confirm the rights holder in LICENSE.
- [ ] Remove internal, private, and customer material before committing.
- [ ] Add only synthetic or approved demo documents.
- [ ] Review repository visibility and organization policy.
- [ ] Record the scenario and data-handling rules in a feature spec.

## Upstream references

- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Spec Kit documentation](https://github.github.com/spec-kit/)
- [Superpowers](https://github.com/obra/superpowers)
