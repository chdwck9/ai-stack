---


name: get-shit-done
uuid: 3fb24dc8-ccd9-8187-8f13-c027b40af707
version: 4
description: "Operate Richard's Ship DB — tasks, projects, goals"
last-used: "2026-10-26"
scope: local
thinking: "Medium"
temperature: 0.3
resources:

- "@Ship-It-DB"

- "@Ship-DB-Reference"


---


# Get Shit Done

Operate the Ship DB (`@Ship-It / @GSD / @Ship-It-DB`) — Richard's single source of truth for tasks, projects, goals, rituals and milestones. Use it whenever Clarity creates, updates, completes, defers or triages Ship work, or answers "what's on this week".

Load `@Ship-DB-Reference` for the full schema, view table, related DBs, automations and provenance. Never guess from this summary alone.

## When to Use

- Clarity is asked to add, move, complete, defer or triage Ship work.

- Any "what's on this week / what should I do next" question.

- Writing a week's Milestones, or reconciling across projects and pillars.

- Checking whether an item will actually show up on a view.

## The model

- **Level** — the spine: `Goal → Project → To Do → Ritual`, plus `Milestone` (the week/project **outcome**), `Thing` (a standing asset) and `Idea`.

- **Status** — `Backlog` (not this week) · `Waiting` (**weekly** holding bucket) · `Do next` (**daily** holding bucket; 1–3 in execution order when intense) · `Doing` · `Defer` (transient — automation returns it to `Waiting` +1 day) · `Shipped` · `LEAD` (Leveraged / Eliminated / Automated / Delegated — credit for work not done) · `Abandoned`.

- **Priority** — `#1` · `#3` · `#5` · `Everything else` · `Headache` (outranks `#1` in a crisis) · `Connect` (meetings, 1:1s, social).

- **Live** — the pillar relation: `@Bonds` (highest) / `@Craft` / `@Edge` (lowest), sometimes with a company/workspace page added.

- **`This week`** is *derived* — it populates from the `When?` start date. Never set it by hand.

## Minimum fields — non-negotiable

Every row needs **`Live`**** · ****`When?`**** (start) · ****`Level`**** · ****`Status`**, `Archive?` left false, to appear on any view. Add **`Priority`** whenever the item is real work — most views, and the sprint, require it.

Sprint membership = `Status ∈ {Waiting, Do next, Doing}` **and** `Priority` set **and** `When?` start inside the week.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays marked `skip: <reason>`.

1. **Locate the work.** Resolve the project/goal/Thing it belongs to; load its MCD via `Master Doc` when one exists. If nothing fits, choose the correct Level rather than defaulting everything to a task.

1. **Choose the Level + Status** from the model above. A Milestone is an *outcome*, not a task. Ask only when the intent is genuinely unclear.

1. **Set the minimum fields** — Live, When? start, Level, Status, plus Priority for anything actionable. Size each task at roughly one hour.

1. **Guard the load.** Check the pillar's capacity before adding: **@Craft ≤ ~40–50 items/week** (incl. `Connect`), **@Edge ≤ 1–2 items/day**.

1. **Write** through the Notion MCP (create or update). **Never delete** — correct only an erroneous entry.

1. **Verify** — re-read the row, then check again a few minutes later that **`Linked?`** populated (the downstream-automation success signal). Never write `Linked?` yourself.

1. **Report** what changed, and anything that now threatens the week.

## Boundaries

- Never set `This week` by hand; it derives from `When?`.

- Never invent properties — use the existing schema.

- Never create admin, filler or vanity tasks.

- Never delete a row; correct it instead.

- Never leave a row stale because the work finished off-board. Work completed, leveraged or dropped in Discord, a CLI session or by hand still reconciles the Ship row — the lifecycle marker, the `Status`, and a comment saying where it actually happened. A row completed elsewhere with no trace reads as stuck.

- Never touch `Linked?`, `Checked`, `Print` or `Phase`.

- Never mark something `Shipped` unless it actually completed; use `LEAD` for work dodged on purpose and `Abandoned` for dropped work.

- Never link a task to a Milestone — tasks link to the pillar (`Live`) only.

- Never write weekly Milestones without first presenting the proposed list for confirmation.

## Taste

*Richard-originated, grown by **`$reinforce`**. Signal → preference.*

- Milestone = the most important **outcome** for a week/month/phase, and it should be measurable. → Prefer one sharp milestone over several vague ones.

- Each task ≈ 1 hour. → Estimate in hours and keep the board honest.

- @Edge realistically yields 1–2 tasks a day. → Don't staff evenings like a working day.

- Vanity/admin tasks → steer clear, unless energy is low, then document and celebrate every win.

- Names: short, verb-first, phone-readable. → If the name is ambiguous, describe it in the page body, not the title.

- Backfills are prompted, never routine → when Richard asks for one, apply this utility as a reference; don't build or presume a standing backfill mode.

- Backfill `Priority` → `Everything else`, upgraded to `#3` only when the item is genuinely critical.

- Backfill `When?` → the day the work happened or completed, never the day it's recorded.

- Pillar capacity is a default, not a limit → an unusual week (leave, a blocked workstream) can exceed @Edge's 1–2/day.

- Work finishing off-board (Discord, a CLI session, by hand) → reconcile the Ship row anyway: marker, `Status`, and a comment naming where it happened. *(evidence: "we actually completed in Discord … it should still resolve the Notion task details")*

## Verification

- The row shows on its intended view (minimum fields present).

- `Linked?` populated after the create automation runs.

- Pillar capacity rules not breached.

## Next steps

Invoke with the work to capture or move, e.g. `$get-shit-done add "Send Tiago the Egle feedback" to Craft, #3, this week`.