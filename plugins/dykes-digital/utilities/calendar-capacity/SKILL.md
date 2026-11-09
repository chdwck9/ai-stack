---


uuid: 40524dc8-ccd9-81be-8a1f-c69448430db1
name: calendar-capacity
description: "Use when sizing calendar capacity or finding free time."
version: 1
last-used: "2026-10-19"
scope: local
author: Hermes Agent
license: MIT
platforms: [macos, linux]
thinking: "Low"
temperature: 0.2
resources:

- "@Resource-Index"
metadata:
hermes:
tags: [calendar, capacity, deep-work, planning, google]
related_skills: [calendar-meetings-to-ship, monday, travel-planning]


---


# Calendar capacity

Answer "how much time do I actually have?" from Richard's real calendars — free gaps, deep-work slots, conflicts — instead of guessing from the Ship board. Called by the Monday reset for its deep-work line, and by any capacity or planning question.

## When to Use

- "How many deep-work slots do I have this week?" / "what does my week look like?".

- The Monday reset's **Deep work** report line.

- Checking whether something can actually fit before committing to a date.

- Finding where a meeting can move to, or spotting double-bookings.

## Sources — three calendars, never just the primary

- **Mambu (work)** — `richard.dykes@mambu.com`, a *shared read-only feed* into the `dykes.digital` account. It is **not** the primary calendar: a `calendar list` against the primary returns nothing from it.

- **Dykes Digital** — `richard@dykes.digital`, the account's own `primary`.

- **Personal** — `chdwck9@gmail.com`, via the `gpers` wrapper.

Reach them with the `gwork` / `gpers` wrappers (`~/config/google/`), which pin `HERMES_HOME` per account. Enumerate calendars, then query each target `calendarId` directly — reading only `primary` misses every Mambu meeting.

## Procedure

1. **Fix the window explicitly** as ISO 8601 **with a UTC offset**. The wrapper's `calendar list` defaults to the next 7 days only, so an unwindowed call silently answers the wrong question. Convert local (Europe/Amsterdam) bounds to UTC when the numbers matter.

1. **Pull events from all three calendars** for the window. Keep `id`, `summary`, `start`, `end`, `attendees`.

1. **Classify each event** before doing any arithmetic:

  - **All-day markers** (`Home`, travel spans, birthday entries) carry a `date`, not a `dateTime` — no clock time, so they consume no capacity.

  - **Placeholders** — `Focus Block`, `Lunch` — carry 0 attendees. Treat them as capacity *available*, never as busy.

  - **Real commitments** — events with attendees, plus the standups/dailies Richard attends.

1. **Compute** what was asked:

  - *Free gaps:* merge overlapping busy intervals, then take the gaps between them inside the working window; collapse gaps below whatever minimum was asked for.

  - *Conflicts:* two busy intervals overlapping on the same day.

  - *Deep-work slots:* see below.

## Deep-work slots

The Monday report's **Deep work** line = straight blocks long enough for focused work.

- **Window:** Mon–Fri, **09:00–18:00 Europe/Amsterdam**. Weekends and evenings are not counted.

- **Busy** = real commitments (meetings with attendees, the dailies). **`Focus Block`**** and ****`Lunch`**** are excluded from busy** — `Focus Block` *is* the deep-work slot, so counting it busy guarantees a meaningless zero.

- Take gaps **≥ 90 minutes** between merged busy intervals inside each weekday window.

- **Report the count, the total hours, and the best few** (day · start–end · length).

- Note the window and the exclusions when you first report it, so the number is auditable.

## Pitfalls

- **Only the primary calendar is queried by the wrapper's default list.** A shared feed (the Mambu one) is invisible that way — enumerate calendars first, then query the target `calendarId`.

- **The ****`Focus Block`**** trap.** Counting the work calendar's own focus placeholders as busy returns zero deep slots on a week that is actually open — the placeholder is the answer, not the obstacle.

- **All-day events are not capacity.** They have no start/end clock time; including them blanks whole days.

- **Timezone/offset.** `Europe/Amsterdam` is UTC+2 in summer and UTC+1 in winter, flipping on the last Sunday of October — take the offset from the date, not from habit. A partial date payload can also silently default to "now".

- **A meeting-heavy week can genuinely have no deep slots.** Say zero rather than padding the number with sub-90-minute crumbs.

- **Do not add recurring standups to Ship to model this** — read them from the calendar and leave the board alone. Which meetings belong on the board is `calendar-meetings-to-ship`'s call.

## Output

A short block, not an itinerary: the window used, the deep-work count and hours, the named slots, any conflicts, and the assumptions (window + placeholder exclusions). Flag anything you could not read rather than silently filling the gap.