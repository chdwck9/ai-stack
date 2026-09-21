---
doc_id:
  - os-slug/environment-infrastructure
version:
  - inherit from parent
last updated:
  - YYYY-MM-DD
tags:
  - infrastructure
  - deployment
  - environment
  - configuration
  - services
use_when:
  - Deployment queries; infrastructure tier questions; service configuration; environment-specific questions (staging vs production); "where does it run" queries
agent_notes:
  - Environment configs here are the canonical source — do not duplicate in Section 4 (Structure) or Section 6 (Mechanics). Sensitive values (secrets, keys) should be referenced by name only, never stored here.
---

## What this section is for

Where and how the system runs. An agent cannot complete a rebuild without knowing the operational environment. This is the hardest section to reconstruct from documents alone — populate it early and keep it current.

**Reverse-engineering note:** Architecture diagrams give you topology. ADRs give you decisions. The gaps (exact config values, secret names, IAM roles) require either IaC files or a 45-minute structured interview with an engineer. Do that interview and document it here.

---

## Building Blocks

### Environment Tiers

_Ask: "How many environments do you run? What's different between them?"_

|Tier|Purpose|URL / Endpoint|Notes|
|---|---|---|---|
|Development||||
|Staging||||
|Production||||

---

### Service Inventory per Tier

_Ask: "What services run in each environment?" and "Is anything production-only?"_

|Service|Dev|Staging|Prod|Notes|
|---|---|---|---|---|
||Yes/No|Yes/No|Yes/No||

---

### Cloud / Hosting Provider

_Ask: "Where does this run?" Cover: provider, region, account structure._

|Item|Value|
|---|---|
|Provider|e.g. AWS / GCP / Azure / On-prem|
|Region(s)||
|Account / Project structure||

---

### Configuration & Environment Variables

_Ask: "What changes between environments?" and "What would a new engineer need to set up locally?"_

_Do NOT store actual secret values here. Store names, descriptions, and sources only._

|Variable name|Description|Environment|Source / Vault location|
|---|---|---|---|
|||All / Prod only / etc.||

---

### External Service Accounts

_Ask: "What third-party API keys or service accounts do you manage?"_

|Service|Auth type|Environment|Owner|Rotation policy|
|---|---|---|---|---|
||||||

---

### Deployment Mechanism

_Ask: "How does code get from the repository to running in production?"_

|Stage|Tool / Method|Trigger|Owner|
|---|---|---|---|
|Build||||
|Test||||
|Deploy||||

---

### Scaling Rules

_Ask: "What auto-scales? What is fixed? What happens under traffic spikes?"_

|Service|Scaling type|Min|Max|Trigger|
|---|---|---|---|---|
||Auto / Manual / Fixed||||

---

### IaC / Config Links

_Link to Terraform, CloudFormation, Helm charts, or equivalent if they exist._

[LINK]