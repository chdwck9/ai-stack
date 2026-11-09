---


name: open-week
uuid: TBD
version: 1
description: "Open Week"
return: "Milestones proposed · alerts written · Waiting dated · MCD flags · automation candidates"
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
tags: [monday, weekly, planning, milestones, alerts, clarity]
related_skills: [monday, review-week, sweep-meetings, calendar-capacity, ship-db]


---


# Open Week

Open the week ahead: propose its milestones, write the alerts, time the `Waiting` queue, and flag what should stop being manual.

## Inputs

The current week's calendar (from the mechanical step), the closed week's outcome, and whatever the mail and meeting steps surfaced.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Propose the new week's milestones** — one sharp, measurable outcome per active line of effort, plus the tasks that follow from the closed week (committed dates, carry-overs, anything surfaced in mail or meetings). **Propose only**; never write without confirmation.

1. **Alerts → ****`Waiting`****.** Anything that needs Richard — a critical task, a committed deadline, a follow-up owed — becomes a `Waiting`, `To Do`, `#3` row dated this Monday, pillar per source, evidence in the body. **Birthdays and anniversaries are listed in the report only, never written to Ship.**

1. **Time the ****`Waiting`**** queue.** A related 1:1 gives the deadline — date the task to land **before** it. Otherwise `@Craft` → Thursday, `@Edge` → Friday, `@Bonds` left alone. Check the target day has a workable slot via `$calendar-capacity`. Report every date set and its reason.

1. **MCD flags.** Where the week produced a needle-mover — a decision, a scope change, a new risk, a corrected assumption — raise `Update MCD: <project> — <what changed>` with the evidence. Routine drift is another cron's problem.

1. **Automation candidates.** Read the week's tasks, sessions and meetings; propose what **repeats**, with the evidence and the right stack — **n8n** for event/webhook glue, **dagu** for scheduled shell/DAG work, **Hermes** for anything needing judgement. Routine-mechanical first. **Propose only; build nothing unprompted.**

## Examples

- **Timing by meeting** — a Wednesday 1:1 on the Wally launch → its `@Craft` row dated Tuesday, reason given.

- **An automation candidate** — four private channels provisioned by hand in two weeks → one candidate: a provision-a-channel utility, Hermes, routine.

- **A birthday on the calendar** → listed in the report, never a Ship row.

## Boundaries

- Never write a milestone or a task without confirmation.

- Never write a birthday or anniversary into Ship.

- Never re-date a `@Bonds` row — social is not scheduled work.

- Never date a `Waiting` row without a reason: a related meeting, or the pillar rule.

- Never build an automation unprompted, or propose one for work that is not actually repeating.

## Output

Milestones proposed · alerts written · `Waiting` rows dated (each with its reason) · MCD flags · automation candidates (what repeats · stack · priority).

## Next steps

Richard accepts, edits or discards. Accepted milestones are written after the reset.