---


name: weekly-model-review
uuid: 40d24dc8ccd98164b1dadd5bd850e7a6
version: 2
description: "Use when re-picking the default model on price or release."
last-used: "2026-11-05"
scope: local
thinking: "Medium"
temperature: 0.2
author: clarity
license: proprietary
metadata:
hermes:
tags: [openrouter, model-routing, cost, benchmark, cron, monday]
related_skills: [openrouter-model-pick, openrouter-usage, token-costing]


---


# Weekly model review

Every Monday: re-check the OpenRouter catalogue against the current default, benchmark any
unbenchmarked model that undercuts it, and tell Richard whether to stay or switch.

Goal: the **<$1/day sweet spot** with rising chat and tool activity. Hard stops matter more
than the ranking — a model that fails the Notion task or blows $2/day is out regardless.

## When to Use

- The weekly Monday cron (`weekly-model-review`, Discord Home channel).

- Any time a new model lands, a price moves, or Richard asks "should we switch?"

## Layout

```javascript
~/.hermes/scripts/or_model_pick.py     filter + cost the live catalogue
~/.hermes/scripts/bench_models.py      Phase A: 16 real tasks from eval_tasks.json
~/.hermes/scripts/bench_tools.py       Phase B: 8 tool-calling scenarios
~/.hermes/scripts/bench_report.py      merge A+B into a head-to-head verdict
~/.hermes/scripts/bench_baseline.py    durable store + taste scorer
~/.hermes/bench/baseline.json          the store (current_default, per-model metrics)
~/.hermes/bench/runs/<date>/           raw run files, verdict, cost basis
```

`baseline.json` is the memory of this review. Always read it first; always update it.

## Steps

1. **Load the baseline.** `python3 ~/.hermes/scripts/bench_baseline.py show`
→ current_default, each model's Phase A/B accuracy, latency, est $/day, hard stops.

1. **Pull today's filtered list.**
`or_model_pick.py --days 150 --max-in 1.0 --max-out 1.0 --workload-in 5607892<br>   --workload-out 499488 --workload-cache 75991413 --calls 478 --json /tmp/pick.json`
Re-derive the workload quarterly from `state.db` (see openrouter-model-pick).

1. **Identify contenders.** A model is a contender if it is (a) recent, (b) in an approved
family, (c) tools+reasoning, and (d) **cheaper est $/day than the current default** — or
matches its price with a materially newer release. Skip anything already in the baseline.
No contender → report "no change" in two lines and stop. Do not invent work.

1. **Benchmark each contender** (Phase A then Phase B), always against the **current default**
as the control, same day, same conditions:

  ```javascript
  python3 bench_models.py --models m.json --max-tokens 6000 --temp 0.0 --reps 1
  python3 bench_tools.py  --models m.json --temp 0.0 --max-turns 4
  python3 bench_report.py <A.json> <B.json>
  ```

  `m.json` url is the API BASE `https://openrouter.ai/api` — the harness appends
  `/v1/chat/completions`. Passing `.../api/v1` scores a silent 0/0 on every call.

1. **Persist.** Copy run files to `~/.hermes/bench/runs/<date>/`, then
`bench_baseline.py save --label <date> --a <A> --b <B> --cap 6000 --est est.json`.
Build `est.json` with `or_model_pick.py` at the reasoning-inclusive output volume.

1. **Report** to the Discord Home channel and suggest stay-or-switch.

## Taste criteria (Richard, 2026-11-03)

Blend, in rough priority order:

1. **Estimated total daily cost** — the point of the exercise. Show 1x and 2x-activity figures.

1. **Real-task reasoning capability** — Phase A pass rate on tasks sampled from his real week.

1. **Tool-call outcomes** — Phase B pass rate. Tool-intensive flows are the headline use case.

1. **Speed** — Qwen3.7-Flash is the **floor**: slower than that is a real cost, but speed is
*not* the top priority. Never rank on latency ahead of cost or correctness.

1. **Turns to completion, not just per-token price** (Richard, 2026-11-05). A cheaper model that
needs ~10x the back-and-forth does **not** reduce the bill — it frustrates and can cost more in
total. Weigh turns-to-done alongside price. On that basis the preferred default is
**DeepSeek V4.1-Flash 1017** (`deepseek/deepseek-v4.1-flash-1017`): Qwen is cheaper per token but
loses on total turn count. Do not switch away from it on price alone.

### Hard stops — report the model as OUT, whatever else it scores

- **Fails ****`me-ship-json`** (the Notion MCP property-JSON task) → it will break working with
Notion. This is a binary, verified from the run file, not a judgement.

- **Estimated cost > $2/day** → it blows the ceiling. The target is <$1/day, so a model above
$2 is out and one between $1 and $2 needs an explicit reason to be preferred.

Also treat as disqualifying, and say so plainly: empty `content` at the cap (see Pitfalls),
and any fabrication of a value a tool never returned.

## Decision rule

Switch only when the contender **beats the current default on the blend and clears both hard
stops**. If it wins on price alone, or ties while costing less, present it as a switch
candidate but state the tradeoff explicitly. Otherwise recommend staying — and say what would
change the recommendation.

## Reporting format (Discord, no tables)

```javascript
**Signal** one line: contending model + the price delta vs the current default.
**Benchmark** Phase A x/16 and Phase B y/8 for contender vs control, est $/day, latency.
**Hard stops** pass/fail for each, named.
**Caveats** rubric artifacts, single-rep noise, truncation, anything you discounted and why.
**Recommendation** stay or switch, in one line, with the reason.
**Needs Richard** the exact action (switch command / nothing).
```

State explicitly when nothing changed. Never pad a quiet week into a report.

## Pitfalls

- **Never benchmark at a tight output cap.** Reasoning models spend output tokens on reasoning
*before* content; at 1600 tokens Qwen3.7-Flash returned empty content on 6/16 tasks (100% of
the budget on reasoning, `finish_reason=length`). Use `--max-tokens 6000` and re-check any
contender that shows `finish=length` with `text==""`. Empty content on a real task is a
disqualifier, not a rounding error.

- **Reasoning tokens bill as output** and vary by task, not just by model. On one identical
prompt DeepSeek V4.1-Flash spent 4,899 reasoning tokens vs Qwen3.7-Flash 1,681. Never infer
a model's reasoning overhead from a single probe.

- **Daily vs weekly counts.** `state.db` aggregates over a window: 3,343 tool calls was a
**7-day** total, 478/day. Passing a 7-day total as a per-day figure inflates every cost
estimate ~7x. Divide by the window length first.

- **Calibrate the estimate against a real day.** Rate-card on `state.db` tokens ran 1.6x the
2026-11-02 actual; on the 7-day measured mix it landed within 10% of actual. Say which basis
you quote, and reconcile with `openrouter_usage.py --activity`.

- **Discount broken rubrics before declaring a winner.** `hx-cite` keyed on the literal string
"tokens per second", so the model that fabricated the *more confident* number scored better.
Re-read the raw text of every disagreement and exclude a row you cannot defend.

- **Score tool calls on outcomes, not tool names** (`write_file` vs `terminal`+redirect), and
cap turns at 4 — a model still probing at the cap "did not conclude in budget", it did not
fail.

- **One rep at temp 0 is still non-deterministic.** Treat a single-task gap as noise unless it
repeats across both phases.

- **Never claim a family qualified without checking.** Gemini, Grok and Kimi K3 all sit far
above $1/M output today; say they produced no candidate rather than omitting them.

- `hermes config set model.default <id>` is the only sanctioned way to switch — direct edits to
`~/.hermes/config.yaml` are refused for the agent.