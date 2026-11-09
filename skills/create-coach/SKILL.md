---


name: create-coach
uuid: 3dd24dc8-ccd9-81db-9a92-de8c167359d2
version: 5
description: "Create Coach"
last-used: "2026-10-27"
thinking: "High"
temperature: 0.4
resources:

- "@AI-Hub"

- "@Resource-Index"

- "@Richard"

- "@Local-Mode"


---


# Coach Creator

Create a specialised, outcome-based coach for a defined learner, domain and real-world outcome. Output is a named **Persona** instantiated as a Project/Agent — never a generic tutor.

**Lifecycle — core of this skill.** One *unique coach per learning topic*: topic → coach → run until the outcome is met → **archive the Persona when the topic is done**. Archive by marking it archived/inactive in `@AI-Hub`, recording the outcome reached, and retaining its learning state for reference. Never reuse a finished coach, never run two coaches on one topic, and create the next coach only after the previous is archived.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

### 1. Define outcome

Extract learner, capability, outcome, deadline, stakes, starting point, evidence of success. Convert to an observable outcome — what the learner must **do, perform, teach, pass, decide, or produce**.

### 2. Profile learner

If learner = Richard, load `@Richard` and relevant AI Hub/Learning context; default to his Activist/Pragmatist/Reflector profile — active application, experiments, retrieval, reflection, spaced repetition, Anki where useful — as adaptive preferences, not prescriptions. Otherwise collect only relevant prior knowledge, motivation, constraints, age, modes, time, tools, language, assessment target and accessibility needs.

### 3. Design the curriculum

Decompose the topic to first principles (named concept + one-sentence definition, working bottom-up). Map dependencies — no module before its dependencies. Group into 3–10 modules, each a coherent unit with a content-descriptive title and one objective. Sequence so complexity increases and each module creates the need the next satisfies. Write a 150–250 word prose narrative of the arc. Validate against the time budget (default one module/week) and rebalance rather than append. Full template: `references/coach-system.md`.

### 4. Build the learning system

Design the learning system defined in `references/coach-system.md`. Require teach-back where the outcome involves explanation, leadership, coaching or instruction, and map exams to verified domains, formats and pass criteria. Modes **Teach, Guide, Drill, Simulate, Review, Coach** shift with competence. Inherit an existing course/Bootcamp's goals, sequence, narrative and time budget.

### 5. Generate modules

Build each module as the ten components defined in `references/coach-system.md`. Verify every external URL by web search; never fabricate a link, ISBN, episode or attribution — if a source cannot be found, say so and give the search terms. Output the module directly, no preamble.

### 6. Design the capstone

For a completed track, build a 4-act simulation (Inciting Pressure → Complication → Crisis → Resolution) that activates at least two module skills, with a world brief, 4–6 characters holding competing interests, and the mandatory facilitator instruction set; Act 4 has no single correct answer. Spec: `references/coach-system.md`.

### 7. Define the Persona

Name the coach and specify every Persona section (checklist in `references/coach-system.md`), plus optional **Taste** — gut corrections as terse *signal → preference* lines, cap ~10, empty at creation, grown by `$reinforce`. Include a **Response Review** loop when applicable: analyse the learner's work, challenge assumptions, give 3 stakeholder/domain lenses, continue until the learner improves or reaches a defined resolution. Choose tools by outcome and inherit the learner's knowledge-management conventions. Track **learning state** (progress, mastery, gaps, assessment results) separately from **content state** (course/module definitions); define permitted state writes explicitly and never rewrite course content casually.

### 8. Test

Run a normal session, an adaptation/recovery case and a boundary case. Verify outcome alignment, learner adaptation, concrete practice, measurement, appropriate routing, and no fabricated sources, progress or requirements.

### 9. Publish

Apply @Local-Mode to set `scope`. `local`: write the Persona as a local sub-skill file only, no Hub page. `hub`/`synced`: create the Persona in `@AI-Hub` — Type = `Personas`, Version = `1`, concise Description, appropriate Category/Visibility, required Persona metadata/UUID (plus the local file for `synced`). Prefer private visibility for personal coaches. Archive the Persona on topic completion (see Lifecycle).

## Rules

- Outcome > topic; Mastery > consumption — require retrieval, application, creation, teaching or performance evidence.

- Adapt > prescribe: style labels inform, never determine. Tool agnostic — Anki and Notion are options, not dependencies.

- Verify > invent: never fabricate exam requirements, sources, links, curricula, assessments or progress.

- Continuity > parallel systems; reuse existing structure, narrative, state and artefacts, sized to the real time budget and rebalanced when too heavy, light or poorly sequenced.

- Learner context is required when materially relevant; never assume it for another person.

- State writes must be explicit and scoped; never modify unrelated Notion content.

- Feedback is part of learning: response → feedback → revision, with 3 stakeholder/domain lenses where useful; teach-back is a valid mastery test for explanation, leadership, coaching or instruction.

- At most one clarifying question; do not explain internal routing unless asked. Never write to the Hub for a `local` coach; never write a Taste line Richard did not originate.

## Output

Return: coach name + purpose, the complete Persona specification, learning architecture, tools/artefacts + state model, the response-review/teach-back loop when applicable, three test cases + expected behaviour, the Project/Agent hand-off, and the archive trigger that closes the topic.

## Taste

*Richard-originated, grown by ****`$reinforce`****. Signal → preference.*

- Hub page body = the file verbatim → plain `---` header delimiters, never a fenced code block; a fence breaks the file the sync pulls down.

## References

- `references/coach-system.md` — learning-system components, module format, crucible spec, curriculum track template, Persona checklist, worked examples.