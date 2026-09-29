# Feature Specification: Agentic RAG Workshop Demo

**Feature ID:** 001-agentic-rag-demo  
**Status:** Draft — scenario decisions required  
**Owner:** QALQIO workshop team  
**Last updated:** 2026-09-29

## Problem and outcome
Workshop participants need to see how an AI-native repository supports agent-readable context and how retrieval can be used in a bounded agent loop.

Demonstrate a small application that retrieves approved source material, evaluates evidence sufficiency, produces a cited response, and makes its tool and memory boundaries inspectable.

## Scope

### In scope
- One end-to-end question-to-cited-answer path
- One approved synthetic or public source corpus
- Visible retrieval evidence and provenance
- An explicit answer, refine, or abstain decision
- Evaluation cases for supported, unsupported, and conflicting questions

### Out of scope until approved
- Production deployment or customer data
- Autonomous consequential actions
- Persistent user memory
- Broad multi-agent orchestration
- A specific model, vector database, cloud, or UI choice

## Scenario to select
**Decision required:** Choose a narrow domain scenario and approved source material before implementation.

Select a scenario that is easy to explain, safe to demo, grounded in clear source documents, and shows retrieval refinement and uncertainty.

## User scenario
### Ask a question and inspect its evidence (P1)
**Given** an approved corpus has been indexed,  
**When** a participant asks an in-scope question,  
**Then** the demo shows retrieved evidence, assesses sufficiency, and returns a cited answer or explicit abstention.

## Initial functional requirements
- **FR-001:** Show source passages used for every factual answer.
- **FR-002:** Abstain or ask a bounded question when evidence is insufficient.
- **FR-003:** Ignore instructions embedded in retrieved documents that conflict with policy.
- **FR-004:** Show the retrieval and refinement path.
- **FR-005:** Use only approved synthetic or public workshop sources.
- **FR-006:** Test answerable, unanswerable, conflicting, and adversarial-document cases.
- **FR-007:** Specify memory separately from the document index; keep it disabled by default.

## Decisions still open
| Decision | Options to evaluate | Owner | Status |
|---|---|---|---|
| Scenario / domain | Workshop-selected use case | Project owner | Open |
| Source corpus | Synthetic, public, or both | Project owner | Open |
| Runtime / language | Choose for teaching clarity and time | Technical lead | Open |
| Model provider | Select after constraints are known | Technical lead | Open |
| Embedding and vector store | Compare lexical and hybrid needs | Technical lead | Open |
| Memory | None for first slice unless required | Project owner | Open |
| UI | CLI, notebook, or small web interface | Workshop team | Open |

## Acceptance criteria
- **AC-001:** Ask an in-scope question and inspect passages and metadata.
- **AC-002:** Supported factual claims trace to displayed sources.
- **AC-003:** An unanswerable question gets an insufficiency response, not invented content.
- **AC-004:** Conflicting sources are surfaced with provenance.
- **AC-005:** A prompt-injection string in a retrieved document cannot override policy.
- **AC-006:** Setup is documented and works with synthetic/public data only.

## Evaluation plan
Build a reviewed set of questions supported by one source, requiring multiple passages, unanswerable, conflicting/stale, and containing an adversarial instruction. Measure retrieval relevance, citation correctness, groundedness, abstention, and tool-boundary compliance. Set numeric thresholds after scenario selection.

## Risks and assumptions
| Type | Item | Owner | Resolution |
|---|---|---|---|
| Assumption | A thin end-to-end slice is best for the workshop | Project owner | Confirm scope |
| Risk | Polished responses can hide weak evidence | Technical lead | Show sources and evaluation |
| Risk | Public repo could contain restricted source material | Maintainer | Review corpus and commits |
| Question | Which scenario and documents are approved? | Project owner | Decide before implementation |
