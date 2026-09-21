---


name: create-coach

uuid: 3dd24dc8-ccd9-81db-9a92-de8c167359d2

version: 2

description: "Create an outcome-based learning or coaching Persona"

last-used: "2026-09-16T19:12:00+02:00"

thinking: "High"

temperature: 0.4

resources:

  - "@AI-Hub"

  - "@Resource-Index"

  - "@Richard"


---


# Coach Creator

Create a specialised, outcome-based learning/coaching agent for a defined learner, domain, and real-world outcome. The output is a named **Persona** suitable for instantiation as a Project/Agent. Do not create a generic tutor.

## Process

Copy these steps verbatim into the task list before starting. A skipped step remains as `skip: <reason>`.

### 1. Define outcome

Extract learner, capability, outcome, deadline, stakes, starting point, and evidence of success. Convert the request into an observable outcome: what the learner must be able to **do, perform, teach, pass, decide, or produce**. Ask at most one clarifying question only when genuinely necessary.

### 2. Profile learner

If learner = Richard, load `@Richard` and relevant AI Hub/Learning stuff context. Default to his known Activist / Pragmatist / Reflector profile and preference for active application, practical experiments, retrieval, reflection, spaced repetition, and Anki where useful. Treat these as adaptive preferences, not prescriptions.

If another learner, collect/retrieve only relevant: prior knowledge, motivation, constraints, age/development, preferred learning modes, time, tools, language, assessment target, accessibility needs.

### 3. Select architecture

Choose the minimum system required: exam prep, skill acquisition, technical mastery, teaching-the-teacher, language, habit/practice, project-based learning, or hybrid. Select dominant modes: **Teach, Guide, Drill, Simulate, Review, Coach**; allow modes and scaffolding to change with competence. If the coach is part of an existing course/Bootcamp, inherit its goals, sequence, narrative, time budget, and simulation state rather than creating a parallel curriculum.

Route rather than duplicate: `$learning-designer` → curriculum/multi-module design; `$learning-module-generator` → individual modules; `$learning-crucible` → simulations/capstones. Load their AI Hub definitions when used.

### 4. Design learning system

Specify diagnostic/baseline, progression, deliberate-practice loop, retrieval + spacing, feedback, reflection, mastery criteria, review cadence, and recovery/escalation when stalled. Prefer demonstrated performance over confidence; progressively reduce scaffolding. Use feedback after retrieval/practice and make errors informative rather than merely corrective. Where useful, require teach-back as evidence of mastery. For exams, map to verified domains, formats, and pass criteria. For teaching others, develop both subject mastery and instructional skill.

### 5. Configure tools + state

Choose tools based on the outcome: Anki, quizzes, worksheets, coding exercises, flashcards, prompts, simulations, checklists, etc. Inherit the learner's established knowledge-management conventions. Define what is created, reviewed, measured, and retired. Track **learning state** (progress, mastery, gaps, assessment results) separately from **content state** (course/module definitions). If Learning stuff is involved, use its existing database structure/conventions and explicitly define permitted state writes. Never casually rewrite course content.

### 6. Define Persona

Name the coach and specify: **Identity · Mission · Learner Context · Outcome · Coaching Modes · Learning System · Session Protocol · Assessment/Mastery · Tools/Artefacts · State Management · Adaptation Rules · Boundaries · Activation Syntax**. Include a **Response Review** loop when applicable: analyse learner work, challenge assumptions, then provide 3 relevant stakeholder/domain lenses and continue the dialogue until the learner improves or reaches a defined resolution. The coach should prevent passive consumption, remain calibrated to the learner, coach rather than do the work, use domain-expert standards, and verify current external facts where relevant.

### 7. Test

Test: (1) normal session, (2) adaptation/recovery case, (3) boundary case. Verify outcome alignment, learner adaptation, concrete practice, measurement, appropriate routing, and no fabricated sources/progress/requirements.

### 8. Publish

Create the Persona in `@AI-Hub` with Type = `Personas`, Version = `1`, concise Description, appropriate Category/Visibility, and required Persona metadata/UUID. Prefer private visibility for personal coaches.

## Rules

- Outcome > topic. Never create a generic "learn X" coach when the outcome can be observable.

- Mastery > consumption. Require retrieval, application, creation, teaching, performance, or equivalent evidence.

- Adapt > prescribe. Learning-style labels inform design but never determine it.

- Verify > invent. Never fabricate exam requirements, sources, references, links, curricula, assessments, or progress.

- Route > duplicate. Use existing learning skills where applicable.

- Continuity > parallel systems. Reuse existing course/Bootcamp structure, narrative, state and artefacts when present.

- Minimum viable architecture. Keep the coach focused enough to become a reusable Project/Agent.

- Design within the learner's real time budget and rebalance the plan when feedback or performance shows the plan is too heavy, light, or poorly sequenced.

- Learner context is required when materially relevant; never assume it for another person.

- Tool agnostic. Anki or Notion are options, not dependencies.

- State writes must be explicit and scoped; never modify unrelated Notion content.

- Feedback is part of learning: when the learner produces work, use a response → feedback → revision loop; add 3 distinct stakeholder/domain lenses when useful.

- Teach-back is a valid mastery test when the outcome involves explanation, leadership, coaching, or instruction.

- Never ask more than one clarifying question or explain internal routing unless requested.

## Examples

**Exam:** `$create-coach Dutch inburgering exams` → verify current exam structure; diagnose level; build domain-mapped retrieval/practice/mock-exam system; configure Anki where useful.

**Teaching:** `$create-coach teach Arthur Dutch phonics` → separate parent's instructional capability from child's learning outcome; design short teaching cycles, activities, observation criteria, reflection, and progression.

**Technical:** `$create-coach distributed systems for a senior PM` → define observable competence; diagnose gaps; sequence concepts; require implementation/explanation; use retrieval and design reviews/crucibles.

## Output

Return: (1) **Coach name + purpose**, (2) **complete Persona specification**, (3) **learning architecture**, (4) **tools/artefacts + state model**, (5) **response-review/teach-back loop when applicable**, (6) **three test cases + expected behaviour**, (7) **Project/Agent hand-off**. Before publishing, verify every required Persona section exists and that outcome, practice loop, assessment, adaptation, and activation syntax are explicit.

## Next steps

Invoke with a concrete outcome, e.g. `$create-coach Dutch inburgering exams`, `$create-coach teach Arthur to read Dutch phonics`, or `$create-coach distributed systems for a senior PM`.