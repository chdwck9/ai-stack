---


name: dt-loop
uuid: 38b24dc8-ccd9-81b1-b70b-c10b8e991b05
version: 7
description: "Dt Loop"
return: "Artifact per completed high-level phase (skeleton, mockup, MVP), plus a final loop-complete summary"
thinking: "High"
temperature: 0.5


---


# Design Thinking Loop

A design-sprint execution wrapper. Wraps any goal in a structured iterative loop that runs to
completion — always an artifact unless the type is a document. Runs autonomously unless external
critique mode is active.

## When to Use

- **Artifact goals** (UI, JSX/HTML, SVG, diagrams, designs, documents) → three-phase artifact
contract: Skeleton → Mockup → MVP.

- **Non-artifact goals** (analysis, synthesis, writing, research, Notion ops, data tasks) →
single-loop mode: run the atomic loop until the Pareto gate fires, then one summary.

- **Prototype sprints** (brief + success criteria + HMW-scoped specs) → prototype mode: build each
prototype through the artifact contract, then mandatory write-ups.

If a non-artifact request actually produces a designed artifact, halt and direct it there instead.

## Core Principle

Iterate in short cycles. Verify each cycle against the stated goal — the phase test in artifact
mode, the goal statement in single-loop mode. Stop when the goal is verifiably met, never when a
budget or loop count runs out. If the Pareto gate fires but the goal is unmet, run one more loop
targeting the gap.

## The Atomic Loop

The irreducible unit of work, run inside every phase and mode:

1. **DEFINE** — the specific problem this loop solves

1. **PLAN** — the best approach (medium, structure, tooling)

1. **BUILD / EXECUTE** — produce or improve the artifact/output (output in full)

1. **CRITIQUE** — evaluate from the declared user's / recipient's perspective

1. **REFLECT** — evaluate from your own perspective

**Reflections** combine steps 4–5: discrete, named observations — gaps, improvements, risks,
strengths to preserve. Each is one actionable item; the same observation never counts as new
across loops.

## The Pareto Gate (80% threshold)

A phase (artifact mode) or the loop (single-loop mode) closes when marginal yield of new
reflections drops to ≤20% of the first loop's count.

- Loop 1 surfaces N reflections → this is the baseline.

- When a loop surfaces ≤ 0.2 × N new reflections, the threshold is met / gate fires.

- N = 0 in loop 1 → close immediately after loop 1.

- Evaluated after BUILD/EXECUTE + CRITIQUE + REFLECT — never before.

In artifact mode the phase must also pass its declared phase test before closing.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list
marked `skip: <reason>` — never dropped silently.

### 1. Parse invocation

Extract the `skill` (optional — if named, load its [SKILL.md](http://skill.md/) and apply its domain knowledge,
resources, and permissions), the `goal`, and `--external-critique` (or equivalent mid-run phrases —
see `references/artifact-phases.md`). If the goal is ambiguous, ask one question: "What are you
building and who is the primary user?" Do not proceed without a clear goal.

### 2. Declare setup

One block before the first loop: goal summary, skill (or none), medium, user persona, external
critique on/off, starting phase/mode. Infer the medium from goal context; hold it constant unless a
phase test reveals otherwise. Proceed immediately.

### 3. Run the loop(s)

- **Artifact mode:** Skeleton (feasibility, unstyled but wired) → Mockup (desirability, looks
finished) → MVP (viability, production-handover-ready). Each phase runs as many atomic loops as
needed until both the Pareto threshold and its phase test pass. Handoff block at each phase
close, compression block between loops.

- **Single-loop mode:** DEFINE → PLAN → EXECUTE → CRITIQUE → REFLECT until the gate fires and the
goal is met. Batch all ask-first writes into a single confirmation gate.

- **Prototype mode:** parse and clarify brief + criteria + specs; assess and augment; plan build
order; build each via the artifact contract; produce mandatory write-ups.

### 4. Complete

**MCD write-back:** if a loaded skill has an associated MCD, or findings extend/contradict any
MCD, invoke /mcd-sync (event trigger) with decisions, learnings (pattern/anti-pattern), and
resolved/new ambiguities. Context-class auto-applies; contract-class joins the final write gate.
"Nothing to write" is valid — skipping the evaluation is not. Then emit the single completion
summary.

## Boundaries

- Never ask clarifying questions mid-run — one pre-run question only.

- Never collapse phases — each must produce a distinct artifact.

- Never skip CRITIQUE or REFLECT, or advance a phase without both threshold AND phase test passing.

- Never produce prose-only output when the medium is not a document type.

- Never restart the baseline mid-phase/run, or re-read compression blocks older than N-2 loops
unless a halt requires backtracking.

- Never close without evaluating the MCD write-back.

- Ask first before writing the final artifact to external systems (Notion, Figma, Google Drive)
unless the loaded skill auto-approves.

## Pitfalls

- **HTML-for-JSX substitution** is a known failure mode: a declared `jsx`/`app` medium is a hard
constraint — always a JSX React component, never HTML dressed as JSX.

- Never emulate the artifact contract inline — invoke it explicitly; single-loop mode is not a
valid fallback for artifact work.

- Never ship empty states or lorem ipsum — prototypes carry domain-appropriate demo data.

- In prototype mode the Step 2 assessment is the only input gate; never proceed past it without
input, and never wait for input between build and write-up.

## References

- `references/atomic-loop.md` — loop + compression formats, Pareto/reflection handling.

- `references/artifact-phases.md` — invocation, setup, phase tests, handoffs, completion,
external critique mode, examples.

- `references/prototype-sprint.md` — input template, Steps 0–6, write-ups, Notion publish,
boundaries.

- `references/operations.md` — single-loop mode, agent permissions, escalation ladder, halts,
mobile contract, examples.