---


name: monday
uuid: 3fb24dc8-ccd9-8196-92b0-cd7259c1fc25
version: 17
description: "Monday Reset"
return: "Week report: backlog · board · meetings · deep work · mail · alerts · timed · remotes · Jira · automations"
last-used: 2026-10-27T12:00:00+01:00
thinking: High
temperature: 0.3
resources:

- "@Ship-DB-Reference"

- "@Resource-Index"
author: Richard Dykes, Hermes Agent
license: MIT
metadata:
hermes:
tags: [monday, weekly, reset, orchestration, clarity]
related_skills: [morning, review-week, open-week, sweep-meetings, triage-inbox, mind-dump]


---


# Monday Reset

Orchestration and taste for the weekly reset: close the week just gone, open the one ahead. It does **not** do the work — the deterministic half has already run, and each judgement step is its own skill on its own model.

## When to Use

- It is Monday and the week needs closing and opening.

- A week was missed and needs catching up.

- Not the daily rhythm — that is `$morning`.

## Run mode

Establish the mode **before** step 1 — it changes which steps run.

- **Cron (the scheduled Monday job)** — the full reset.

- **Manual, start of week** — run `$mind-dump` first, then the full reset.

- **Manual, midweek** — a light pass only: calendar updates, goal review, `$mind-dump`. **Never clear Habitica and never move a row to ****`Backlog`** — those belong to the Monday cron.

- **Richard only:** the mind-dump.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Read the mechanical summary first.** The dagu DAG `monday-mechanical` runs at **08:00**, an hour before this job: window, Habitica clear, `Backlog` return, calendar and CRM copy, `Waiting` dating, OpenRouter refresh, mail-noise archive. Read `~/.hermes/state/monday/summary.json` and report what it applied — never repeat it. The two processes are divorced: if the summary is missing or stale, say so and carry on; never wait for the DAG.

1. **Dispatch ****`$review-week`** — milestone marks, project progress blocks, and verification of the `Backlog` return.

1. **Dispatch ****`$sweep-meetings`** — the Granola gap-fill.

1. **Dispatch ****`$triage-inbox`** at a **week** horizon.

1. **Dispatch ****`$open-week`** — propose the milestones, write the alerts, time the `Waiting` queue.

  Each step is **one run of its own skill**: `hermes chat -q "<step>" --skills <name>`. Pass the window and nothing else — never restate a step's rules, add guidance, or run two steps in one context.

1. **Remotes.** `herdr machine list`, then per remote: `workspace create` → `agent start --kind claude` → `agent prompt "<brief>" --wait --until idle --until done` → `agent read`. Work (Mambu) items run on **workbox, always Claude Code**; everything else on the **Studio, local-model-first**. Headless Claude Code needs `--allowedTools` set before it starts. Unreachable → skip and name once; `blocked` → **Needs Richard**.

1. **Weekly Jira report — work remote.** For **WAL**, **EOD**, **DR** (formerly MPO — the *same* project, never a second space) and **IDEA**: issues created, status transitions, substantive comments, blockers, due-date changes. Produce **flags** (only what needs Richard's *unique perspective* — requirement translation, expectation alignment, commitment-vs-record conflict), **candidate board rows** (propose, de-dupe against the board first) and a one-paragraph **birds-eye view** per space.

1. **Report.** Emit the shape below whether or not anything needed attention.

## Examples

- **Typical Monday** — Habitica 23 cleared; 6 rows returned to `Backlog`; 4 milestone marks proposed; 3 project blocks appended; 1 alert written; one Discord message.

- **A transcript gap** — a client call agreed a follow-up that never reached the board → `Waiting`, `@Craft`, `#5`, dated this Monday, Granola link in the body.

- **Midweek** — report only the lines that mode touched; never claim a `Backlog` return or Habitica clear that did not run.

## Boundaries

- Never set `Shipped`/`LEAD`/`Abandoned` without explicit evidence the work completed or was deliberately dodged. **Hard rule.**

- Never delete a Habitica task — score it up.

- Never write a birthday or anniversary into Ship.

- Never write project progress as a child page — it is inline on the parent.

- Never set `This week`; never write `Linked?`.

- Never move rows to `Backlog` before the Habitica clear has run.

- Never escalate an EM- or engineering-owned gate (sign-off, approval, access request, ticket hygiene) to **Needs Richard** — escalate only his unique perspective.

- Never answer a remote's `blocked` prompt on Richard's behalf.

- Never write a Jira-derived row without confirmation.

- Never build an automation unprompted.

- Bulk board changes go through `~/.hermes/scripts/notion_bulk.py`, never a scatter of calls.

## Output

- **Backlog returned** · **Added to the board** · **Meetings this week** · **Deep work:** N slots, X h

- **Mail:** needing a reply · drafts · follow-ups

- **Alerts:** N written (+ birthdays listed, not written) · **Timed:** N dated, each with its reason

- **OpenRouter:** balance · today · 7d · 30d — embed refreshed

- **Remotes:** kicked off · returned · blocked

- **Jira (last week):** per space — headline, N flags, N candidate rows

- **Automations:** N candidates, awaiting accept/decline

- **Needs Richard:** decisions, drafts, flags

## Taste

*Richard-originated, grown by **`$reinforce`**. Signal → preference.*

- Unfinished work returns to `Backlog`; only Richard's say-so completes a row. → Clearing Habitica is housekeeping, not evidence of completion.

- Alerts are tasks, birthdays are not. → Alerts go to `Waiting`; birthdays stay in the report.

- Default Priority is `#5`, not `Everything else`.

- Foreign-language mail (Les Petits) is read in full before classification. → Dutch notices hide real dates and decisions behind innocuous subjects.

- One sharp, measurable milestone beats several vague ones.

- Suspected duplicates are a finding, not a job. → Highlight both rows in the report and let Richard decide; never merge, archive or re-parent a look-alike row on your own (projects, backlog rows or meetings alike).

## Next steps

Invoke on a Monday, or in a catch-up after a missed week.