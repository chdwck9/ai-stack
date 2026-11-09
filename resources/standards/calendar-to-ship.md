# @Calendar-To-Ship — calendar → Ship + CRM standard

**Durable copy.** Skill bodies and `references/` inside a skill directory are pulled
from the AI Hub every night, so anything written there is lost. This file lives in
`@Standards` instead and is the version to edit.

- Canonical skill: `$calendar-meetings-to-ship` (AI Hub, Type=Utilities)
- Mechanical implementation: `~/.hermes/scripts/calendar_apply.py`
  (dagu `monday-mechanical` and `morning-mechanical`, 08:00)
- Related: `monday_time_waiting.py` (never re-dates a row that carries a datetime)

## Source

- **Accounts:** `dykes.digital` Google account via the `gwork` wrapper
  (pins `HERMES_HOME=~/config/google/dykes.digital`); Personal via `gpers`.
  Read three calendars:
  - **Mambu** — `richard.dykes@mambu.com`, shared read-only into the work account.
  - **Dykes Digital** — the account's own `primary`.
  - **Personal** — `chdwck9@gmail.com` (also listed in the work account's list).
- **Window:** default = the current week (Mon 00:00 → Sun 23:59, `Europe/Amsterdam`).
- A **meeting** = ≥1 attendee, excluding daily/standup recurring series and
  0-attendee placeholders (`Focus Block`, `Lunch`, all-day markers like `Home`, `OOO`).
- **Dailies excluded by default** — `DR daily` / `DRDaily`, `Platform eng AWS daily`, …
  Detected by a `daily` token in the summary, or a series landing on ≥4 days in the
  window. An explicit name include-list overrides.

## Routing

1. **Daily / standup** → skip entirely. Never a Ship row.
2. **1:1** — two-person meeting, Richard plus one known **Active** connection
   (`Artūras / Richard`, `1:1 Adrian / Richard`, `Dom / Richard`) → **no Ship task**.
   Set that connection's `Next Connection` (Live → `@Bonds` → CRM) to the meeting
   date. Match fuzzy (`Artūras` = `Arturas`). Person not an Active connection →
   report the miss, create nothing.
3. **Every other meeting** → one Ship `Connect` task.

## Task shape

`Level = To Do` · **`Priority = Connect`** · `Live = <pillar>` ·
`When?` = the event's `start`→`end` as a **datetime pair** (`is_datetime = 1`).

- **Live comes from the event's CALENDAR, never the Google account.** Mambu →
  `@Craft`. `Dykes Digital` + `Personal` → `@Bonds` (family, relationships, social)
  or `@Edge` (health, habits, personal development). The Personal calendar is
  shared into the work account, so an account-based rule files `Clean cat box`
  under `@Craft`. Resolve pillar page ids at runtime.
- **Status:** future → `Waiting`; today → `Do next`; happened → `Shipped`.
- **Names:** short and phone-readable (`DRDaily`, `Platform Weekly`, `EOD Weekly`).

## Pitfalls

- **A CRM `Next Connection` write makes Notion auto-create a date-only Ship row for
  that person** (`is_datetime = 0`, `Live = @Bonds`) a few seconds later. Never
  create your own 1:1 row — wait ~10 s, find it, and set `When?` to the full
  datetime. If the 1:1 already had a `1:1 X / Richard` row, archive it.
- **Never treat an errored/rate-limited query as "no rows".** That is how duplicate
  meeting rows appear: the dedupe read returns nothing, every event looks new.
  Fail loudly and retry.
- A partial `When?` payload can silently default to "now" — verify `start`, `end`
  and `is_datetime` after writing.
- `Lunch` / `Focus Block` sit on the work calendar daily with 0 attendees.
- **An untitled invite is not a Ship row yet** — report it and ask; never invent a
  title from the attendees.
- Re-pointing `HERMES_HOME` by hand mixes the Google accounts. Use `gwork` / `gpers`.

## Verification

- Re-read the window: every created row has `Level`, datetime `When?`, `Live`,
  `Priority = Connect`, `Status`; no (Name, `When?`) pair twice.
- Excluded = 0-attendee placeholders and daily series only.
- Each 1:1 connection shows the meeting date in `Next Connection`, and its
  auto-created Ship row carries the full datetime.

## Taste

- A 1:1 is relationship building → `@Bonds`, managed in the CRM; never `@Craft`
  and never Get Shit Done.
- Work wraps by Thursday; a meeting is not work to re-date — its date is when it
  happens.
