---


name: calendar-meetings-to-ship
uuid: 3fb24dc8-ccd9-8139-8845-c93518322ded
version: 7
description: "Calendar Meetings To Ship"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
resources:

- "@Ship-It-DB"

- "@Resource-Index"


---


# Calendar meetings → Ship

Copy Richard's calendar meetings into Ship — routing 1:1s to the CRM's `Next Connection` instead — so meetings surface on the board, the sprint and the n8n/Habitica syncs. Callable from Clarity, skills/utilities and cron. Idempotent. Full detail, pitfalls and quick reference: `references/pipeline-detail.md`.

## When to Use

- Weekly rhythm: copy the week's meetings into Ship on Monday morning.

- Ad-hoc catch-up after travel / OOO.

- Any skill or cron needing meeting slots as Ship rows.

## Source & routing

- **Account** — Richard's external `dykes.digital` (`richard@dykes.digital`) via the `google-workspace` wrapper `~/config/google/gwork` (pins `HERMES_HOME=~/config/google/dykes.digital`); Personal uses `gpers` (see `~/config/google/README.md`).

- **Three calendars** (external to Mambu): **Mambu** `richard.dykes@mambu.com` (shared read-only); **Dykes Digital** `richard@dykes.digital` `primary`; **Personal** `chdwck9@gmail.com` (via `gpers`). **Window** default = current week (Mon 00:00 → Sun 23:59, `Europe/Amsterdam`); accept caller `start`/`end`.

- **Meeting** = ≥1 attendee, excluding daily/standup recurring series and 0-attendee placeholders (`Focus Block`, `Lunch`, all-day markers like `Home`, `OOO`). Dailies (`DR daily`/`DRDaily`, `Platform eng AWS daily`) excluded by default (a `daily` token, or a series landing ≥4 days in-window); a name include-list overrides.

- **Routing:** dailies → skip. A **1:1** (two-person, one connection) → set that **Active** connection's `Next Connection` (Live → `@Bonds` → CRM) to the meeting date; no Ship task. Else → a Ship `Connect` task: `Level = To Do` · `Priority = Connect` · `Live = <pillar>` · `When?` = `start`→`end` datetime (`is_datetime = 1`) · `Status`. **Live**: Mambu → `@Craft`; Dykes Digital + Personal → `@Bonds`/`@Edge` (resolve pillar ids at runtime). **Status**: future → `Waiting`; today → `Do next`; happened → `Shipped`. Names short/phone-readable.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Resolve inputs** — window (default current week) and wrappers; accept a caller override.

1. **Fetch events** for the window from all three calendars; keep `id`, `summary`, `start`, `end`, `attendees`.

1. **Filter to meetings** — ≥1 attendee, not a daily series; drop placeholders; honor an explicit name include-list.

1. **Split 1:1s** → CRM (step 5); else → Ship (step 6).

1. **1:1s → CRM, then enrich.** Match the person among **Active** connections (Live → `@Bonds` → CRM), fuzzy (`Artūras` vs `Arturas`); set `Next Connection` to the meeting date. Never create a 1:1 Ship task; if not active, report the miss. The write auto-creates a date-only row (`Live = @Bonds`, `is_datetime = 0`): wait ~10s, find it (Name = person, `When?` = date, `is_datetime = 0`) and set `When?` to the full `start`→`end` datetime.

1. **Other meetings → Ship.** Dedupe: read existing `To Do` rows in the window from `@Ship-It-DB` (SQL on `date:When?:start`), skip any (Name, `When?` start) present; write one page per meeting.

1. **Verify** by re-fetching the window and touched CRM rows; confirm `start`/`end`/`is_datetime`/`Live`/`Status` and new `Next Connection`. Never write `Linked?` (automation-owned).

1. **Report** the delta: rows created/skipped; CRM `Next Connection` set (time enriched); events excluded.

## Boundaries

Dedupe before creating; never set `This week`, `Linked?`, `Checked`, `Print`, `Phase`. Copy only — never accept/decline invites, message attendees, or move events. Default-exclude dailies. 1:1s go to the CRM, never your own Ship row. Never create a CRM connection that doesn't exist — report the miss. Current week only unless asked. `Live` is required and pillar-only.

## Verification

- In `@Ship-It-DB`: every created row has `Level`, `When?` datetime, `Live`, `Priority`, `Status`; no duplicate (Name, `When?` start).

- Excluded = only 0-attendee placeholders and daily series.

- CRM: each 1:1 connection shows its date in `Next Connection`; its auto Ship row carries the full datetime.

## Pitfalls

Read all three calendars — `primary` alone misses every Mambu meeting. Store UTC ISO with `is_datetime = 1` (a partial `When?` can default to "now"). Never copy `Lunch`/`Focus Block`. An untitled invite (`summary = null`) is not a row yet — report the miss, then write a full-day task for its window; never invent a title. Use `gwork`/`gpers`, never re-point `HERMES_HOME` by hand. Full pitfalls: `references/pipeline-detail.md`.

## Output

Compact delta: rows created (Name · day · time · Status), skipped, CRM `Next Connection` set + time enriched, events excluded; cron/headless silent when nothing changes.

## Next steps

Invoke with a window, e.g. `calendar-meetings-to-ship 2026-10-19..2026-10-23`.