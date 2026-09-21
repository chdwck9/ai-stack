---


name: loop

uuid: 38824dc8-ccd9-8152-ab25-c0b173e30b9b

version: 9

description: "Loop"

return: "Single completion summary after goal execution, with per-loop reflection log"

tools:

- notion

thinking: "Medium"

temperature: 0.5


---


# Loop

Mobile-first execution wrapper. Accepts a skill and goal, runs atomic improvement loops until the Pareto gate fires, then stops. No mid-run questions. One summary at the end.

For artifact-producing goals (UI, diagrams, designs, documents), use `/dt-loop` instead — it runs the full Skeleton → Mockup → MVP contract with phase-level quality gates. `/loop` is for everything else: analysis, synthesis, writing, research, Notion operations, data tasks, and any goal where the output is not a designed artifact.


---


## Invocation

```javascript
/loop [skill] [goal]
```

Examples:

- `/loop bcaas summarise all open ambiguity zones and write them to Notion`

- `/loop tiago review the pricing proposal and surface three objections`

- `/loop wally audit the WAZ log for unresolved entries`

- `/loop weekly-status-update pull last week's chats and draft the Slack update`


---


## The Atomic Loop

The irreducible unit of execution. Repeats until the Pareto gate fires.

```javascript
1. DEFINE    — state the specific sub-problem this loop solves
2. PLAN      — select the best approach for this loop
3. EXECUTE   — do the work; produce or improve the output
4. CRITIQUE  — evaluate from the intended recipient's perspective
5. REFLECT   — evaluate from your own perspective
```

**Reflections** are the combined outputs of steps 4 and 5: discrete, named observations — gaps, errors, missing elements, improvements, or risks. Each is a single actionable item. The same observation does not count as a new reflection across loops.


---


## The Pareto Gate

The loop closes when marginal yield of new reflections drops to ≤20% of loop 1's count.

- Loop 1 surfaces N reflections. This is the baseline.

- Each subsequent loop surfaces some number of new reflections.

- When a loop surfaces ≤ 0.2 × N new reflections, the gate fires and the loop closes.

- If N = 0 in loop 1, the goal is met immediately — loop closes after loop 1.

- Threshold is evaluated after EXECUTE + CRITIQUE + REFLECT, not before.

The goal must also be verifiably met before the loop closes. If the Pareto gate fires but the goal is not met, run one more loop explicitly targeting the gap, then re-evaluate.


---


## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

### 1. Parse invocation

Extract:

- `skill` — the named skill to operate within (must exist in AI Hub)

- `goal` — the full goal statement

If either is missing, ask once: "Which skill and what goal?" Do not proceed without both.

### 2. Load skill

Load the named skill's [SKILL.md](http://skill.md/). Extract:

- Declared resources

- `## Agent mode` permissions block (if present)

- Domain knowledge and decomposition hints

If the skill has no `## Agent mode` block, apply global defaults: reads auto-approved, all writes ask first.

### 3. Plan

Decompose the goal into ordered steps. Do not present the plan to the user — proceed immediately.

### 4. Run atomic loops

Run loops sequentially. Each loop follows the DEFINE → PLAN → EXECUTE → CRITIQUE → REFLECT structure.

**Loop format:**

```javascript
--- Loop N ---
DEFINE:   [specific sub-problem this loop solves]
PLAN:     [approach selected]
EXECUTE:  [work output]

CRITIQUE: [evaluation from the recipient's perspective — what's missing, wrong, or weak]
REFLECT:  [evaluation from own perspective — gaps, risks, improvements, strengths to preserve]

Reflections this loop: [N]
Baseline (loop 1): [N_baseline] → Pareto threshold: ≤[0.2 × N_baseline]
Gate fires: [yes / no]
Unresolved carry-forward: [list]
```

**Compression between loops:**

After each loop, discard the full work output from that loop and retain only:

```javascript
[Loop N closed]
Output state: [what exists, what changed]
Unresolved reflections: [carry-forward list]
Next loop focus: [highest-priority unresolved item]
```

Loops older than N-2 are closed. Do not re-read them unless a halt requires backtracking.

**Write/send actions:** Apply the skill's declared permissions. Auto-approved actions execute silently. Ask-first actions are batched into a single confirmation gate — never ask per-action. If multiple ask-first actions are needed: "Before I continue, I need to: 1) [...] 2) [...] — proceed with all, some, or none?"

### 5. Complete

**MCD write-back:** if a skill with an associated MCD was loaded, or findings extend or contradict any MCD, invoke /mcd-sync (event trigger) with a compressed findings payload: decisions, learnings (pattern/anti-pattern), resolved/new ambiguities. Context-class auto-applies; contract-class items join the loop's single gate. "Nothing to write" is a valid outcome — skipping the evaluation is not.

When the Pareto gate fires and the goal is met, output one summary block:

