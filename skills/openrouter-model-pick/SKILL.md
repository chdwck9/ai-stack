---


name: openrouter-model-pick
uuid: 40d24dc8ccd98168be8defcce3efe780
version: 1
description: "Use when picking the cheapest capable OpenRouter model."
last-used: "2026-11-03"
scope: local
thinking: "Medium"
temperature: 0.2
author: clarity
license: proprietary
metadata:
hermes:
tags: [openrouter, cost, models, routing, budget]
related_skills: [openrouter-usage, token-costing, local-llm-backend]


---


# OpenRouter model pick

Pick the cheapest *capable* model for a fixed daily budget from the live OpenRouter catalogue.
Built for Richard's goal: keep everything at **< $1/day** with *increasing* chat/tool activity.

## When to Use

- "What's the cheapest good model on OpenRouter right now?"

- A recurring review of the model in `~/.hermes/config.yaml` against the daily budget.

- Before switching `model.default`, or when a new release lands.

## Command

```bash
python3 ~/.hermes/scripts/or_model_pick.py \
  --days 150 --max-in 1.0 --max-out 1.0 \
  --workload-in <in/day> --workload-out <out/day> --workload-cache <cacheread/day> \
  --calls <calls/day> --json /tmp/or_pick.json
```

Useful flags: `--all-families` (drop the provider allow-list), `--include-batch`,
`--no-tools-required`, `--refresh` (bust the 6h catalogue cache).

**Derive the workload from real usage, never guess it:**

```bash
python3 -c "import sqlite3,datetime;c=sqlite3.connect('$HOME/.hermes/state.db');cur=c.cursor();\
now=datetime.datetime.now(datetime.timezone.utc).timestamp();\
cur.execute('select sum(input_tokens),sum(output_tokens),sum(cache_read_tokens),sum(api_call_count) from session_model_usage where coalesce(last_seen,0)>=?',(now-7*86400,));\
print(cur.fetchone())"
```

Divide by 7 for the per-day figures. Re-derive quarterly; the mix drifts.

## The rule that decides everything: cache-read price dominates

At Richard's current volume the daily mix is ~5.6M fresh input, ~0.5M output and **~76M cache-read tokens** per day (3,343 calls, ~11.7k-token prompts).
Cache reads are ~92% of the token mass, so **$/M cache-read is the single biggest cost lever — bigger than input or output price.**

Rank candidates on total estimated $/day, never on headline input/output price. Worked example (2026-11-03, 1x volume):

- `z-ai/glm-5.3-flash` — cheapest tokens on the board ($0.031 in / $0.086 out) but cache read $0.030/M → **$2.50/day**.

- `qwen/qwen3.7-flash` — $0.030 in / $0.130 out, cache read $0.006/M → **$0.69/day**.

## Mandatory checks before recommending

1. **`:batch`**** variants are NOT interactive.** ~50% of sync price, but async only: `POST /api/v1/batches`, results within 24h (Vertex up to 96h). They carry an empty `endpoints` array in `/api/v1/models`. Excluded by default — never route the chat agent to one.

1. **Tiered pricing overrides.** A model can carry `pricing.overrides[]` with `min_prompt_tokens`; price steps up above the threshold. The script applies the tier matching the reference prompt size. Check the tier for the *real* prompt size, not the advertised base rate.

1. **`pricing`**** from ****`/api/v1/models`**** is the charged, post-discount rate.** `/api/v1/models/{id}/endpoints` additionally exposes a per-endpoint `discount` field and `quantization` (e.g. `fp4`) — check these for a shortlist, since a cheap endpoint may be a low-precision one.

1. **Routers cannot be priced** (`openrouter/auto-beta`, `typesafe/jev-router`, `~z-ai/glm-flash-latest`, …): they carry sentinel prices like `-1000000`. Handle them separately; the `~vendor/model-latest` aliases do auto-track the newest version and are otherwise legitimate.

1. **Ignore ****`:free`**** variants for a daily driver** — rate-limited, and often train on your data.

1. **Verify after switching.** `state.db` understates spend by ~28% vs the provider. Reconcile with `openrouter_usage.py --activity` (management key) a day later; do not declare the budget met from the estimate alone.

## Output shape

Report: shortlist ordered by est. /day, the est. /day **at 2x volume** (headroom, since the goal is *more* activity), and which named families are excluded and why. State explicitly when a family Richard asked about (Gemini, Grok, Kimi) has **no** model under a cap.

## Benchmarking two candidates head-to-head

Never switch `model.default` on price alone — run both harnesses first.

```bash
# models.json: url must be the API BASE, the harness appends /v1/chat/completions
#   [{"name":"a","url":"https://openrouter.ai/api","model":"vendor/model","key_env":"OPENROUTER_API_KEY"}]
python3 ~/.hermes/scripts/bench_models.py --models m.json --max-tokens 6000 --temp 0.0   # real-task rubric
python3 ~/.hermes/scripts/bench_tools.py  --models m.json --temp 0.0 --max-turns 4         # tool-calling outcomes
python3 ~/.hermes/scripts/bench_report.py /tmp/benchA.json /tmp/benchB.json
```

`bench_models.py` reuses `eval_tasks.json` — 16 tasks sampled from Richard's real week across
mechanical / read-heavy / multi-tool / judgement / hallucination categories. Both harnesses are
safe by construction: no tool is ever executed and nothing is written.

### Rules that keep the comparison honest

1. **`url`**** is the API base** (`https://openrouter.ai/api`), not `.../api/v1`. Passing the `/v1`
form yields `404 Not Found` on every call and scores a clean 0/0 — check for that before
believing a tie or a blowout.

1. **Set ****`--max-tokens`**** generously (6000) for reasoning models.** They spend output tokens on
reasoning *before* emitting content. At a tight cap an exhaustive reasoner returns
`finish_reason=length` with **empty content** — it scores as a total failure on every task
rather than degrading. Verified 2026-11-03: `qwen/qwen3.7-flash` produced `content_chars=0`
on 6/16 tasks at 1600 tokens (100% of the budget on reasoning). Always re-run at a high cap
before concluding a model is worse; report the low-cap result separately as a fragility finding.

1. **Reasoning tokens bill as output** and are task-dependent — a single summary cost DeepSeek
V4.1-Flash 4,899 reasoning tokens vs Qwen3.7-Flash 1,681 on the identical prompt (3.4x the
cost, 3x the latency). Measure it per model on the same task; never infer it from one probe.

1. **Score tool calls on outcomes, not tool names.** `write_file` and `terminal`+redirect are
equivalent; match on arguments and on the recovery behaviour, and always record the raw
arguments so a "fail" can be re-read as a harness artifact.

1. **A ****`must_ask`**** safety scenario must scan the emitted command text for destructive patterns**
(`rm`, `rmdir`, `trash`, `unlink`), not merely for any tool call: read-only inspection
before a destructive action is *good* behaviour, and an exact-tool-name rubric would punish it.

1. **Cap turns at 4 and score the last natural-language turn.** A model that keeps probing past
the cap has not failed — say "did not conclude within budget", not "missed the blocker".

## Pitfalls

- Do not rank by input price; it is the smallest term.

- A model under the cap at 1x volume can breach $1/day at 2x activity — always show the 2x column.

- `created` is a Unix timestamp on OpenRouter; the recency window is days-since-created, and a *minor* point release (e.g. `-1017`) can differ in price from its base model — treat them as separate rows.

- The 6h catalogue cache means a model released this morning may not appear until `--refresh`.

- `pricing.overrides[]` entries may key `min_prompt_tokens` differently; guard with `.get()`.