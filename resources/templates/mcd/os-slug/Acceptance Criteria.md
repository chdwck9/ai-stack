---
doc_id:
  - os-slug/acceptance-criteria
version:
  - inherit from parent
last updated:
  - YYYY-MM-DD
tags:
  - acceptance
  - validation
  - pass-fail
  - rebuild-checklist
use_when:
  - Validating a rebuild or implementation; QA or testing queries; checking pass/fail conditions; "is it done" or "is it correct" queries. For executable test commands, coverage targets, and the Evidence Gate (completion protocol), fetch §9a Test Plan & Evidence Gate.
agent_notes:
  - Criteria here are binary pass/fail — no partial passes. REQ-IDs must reference FR-NNN entries from §3 Constitution — do not create standalone checks without a linked requirement. If a criterion cannot be verified objectively, rewrite it. Performance targets belong in §11, not here. Evidence Gate and test runner commands are in §9a.
---

## What this section is for

The pass/fail test for a completed rebuild. An agent needs to know when it's done. This section defines the binary checks that confirm the system is correct, not just running.

**Reverse-engineering note:** Pull from existing UAT scripts, test plans, user stories with acceptance criteria, and SLA documents. If none exist, derive from the primary use cases in §2 (Core Identity) — each use case generates at least one validation check.

---

## Building Blocks

### Critical User Journey Checks

_For each primary use case in §2, define a pass/fail test. Every check must link to a FR-NNN ID from §3 Constitution._

_Ask: "If a user tried to do this, what would success look like? Which FR does this validate?"_

|#|Use case|Test action|Expected result|Pass?|
|---|---|---|---|---|
|CUJ-01||||[ ]|

---

### System Health Checks

_Ask: "What signals confirm the infrastructure is healthy, not just the application?"_

|#|Check|Target|Method|Pass?|
|---|---|---|---|---|
|SH-01|Response latency|< Xms||[ ]|
|SH-02|Error rate|< X%||[ ]|
|SH-03|Uptime|> X%||[ ]|

---

### Integration Smoke Tests

_For each integration in §7, define a minimal test confirming the connection is live._

|Integration|Test|Expected response|Pass?|
|---|---|---|---|
||||[ ]|

---

### Data Integrity Checks

_Ask: "Is the right seed and reference data present?"_

|Dataset|Check|Expected state|Pass?|
|---|---|---|---|
||||[ ]|

---

### Access Verification

_Ask: "Can the right roles do the right things? Can the wrong roles not?"_

|Role|Can do|Cannot do|Pass?|
|---|---|---|---|
||||[ ]|

---

### Definition of Done

_The rebuild is complete when:_

- [ ] All CUJ checks pass
- [ ] All system health checks pass
- [ ] All integration smoke tests pass
- [ ] All data integrity checks pass
- [ ] All access verification checks pass
- [ ] Evidence Gate in §9a is satisfied with specific output cited

