# Ship — Notion triggers: webhooks vs in-app automations (rebuilt standard)

**Rebuilt** 2026-11-09 after the original `references/notion-triggers.md` was lost to the nightly
Hub→local skill sync. Grounded in `notion_task_intake.py`, `notion_comment_event.py`,
`notion_comment_intake.py` and observed automation behaviour.

## Two kinds, and they fail differently

1. **In-app Notion automations** — buttons (`Done`, `Add to Sprint`, `Add to Library`, `Clear it`),
   `Defer` → `Waiting`, `Linked?` population, and the CRM `Next Connection` → auto-created Ship row.
   These are **not writable or inspectable via the API**. Treat their outputs as facts and never try
   to reproduce them by hand.
2. **Webhooks out of Notion into Hermes routes** — `notion-ship` (task intake) and `clarity-comment`.
   Route scripts normalise the payload and gate what the agent sees.

## Route-script contract (Hermes webhook routes)

- Payload arrives as **JSON on stdin**.
- A **JSON object on stdout REPLACES the payload** before `{dot.notation}` prompt templating.
- **Empty stdout / `[SILENCE]` / non-zero exit ignores the webhook.**
- Notion sends **properties only, never the page body** — fetch the page if the body is needed.
- Every raw payload is logged (`~/.hermes/logs/notion_task_intake.jsonl`,
  `notion_comment_event.jsonl`) because the real shape is only knowable from a live trigger. Read the
  log before changing a parser.

## `notion-ship` — task intake

`notion_task_intake.py` normalises any payload into `{page_id, url, title, found, authorised,
creator_id}`; `found=false` means no page reference could be recovered and the agent must ask.
Authorised payloads are also appended to `~/.hermes/logs/kanban_pending_tasks.log` so a run can scan
them on start.

## `clarity-comment` — delegation by comment

`notion_comment_event.py`. **Gate = the @-mention of `CLARITY_USER_ID`.** A page-creator check is not
possible on this surface (notion-fetch returns body markdown with no `created_by`), and authorship is
not separable because Clarity posts as Richard's own Notion account. So the automation filters to the
Ship DB and the mention filters to the event.

## Monitor gate

`notion_intake_monitor.sh` runs `notion_comment_intake.py --monitor` and prints a deterministic
digest; the cron engine skips the agent run while that output is unchanged. Cheap, no LLM. If the job
"isn't firing", check the digest changed — not the schedule.

## Dedupe guards

- **Idempotent by (Name, When? start)** — read the window before writing, and never trust an empty
  result from an errored query (see `notion-bulk-and-query.md`).
- **Automations create rows too.** The CRM `Next Connection` write makes Notion create a date-only
  Ship row for the person a few seconds later — wait, find it, enrich it. Never create your own.
- Buttons and webhooks can both fire on one action; the route's gate (mention / property filter) is
  what keeps it to one event.

## Habitica sync (Richard, 2026-11-09)

A **status change scores the task in Habitica**. Shipping and archiving therefore leave **orphans**
in Habitica — that is expected, and it is exactly what the Monday clean-up (clearing Habitica) is
for. Never "fix" an orphan by hand mid-week.

The n8n workflow names/ids behind the sync (tasks→tasks, milestones→habits, rituals→dailies) are
**not needed for normal work** — only for remediation, or as an FYI. Don't carry them around; look
them up in `n8n-prod` if a sync actually breaks.
