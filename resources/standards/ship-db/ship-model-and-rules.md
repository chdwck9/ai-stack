# Ship — model and rules (rebuilt standard)

**Rebuilt** 2026-11-09 after the original `references/ship-model-and-rules.md` was lost to the
nightly Hub→local skill sync. Durable home: `@Standards`. **Canonical schema lives in
`@Ship-DB-Reference`** (AI Hub page `3fb24dc8-ccd9-814b-a739-f79b7f21f826`) — this file is the
operational layer, not a second copy of the property list.

Ship data source: `collection://55b38845-c284-4e37-9212-55c8e289da97` (DB page
`50a0b103-d3e04e2d93f0b899b79edeb3`), top-level workspace DB, not in the AI Hub.

## The model in one screen

- **`Level` is the spine** — `Idea · Ritual · Goal · Project · To Do · Thing · Milestone`. It decides
  which views a row can ever appear in.
- **`Status`** — `Backlog` (not this week) · `Waiting` (weekly bucket — must happen this week) ·
  `Do next` (daily bucket, 1–3 in order) · `Doing` · `Defer` (transient; an automation returns it to
  `Waiting` +1 day) · `Shipped` · `LEAD` · `Abandoned`.
- **`Priority`** — `#1 · #3 · #5 · Everything else · Headache · Connect`. `Connect` = meetings, 1:1s,
  social. `Headache` sorts above `#1`.
- **`Live`** — pillar `@Bonds / @Craft / @Edge`, sometimes plus a company space (`@Mambu`).
- **`When?`** — a date **range** (start + optional end). It is the single driver of "this week".
- **`This week`** — derived from `When?`. Never set it by hand.

## Why a row is invisible (the four causes)

1. **Wrong `Level`** — a `To Do` with no `Priority` never reaches Get Shit Done.
2. **No `Live`** — Goals, This week, Got Shit Done and Things all filter on it → orphan row.
3. **`Archive?` set** — Backlog, Goals, Roadmap, Outcomes, Things and To do list all require
   `Archive? = false`.
4. **`When?` outside the window** — the sprint is timeboxed to the current week; a future-dated row
   being invisible now is correct behaviour, not a bug to "fix".

**Sprint membership** = `Status ∈ {Waiting, Do next, Doing}` **AND** `Priority` set **AND**
`When?` inside the current week.

## Status rules that bite

- `Waiting` reads as *in progress*: putting something there means it must get done this week.
- `Backlog` requires an explicit move into the sprint; it is not a waiting room.
- **Never** set `Shipped` / `LEAD` / `Abandoned` without evidence the work completed or was
  deliberately dodged. `LEAD` = Leveraged / Eliminated / Automated / Delegated — credit for work
  not done on purpose.
- After any `Status` change, re-apply and re-verify `When?`.

## Meetings are not work

A meeting or 1:1 row is `Priority = Connect` with a **datetime** `When?`
(`is_datetime = 1`). Its date is when it happens — never re-date one to "work wraps by Thursday".
Procedure: `$calendar-meetings-to-ship` + `@Calendar-To-Ship`
(`resources/standards/calendar-to-ship.md`). Dailies are not board rows at all.

## Capacity discipline

- Each task ≈ **1 hour**.
- **@Craft** ≈ a working week → **≤ ~40–50 items/week**, including `Connect` events.
- **@Edge** ≈ evening free time → **1–2 tasks/day** realistically.
- No admin / filler / vanity tasks.

## Hard boundaries

Never set `This week`, `Linked?`, `Checked`, `Print`, `Phase` — derived or automation-owned.
Never delete (use `Archive? = __YES__`, reversible). Never invent properties. Never write a
birthday or anniversary into Ship. Never write project progress as a child page — it is inline on
the parent.

## Confirmed behaviours (Richard, 2026-11-09)

- **`Defer` is still automated** — it returns to `Waiting` +1 day. Don't hand-restore it.
- **`Headache`** is intended to **pareto useless tasks out of existence** (sort above `#1`, then
  discard or kill them). Richard is not currently enforcing it, so don't treat a `Headache` row as
  an instruction to delete anything — surface it, let him call it.
