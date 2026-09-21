---


name: dt-loop

uuid: 38b24dc8-ccd9-81b1-b70b-c10b8e991b05

version: 6

description: "Design Thinking Loop"

return: "Artifact per completed high-level phase (skeleton, mockup, MVP), plus a final loop-complete summary"

thinking: "High"

temperature: 0.5


---


# Design Thinking Loop

A design sprint execution wrapper. Wraps any goal in a structured iterative loop that runs to completion, always producing an artifact. Never produces prose-only output unless the artifact type is a document.

Three high-level phases run sequentially — Skeleton, Mockup, MVP. Each phase runs as many atomic loops as needed until its quality threshold is met. Claude runs fully autonomously unless `external critique` mode is active.


---


## Invocation

```javascript
/dt-loop [goal] [--external-critique?]
```

Or as a wrapper:

```javascript
/dt-loop [skill] [goal] [--external-critique?]
```

When a skill is named, load it first and apply its domain knowledge, resources, and declared permissions throughout.

Examples:

- `/dt-loop build a pricing tier comparison component for the BCaaS sales deck`

- `/dt-loop bcaas design a service blueprint for the DR onboarding flow --external-critique`

- `/dt-loop create an interactive RTO/RPO calculator`

- `/dt-loop wally map the migration state machine as a diagram`


---


## Framework

### The Atomic Loop

The irreducible unit of work. Runs inside every high-level phase.

```javascript
1. DEFINE    — state the specific problem this loop solves
2. PLAN      — select the best approach (medium, structure, tooling)
3. BUILD     — produce or improve the artifact (always output in full)
4. CRITIQUE  — evaluate from the declared user's perspective
5. REFLECT   — evaluate from your own perspective
```

**Reflections** are the combined outputs of steps 4 and 5: discrete, named observations — gaps, improvements, risks, or strengths to preserve. Each reflection is a single actionable item. The same observation does not count as a new reflection across loops.

### The 80% Threshold (Pareto Gate)

A high-level phase closes when the marginal yield of new reflections drops to ≤20% of the first loop's count.

- Loop 1 surfaces N reflections. This sets the baseline.

- Each subsequent loop surfaces some number of new reflections.

- When a loop surfaces ≤ 0.2 × N new reflections, the Pareto threshold is met.

- If N = 0 in loop 1 (perfect first build), phase closes immediately after loop 1.

- Threshold is evaluated after BUILD + CRITIQUE + REFLECT — not before.

The phase must also pass its declared phase test before closing.

### High-Level Phases


---


## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

### 1. Parse invocation

Extract:

