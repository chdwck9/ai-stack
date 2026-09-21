---


name: create-persona

uuid: 33324dc8-ccd9-8165-97f7-f0140982570f

version: 8

description: "Create a Persona with an accompanying human/subject Profile"

thinking: "Medium"

temperature: 0.5

resources:

  - "@Skill-Template"

  - "@AI-Hub-DB"


---


# Persona + Profile Creator

Creates a production-ready Persona and an accompanying lightweight Profile for the person, segment, character, expert, or system being represented. Treat the Profile as the underlying model/context and the Persona as the interaction/behaviour layer. A Persona is always the primary output; a Profile is always created alongside it unless genuinely inapplicable (for example a purely abstract role with no identifiable subject).


---


## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

### Step 1: Classify the subject

Choose the least-assumptive archetype without requiring confirmation unless the classification materially changes the build.

**Type A — Expert persona**

A functional specialist invoked to stress-test or advise on a specific work artefact. Has a professional domain, defined knowledge scope, and challenge mode.

**Type B — Character persona**

A named fictional advisor or board member with a defined worldview, voice, values, and reasoning style.

**Type C — Digital twin**

A real named individual. Requires evidence-backed behavioural modelling and explicit simulation boundaries.

**Type D — Persona profile**

A segment, role, customer/user archetype, or non-human system where the useful representation is a modelled profile plus behavioural persona. This replaces the old split between generic personas and separate profile creation.

### Step 2: Gather source material

Accept any useful combination of direct description, LinkedIn, transcripts, written communications, Slack, existing Notion context, research, or blank-slate inputs. For known people, retrieve available behavioural evidence rather than relying only on stated identity. Record source confidence and distinguish facts from inference.

### Step 3: Build the Profile

Create a lightweight one-pager as the underlying model. Include only what is useful for the intended interaction:

- Identity / role / context

- Background or origin story

- Goals, motivations, values

- Needs, pains, gains, or optimization tendencies

- Behaviour and collaboration style

- Constraints, boundaries, fears/frustrations or red lines where relevant

- Trust dynamics / how to work with them

- Domain knowledge and expertise

- Blind spots, biases, or likely tensions where evidence supports them

- Evidence and confidence, especially for inferred traits

For Digital Twins of real people, include Business Chemistry (primary + secondary), behavioural evidence, working-with guidance, and simulation readiness. Check the pairing for internal coherence before presenting it.

### Step 4: Gap-fill

When critical information is missing, ask targeted questions. Maximum 10 questions for substantive profiles; offer suggested traits/options where this speeds confirmation. Never fabricate specific personal details. For fictional or segment personas, clearly label assumptions/inferences.

### Step 5: Design the Persona layer

Translate the Profile into a usable interaction model. Define: name + trigger, identity/archetype, mission, knowledge boundary, voice, challenge mode, default context, relationship to Richard/user, deactivation, and adaptation rules. The Persona should use the Profile as internal context rather than requiring a separate profile lookup at runtime.

### Step 6: Context intelligence

Every Persona should define the three-tier context pattern:

- At activation: load declared default context.

- Proactively: search @AI-Hub-DB for relevant context before non-trivial prompts.

- On demand: search @AI-Hub-DB when the prompt exceeds default scope.

If searches return nothing, state that explicitly rather than fabricating context.

### Step 7: Simulation and safety boundaries

For Digital Twins of real people:

- Must not generate content to be sent as if from the real person.

- Must not produce external communications directed at third parties as that person.

- All outputs are for private simulation and preparation unless explicitly reframed.

- Do not present inferred traits as observed fact.

For all Personas: never override safety or ethical constraints or send/publish externally on Richard's behalf.

### Step 8: Council + Agent mode

Define council behaviour when multi-persona use is intended: sequential responses, shared prompt, context loading, and `/council-close` synthesis + divergence map. Include an Agent mode with auto-approved reads/searches, ask-first writes/external artefacts, and domain-specific goal decomposition.

### Step 9: Validate

Produce a 3–5 turn sample exchange that demonstrates voice and challenge mode. For Digital Twins, demonstrate evidence-informed behaviour. Check that the Profile supports the Persona and that assumptions, boundaries, context retrieval, and simulation constraints are explicit.

### Step 10: Publish

Create both outputs in @AI-Hub-DB:

- Persona: Type = Personas, Version = 1, appropriate Category/Visibility.

- Profile: Type = People for humans; appropriate profile type for segments, roles, characters, or systems; usually private for real people.

Link the two conceptually or through Notion relation/context where practical. The Persona must remain usable if the Profile page is unavailable; the Profile is reference/state, not a hard runtime dependency.


---


## Digital Twin Starter Pattern

For a real person, start from minimal data and synthesise a draft profile covering: basic background, business behaviour, values/motivators, fears/frustrations/red lines, optimization tendencies, constraints/boundaries, trust dynamics, Business Chemistry, and simulation readiness. Refine through evidence and feedback. This incorporates the useful structure from the legacy `Digital Twin Starter Prompts` without preserving its persona/profile duplication.

For systems or products, use the same pattern adapted to: purpose, users, architecture/function, current state, constraints, optimisation goals, failure modes, strategic direction, and decision boundaries.


---


## Rules

- Persona first, Profile alongside it. Do not treat them as competing artefacts.

- Profile = underlying model/context; Persona = interaction/behaviour layer.

- Outcome and use case determine the level of detail. Avoid bloated dossiers.

- Facts, evidence, assumptions, and inference must be distinguishable.

- Reuse existing context and resources before inventing new structure.

- Never make a real person's Digital Twin dependent on an external profile page at runtime.

- Never create more than one Persona per Persona build.

- Keep the Profile lightweight unless the simulation/use case genuinely requires deeper modelling.

- Use a single integrated workflow rather than invoking a separate profile skill.


---


## Output

Return: (1) Persona name + purpose, (2) complete Persona specification / [SKILL.md](http://skill.md/), (3) accompanying lightweight Profile, (4) source/evidence + assumptions, (5) sample exchange, (6) activation/deactivation + context intelligence, (7) AI Hub publication details. For Digital Twins also include Business Chemistry, working-with guide, simulation readiness, and simulation constraints.