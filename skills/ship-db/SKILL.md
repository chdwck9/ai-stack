---


name: ship-db
uuid: 3fb24dc8-ccd9-8172-aa13-d15ce25bfabc
version: 11
description: "Ship DB"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
author: Richard Dykes, Hermes Agent
license: MIT
metadata:
hermes:
tags: [ship, notion, tasks, gsd, ship-it, richard-os]
related_skills: [track-project, mind-dump, weekly-status-update, create-project, handle-delegated-task]


---


# Ship DB

Ship (`@Ship-It` / `@GSD` / `@Ship-It-DB`) is Richard's Notion database — the single source of
truth for tasks, projects, goals and rituals, and the task layer under Richard OS. The whole persona
stack reads it: Kagetsu/mind-dump, Ari/Floki/Shin, Wayfinder, track-project, weekly-status-update,
and Clarity.

## When to Use

- Creating, reading or updating anything in Ship; adding, moving, completing, deferring or triaging
work; "what's on this week / what should I do next".

- Deciding where a new item belongs, or checking whether it will show up on a view.

- Writing a week's Milestones, or reconciling across projects and pillars.

Full property list and per-view filter rules: `@Ship-DB-Reference`. Never guess from this summary.

## The model

- **`Level`**** is the spine** — `Idea · Ritual · Goal · Project · To Do · Thing · Milestone`. It decides
which views a row is eligible for; get it right first.

- **`Status`** — `Backlog` (not this week) · `Waiting` (**weekly** bucket; must get done this week) ·
`Do next` (**daily** bucket, 1–3 in order) · `Doing` · `Defer` (transient — returns to `Waiting`
+1 day) · `Shipped` · `LEAD` (credit for work not done) · `Abandoned`.

- **`Priority`** — `#1` → `#3` → `#5` → `Everything else` → `Headache` (sorts above `#1`) →
`Connect` (meetings, 1:1s, social).

- **`Live`** — the pillar `@Bonds` / `@Craft` / `@Edge`, sometimes plus a company space (`@Mambu`).
Effectively mandatory; may hold more than one relation.

- **`This week`**** is derived** from `When?` — never set it by hand.

**Minimum fields:** `Live` · `When?` start · `Level` · `Status`, `Archive?` unset, plus `Priority`
whenever it is real work. **Sprint membership** = `Status ∈ {Waiting, Do next, Doing}` **AND**
`Priority` set **AND** `When?` start inside the current week.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays marked
`skip: <reason>`.

1. **Locate the work.** Resolve the project/goal/Thing it belongs to; load its MCD via `Master Doc`
when one exists. If nothing fits, choose the correct `Level` rather than defaulting to a task.

1. **Choose Level + Status** from the model. A Milestone is an *outcome*, not a task.

1. **Set the minimum fields**, plus Priority for anything actionable. Size each task at ~1 hour.

1. **Guard the load:** @Craft ≤ ~40–50 items/week (incl. `Connect`), @Edge ≤ 1–2 items/day.

1. **Write** through the Notion MCP. **Never delete** — correct only an erroneous entry.

1. **Verify** — re-read the row, then check a few minutes later that **`Linked?`** populated (the
downstream-automation signal). Never write `Linked?` yourself.

1. **Report** what changed, and anything that now threatens the week.

## Boundaries

- Never set `This week` by hand; never invent properties; never create admin, filler or vanity tasks.

- Never delete a row — archive (`Archive? = __YES__`, reversible) or correct it. Deleting moves the
page to Trash: **only on Richard's explicit word.**

- Never touch `Linked?`, `Checked`, `Print` or `Phase`; never mark `Shipped` unless it completed
(use `LEAD` for work dodged on purpose, `Abandoned` for dropped work).

- Never leave a row stale because the work finished off-board — reconcile the marker, the `Status`
and a comment naming where it happened.

## Taste

*Richard-originated, grown by **`$reinforce`**. Signal → preference.*

- Work wraps by **Thursday** by default; craft → Thursday, Edge → Friday, Bonds leave alone.

- A meeting or 1:1 related to a task **is** that task's deadline — use it.

- Future-dated reminders are `Waiting`, not `Backlog`; `Backlog` needs an explicit move into the sprint.

- The sprint is timeboxed to the **current week only** → a future-dated row being invisible now is
expected, not a fault to fix.

- After any Status change, re-apply and re-verify `When?`.

- Milestone = the most important **measurable outcome** for the week/month/phase → one sharp
milestone beats several vague ones.

- Each task ≈ 1 hour → estimate in hours and keep the board honest.

- @Edge realistically yields 1–2 tasks a day → don't staff evenings like a working day.

- Vanity/admin tasks → steer clear; unless energy is low, then document and celebrate every win.

- Names: short, verb-first, phone-readable → ambiguity goes in the page body, not the title.

- Backfill `Priority` → `Everything else` (upgraded to `#3` only when genuinely critical);
`When?` → the day the work happened, never the day it is recorded.

- Pillar capacity is a default, not a limit → leave or a blocked workstream can exceed @Edge's
1–2/day.

- A project with no next action is **stalled** — say so.

- Report shape: what you did, the outcome, next actions — brief. Drafts only for anything that
reaches another person; never send.

## References

- `@Ship-DB-Reference` — every property, the ten views and their filter rules, automations, and the
write-authority contract.

- `@Calendar-To-Ship` — `/Volumes/Live/@Edge/.ai/resources/standards/calendar-to-ship.md` — the
calendar → `Connect` procedure, pillar routing and the CRM rules. Callable form: `$calendar-meetings-to-ship`.

- `@Ship-DB-Rules` — `/Volumes/Live/@Edge/.ai/resources/standards/ship-db/` — the rebuilt operational
standards: `ship-model-and-rules.md`, `notion-bulk-and-query.md`, `notion-write-mechanics.md`,
`notion-triggers.md`, `ship-projects.md`. A `references/` folder next to this file is wiped by the
nightly Hub → local sync — do not put extended notes there.
