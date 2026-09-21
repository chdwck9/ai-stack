---
doc_id:
  - os-slug/data-model
version:
  - inherit from parent
last updated:
  - YYYY-MM-DD
tags:
  - schema
  - entities
  - data-model
  - state-machines
use_when:
  - Conceptual data model questions — what entities exist, how they relate, what states they move through. For machine-readable schemas suitable for code generation or validation, fetch §5a Schema Contracts instead.
agent_notes:
  - This section may not apply to non-software subjects. If no formal schema exists, reconstruct from UI observation — every form field is a column, every dropdown is an enum, every related record is a foreign key. All formal schema definitions (Zod, JSON Schema, Pydantic, SQL DDL) live in §5a, not here.
---

## What this section is for

The formal data layer. An agent rebuilding a system needs this to recreate the right structures before it can recreate behaviour. Without schema, everything is guesswork.

**Reverse-engineering note:** If you don't have a formal schema, use the UI as proxy. Every form field is a column. Every dropdown is an enum. Every related record is a foreign key. Walk the product systematically and reconstruct from observation.

---

## Building Blocks

_Answer each question. Delete the instructions once populated._

### Entity Inventory

_Ask: "What are the nouns of this system — what does it track, store, or manage?"_

_Observation: Look at navigation menus, list views, and API endpoints. Each resource name is an entity._

|Entity|Description|Key relationships|
|---|---|---|
||||

---

### Entity Definitions

_For each entity, define its fields._

_Ask: "What properties does this object have?" and "Which are required vs. optional?"_

#### [Entity Name]

|Field|Type|Required|Notes / Enum values|
|---|---|---|---|
|id|UUID|Yes|Primary key|
|||||

_Repeat block for each entity._

---

### Relationships

_Ask: "How do entities relate to each other?" Map cardinality._

|From|Relationship|To|Notes|
|---|---|---|---|
||one-to-many|||

---

### State Machines

_Ask: "Which entities have a lifecycle? What are the valid states and allowed transitions?"_

_Observation: Look for status fields, filters, or workflow stages in the UI._

#### [Entity Name] States

|State|Description|Allowed transitions to|
|---|---|---|
||||

---

### Linked Spec

_Link to formal schema artefact if it exists: ER diagram, OpenAPI spec, data dictionary, Postman collection._

[LINK]

---

### Schema Contracts

_Machine-readable schema definitions (Zod, JSON Schema, Pydantic, SQL DDL, OpenAPI) live in the child page below. Do not define schemas as prose in this section._

> **§5a Schema Contracts** — fetch this page for code generation, stub creation, output validation, or any task requiring machine-readable type definitions.

[Schema Contracts](https://www.notion.so/Schema-Contracts-36124dc8ccd98157a039da6dee378ac3?pvs=21)