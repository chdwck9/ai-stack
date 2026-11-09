---


uuid: 3f524dc8-ccd9-8127-ae7d-c6f720c570f3
name: operational-alert-monitoring
description: "Operational Alert Monitoring"
version: 1.1.0
author: Hermes Agent
license: MIT
created_by: agent
last-used: "2026-10-28"
metadata:
hermes:
tags: [monitoring, alerts, flights, cron, operations]


---


# Operational Alert Monitoring

Silently watch a concrete upcoming operation and alert only if a material threat appears.

## When to Use

- Richard asks to monitor a concrete upcoming operation — a flight, service, or appointment — and alert only if a material threat appears.

- Not price tracking; use a price-watch skill for fare/listing thresholds.

- Rail watches (NS / Eurostar): start from `references/dutch-rail-watch.md`.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Extract the monitoring contract.** Capture target identifier, date, route/location, time window, normal-state assumptions, alert destination. Flights: flight number, operating carrier if known, route, airport ICAOs, scheduled departure/boarding/arrival window, last-known terminal/gate. Never store or repeat passenger names, QR/barcodes, seat numbers, or booking references unless explicitly required.

1. **Define the threat threshold before scheduling.** Flights: cancellation, a published delay of 20+ minutes, an airport/airline operational disruption likely to affect the flight, or credible aviation-weather risk at departure/arrival. Never alert for routine rain/showers, normal breezy conditions, generic weather notes, ordinary congestion, or routine gate/terminal changes.

1. **Establish a foreground baseline.** Check at least one authoritative operational source before scheduling — official airline/airport status plus METAR/TAF for departure and arrival airports. If an official source is inaccessible, state the limitation and proceed with clearly labelled secondary sources.

1. **Create a silent scheduled monitor.** Use `cronjob_manage` with a self-contained prompt, `continuity=true`, and a bounded `repeat` count so the watch expires after the window. The prompt must send no output when there is no threat (reply exactly `[SILENT]`). To start later: create the recurring job paused, then a one-shot activation job that resumes it.

1. **Alert only on new or materially worsening threats.** Compare against the previous run via continuity. Compact: severity, what changed, expected impact, source/check time, immediate recommended action. No routine all-clear updates unless requested.

1. **Keep authority boundaries.** Monitoring may read and alert. Never rebook, cancel, check in, contact a provider, spend money, or change a reservation without explicit action-specific approval.

1. **Re-check the system date (****`date`****)** before any "today/tomorrow/yesterday" wording — a session or monitor can span midnight. Anchor every relative date to a fresh `date` at answer time.

## Pitfalls

- Baseline before scheduling, or the watch alerts on an unverified target / the wrong window.

- Put the no-output rule in the prompt: reply exactly `[SILENT]` (the engine's canonical suppression token) — "output nothing" works only by luck.

- For one-shot cron schedules pass a **bare ISO timestamp** — a `once at <ts>` prefix is rejected and the job silently never gets created.

- Bound `repeat` to the operational window or a temporary watch becomes a standing monitor; clean it up once an alert no longer helps (flight departed, delay window closed).

- Use METAR/TAF as risk evidence, not user-facing jargon; translate to practical impact and alert only when material.

- A flight number no authoritative source can locate is a real finding — report it once; never fabricate an all-clear or invent the "correct" number.

- Fixed-timing pickups: split into Phase 1 (flight status until expected arrival) and Phase 2 (post-arrival traffic/airport conditions) as two cron jobs.

- "Same alert several times": separate the bounded JOB retry (3 attempts, then one failure) from a level-triggered ALERT repeat; the `os-health-watch` Dagu DAG re-alerts the whole `(job, kind)` set, braked only by `RE_ALERT_HOURS`.

- **Stale failure alerts (the weekly-job trap).** A failing job keeps `last_status=error` until its NEXT successful run — so a weekly job (e.g. `Monday Reset`, `0 9 * * 1`) looks "failing" for up to 7 days and a naive `last_status` check re-alerts it daily, delivering the same stale error on Wed/Thu/Fri. Richard's rule (2026-10-28): *"I just need to know by midday if my morning runs didn't complete. Not every day after that."* So `health_watch.py` pages about exactly ONE thing, ONCE a day: after `MIDDAY_HOUR` (12:00) it checks whether TODAY's expected morning runs (the DAG *and* the agentic cron for today's weekday) completed, and alerts once per calendar day (`last_alert_day`), silent otherwise. General cron-errors / dagu failures / overdue jobs are still written to the `problems` list of `os-health.json` for the dashboard and n8n relay, but they do NOT page — `ok` reflects only the midday morning verdict, so a stale persisted error never re-trips the relay. Scope it to TODAY: never re-report yesterday's gap. A run still in flight is NOT a failure until `RUNNING_FAIL_HOURS` (3) hours after its start — past that it alerts as `still running Xh` (a hung run must not look like progress; Richard, 2026-10-28: "if it's still running 3 hours after it was started then it's a failure").

- **Catch-up must not make a dated job stale.** With `cron.catch_up_missed: true` (or a Dagu DAG missing `catchup_window: ""`), a missed weekly slot can fire days late and emit a report that assumes the original day ("Today is Monday"). Add a day guard to the prompt (no-op unless the real weekday matches) and set `catchup_window: ""` on scheduled Dagu DAGs so a late reset never runs at all.

- A failing job's error names the PROVIDER that actually ran — read the log's `provider=` / `base_url=` / `model=` before blaming the pinned model.

- For "is there a strike / disruption today", verify against current news, not recall — scope the claim to the right carrier/CAO.

`references/flight-watch.md` → flight sources, the reusable `flight_watch.py` engine and its cron stub. `references/monitoring-ops.md` → cron/dedupe/strike/provider/dagu detail.

## Verification

- An authoritative baseline was captured before scheduling.

- The cron prompt suppresses non-threats with `[SILENT]`; `repeat` bounds the window.

- Any alert names severity, change, impact, source/check time, and recommended action.

- No reservation, purchase, or provider contact happened without explicit action-specific approval.

- Relative dates were re-anchored to a fresh `date`.