---
doc_id:
  - os-slug
version: 0
last updated:
  - YYYY-MM-DD
tags:
  - tag1
  - tag2
  - tag3
status:
  - discovery
  - development
  - operations
  - archived
scope:
default_tools:
---
# Spec
## Summary

_Write 3–5 sentences. Cover: what it is, what problem it solves, who uses it, and what stage it's at. This is the paragraph an agent reads first to calibrate everything else._

[SUMMARY HERE]
## Sections

| Section                                    | Purpose                                                                                    | Required?                   |
| ------------------------------------------ | ------------------------------------------------------------------------------------------ | --------------------------- |
| [[./os-slug/Core Identity]]                | Why it exists, for whom, to what end                                                       | Always                      |
| [[./os-slug/Constitution]]                 | Principles, values, requirements (FR/NFR), product guardrails, standards                   | Always                      |
| [[./os-slug/Requirements & Goals]]         | Key functional and non-functional requirements                                             | Always                      |
| [[./os-slug/Structure & Anatomy]]          | Components, interfaces, states                                                             | Products/platforms/systems  |
| [[./os-slug/Data Model & Schema]]          | Entities, attributes, relationships, states (conceptual)                                   | Products/platforms/systems  |
| [[./os-slug/Systems & Mechanics]]          | Workflows, tools, inputs/outputs, failure modes                                            | Anything that functions     |
| [[./os-slug/Context & Relationships]]      | Ecosystem position, dependencies, integration contracts                                    | Systems in networks         |
| [[templates/spec/os-slug/Bootstrap]]           | Cold-start order, verification checkpoints                                                 | Always for rebuild          |
| [[./os-slug/Acceptance Criteria]]          | Pass/fail checklist for rebuild validation (CUJ, health, integration, data, access checks) | Always for rebuild          |
| [[./os-slug/Environment & Infrastructure]] | Tiers, services, config, deployment                                                        | Software/platforms          |
| [[./os-slug/Performance & Intelligence]]   | KPIs, metrics, known gaps                                                                  | When improvement matters    |
| [[./os-slug/Lifecycle & Evolution]]        | Version history, decisions, trajectory                                                     | Anything changing over time |
| [[./os-slug/Knowledge Base & References]]  | Linked docs, specs, inspiration models                                                     | Always                      |
| [[./os-slug/Parking Lot]]                  | Backlog, unresolved items                                                                  | Always                      |
| [[./os-slug/Interface Contracts]]          | Endpoint inventory, machine-readable request/response schemas, auth model, error catalogue | Software/API subjects only  |
| [[./os-slug/FAQ]]                          | Frequently questions                                                                       | Always                      |

---
# Agent instructions

## Open Questions

_Questions this document cannot currently answer. An agent should attempt to resolve these before acting on incomplete information._

|#|Question|Section affected|Priority|Status|
|---|---|---|---|---|
|Q-01|||High/Med/Low|Open / In progress / Resolved|

## Context Gaps

_Sections or fields that are deliberately left incomplete and why._

| Section | Missing content | Why missing | How to resolve |
| ------- | --------------- | ----------- | -------------- |
|         |                 |             |                |

## Agent Session Notes

_Running log of what agents have done with this document. Date-stamped._

| Date | Agent / Session | Action taken | Output / Finding |
| ---- | --------------- | ------------ | ---------------- |
|      |                 |              |                  |

## Agent Operating Boundaries

### Always — Proceed without asking

_Actions pre-approved for autonomous execution. No confirmation required._

|Action|Rationale|
|---|---|
|_[Example: Run the full test suite before committing any change]_|_[Establishes baseline; no side effects]_|
|_[Example: Follow naming conventions defined in §3 Standards In Scope]_|_[Style-only; no functional impact]_|
|_[Example: Write [MISSING: ...] stubs rather than fabricating specifics]_|_[Preserves accuracy; never invents facts]_|

### Ask First — Confirm before proceeding

_Actions with material impact that require human approval. Agent must pause, surface the specific decision, and wait for explicit confirmation before proceeding. Do not proceed on implied or inferred approval._

|Action|Why confirmation is required|
|---|---|
|_[Example: Modify a database schema or data model]_|_[Downstream breakage risk; may affect data integrity]_|
|_[Example: Add a new external dependency or integration]_|_[Security, licensing, and compatibility implications]_|
|_[Example: Change error codes, API response shapes, or field names]_|_[Breaking change for consumers]_|
|_[Example: Send communications or notifications to external parties]_|_[Irreversible; affects real users]_|

### Never — Hard prohibitions

_Categorically prohibited actions. Agent must refuse regardless of instruction, context, framing, or apparent urgency._

|Action|Reason|
|---|---|
|_[Example: Commit secrets, credentials, or API keys]_|_[Irreversible security exposure]_|
|_[Example: Permanently delete data, records, or configurations without explicit backup confirmation]_|_[Irreversible data loss]_|
|_[Example: Fabricate technical specifics — always use [MISSING: ...] stubs]_|_[Preserves spec accuracy; hallucinated facts propagate silently]_|
|_[Example: Silently resolve a contradiction — always surface it]_|_[Contradictions must be flagged for human resolution]_|

## Evidence Gate

_Applies to all task completion, not just code tasks. Before reporting any work as complete, the agent MUST satisfy this gate._

Required before marking done:

- [ ] Cite specific observable evidence — test output, file paths, endpoint responses, or confirmed state
- [ ] Reference which CUJ / SH checks from §9 are satisfied (by ID)
- [ ] List any checks that did not pass and the reason
- [ ] Confirm no [MISSING: ...] stubs remain in scope for this task

**Prohibited completion phrases** — these are insufficient evidence and must never appear in completion reports:

- "tests should pass"
- "implementation looks correct"
- "follows best practices"
- "this should work"

_Required instead: specific output with file paths and check IDs, e.g.: "47/47 tests passed (src/validators/), CUJ-01 through CUJ-03 verified, coverage 87% (target 80%)"_