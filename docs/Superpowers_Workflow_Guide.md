# Spec Kit + Superpowers Workflow

This guide applies the Superpowers workflow to this repository while keeping the existing project requirements authoritative. It uses a small, mock-mode API feature as a hands-on walkthrough.

## Ownership

| Work item | Source of truth |
|---|---|
| Project principles and safety boundaries | `.specify/memory/constitution.md` and `AGENTS.md` |
| Feature behavior and acceptance criteria | The numbered feature spec under `specs/` |
| Technical design and task breakdown | Spec Kit `plan.md` and `tasks.md` for that feature |
| Test-first implementation, debugging, and code review practices | Upstream Superpowers skills |
| Completion evidence | `./scripts/test.sh`, Docker API smoke test, and GitHub Actions |
| Merge and release | Human maintainer after review and required CI pass |

Spec Kit owns the feature spec, plan, and tasks. Do not create a second Superpowers plan for the same feature. After the Spec Kit tasks are reviewed and approved, use Superpowers' test-driven development and plan-execution practices to implement those tasks. Use Superpowers for brainstorming before the scope is approved, systematic debugging when a check fails, code review, and branch completion.

Superpowers skills are usually discovered and invoked automatically by the coding agent. They are not universal terminal commands. Spec Kit commands are also agent skills rather than shell commands; their exact spelling depends on the installed agent integration. The current Spec Kit docs show `/speckit-*` in skills mode, while some integrations expose another form. Use the commands created for this repo and agent.

## Install Superpowers in your coding agent

Install it separately in each agent you intend to use, then restart that agent session.

### Codex CLI

In Codex CLI, open the plugin browser with `/plugins`, search for `Superpowers`, and select **Install Plugin**.

### Claude Code

In Claude Code, run:

```text
/plugin install superpowers@claude-plugins-official
```

### Gemini CLI

The upstream README still lists `gemini extensions install https://github.com/obra/superpowers`, but upstream release notes also state that Gemini CLI support was removed after Google ended Gemini CLI. Treat Gemini support as unverified until upstream reconciles those instructions; use Codex CLI or Claude Code for this walkthrough.

### Verify

Open a fresh session in the project and ask the agent to explain its Superpowers workflow for a small feature. Confirm that it identifies the applicable skills before implementation and reads `AGENTS.md`, the constitution, and the selected feature spec.

## Walkthrough feature

Use [`specs/003-source-catalog/spec.md`](../specs/003-source-catalog/spec.md). It describes a read-only endpoint that lists source IDs and titles already ingested for one use-case profile. It must not return document text or data from another profile. The feature is intentionally specified but not implemented so you can practice the full workflow.

## Prep

Run these commands in the repository on `main` before starting the agent session:

```bash
git switch main
git pull --ff-only
source .venv/bin/activate
./scripts/test.sh
```

The baseline test run should pass before feature work starts. Open Codex CLI or Claude Code from the repository directory. Ask Superpowers to review the feature scope against `AGENTS.md` and the constitution, then approve the small design. Allow its worktree workflow to create an isolated worktree and feature branch; continue all remaining commands from that worktree.

## Build

In the agent conversation, use the Spec Kit commands installed for that harness, one at a time. The expected phases are:

1. Clarify the existing spec and record any accepted corrections.
2. Generate `plan.md` with the repository's Python, FastAPI, Qdrant, and mock-mode constraints.
3. Generate `tasks.md` and run Spec Kit's cross-artifact analysis.
4. Review the spec, plan, tasks, and acceptance criteria yourself before implementation.
5. Ask the agent to execute the approved Spec Kit tasks using Superpowers test-driven development. Require a failing test before each behavior change, the smallest implementation that makes it pass, and a focused review against the acceptance criteria.

Suggested instruction to the agent:

> Work only on `specs/003-source-catalog/spec.md`. Read `AGENTS.md` and `.specify/memory/constitution.md`. Keep this feature mock-mode and offline. Use the reviewed Spec Kit `plan.md` and `tasks.md` as the sole implementation plan. Apply Superpowers test-driven development and plan execution; write a failing test before implementation. Do not broaden scope, add dependencies, use an external model, or return document text. Stop and ask me if the spec and repository behavior conflict.

## Test

Run the fast local checks from the feature worktree:

```bash
source .venv/bin/activate
./scripts/test.sh
```

Then run the same Docker-backed API smoke flow used for the starter:

```bash
docker compose up --build -d
python scripts/api_smoke.py
docker compose down
```

If the API smoke fails, inspect `docker compose logs --tail=100 api`, fix the cause, and rerun the checks. Do not treat a printed message as evidence if a request returned an error; the smoke script must exit successfully.

Before shipping, check the patch and repository state:

```bash
git diff --check
git status --short
git diff
```

The agent should also run Superpowers' verification-before-completion and request a code review against the approved spec, tasks, and tests.

## Ship

After reviewing the diff and confirming both local test gates pass:

```bash
git add specs/003-source-catalog src tests
git commit -m "feat(api): list sources for use cases"
git push -u origin HEAD
```

Open a pull request targeting `main` (or use `gh pr create` if GitHub CLI is installed). Include the feature spec, acceptance criteria, local test results, and Docker smoke result in the PR description. Wait for GitHub Actions and human review. Merge only after required checks pass and the reviewer approves; keep merge authority with the maintainer.

## Agent commands are generated per harness

Do not type Spec Kit skill names as shell commands. To see what exists in a local checkout, inspect the integration files, for example:

```bash
rg --files .claude .agents .github 2>/dev/null | rg 'speckit|specify'
specify version
specify self check
```

For Codex CLI, Claude Code, and other supported integrations, invoke the installed command or skill that corresponds to **clarify**, **plan**, **tasks**, and **analyze**. Review each artifact before moving forward. Do not run a second planning system over the same feature.

## Upstream and maintenance record

- Upstream: [obra/superpowers](https://github.com/obra/superpowers)
- Instructions reviewed: upstream README on 2026-09-30
- Install model: host-managed plugin/extension; this repository does not vendor upstream skill files
- Update check: re-read the upstream installation and release notes before changing harness instructions
- Maintainer: repository maintainers, through pull request review
- Optional telemetry: upstream documents an optional visual companion that requests its logo and includes the Superpowers version, not project prompts or content. Disable it with `SUPERPOWERS_DISABLE_TELEMETRY=true` if desired.

## Disable or roll back

Uninstall or disable the plugin from the coding agent's plugin/extension manager and restart the agent. Remove or revise this guide and the README link in a reviewed repository change if the team no longer supports the workflow. No application dependency, API behavior, or product acceptance criterion depends on Superpowers.

## References

- [Superpowers upstream README](https://github.com/obra/superpowers)
- [GitHub Spec Kit quickstart](https://github.github.com/spec-kit/quickstart.html)
- [GitHub Spec Kit installation guide](https://github.github.com/spec-kit/installation.html)
- [Superpowers Integration PRD](Superpowers_Integration_PRD.md)
