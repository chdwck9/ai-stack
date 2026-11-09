---


name: token-costing

uuid: TBD

version: 1

description: "Cost a run, session, day or model from real token counts."

last-used: "2026-10-20"

scope: local

thinking: "Low"

temperature: 0.2

author: clarity

license: proprietary

metadata:

  hermes:

    tags: [tokens, cost, usage, accounting]

    related_skills: [clarity-capabilities]


---


# Token costing utility

Measure what Hermes actually spent on tokens — from real sources, never an invented rate card. Two inputs: the session store (`~/.hermes/state.db`) and the per-run `--usage-file` JSON report. Use it to attach a true cost line to any utility or cron test.

## When to Use

- Attaching a token/cost line to a utility or cron test run.

- Answering "what did that run/session cost?" or "what is Clarity spending a day?".

- Comparing cost across models or sessions.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Cost a run as it happens.** Run the test in one-shot mode with a usage file:

  ```bash
  ~/.hermes/hermes-agent/.hermes/bin/hermes -z "<prompt>" --usage-file /tmp/run_usage.json
  ```

  The report is written **even when the run fails**, so a pipeline always accounts.

1. **Read it:** `python3 ~/.hermes/scripts/token_cost.py usage /tmp/run_usage.json` — flags, tokens, api_calls, main cost, plus the **auxiliary** block (vision / compression / title generation) and the grand total.

1. **Cost a session after the fact:** `token_cost.py session <id-prefix>` — per-model and per-task breakdown from `state.db` (the canonical store for anything already run).

1. **Aggregate:** `token_cost.py period --days 7 [--model <substr>]` (daily + per-model) and `token_cost.py models` (lifetime per model).

1. **Attach to a report:** `token_cost.py attach <id-prefix>` — one compact line (`cost … · in … · out … · N tools · model …`).

1. **State the source.** Every figure carries `cost_status` — `estimated` (from the rate card) or `actual`. Local LM Studio models bill `$0` (`billing_provider=lmstudio`) and must be reported as free, not estimated.

## Quick Reference

```javascript
~/.hermes/scripts/token_cost.py usage   <usage.json>
~/.hermes/scripts/token_cost.py session <id-prefix>
~/.hermes/scripts/token_cost.py period  --days N [--model substr]
~/.hermes/scripts/token_cost.py models
~/.hermes/scripts/token_cost.py attach  <id-prefix>
```

Add `--json` anywhere for machine output.

## Boundaries

- **Read-only.** The utility opens `state.db` `mode=ro`; it never writes usage or costs.

- Never present an estimated cost as actual — always print `cost_status`.

- Never compute cost from a guessed rate card; the numbers come from `state.db`/the usage file.

- Do not "estimate" local (`lmstudio`) sessions — they are genuinely `$0`.

## Verification

- `attach <id>` totals match `session <id>` for the same row.

- `period --days N` by-day totals equal the sum of the by-model column for that window.

- A usage file with `failed: true` still reports tokens and cost.

## Pitfalls

- The **session total** is the main loop only; the per-model breakdown adds `background_review` / `title_generation` auxiliary rows, so the two can differ by a few cents. Say which you are quoting.

- `state.db` grows; a `session` prefix that matches more than one id is rejected — be specific.

- Cost is only as good as the rate card snapshot: a model billed through a proxy/relay may differ from the [models.dev](http://models.dev/) list price (`cost_source` records which applied).