# PRD: Superpowers Workflow Integration

**Status:** Accepted for workflow-guide implementation; PR #4 is open for review  
**Date:** 2026-09-30  
**Target repository:** `qalqio-ai/workshop-agentic-rag`  
**Prerequisite:** The Agentic RAG starter and its CI/Docker verification are accepted and merged.

## 1. Purpose

Define a safe, reviewable way to add the upstream Superpowers agent workflow to this repository after the Agentic RAG starter is established. This document is a planning artifact. It does not install, activate, vendor, or modify Superpowers.

The intended result is a clear path through the repository's requirements and implementation lifecycle: use the project's Constitution and GitHub Spec Kit artifacts to define what should be built, then use Superpowers skills to guide design, planning, implementation, testing, review, and branch completion.

## 2. Background

This repository provides an AI-native starter pack, Spec Kit-oriented specification files, and a multi-use-case Agentic RAG API. The API's acceptance criteria and CI checks remain the source of truth for product behavior. Superpowers is an upstream collection of agent skills and workflow instructions whose integrations and installation steps differ by coding-agent harness.

The upstream skill workflow includes brainstorming, worktree setup, planning, plan execution or subagent-driven development, test-driven development, code review, and branch completion. The README and release notes currently disagree about Gemini CLI: the README lists it, while release v6.1.0 says Gemini CLI support was removed after Google's end-of-life announcement. The implementation guide therefore documents Codex CLI and Claude Code and labels Gemini as unverified. The latest tagged release reviewed is v6.1.1 (`d884ae0`, 2026-07-02).

## 3. Problem statement

The repository has project-specific requirements and a structured specification workflow, but no agreed mapping from those artifacts to Superpowers workflows. Installing the upstream plugin without this mapping could create duplicate sources of truth, conflicting planning commands, or unclear ownership of acceptance criteria.

## 4. Goals

- Define how the Constitution, PRD/spec, plan, tasks, and CI acceptance criteria feed the Superpowers workflow.
- Keep project policies and product requirements in this repository; use upstream Superpowers for its maintained, general-purpose workflow skills.
- Document verified harness-specific setup for Codex CLI and Claude Code, and record the unresolved Gemini CLI status without presenting it as supported.
- Provide an onboarding walkthrough that starts from an approved feature spec and ends with verified changes ready for a pull request.
- Make installation an explicit, separately reviewed implementation step.

## 5. Non-goals

- Installing or activating Superpowers in any local or hosted agent environment.
- Copying or forking upstream skills into this repository.
- Replacing GitHub Spec Kit, changing its generated commands, or altering the Agentic RAG API.
- Claiming equivalent feature support across agent harnesses without verifying each harness.
- Changing application CI, Docker deployment configuration, API behavior, or repository visibility as part of a future workflow-only integration.

## 6. Users and primary scenario

**Primary user:** A developer using Codex CLI or Claude Code who wants to implement a feature in the Agentic RAG starter with explicit requirements, tests, and review.

**Scenario:** The developer chooses or drafts a feature in `specs/`, checks it against the Constitution and PRD, uses the agreed design/planning workflow, implements against acceptance criteria, runs the existing local CI and API smoke checks, and presents a branch or pull request with evidence of verification.

## 7. Proposed workflow boundaries

| Concern | Authority | Expected use |
|---|---|---|
| Product behavior and acceptance criteria | Project PRD and feature spec | Defines what the API and demo must do; includes boundaries and testable outcomes. |
| Repository rules and architecture constraints | `.specify/memory/constitution.md` and `AGENTS.md` | Defines project-specific constraints that remain in force during agent work. |
| Specification artifacts and lifecycle | GitHub Spec Kit | Structures specification, planning, and task artifacts using the installed harness commands. |
| General agent SDLC behavior | Upstream Superpowers | Guides design discussion, work isolation, planning, test-first implementation, review, and branch completion where supported. |
| Completion evidence | Local scripts and GitHub Actions | Verifies code quality, tests, Docker image build, and container API behavior. |

The implementation must identify overlapping command or skill behavior before activation. It must preserve one authoritative copy of product requirements and repository policy.

