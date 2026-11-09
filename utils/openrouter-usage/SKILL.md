---


name: openrouter-usage
uuid: 3ff24dc8-ccd9-818c-b248-f5048abdbc76
version: 1
description: "Report OpenRouter balance, usage and per-app spend."
last-used: "2026-10-20"
scope: local
thinking: "Low"
temperature: 0.2
author: clarity
license: proprietary
metadata:
hermes:
tags: [openrouter, cost, usage, balance, reporting, credits]
related_skills: [token-costing, clarity-capabilities]


---


# OpenRouter usage utility

Pull OpenRouter spend and balance for the account behind `OPENROUTER_API_KEY`, and present usage by period. Two sources — know which you are quoting.

## When to Use

- "How much have I spent on OpenRouter?" / "what's my balance?"

- A weekly or monthly spend report, or a low-balance warning.

- Any cost review of the inference key.

## Dashboard Generation (Visual Charts)

To produce a demo-ready **HTML dashboard** with stacked bar charts showing `Actual Cloud Spend` vs `Potential Local Savings`:

1. **Generate the dashboard:** Run `python3 ~/.hermes/scripts/openrouter_usage.py --hermes --html /path/to/dashboard.html`.

  - The script natively renders inline SVG stacked bar charts inside the dark-themed page.

  - **Legend breakdown:**

    - 🟦 Blue: Actual OpenRouter Spend

    - 🟩 Green: Potential Local Savings (tokens processed locally valued at default cloud rates like `qwen3.6/3.7-flash`)

    - 🟨 Yellow/Text: Local Real Spend ($0 infrastructure cost)

1. **Serve or embed:** Save to `~/.hermes/output/inference_dashboard.html`. If hosted locally behind the Cloudflare tunnel or served via HTTP, Richard can review it in his browser. For static hand-offs, open the file and screenshot the `Weekly Breakdown` and `Daily Breakdown` sections.

1. **Sync to AI Hub.** Push the updated skill unconditionally.


---


## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Check the key type first.** `GET /api/v1/key` returns `is_management_key` / `is_provisioning_key`. A normal inference key can read its own usage but **cannot** read `/api/v1/activity` (per-day account history) — that endpoint returns `403 Only management keys can fetch activity for an account`.
1b. **Authoritative daily series (needs a management key).** Richard creates a Management API key at `https://openrouter.ai/settings/management-keys` (name it, set an expiry) and stores it as **`OPENROUTER_MGMT_KEY`** in `~/.hermes/.env` — never in chat, never printed. Then:

  - `GET /api/v1/activity` → daily spend/usage grouped by model endpoint, last 30 **completed** UTC days, whole account (`--activity`).

  - `POST /api/v1/analytics/query` (Explore equivalent) + `GET /api/v1/analytics/meta` → split spend by dimension. This is how you prove a per-app attribution (e.g. Hermes vs Honcho) instead of inferring it. Body shape: `{metrics:[total_usage,request_count], dimensions:[app], granularity:day, limit:1000, time_range:{start,end}}` (ISO-8601 Z times); reply rows carry `date__day`, the dimension value, and the metric. Useful dimensions: `app`, `api_key_id`, `model`, `provider`, `workspace`, `external_user`.

  - Verified 2026-11-03: over 30 days **Hermes Agent = 97.4% ($45.7)**, Honcho = 2.5% ($1.19) — so a shared key is *not* the explanation for a low Hermes figure.

  - A management key can also create/delete keys, so treat it as a secret and set an expiry.

1. **Pull the authoritative numbers** (account-level, all apps using this key):

  - `GET /api/v1/credits` → `total_credits`, `total_usage` → **remaining = total_credits − total_usage**.

  - `GET /api/v1/key` → `usage` (all-time), `usage_daily`, `usage_weekly`, `usage_monthly` (rolling windows), `limit`, `limit_remaining`, `is_free_tier`.

1. **Run the report:** `python3 ~/.hermes/scripts/openrouter_usage.py [--hermes] [--json] [--html PATH]`. With `--hermes` the HTML carries a **Daily — last 7 days** table (bar + cost + sessions + in/out tokens, zero-filled, plus a 7-day total) above the weekly/monthly tables.

1. **For a calendar week/month breakdown of Hermes-driven spend**, add `--hermes` — it aggregates `~/.hermes/state.db` (`session_model_usage`, every task incl. `background_review`) bucketed by `COALESCE(last_activity_at, started_at)` into ISO week/month/day. This is Hermes' **estimate** and covers **only Hermes calls**. Reconcile it against `--activity` (management key) whenever both are available.

