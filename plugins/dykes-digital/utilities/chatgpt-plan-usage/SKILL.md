---


name: chatgpt-plan-usage
uuid: 41424dc8-ccd9-81f0-89d9-ef7f06617ed9
version: 1
description: "Use when checking ChatGPT/Codex quota or reset date."
last-used: "2026-11-06"
scope: local
thinking: "Low"
temperature: 0.1
author: clarity
license: proprietary
metadata:
hermes:
tags: [usage, quota, chatgpt, codex, subscription, billing]
related_skills: [openrouter-usage, token-costing, local-model-backend]


---


# ChatGPT / Codex plan usage

Report what a ChatGPT subscription (Plus / Pro / Go) actually has left on the Codex backend, without touching the API-key bill.

## When to Use

- "How much ChatGPT/Codex quota do I have left?" / "when does it reset?"

- Deciding whether the `openai-codex` provider can carry a workload.

- After a 429 on the Codex route.

## "How many tokens?" — the backend does not say

There is **no token budget** in the response. `rate_limit.primary_window` carries only `used_percent`, `limit_window_seconds` and `reset_at`. Never invent a token cap or a "messages left" figure; quote the percentage and the window.

## Run it

```bash
python3 ~/.hermes/scripts/codex_plan_usage.py
```

Reads `~/.codex/auth.json` (`tokens.access_token` + `tokens.account_id`) and calls, with headers `Authorization: Bearer <token>` and `chatgpt-account-id: <account_id>`:

- `GET https://chatgpt.com/backend-api/wham/usage` → plan + rate limit (the one that works)

- `GET https://chatgpt.com/backend-api/codex/usage` → same shape

- `GET https://chatgpt.com/backend-api/models` → model slugs the account is offered

`/backend-api/codex/models` returns **400** — use `/backend-api/models`.

## Reading the payload

- `plan_type`: `go` / `plus` / `pro`. The window differs per plan; never assume.

- `rate_limit.primary_window.limit_window_seconds`: the real reset period. **Go = 2,592,000 = 30 days**, not the 2 months people assume. `secondary_window` is `null` on Go (no weekly window).

- `reset_at` is a unix timestamp — convert to local time before quoting.

- `rate_limit.allowed` / `limit_reached`: whether a request would pass right now.

- `rate_limit_reset_credits.available_count`: manual "reset the window" credits, if the plan has them.

- `credits.unlimited` / `has_credits`: overage is absent on consumer plans — at 100% the route just refuses.

## Measured calibration (ChatGPT Go, gpt-5.6-terra, 2026-11-10)

Only some slugs are accepted on a ChatGPT account. On Go: **`gpt-5.6-terra`** (balanced), `gpt-5.6-luna`, `gpt-6-luna`. Rejected with *"not supported when using Codex with a ChatGPT account"*: `gpt-6`, `gpt-6-sol`, `gpt-6-mini`, `gpt-6-t-mini`, `gpt-5-6*`, `gpt-5.6`, `gpt-5.6-sol`, `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.3-codex-spark`, `research`. Find the allowed set with `scripts/../codex_model_probe.py`, never from the model list.

Percent is weighted, not raw tokens — output costs ~4.4x input per token. Fitted from two shaped probes (`codex_plan_calibrate.py`):

- **1% ≈ 8,100 uncached input tokens**

- **1% ≈ 1,843 output tokens**

- A typical 16k-context turn (6.4k uncached + 1.2k out) ≈ **1.44% → ~69 turns per 30-day window** (≈530k gross tokens)

- One 130k-context agent pass ≈ **the entire month**

Fit check: predicted 6.05% vs observed 6% for a 3-run 51k-token batch. Cached input is heavily discounted, so context reuse matters as much as volume.

## Economics

A subscription route converts $/token into plan quota; it never adds unmetered inference. Compare against real API burn (`openrouter-usage`) before recommending a switch. Best use: interactive bursts and **fallback**; worst use: cron/agent loops, which exhaust a window at machine speed and lock the user out of their own chat/IDE.

## Pitfalls

- Never print the access token, id token or refresh token. Mask them; print only plan, percentages and dates.

- Hermes' curated `openai-codex` names (`gpt-6-sol`, `gpt-5.6-terra`, …) are not the slugs `/backend-api/models` returns (`gpt-6`, `gpt-5-6`, `gpt-5-6-mini`, …). The alias mapping is not public — confirm in `hermes model` and expect some advertised slugs to 400 with "not supported when using Codex with a ChatGPT account".

- `used_percent: 0` with a 30-day window means untouched since the last reset, not a broken read.

- The plan is checked per request; re-run rather than quoting a stale figure on an active account.