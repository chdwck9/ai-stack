---
doc_id:
  - os-slug/constitution
version:
  - inherit
last updated:
  - YYYY-MM-DD
tags:
  - principles
  - requirements
  - guardrails
  - anti-goals
  - standards
use_when:
  - Queries about operating rules, design principles, or scope guardrails; requirements questions (functional and non-functional); what the system must or must never do. For agent behavioral constraints (Always / Ask First / Never), fetch §3a instead.
agent_notes:
  - Requirements here are capability-level, not implementation-level. For implementation details see §4 (Structure) or §10 (Infrastructure). Guardrails here are hard constraints on the product — not preferences. For constraints on agent behavior during development, see §3a Agent Boundaries.
---

## What this section is for

The operating rules of the system. An agent needs this to make decisions that are consistent with intent — especially when instructions are ambiguous or incomplete.

---

## Building Blocks

_Answer each question. Delete the instructions once populated._

### Key Principles

_Ask: "What beliefs guide how this system is built and operated?" These are not features — they are reasons behind feature decisions._

_Verify: If a principle can't be used to decide between two design options, it's too vague._

---

### Values / Design Beliefs

_Ask: "What do we optimise for when there's a trade-off?" (e.g. simplicity over power, reliability over cost, user autonomy over guardrails)_

|Trade-off|We favour|Reason|
|---|---|---|
||||

---

### Functional Requirements

_Ask: "What must this system do?" (Capability-level, not implementation-level)_

_Source: Stakeholder interviews, user stories, contractual obligations._

|ID|Requirement|Priority|Source|
|---|---|---|---|
|FR-01||Must Have||

---

### Non-Functional Requirements

_Ask: "How must it perform, scale, and comply?" Cover: performance, availability, security, compliance, scalability. Every NFR must have a testable threshold — reject vague aspirations like "fast" or "secure"._

|ID|Requirement|Target|Notes|
|---|---|---|---|
|NFR-01||||

---

### Guardrails / Anti-Goals

_Ask: "What is explicitly out of scope? What should this system never do or become?"_

_Verify: If something is tempting but wrong for the system's purpose, it belongs here._

- ## This system will NOT:
    

---

### Standards In Scope

_List all coding, architecture, design, and writing standards that govern how this system is built. A builder must observe these before writing any code, copy, or architecture._

_Ask: "What standards, design systems, coding conventions, or writing guidelines apply here?"_

|Standard|Domain|Source|Applies to|
|---|---|---|---|
||Coding / Architecture / Design / Writing|||

---

### Roles & Mandates

_Optional. For systems with distinct operating roles._

|Role|Mandate|Permissions|
|---|---|---|
||||