```javascript
**[skill] — loop complete**

Goal: [restate]
Loops run: [N]
Total reflections: [surfaced / resolved / dismissed]
Gate fired: loop [N] — [X] new reflections vs baseline [N_baseline]

MCD: [nodes minted/updated via /mcd-sync, or none]
Done: [what was completed]
Skipped: [what was skipped and why, if anything]
Open items: [anything requiring follow-up]
```


---


## Agent Mode

Full permissions within the skill's declared scope.

**Auto-approved:**

- Reads, fetches, searches (any source)

- Producing and improving output

- Running any number of loops

- Compressing and discarding intermediate context

- Invoking /mcd-sync event write-back for context-class findings

- Escalating thinking level and, if still stuck, stepping the model up one tier at a time per the Escalation Ladder — no confirmation needed

**Ask first (batched, single gate):**

- Writes, deletes, sends, or publishes to external systems — unless the skill's `## Agent mode` block explicitly marks them auto-approved

**Never:**

- Ask clarifying questions mid-run (one pre-run question only if goal is ambiguous)

- Present the plan before executing

- Re-read closed loop compression blocks (N-2 or older) unless a halt requires backtracking

- Restart the baseline calculation mid-run

- Produce more than one summary block at completion

- Use `/dt-loop` logic — if the goal produces a designed artifact, halt and tell the user to use `/dt-loop` instead


---


## Escalation Ladder

When a loop is failing to coalesce — three consecutive loops surface zero new reflections but the goal is still not met — escalate before halting:

1. **Raise thinking.** Bump `thinking` one level (Medium → High → Max). Re-run the current loop once at the raised level.

1. **Raise model tier — incrementally.** If still stuck after the thinking bump, escalate the model one tier at a time (fast → general → frontier), keeping thinking at its raised level. Re-run the current loop once per tier; stop climbing the moment it coalesces.

1. **Exhausted.** If still stuck after both steps, the ladder is exhausted — proceed to Halt Conditions.

Declare each escalation inline before the loop it applies to: `[Escalating: thinking → High]` or `[Escalating: model → next tier]`. Drop back to the skill's default `thinking` and the environment's default model once the goal is met.

## Halt Conditions

Stop and surface once if:

- Skill does not exist in AI Hub — flag and stop

- A required action falls outside the skill's declared permissions

- Three consecutive loops surface zero new reflections but the goal is still not met (stuck) AND the Escalation Ladder above is exhausted

- Goal is so ambiguous no approach can be selected after one clarifying question

On halt: "I am stuck at [X]. Proceed with [option A] or [option B]?"


---


## Mobile Contract

Assume run-to-completion. Suppress all mid-run questions. If a halt condition is hit, surface a single binary: "I need to [X] to continue — proceed or skip?"


---


## Examples

**Read + synthesise:**

`/loop bcaas what are the current RTO targets across all tiers?`

→ Loads BCaaS skill + MCD. Loop 1: reads MCD, surfaces RTO table. Critique: missing AWSc Platinum row. Reflect: wording ambiguous for Silver. 2 reflections baseline. Loop 2: fills Platinum row, clarifies Silver wording. 0 new reflections → gate fires. Summary.

**Write to Notion:**

`/loop bcaas update the ambiguity zones table with the three items I flagged`

→ Loop 1: reads current table, drafts three new entries. Critique: entry 2 lacks owner field. Reflect: entry 3 duplicates OQ-018. 2 reflections. Loop 2: owner added, duplicate merged. 0 new reflections → gate fires. Single write gate: "Write 3 updated entries to Notion — proceed?" → writes → summary.

**Research + draft:**

`/loop tiago review the V20 pricing proposal and surface objections`

→ Loop 1: reads pricing proposal, surfaces 4 objections from Tiago's Integrator lens. Critique: objection 2 lacks commercial consequence framing. Reflect: missing dependency question on deal desk approval. 2 reflections. Loop 2: objection 2 reframed, dependency added. 1 new reflection (no done criteria stated). Loop 3: done criteria added. 0 new reflections → gate fires. Summary.


---


## Boundaries

- Never ask clarifying questions mid-run

- Never present the plan before executing

- Never execute a write without a confirmation gate unless auto-approved by the skill

- Never load a skill that doesn't exist in AI Hub — flag and stop

- Never produce more than one summary block at completion

- Never skip CRITIQUE and REFLECT in any loop

- Never re-read a closed loop compression block (N-2 or older) unless halted

- Never restart the baseline calculation mid-run

- Never invoke `/dt-loop` logic — redirect artifact goals there instead

- Never close a loop without evaluating the MCD write-back step

- Always respect the named skill's hard-stop permissions — they override the goal


---


## Output

Single `**[skill] — loop complete**` summary block with loop count, reflection totals, and gate trigger.