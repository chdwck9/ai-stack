---


name: llm-benchmarking
description: "Use when benchmarking or comparing LLMs."
version: 1
author: Hermes Agent
license: MIT
thinking: "Medium"
temperature: 0.3
metadata:
hermes:
tags: [llm, eval, benchmark, model-selection, local-llm]
related_skills: [local-llm-inference, token-costing, openrouter-usage]


---


# Benchmarking models on real tasks

Compare two or more LLMs on tasks the user actually does, then recommend what each is best for
(usually: which model should back Clarity or an agent).

## When to Use

- "Benchmark X vs Y", "what's best as a local backend", "is model N good enough for Z".

- Choosing, replacing, or sizing the model behind Clarity or a coding agent.

## Non-negotiables

- **Never invent a model id, price, or result.** Resolve every name to a concrete id that responds
to a live probe before benchmarking — see `references/model-identification.md`.

- **Reuse prior results only when the prior run is the SAME benchmark.** A throughput (tok/s) test is
not a quality rubric; do not substitute one for the other, and do not mix stacks. State which
prior numbers you reused and which you re-measured.

- **The runner executes no tools.** Each task is a plain chat completion scored against a
deterministic substring rubric, so it is safe to run unattended. Say so in the report.

## Procedure

1. **Fix the model set.** Confirm each id with `/v1/models` plus a one-shot completion before the
full run. Local and cloud ids are different namespaces.

1. **Use the real task suite:** `~/.hermes/scripts/eval_tasks.json` — sampled from the user's actual
week; categories `mechanical`, `read-heavy`, `multi-tool`, `judgement`, `hallucination`.

1. **Run** `python3 ~/.hermes/scripts/bench_models.py --models models.json --max-tokens 6000` —
N models in one pass (supersedes `eval_models.py`, which is hard-wired to one local + one cloud).
`models.json` = `[{"name","url","model","key_env"}]`; `key_env` resolves from `~/.hermes/.env`.

1. **Checkpoint per model.** Give each model its own output file (or run one model per invocation)
so a long run survives a timeout. **Local models share one server, so their legs must run
sequentially** — parallel local legs thrash the single loaded model.

1. **Report:** pass rate overall and by category, mean latency, output tokens, cost, and RAM/disk
footprint. Keep verified-vs-assumed visibly apart.

## Pitfalls

- **A reasoning model returns EMPTY ****`content`**** when the token cap is too low** — its answer sits in
`reasoning_content`, which the rubric does not read, so every heavy task scores FAIL and the model
looks broken. Cause: it spends the whole budget "thinking" and finishes `finish_reason: length`
before emitting an answer. Raise `--max-tokens` (≈6000) and record `finish_reason` +
`reasoning_chars` so you can tell truncation from a genuine miss. This is the most common way a
benchmark lies about a capable model.

- **Speed is stack-specific; quality is not.** A GGUF runs on llama.cpp / LM Studio; MLX quants run on
rapid-mlx. You cannot compare tok/s across those stacks, and a model may exist on only one.
Measure QUALITY on one shared stack, and report SPEED per each model's best stack — naming the stack.

- **Prefill dominates, so a small model can be far slower than a big one.** A 2-bit dense 27B can take
~60 s on a long prompt where a larger low-active MoE answers in seconds. Latency spreads of
0.5 s vs 60 s are signal, not noise.

- **Do not judge speed by total parameters** — MoE with few active params decodes far faster.

- **Long local runs belong in the background** (`background=true`, `notify=true`); never block a
foreground call for tens of minutes on a slow local model.

## Report shape (this user)

Honest tradeoffs and real numbers — RAM, tok/s, pass rate — with verified versus assumed clearly
separated, and a recommendation rather than a long menu; he makes the call. State plainly when a
search found nothing instead of filling the gap.

## References

- `references/model-identification.md` — resolving a nickname/codename to a concrete, live model id.