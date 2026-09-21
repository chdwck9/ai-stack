---
doc_id:
  - os-slug/systems-mechanics
version:
  - inherit from parent
last updated:
  - YYYY-MM-DD
tags:
  - workflows
  - processes
  - input-outputs
  - failure-modes
use_when:
  - Workflow or process questions; input/output queries; failure mode analysis; step-by-step operational queries; "how does it work" questions.
agent_notes:
  - Workflows here describe what the system does, not how it’s built. For infrastructure details see Section 10. For data structures see Section 5.
---

## What this section is for

How the system operates day-to-day: what goes in, what comes out, what tools power it, and where it breaks. An agent needs this to understand behaviour, not just structure.

---

## Building Blocks

_Answer each question. Delete the instructions once populated._

### Inputs & Outputs

_Ask: "What does this system consume and what does it produce?"_

|Input|Source|Format|Output|Destination|Format|
|---|---|---|---|---|---|
|||||||

---

### Core Workflows

_Ask: "What are the 3–7 recurring processes this system runs?" For each: name it, describe the trigger, the steps, and the end state._

_Observation: Follow a user through the product end-to-end. Each distinct journey is a workflow._

#### Workflow: [Name]

- **Trigger:**
- **Steps:** 1. 2.
- **End state:**
- **Owner:**

_Repeat for each core workflow._

---

### Tools & Technologies

_Ask: "What tools, services, or platforms does this system depend on to function?"_

|Tool / Technology|Role|Version / Tier|Notes|
|---|---|---|---|
|||||

---

### Feedback Loops

_Ask: "How does the system learn or correct itself? What signals does it use to improve over time?"_

[ANSWER]

---

### Failure Modes & Mitigations

_Ask: "What are the most common ways this breaks? What are the catastrophic failure scenarios?"_

_Interview: Ask an engineer or ops lead: "What wakes you up at 3am?"_

|Failure mode|Likelihood|Impact|Mitigation|Recovery|
|---|---|---|---|---|
||High/Med/Low|High/Med/Low|||