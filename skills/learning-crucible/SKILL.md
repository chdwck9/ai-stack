---


name: learning-crucible

uuid: 32c24dc8-ccd9-81a9-b60b-ffaf62e6cf7b

version: 7

description: "Learning Crucible"

thinking: "Medium"

temperature: 0.6


---


# Learning Crucible

Design and facilitate a 4-act capstone simulation that pressure-tests the concepts from a completed learning track. The simulation escalates in stakes and conflict across four acts, uses named characters with distinct agendas, and integrates the specific frameworks and skills the learner has covered. Output includes both the scenario content and the facilitator instruction set so the agent can run the simulation live.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Ingest the learning context**

Accept the completed modules/track plus any existing simulation world, character roster, narrative arc, or prior state. Reuse existing continuity when provided; otherwise create a new world.

Accept the list of completed modules or track title. Extract the key concepts, frameworks, and skills covered — these are the competencies the simulation must activate. If no module list is provided, ask: "Which modules or topics has the learner completed?" (Load @Team-Learning-Coach for full methodology context and audience profile if available — resolve location via @global-instructions.)

1. **Define the simulation world**

Establish the fictional company context: name, industry, stage, and a one-paragraph situation brief. The world must be realistic enough to sustain four acts of escalation without becoming implausible. Do not use Project Halcyon unless the user specifies it.

1. **Create the character roster**

Define 4–6 named characters. For each: name and role, primary agenda, conflict vector, communication style. Characters must represent genuinely competing interests.

1. **Design the 4-act story structure**

  - **Act 1 — Inciting Pressure**: A credible business problem surfaces. Stakes are real but manageable.

  - **Act 2 — Complication**: A second pressure point emerges that conflicts with the Act 1 response. A character's agenda becomes an obstacle.

  - **Act 3 — Crisis**: Stakes peak. A decision must be made with incomplete information and conflicting stakeholder demands.

  - **Act 4 — Resolution and Consequence**: The learner delivers a final position. Characters respond based on the quality and approach of the learner's response. There is no single correct answer.

  Each act includes: situation description, active characters, challenge posed to the learner, and the escalation trigger into the next act.

1. **Write the facilitator instruction set**

  - How to open each act

  - How to play each character (triggers, escalation cues, what a strong vs weak response unlocks)

  - How to evaluate the learner's response at Act 4 (criteria tied to learning objectives)

  - How to deliver the debrief (3 dimensions: what worked, what the learner avoided, executive-level benchmark)

1. **Output the full simulation package** in the format defined in the Output section.

## Examples

**Example 1: Full track input**

> "The learner has completed: stakeholder alignment, product prioritisation, and communicating strategy to executives."

Expected: Agent designs a company context where a strategic prioritisation decision must be made, defended to a sceptical executive, and navigated through competing stakeholder agendas — escalation tied to alignment and communication breakdowns.

**Example 2: Single module input**

> "Run a crucible on giving difficult feedback."

Expected: Agent scopes the simulation tightly — a single relationship under pressure across 4 acts, escalating from awkward feedback to a formal performance conversation. Character roster is smaller (2–3 characters).

## Boundaries

- Never reuse the same conflict type across two acts

- Never create characters without competing interests

- Never design Act 4 with a single correct answer — evaluate on reasoning quality, not outcome

- When the simulation belongs to an ongoing narrative, preserve character motivations, unresolved consequences, and prior decisions across cycles

- On learner response, continue the simulation dynamically until a credible resolution or defined terminal state; then debrief against the learning objectives

- Never produce a simulation that does not activate at least 2 distinct skills or frameworks from the learner's completed modules

- Never skip the facilitator instruction set — scenario content alone is not a complete output

- Debrief criteria must map explicitly back to the learning objectives of the modules covered

## Output

Format: Markdown, structured as: Crucible title, World Brief, Character Roster (table), 4 Acts (each with Situation, Active Characters, Challenge, Escalation Trigger), Facilitator Instructions (per-act opening, per-character triggers, Act 4 evaluation criteria, debrief structure).