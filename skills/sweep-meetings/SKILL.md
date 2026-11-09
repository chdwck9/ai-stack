---


name: sweep-meetings
uuid: TBD
version: 1
description: "Sweep Meetings"
return: "Meetings read · board rows added from meeting commitments · blank captures named"
last-used: 2026-10-27T12:00:00+01:00
thinking: Medium
temperature: 0.3
resources:

- "@Ship-DB-Reference"

- "@Resource-Index"
author: Richard Dykes, Hermes Agent
license: MIT
metadata:
hermes:
tags: [monday, weekly, granola, meetings, ship, clarity]
related_skills: [monday, open-week, ship-db]


---


# Sweep Meetings

Turn the closed week's meetings into board rows: the commitments agreed in a call that never reached Ship.

## Inputs

The closed Mon–Sun window, passed **explicitly** as `custom_start`/`custom_end`. Never `last_week` — it resolves Sun→Sat and clips the Sunday.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **List the window's meetings** (`list_meetings`), then read each one's **AI summary** via `get_meetings`. The summary is the source of record: `get_meeting_transcript` is paywalled on this plan, so never rely on verbatim transcripts.

1. **Extract** anything that reads like a task or a commitment.

1. **Cross-check each against the board** — it may already sit under any pillar, level or status.

1. **Add the gap yourself: no clarifying question, no notification.** Short, phone-readable name; `Level = To Do`, `Status = Waiting`, `Priority = #5`, `When?` = Monday of the current week, `Live` = the meeting's pillar (work → `@Craft`; personal → `@Bonds` or `@Edge`), and the **Granola note URL in the page body**.

1. **Handle a blank capture honestly.** A blank summary on a meeting that clearly happened is a capture artefact — note it; never infer content or skip the meeting silently.

## Examples

- **A client call agreed a revised scope** → one `Waiting` row with the Granola link in the body.

- **A meeting with a blank capture** → named under **Needs Richard**; nothing invented.

## Boundaries

- Never invent a task from a summary that could not be read.

- Never raise a Granola task without its note URL in the body.

- Never use `last_week` shorthand.

- Never rely on `get_meeting_transcript`.

- This gap-fill is one of the two places rows are added unprompted — add them and stay silent.

## Output

Meetings read · rows added (names) · blank captures named.

## Next steps

Feeds `$open-week`, which proposes the week's milestones from what surfaced here.