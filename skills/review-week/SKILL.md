---


name: review-week
uuid: TBD
version: 1
description: "Review Week"
return: "Milestone marks proposed · project blocks appended · Backlog return verified"
last-used: 2026-10-27T12:00:00+01:00
thinking: Medium
temperature: 0.3
resources:

- "@Ship-DB-Reference"
author: Richard Dykes, Hermes Agent
license: MIT
metadata:
hermes:
tags: [monday, weekly, review, projects, ship, clarity]
related_skills: [monday, track-project, ship-db]


---


# Review Week

Close the week just gone: milestone marks, project progress blocks, and a check that the mechanical `Backlog` return did what it claimed.

## Inputs

The closed Mon–Sun window and the mechanical summary from `monday-mechanical`.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Milestone marks.** Count the week's marks per habit and cross-check Ship's `Shipped` state. Propose a raise to 8 or 10 only where warranted — never invent a mark.

1. **Project progress.** For each active project with evidence in the window, append a dated block (Plan · Achieved · Missed · Why/Risks · Next · Evidence) **inline** to the project page via `$track-project`. A project with no window evidence is named as silent — never stamp a hollow block.

1. **Verify the ****`Backlog`**** return.** Confirm the mechanical step moved every unfinished in-window row. Anything it missed, move now, and say which.

1. **Report the counts.**

## Examples

- **Three projects had evidence** → three blocks appended; a fourth had none → named as silent, not stamped.

- **A row was left in ****`Waiting`** with a closed-week date → moved to `Backlog` and reported as a mechanical miss.

## Boundaries

- Never set `Shipped`/`LEAD`/`Abandoned` without explicit evidence the work completed or was deliberately dodged.

- Never write project progress as a child page — it is inline on the parent.

- Never invent a milestone mark. Clearing Habitica is housekeeping, not evidence of completion.

- Never move a row to `Backlog` before the Habitica clear has run.

## Output

Milestone marks proposed · Project blocks appended (names) · `Backlog` return verified (N moved, N missed by the mechanical step).

## Next steps

Feeds `$open-week`, which proposes the week ahead.