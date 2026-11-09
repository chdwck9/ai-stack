---


name: plan
description: "Plan Task Decomposition"
uuid: 40e24dc8ccd981c4b7ae-ea452654cb35
version: 4
scope: local
thinking: Medium
temperature: 0.3
last-used: "2026-11-05"
resources:

- "@Ship-It-DB"


---


# $plan — Task Decomposition

Break a complex Ship-level task into discrete, atomic subtasks posted to the board as `Do next`. Planning only — `$plan` never executes the brief. Each row then runs its own `$handle-delegated-task` lifecycle.

## When to Use

Richard invokes `$plan <task description>` on a complex item. Use when the work has more than two logical steps, mixes human and agent work, or admits parallel execution. Do not use for simple single-step items — create those directly.

A `$plan`-prefixed title means **decompose, never execute** — even when the ask looks trivial. Decomposition and execution are different runs.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Clarify scope.** Parse the request into component workstreams. If ambiguous, make reasonable splits; ask Richard only if truly unparseable.

1. **Decompose.** Split into atomic steps, each completable by exactly one participant — Richard (human) or Clarity (clanker). No hybrid steps. Keep each within ~1 hour of focused work.

1. **Classify.** Label each `human` or `clarity`. Clarity steps get a short body with context or a `$one-shot` spec. **The agent's own research is not a row** — reading a source doc, fetching a page, or checking the board is implicit work, never a deliverable (see Taste).

1. **Create Ship rows.** One row per step, via the Notion MCP `notion-create-pages` (or `notion_bulk.py create`) — **never ****`props`** (see Pitfalls):

  - **Title:** short, verb-first, action language. Clarity steps end with ` *`; human steps carry no suffix. Never numbered headings ("Module 1", "Phase A") — say what the work actually is.

  - **Live:** inherit the parent's pillar (@Edge / @Craft / @Bonds / @Mambu). Unlinked → @Edge.

  - **When?:** today's date — `YYYY-MM-DD` (`is_datetime: 0`).

  - **Status:** `Do next`.

  - **Priority:** `#5`.

  - **Body:** clarity steps only — context, inputs, `$one-shot` spec. Human steps: no body beyond the title.

  - **Parent:** none — decomposition rows are board-level tasks, not child pages.

  - **Do NOT set Who.** The `*` suffix is the classifier; `Who` fires the delegation webhook, which `$plan` is not.

1. **Verify by read-back.** Re-fetch at least one created row and confirm it **exists** in Ship with Status `Do next`, Level `To Do`, When? today, Live correct. Report the count of rows you actually read back. If a row is missing, say so — never report success off a write you did not verify.

## Examples

**Input:** `$plan propose a price increase`

**Output — rows created (all ****`Do next`****, today):**

## Boundaries

- **Never execute a decomposed task.** `$plan` stops after Step 4 — no `$one-shot`, no external tool work, nothing performed. The rows are for Richard, or a later pass.

- **Never let a clanker author the deliverable itself.** Proposal writing, judgement, and sign-off are **human** steps. Clankers support with separate evidence-gathering and market-research rows only.

- **Never put the agent's own research on the board.** Fetching the source, reading the page, or checking the board is implicit and baked into the run — not a row.

- **Never assign ****`Who`****.** The `*` suffix is the sole classifier.

- **Never set a ****`Parent`****.** Decomposition rows are board-level, not child pages.

- **Never create fewer than three rows.** If the input admits only one or two, note it and create those anyway with a one-line explanation.

- **Do not modify the original parent task.**

- **Never leave a row unassigned** — every row is `*` (clanker) or bare (human).

## Output

A short confirmation listing each created row: title, type, status, when, live, suffix — plus the total count and any errors. Report only rows you read back.

## Taste

Richard-originated, grown by `$reinforce`. Signal → preference.

- Decomposed rows land in **`Do next`**, not `Waiting`. → They must appear on the board immediately.

- The agent's first research step is **not a board row** — fetching the source is baked into the agent. → Never emit a "Fetch the docs" row.

- **Clankers never author the proposal.** Proposal writing is a human step; clankers supply evidence gathering and market research as two separate rows (one evidence, one market research).

- Keep titles under ten words. Long descriptions go in the body.

- A `$plan` run should feel like unrolling a map, not writing a novel — terse steps, clear owners, actionable bodies.

## Pitfalls

- **`notion_bulk.py props`**** only UPDATES; it does not create.** Against a name that does not exist it still prints `ok`, so a "created" report off `props` is a lie. Use `notion-create-pages` (or `notion_bulk.py create`) and verify by read-back.

- **A ****`$plan`**** title is planning, not doing.** If you catch yourself executing the brief, stop — the decomposition is the whole deliverable.