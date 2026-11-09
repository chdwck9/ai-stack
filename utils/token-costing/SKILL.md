---


name: token-costing
uuid: 3ff24dc8-ccd9-81b3-a74f-caafdb75548b
version: 2
description: "Token Costing"
last-used: "2026-10-27"
thinking: "Low"
temperature: 0.2
author: clarity
license: proprietary
metadata:
hermes:
tags: [tokens, cost, usage, accounting, openrouter, cron]
related_skills: [clarity-capabilities, openrouter-usage]


---


# Token costing

Reach the numbers that say what a run, session, day or account actually spent — never from a
guessed rate card. `state.db` is canonical for anything already run; the per-run
`--usage-file` covers a test while it happens; the provider API is the only source for the
*account* total.

## When to Use

- Attaching a true cost line to a utility or cron test.

- "Why am I spending €X a day?" / "how do I cut it?" / "is it all the skills?".

- Choosing a cheaper model for the user's *actual* token mix.

- Auditing which cron jobs bill paid vs local models.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the
list marked `skip: <reason>` — never dropped silently.

1. **Cost a run as it happens** — one-shot with a usage file:
`~/.hermes/hermes-agent/.hermes/bin/hermes -z "<prompt>" --usage-file /tmp/run_usage.json`.
The report is written *even when the run fails*, so a pipeline always accounts.

1. **Read it:** `token_cost.py usage /tmp/run_usage.json` → tokens, `api_calls`, main cost,
the **auxiliary** block (vision / compression / title generation) and the grand total.

1. **Cost a session after the fact:** `token_cost.py session <id-prefix>` — per-model and
per-task from `state.db`.

1. **Aggregate:** `token_cost.py period --days 7 [--model <substr>]`, `token_cost.py models`.

1. **Attach to a report:** `token_cost.py attach <id-prefix>` → one compact line.

1. **Separate the account figure from Hermes' own.** The authoritative account total comes
from the provider API (`openrouter-usage` → `/api/v1/credits` + `/api/v1/key`); Hermes'
share comes from `state.db`. A shared key bills spend this store never sees. Report both.

1. **Attribute by model before optimising.** One frontier session routinely outweighs a
month of cheap chat — find that line first or you optimise the wrong thing.

## Quick Reference

```javascript
token_cost.py usage <usage.json>   session <id-prefix>
token_cost.py period --days N [--model substr]   models   attach <id-prefix>
```

`--json` anywhere for machine output. `hermes prompt-size --platform <cli|cron|…>` is
offline and gives the fixed-prompt split. Deep detail: `references/fixed-prompt-and-prefill.md`,
`references/skills-catalogue-and-curator.md`.

## Levers, ranked (change one, re-measure)

1. `recallMode: hybrid -> tools` in `~/.hermes/honcho.json` — drops the ~5k-token/turn
memory prefetch. Usually the largest input saving.

1. Smaller tool output — the parameterised scripts, never raw payloads.

1. Scope the tool schemas — usually the largest fixed block (`tools.tool_search.defer`;
per-surface `enabled_toolsets`).

1. Shorter sessions — new session when the topic changes.

1. Trim the skills catalogue — ~18 tokens/skill and cached, so trim for relevance, not cost.

## Cron model rule

A cron with **no pinned model** runs on the MAIN agent model at fire time, so it bills at
that rate; `pinned: true` locks the job to the current model+provider — that is how a job is
made local/free. Audit with `cronjob_manage action=list`.

## Boundaries

- Read-only: opens `state.db` `mode=ro`; never writes usage or costs.

- Never present an estimate as actual — always print `cost_status` (`estimated` | `actual`).

- Local (`lmstudio`) sessions bill `$0` — report them as genuinely free, not estimated.

- Never compute cost from a guessed rate card.

## Pitfalls

- The **session total** is the main loop only; the per-model view (`session_model_usage`) adds
`background_review` / `title_generation` / `approval` rows. The gap is **not** cents: over 30 days
`sessions` totalled $27.73 vs $33.42 with all tasks — `background_review` alone was $4.91 (~15%).
Quote `session_model_usage` when reconciling against a provider bill. Say which you quote.

- **Bucket daily/monthly totals by ****`COALESCE(last_activity_at, started_at)`**, never `started_at`
alone: a long or cross-midnight session puts its whole cost on its start day, making single-day
figures read 2×–7× off (measured: Oct 30 $0.50 start vs $0.07 activity; Nov 2 $1.12 vs $2.41).

- The cache-read discount is a **hosted-model** fact. Locally the KV cache is exact-prefix
only: a changed toolset, skill set, memory write or model re-prefills cold, so local cost
is wall-clock — measure prefill tok/s and divide.

- `COALESCE(actual_cost_usd, estimated_cost_usd, 0)` returns 0 — `actual_cost_usd` is `0.0`,
not NULL. Use `COALESCE(NULLIF(actual_cost_usd,0), estimated_cost_usd, 0)`.

- `sessions.system_prompt` is usually NULL — the prompt actually sent lives in
`system_prompts` (`hash` → `prompt`), and `len(prompt)//4` estimates tokens.

- "Never used" ≠ "not useful". The never-used set is dominated by occasional reference
skills, and time-based staleness cannot move a skill whose activity fields are both null.
Prune on a long window and keep a pin list.

- Cost work on an already-cheap model saves cents, not euros — say so.

## Verification

- `attach <id>` totals match `session <id>` for the same row.

- Any claimed saving is re-measured after the change, not projected.

- Every cron is classified paid or local from its own `model`/`pinned` fields.