- `skill` (optional) — if named, load its [SKILL.md](http://skill.md/) and apply its domain context and resources

- `goal` — what needs to be designed or built

- `--external-critique` — flag, or watch for equivalent phrases mid-run: "external critique", "pause for critique", "I want to review between phases"

If goal is ambiguous, ask one question: "What are you building and who is the primary user?" Do not proceed without a clear goal.

**Infer output medium from goal context:**

Medium is declared upfront and held constant across all phases unless a phase test reveals it is wrong.

### 2. Declare setup

Single block before the first loop:

```javascript
**dt-loop — [goal summary]**
Skill: [named skill or none]
Medium: [declared medium]
User persona: [inferred or stated]
External critique: [on / off]
Starting Phase 1: Skeleton
```

Proceed immediately.

### 3. Run Phase 1 — Skeleton

**Goal:** Feasibility. Core concept must work end-to-end, unstyled.

**Phase test:**

- Does the artifact render or execute without errors?

- Does the core flow make sense without explanation?

- Is every interactive element wired to a state change?

- Does it answer the primary design question — even roughly?

**Atomic loop format:**

```javascript
--- Loop 1.N ---
DEFINE: [specific problem this loop solves]
PLAN:   [approach selected]
BUILD:  [full artifact output]

CRITIQUE (user — [persona]): [reaction / blocker / confusion]
REFLECT (self): [observations — gaps, improvements, risks, strengths to preserve]

Reflections this loop: [N]
Baseline (loop 1.1): [N_baseline] → Pareto threshold: ≤[0.2 × N_baseline]
Threshold met: [yes / no]
Unresolved carry-forward: [list]
```

When threshold met AND phase test passes → close Phase 1.

**Compression between loops:**

```javascript
[Loop 1.N closed]
Artifact state: [what exists, what changed]
Unresolved reflections: [carry-forward list]
Next loop focus: [highest-priority unresolved item]
```

Discard full artifact body from prior loops. Rebuild from carry-forward state.

### 4. Phase 1 handoff

```javascript
[Phase 1 complete — Skeleton]
Artifact: [description + medium]
Feasibility verdict: [pass — one line]
Loops run: [N]
Reflections: [total surfaced / resolved / dismissed]
Carry forward to Phase 2: [locked decisions, assumptions]
Open: [anything deferred]
```

**If external critique is on:** Pause. Present the final Phase 1 artifact and handoff block. Prompt: "Phase 1 complete. Add your critique or type 'continue' to proceed to Phase 2." Incorporate any critique as additional reflections carried into Phase 2 loop 1. Wait before proceeding.

### 5. Run Phase 2 — Mockup

**Goal:** Desirability. A real user should want to interact with this.

**Phase test:**

- Does it look and feel finished?

- Can the declared user persona complete the success scenario without instruction?

- Does it deliver on the core promise from Phase 1?

- Is it simple and intuitive?

Same atomic loop structure as Phase 1. Carry in Phase 1 handoff block only — do not re-read earlier compression blocks.

**CRITIQUE prompt (Phase 2):** "I am [persona]. This looks [reaction]. I would [action]. What delights me is [delight]. What would make me abandon it is [abandon reason]."

**REFLECT prompt (Phase 2):** "The biggest risk to viability I see is [risk]. I'll address it by [approach]."

Phase 2 handoff block mirrors Phase 1 format. External critique pause if on.

### 6. Run Phase 3 — MVP

**Goal:** Viability. Production-handover-ready.

**Phase test:**

- Does it function end-to-end with no dead states or broken flows?

- Is the underlying logic explainable in one paragraph?

- Could an engineer unfamiliar with this upskill on it quickly?

- Is the ROI case defensible?

**CRITIQUE prompt (Phase 3, customer/buyer lens):** "As a [buyer/customer], this product [value statement]. The thing I'd pay for is [value]. What would stop me buying is [objection]."

**REFLECT prompt (Phase 3):** "The hardest part to implement in production is [hard part]. The simplest path is [path]."

**Final walk:** Before closing Phase 3, walk each element of the design goal. Declare pass or fail per element. Only close when all pass.

External critique pause if on.

### 7. Complete

**MCD write-back:** if a skill with an associated MCD was loaded, or findings extend or contradict any MCD, invoke /mcd-sync (event trigger) with a compressed findings payload: decisions, learnings (pattern/anti-pattern), resolved/new ambiguities. Context-class auto-applies; contract-class items join the final write gate. "Nothing to write" is a valid outcome — skipping the evaluation is not.

```javascript
**dt-loop — complete**

Goal: [restate]
Skill: [named or none]
Medium: [final]
Atomic loops run: [N total — Phase 1: N1, Phase 2: N2, Phase 3: N3]
Total reflections: [surfaced / resolved / dismissed across all phases]

Phase 1 (Skeleton): [pass — feasibility verdict]
Phase 2 (Mockup):   [pass — desirability verdict]
Phase 3 (MVP):      [pass — viability verdict]

Engineering handover: [one paragraph — what this is, complexity, simplest production path]
MCD: [nodes minted/updated via /mcd-sync, or none]
Open items: [anything deferred or unresolved]
```


---


## External Critique Mode

Activated at invocation via `--external-critique` flag, or mid-run when equivalent phrases are detected. Once activated, it stays on for all remaining phase boundaries.

Behaviour:

- Claude runs each phase fully and autonomously

- At each phase boundary: pause, present artifact + handoff block, invite critique

- User critique is ingested as additional reflections for Phase N+1 loop 1 — they count toward that phase's baseline

- "continue" or equivalent with no content → proceed immediately

- Mid-run activation (e.g. "pause for critique going forward") → takes effect at the next phase boundary, not the current one


---


## Agent Mode

Full permissions. No confirmation gates inside phases.

**Auto-approved:**

- Producing and iterating artifacts (any medium)

- Running any number of atomic loops

- Compressing and discarding intermediate context

- Advancing between phases when threshold + phase test are both met

- Loading named skills and their resources

- Invoking /mcd-sync event write-back for context-class findings

- Escalating thinking level and, if still stuck, stepping the model up one tier at a time per the Escalation Ladder — no confirmation needed

**Ask first:**

- Writing the final artifact to external systems (Notion, Figma files, Google Drive)

**Never:**

- Ask clarifying questions mid-run (one pre-run question only, before loop 1.1)

- Collapse phases — each must produce a distinct artifact

- Skip CRITIQUE or REFLECT in any atomic loop

- Advance a phase without both the Pareto threshold AND phase test passing

- Produce prose-only output when the medium is not a document type

- Re-read compression blocks older than N-2 loops unless a halt requires backtracking

- Restart the baseline calculation mid-phase

- Close the loop without evaluating the MCD write-back step


---


## Escalation Ladder

When a loop is failing to coalesce — three consecutive loops surface zero new reflections but the phase test still fails — escalate before halting:

1. **Raise thinking.** Bump `thinking` one level (Medium → High → Max). Re-run the current atomic loop once at the raised level.

1. **Raise model tier — incrementally.** If still stuck after the thinking bump, escalate the model one tier at a time (fast → general → frontier), keeping thinking at its raised level. Re-run the current atomic loop once per tier; stop climbing the moment it coalesces.

1. **Exhausted.** If still stuck after both steps, the ladder is exhausted — proceed to Halt Conditions.

Declare each escalation inline before the loop it applies to: `[Escalating: thinking → High]` or `[Escalating: model → next tier]`. Once a phase closes successfully, drop back to the skill's default `thinking` and the environment's default model for the next phase.

## Halt Conditions

Stop and surface once if:

- Goal is ambiguous and medium cannot be inferred after one clarifying question

- Three consecutive loops surface zero new reflections but the phase test still fails (stuck) AND the Escalation Ladder above is exhausted

- A required external write falls outside auto-approved permissions

- Phase 3 test fails after 10+ loops with no progress, even after escalation

On halt: "I am stuck at [X]. Proceed with [option A] or [option B]?"


---


## Examples

**Standard — JSX component:**

`/dt-loop build a BCaaS tier comparison table as a JSX component`

→ Setup: medium=JSX, persona=Account Executive.

→ Phase 1: bare table, 3 tiers, row labels only. Critique: missing pricing row, no hierarchy. Reflect: column widths equal — Silver looks same weight as Gold. 4 reflections baseline. Loop 2: pricing row added, Gold column highlighted, labels clarified. 1 new reflection (tooltip missing). ≤0.2×4=0.8 → threshold met (1 > 0.8, not quite). Loop 3: tooltip added. 0 new reflections → threshold met. Phase test passes.

→ Phase 2: full styling, Mambu tokens, hover states, tier highlight logic. Baseline 5 reflections. Loops until ≤1 new reflection per loop.

→ Phase 3: configurable tier data, stateless, export-ready, inline comments. Engineering handover: single-file JSX, no backend, drop-in ready.

**Wrapper with skill:**

`/dt-loop bcaas design a service blueprint for the DR failover process --external-critique`

→ Loads BCaaS skill, reads MCD for failover steps.

→ Phase 1 runs. Pauses: presents Markdown blueprint + handoff block. "Phase 1 complete. Add your critique or type 'continue'." User: "Missing the comms step to customers during failover." Carried into Phase 2 loop 1 as a seeded reflection.

→ Phase 2 adds comms step, visual swim lanes. Pauses.

→ Phase 3 fully operational blueprint with SLA tags, owner columns, tool references. Summary block.

**Document output:**

`/dt-loop write the BCaaS DR runbook for Silver tier`

→ Medium inferred as Markdown. Three phases: skeleton (structure + headers), mockup (full content, no polish), MVP (complete, accurate, engineer-handover-ready).


---


## Output

- Always an artifact: JSX, HTML, SVG, Mermaid, Markdown document, or Figma-ready structure

- Medium determined at invocation, held constant unless a phase test reveals mismatch

- One artifact per phase, iteratively improved

- Final deliverable is the Phase 3 artifact plus the loop-complete summary block