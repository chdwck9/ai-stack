---
doc_id:
  - os-slug/structure-anatomy
version:
  - inherit from parent
last updated:
  - YYYY-MM-DD
tags:
  - architecture
  - components
  - interfaces
  - states
use_when:
  - Technical architecture questions; component inventory; interface or API queries; understanding system operating states or modes; "what parts exist" queries.
agent_notes:
  - Components here are structural (what exists). For how they work together in workflows, see Section 6 (Systems & Mechanics). For data structures see Section 5.
---
## What this section is for

The structural blueprint of the system. An agent needs this to understand what parts exist, how they connect, and what states the system can be in. Without this, a rebuild agent is guessing at components.

---

## Building Blocks

_Answer each question. Delete the instructions once populated._

### Component / Subsystem Inventory

_Ask: "What are all the distinct parts of this system?" and "What would need to be rebuilt independently?"_

_Interview: Ask an engineer or operator: "If this went down, what would you check first?" Each answer is a component._

_Observation: Navigate the product or system end-to-end. Every distinct screen, service, or module is a candidate._

|ID|Component|Type|Description|Owner|
|---|---|---|---|---|
|C-01||e.g. UI / API / Service / DB / Integration|||

---

### Architecture Diagram

_Attach or link a diagram showing how components connect. If none exists, describe the topology in prose._

_Minimum viable: a box-and-arrow diagram showing what calls what._

[LINK OR EMBED DIAGRAM]

---

### Interfaces & APIs

_Ask: "How do components talk to each other? How do external systems talk to this one?"_

|Interface|From|To|Protocol|Notes|
|---|---|---|---|---|
||||e.g. REST / gRPC / Event / Webhook||

---

### States & Modes

_Ask: "What different operating states can this system be in?" Cover: normal operation, degraded, maintenance, recovery, off._

_Verify: For each state, an agent should know: how to enter it, what changes, and how to exit it._

|State|Description|Entry condition|Exit condition|
|---|---|---|---|
|Active||||
|Degraded||||
|Recovery||||

---

### Operating Manual

_Optional. Step-by-step guide for how a human (non-engineer) operates or navigates this system day-to-day._

[CONTENT OR LINK]