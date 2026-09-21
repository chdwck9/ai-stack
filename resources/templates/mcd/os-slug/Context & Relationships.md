---
doc_id:
  - os-slug/ontext-relationships
version:
  - inherit from parent
last updated:
  - YYYY-MM-DD
tags:
  - stakeholders
  - dependencies
  - integrations
  - ecosystem
use_when:
  - Stakeholder queries; dependency mapping; integration spec questions; ecosystem positioning; "who is affected" or "what does this connect to" queries.
agent_notes:
  - Integration contracts here are the canonical source — do not duplicate in Section 4 (Structure) or Section 6 (Mechanics). This section owns the full integration spec for each external connection.
---

## What this section is for

Where this system sits in its broader ecosystem and how it connects to everything around it. Covers stakeholders, dependencies, and the full spec for each external integration. An agent needs this to know what it can't rebuild in isolation.

---

## Building Blocks

### Ecosystem Position

_Ask: "What category does this belong to? Who are the alternatives? Where does this sit in the user's workflow — before or after what?"_

[ANSWER]

---

### Stakeholders

_Ask: "Who has a stake in this system's success or failure?" Include users, buyers, internal owners, regulators, and affected parties._

|Stakeholder|Role|Interest|Influence|
|---|---|---|---|
||||High/Med/Low|

---

### Dependencies

_Ask: "What must exist for this system to function?" and "What breaks if this system goes down?"_

|Dependency|Type|Direction|Criticality|Fallback|
|---|---|---|---|---|
||Upstream/Downstream|Inbound/Outbound|Blocking/Degraded||

---

### Integration Contracts

_For each external integration, complete this block. This is rebuild-critical — an agent cannot wire up integrations without this._

_Ask: "What external systems does this connect to?" and "What would break if the internet went down?"_

_Verify: Cross-reference against the dependency list above. Every blocking external dependency needs a contract entry._

#### Integration: [System Name]

|Field|Value|
|---|---|
|**Direction**|Inbound / Outbound / Bidirectional|
|**Trigger / Event**|What initiates the data exchange?|
|**Endpoint**|URL or queue name|
|**Auth mechanism**|API key / OAuth / mTLS / other|
|**Payload summary**|What data moves, in which direction?|
|**Error handling**|Retry / queue / alert / fail-silent?|
|**SLA / criticality**|Blocking or degraded-mode tolerable?|
|**Docs link**||

_Repeat block for each integration._

---

### Allies, Competitors & Complements

_Optional. For products and services._

|Entity|Relationship|Notes|
|---|---|---|
||Ally/Competitor/Complement||