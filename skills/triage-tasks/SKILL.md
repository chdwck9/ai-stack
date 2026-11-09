---


name: triage-tasks
uuid: TBD
version: 1
description: "Triage Tasks"
return: "Day blocks (day · time · purpose) + Do next: moved, stale flagged, clog reported"
last-used: 2026-10-27T12:00:00+01:00
thinking: Medium
temperature: 0.3
resources:

- "@Ship-DB-Reference"
author: Richard Dykes, Hermes Agent
license: MIT
metadata:
hermes:
tags: [morning, daily, planning, blocks, ship, clarity]
related_skills: [morning, monday, ship-db]


---


# Triage Tasks

Turn the day's commitments and the week's ranked goals into the blocks Richard works in, then open the execution bucket they serve.

## Inputs

The window and its commitments (from the `morning-mechanical` summary); this week's Milestones/Goals via `@Ship-DB-Reference`, ranked Bonds → Craft → Edge, Craft operational first.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Rank the goals.** Milestones are week-bound, never filtered by `When?`. No current-week Milestone → flag the week unopened, rank by task `Priority`. Never invent a goal.

1. **Gaps.** A `Focus Block`/`Lunch` placeholder is not busy; an all-day marker is not capacity. Never block over a commitment.

1. **Prep-first** for a performance-type event (showcase, demo, review); otherwise **focus-first** on the top 1–3 goals.

1. **Name each block** day · start–end · purpose. Only blocks beginning after now.

1. **Count ****`Do next`** — rows dated before the target day are stale.

1. **Flag, never trim** — stale rows go to **Needs Richard**; trimming is `$monday`'s call.

1. **Move only existing rows** serving a chosen block; `When?` = the block window as a datetime, never a day range.

1. **Cap is 1–3 execution rows.** Over-full → stop promoting; the clog is the finding, not a fourth row.

1. **Verify** each changed row by re-reading it.

## Examples

- **Clean bucket** — one row, the focus block serves the pricing model → promote it.

- **Clogged bucket** — 12 rows, all stale → promote nothing; name the clog.

- **No usable gap** — report and stop; never invent a focus to justify a move.

## Boundaries

- Never create tasks; never move a row to `Backlog`; never set `Shipped`/`LEAD`/`Abandoned`.

- Never set `This week` or write `Linked?`.

- Never trim a stale row, however dead it looks.

- Never block over a commitment, or before now.

- Bulk board changes via `~/.hermes/scripts/notion_bulk.py`, never a scatter of calls.

## Output

Blocks · Do next (moved · bucket N of 3) · Stale (Needs Richard) · Blocked.

## Next steps

Feeds the day report; `$monday` runs the weekly equivalent.