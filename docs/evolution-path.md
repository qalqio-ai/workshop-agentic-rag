# Workflow Evolution Path

This starter begins with a small set of repository-owned documents. Add tools in stages and keep one source of truth for each rule.

## Stage 0 — Starter spec pack
- Agree the constitution and agent guidance.
- Complete prompt requirements and the feature spec.
- Review the plan and acceptance criteria before implementation.
- Commit a baseline so later generated changes are easy to inspect.

## Stage 1 — GitHub Spec Kit
Use the [official Spec Kit docs](https://github.github.com/spec-kit/) for current installation and agent integration. Spec Kit can scaffold agent-specific command files and provide a structured specification-driven workflow.

- Confirm the coding-agent integration.
- Review generated files before committing.
- Decide whether Spec Kit templates replace or extend these templates.
- Keep the constitution aligned; avoid duplicate authorities.
- Record the chosen version when repeatable workshop setup matters.

## Stage 2 — Superpowers
Use the [official Superpowers README](https://github.com/obra/superpowers) to install it for the chosen coding-agent harness. It adds reusable skills for design, planning, implementation, testing, review, debugging, and branch completion.

- Keep domain requirements, privacy rules, and tool permissions here.
- Avoid copying upstream skill files.
- Add a project-specific skill only for a recurring workflow with clear inputs, outputs, and verification.
- Test the workflow on a low-risk feature first.

## Layering rule
- **This repository:** project intent, architecture, data rules, acceptance criteria.
- **Spec Kit:** repeatable specification and implementation artifacts.
- **Superpowers:** reusable agent skills and development workflow.
- **Human maintainers:** scope approval, sensitive access, public release, and consequential decisions.