1. **State the source.** API figures are authoritative for the key/account; the `--hermes` breakdown is estimated and is a subset. The gap between them is spend from other apps on the same key. `--activity` prints the authoritative by-app split *and* the reconcile line (state.db estimate as a % of actual) — quote that %, and never let the estimate stand in for the account figure.
5b. **Daily figures: the provider series is the only truthful one.** `/activity` (grouped by model endpoint) and the analytics query both bucket by the *date the spend occurred*, which a state.db estimate cannot reproduce. `--html` now leads with **Spend by app (AUTHORITATIVE)** and a 14-day daily split; the state.db tables follow, relabelled as estimates.

1. **Never accept the API key as a chat message.** If Richard pastes a key, retype it straight into `~/.hermes/.env` (chmod 600), never echo it, never reprint it in a tool result — print only a masked confirmation. A management key can also mint/delete keys, so it is the more sensitive credential.

1. **Report OUR spend, not just OpenRouter's.** The report leads with *Our inference spend* (day / last 7d / last 30d) = OpenRouter **actual** + **local equivalent**, where local = tokens run on our own hardware (Studio `rapid-mlx`/LM Studio, loopback base URL) valued at the **online price of their hosted sibling** — `qwen/qwen3.6-35b-a3b` (in $0.10/M, out $0.90/M). Local runs bill $0, so that column is *avoided spend*. Rate constants: `LOCAL_RATE_MODEL` / `LOCAL_IN_RATE` / `LOCAL_OUT_RATE` in the script.

## Quick Reference

```javascript
GET /api/v1/credits   -> balance (authoritative)
GET /api/v1/key       -> usage daily/weekly/monthly + limits
GET /api/v1/activity  -> 403 unless management/provisioning key
~/.hermes/scripts/openrouter_usage.py [--hermes] [--json]
```

## Boundaries

- **Never print or transmit the API key.** Read it from `~/.hermes/.env` inside the script; the API returns only a masked label.

- The script is read-only — it never spends, tops up or changes settings.

- Do not present the `--hermes` estimate as the account total; the API total is authoritative and larger.

## Verification

- `remaining == total_credits − total_usage` to the cent.

- `usage_monthly ≥ usage_weekly ≥ usage_daily` unless the account is idle.

- If `/api/v1/activity` is attempted it must be reported as `403`, not silently skipped.

## Pitfalls

- **`/api/v1/activity`**** needs a management key.** With a plain inference key it is `403` (re-confirmed 2026-11-03: `is_management_key=false`). Richard creates one at `https://openrouter.ai/settings/management-keys`; store as `OPENROUTER_MGMT_KEY`. Until then the only daily series available is Hermes' own (`--hermes`), which excludes other apps on the key — never present it as the account's daily spend.

- **The Hermes estimate reads ****`session_model_usage`****, not ****`sessions`****, and buckets by ****`last_activity_at`****.** Reading only `sessions` misses auxiliary tasks — `background_review` alone was ~15% of 30-day spend ($4.91 of $33.42) — and bucketing by `started_at` dumps a long or cross-midnight session's whole cost on its start day, which made single-day figures read **2×–7× off** vs the provider's own daily number (the "estimate is half of OpenRouter" symptom). Both are fixed in the utility; keep them fixed.

- `usage_daily/weekly/monthly` are **rolling** windows (last 1/7/30 days), not calendar buckets. For calendar weeks/months use the `--hermes` breakdown, or snapshot the rolling values on a schedule.

- The key can be shared: OpenRouter spend may exceed what Hermes records (the Honcho deriver and other agents can bill the same key). Always show both figures.

- **The estimate still runs ~28% light even after the fixes.** Measured 2026-11-03: state.db `session_model_usage` 30d $32.73 vs OpenRouter 'Hermes Agent' $45.69 = **72% of actual**. Cause is the Hermes-side rate card / cache accounting, not attribution. Never quote the state.db figure as the bill; quote `--activity` and show the % gap.

- **Local rows must have a loopback base URL to count.** A `custom` provider pointed at a remote host is not our hardware; `local_breakdown()` requires `127.0.0.1`/`localhost` in `billing_base_url`. Local usage is also only as complete as `state.db` logs it — say so rather than implying the saving is exhaustive.

- **SQLite pitfall that silently zeroed the local query:** `COALESCE(s.last_activity_at,s.started_at) > strftime('%s','now','-30 days')` is always false — comparing a non-column REAL expression to a TEXT literal applies no affinity, and REAL sorts before TEXT. Compare a **column** directly (`m.started_at > ...`) or pass a numeric bound from Python (`since.timestamp()`).

- **Probe/test calls must use the configured default model** (`model.default` in `~/.hermes/config.yaml` — currently `deepseek/deepseek-v4.1-flash`), not a model picked from habit. A probe on an off-config model emits an event that does not represent real traffic, so it cannot validate a usage/cost pipeline. Read the config before choosing the probe model; a raw `curl` probe bypasses Hermes routing entirely, so it only tests the provider side.