## 8. Functional requirements

1. **Workflow map:** Document a table mapping each project artifact and Spec Kit phase to the relevant Superpowers workflow phase or skill, including phases that have no direct mapping.
2. **Harness setup guide:** Provide separately verified setup instructions for Codex CLI and Claude Code. Record the Gemini CLI README/release-note conflict and do not recommend it as a supported path until upstream resolves that conflict. State prerequisites and the upstream sources consulted. Do not run installation commands as part of authoring this PRD.
3. **Conflict handling:** Explain how to resolve overlapping instructions, especially spec approval versus brainstorming approval, task breakdown versus plan writing, and implementation via Spec Kit commands versus Superpowers plan execution.
4. **Demo walkthrough:** Provide a small change scenario in mock mode that shows the workflow from accepted feature spec through tests and pull request readiness.
5. **Verification gates:** Require the existing Python test script and Docker/API CI job before describing a change as complete. A workflow-only addition must not weaken or bypass those checks.
6. **Upstream maintenance:** Record the upstream repository URL, version or commit selected at implementation time, review date, update procedure, and maintainer owner.
7. **Security and privacy:** Review plugin permissions, code execution behavior, and any optional network or telemetry behavior. The guide must distinguish optional behavior from required behavior and explain how to disable optional telemetry if applicable.
8. **Rollback:** Document how to deactivate or remove the integration without changing application source or the project's requirements and acceptance criteria.

## 9. Acceptance criteria for the future implementation

- A maintainer can explain from the docs which files own product requirements, repo policy, implementation plan, task breakdown, and workflow guidance.
- A developer can follow one complete mock-mode feature walkthrough using a supported harness and produce a tested change.
- The walkthrough shows the correct Spec Kit and Superpowers sequence without duplicated or contradictory approval steps.
- The chosen upstream version and per-harness setup path are recorded and verified from official upstream documentation at implementation time.
- No upstream skill content is copied into the repository unless a separate, explicit decision justifies maintaining a local adaptation.
- Existing CI remains required and green, including Docker build and black-box API smoke tests.
- The integration can be disabled or removed using the documented rollback steps.
- Installation and activation occur only after this PRD is reviewed and implementation is separately authorized.

## 10. Constraints and assumptions

- The Agentic RAG API defaults to mock mode; the walkthrough must not require an API key or external LLM service.
- The demo repository has no authentication and must not be exposed publicly as a production service.
- Agent harness plugin systems change over time. Commands and upstream review dates belong in `Superpowers_Workflow_Guide.md` and must be rechecked before they are changed.
- The project expects a pull request review and passing GitHub Actions before merging.
- This PRD assumes GitHub Spec Kit artifacts are present in the accepted starter baseline; it does not install or initialize Spec Kit.

## 11. Open decisions for implementation planning

- Which harness should be used for the first end-to-end walkthrough: Codex CLI, Claude Code, or Gemini CLI?
- Should the integration guide cover all three harnesses in the first implementation or stage support after one verified reference path?
- Should plugin versioning use a pinned commit, a tagged release, or the host's managed marketplace update path?
- Who will own periodic upstream compatibility checks?

## 12. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Spec Kit and Superpowers both try to control planning or approval | Publish an explicit workflow map and test it with a short feature walkthrough before activation. |
| Upstream install or plugin instructions change | Recheck official docs at implementation time and record the date and chosen version. |
| Harness support differs | Validate each named harness independently and label untested paths as unsupported. |
| Workflow instructions encourage unreviewed broad changes | Keep PR review and the repository's CI gates mandatory. |
| Optional upstream behavior makes network requests | Review permissions and telemetry; document any opt-out and required network access. |

## 13. References

- [Superpowers upstream repository and README](https://github.com/obra/superpowers) and [release notes](https://github.com/obra/superpowers/releases) — rechecked 2026-09-30; README/release notes conflict on Gemini CLI.
- [GitHub Spec Kit](https://github.com/github/spec-kit).
- [Agentic RAG starter PRD](Agentic_RAG_Multi_Use_Case_API_Starter_PRD.md).
- [Repository evolution path](evolution-path.md).
