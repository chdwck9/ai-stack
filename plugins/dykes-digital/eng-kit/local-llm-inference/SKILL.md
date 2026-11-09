---


name: local-llm-inference
uuid: 40524dc8-ccd9-81e3-aeab-c21e429f9d41
version: 2
description: "Local LLM Inference"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
author: Hermes Agent
license: MIT
metadata:
hermes:
tags: [local-llm, mlx, apple-silicon, inference, rapid-mlx]
related_skills: [tech-landscape-research, token-costing]


---


# Local LLM inference (Apple Silicon)

Install, size, serve and manage a local model server on a Mac (usually the always-on Studio) and
point agents at it. Default runner **Rapid-MLX**; pair with `tech-landscape-research`.

## When to Use

- Installing, sizing, serving or managing a local endpoint.

- Backing a coding agent (Claude Code, Codex, Pi, Hermes) with zero external tokens.

- Judging why a local job that "worked" started erroring.

## 0. Probe the real hardware — never assume

```bash
sysctl -n hw.model hw.memsize hw.ncpu
system_profiler SPHardwareDataType | grep -iE 'chip|memory|cores'
```

Usable budget ≈ RAM − ~8–10 GB for the OS (~70–75% for weights + KV). A 64 GB Mac comfortably
runs ~20 GB models; a 120B MoE at 4-bit (~60 GB) does not fit. **Choose the model equal to the
measured RAM, not to optimism.**

## 1. Size the model

- **Prefer MoE and size by ACTIVE parameters, not total.** A 30B-A3B decodes like a small dense
model per token; do not judge speed by total params.

- Context grows the KV cache — a model that fits at 4-bit may not fit with a long context.
The quant is in the alias (`-4bit` / `-6bit` / `-8bit`): take the highest that fits.

## 2. Pick the runner

Default **Rapid-MLX** — Homebrew core, MLX, OpenAI *and* Anthropic `/v1/messages`, tool-call
focus, `rapid-mlx launch <agent>`. It cannot run GGUF. Alternatives and the RAM→model table:
`references/apple-silicon-runners.md`.

## 3. Procedure (Rapid-MLX — verified end-to-end)

Copy these steps verbatim into the task list before starting. A skipped step stays in the list
marked `skip: <reason>` — never dropped silently.

1. Install: `brew install rapid-mlx` (alt `curl -fsSL https://rapidmlx.com/install.sh | bash`).

1. Diagnose: `rapid-mlx doctor`.

1. **Ask the tool which model fits — do not guess:** `rapid-mlx recipe` prints the smart + fast
pick *for this Mac* (RAM, capability %, tok/s).

1. Pull: `rapid-mlx pull <alias>` (avoid GGUF aliases — the name reveals MoE, `A3B` = 3B active).

1. Serve: `rapid-mlx serve <alias> --port 8000` (load ≈ 30 s).

1. **Verify BOTH surfaces before declaring done** — a bound port is not proof:

  - OpenAI: `curl -s localhost:8000/v1/models`, then a `/v1/chat/completions` probe.

  - Anthropic: `curl -s localhost:8000/v1/messages -H 'anthropic-version: 2023-06-01' -H<br>     'content-type: application/json' -d '{"model":"<alias>","max_tokens":20,<br>     "messages":[{"role":"user","content":"ping"}]}'`

1. Wire an agent: `rapid-mlx launch <claude-code|codex|opencode|…>` patches that client's config.

1. Manage: `rapid-mlx ps | ls | rm | info`; `rapid-mlx models` lists the **full alias
catalogue** (size, tool parser, spec-decode, preset) — the size column is how you check a
model fits before pulling it.

**Telemetry is ON by default** — turn it off once: `rapid-mlx telemetry off` (or
`RAPID_MLX_TELEMETRY=0`), and set it in any launchd plist.

### Tuning the serve (context + KV cache)

The launch flags — not the model — decide whether a long agent loop stays fast. Read the live
LaunchAgent plist before advising; the flags it passes ARE the current config.

- `--context-length <n>` — cap it so the harness compacts rather than re-prefilling a huge
prompt; the single biggest latency lever on a long run.

- `--cache-memory-percent <fraction>` — a **fraction of RAM, not a percent** (default `0.20`).
`--cache-memory-percent 35` means 3500%, not 35%, and silently makes the budget meaningless.
Pass `0.40`-style values.

- `--enable-prefix-cache` — re-use the shared prefix across an agent loop's turns (on by default).

- **`--kv-cache-dtype int8|int4`**** only works on full-attention models.** On a hybrid
(linear-attention/Mamba) architecture — e.g. any `qwen3_5`/`qwen3_5_mtp` alias — the loader
raises `KVCacheQuantizationUnsupportedError` (`the loaded model is incompatible: ArraysCache`)
and the server **fails to start**. Leave KV at bf16 for hybrids; a 130k context at bf16 is only
a few GB. Quantised KV is for full-attention families only.

- `--enable-auto-tool-choice --tool-call-parser <parser>` — pin the tool-call format explicitly.
`--enable-tool-logits-bias` is optional and can be *inert* (it warns `tokenizer not available`),
so do not rely on it as the fix for bad tool calls.

- **Test a flag set on a spare port before committing it to the LaunchAgent.** A rejected flag
fails at model-load time, so a bad plist means a crash-looping service; a throwaway
`--port 8011` instance proves the flags load first.

## Benchmark a local model on a real task

Measure, never estimate. Speed = `completion_tokens / wall_seconds` from one
`/v1/chat/completions` call on a fixed prompt; accuracy = both models' full outputs scored against
the SAME rubric, written to files so the comparison is reviewable.

- Run the identical prompt through the local endpoint and a cloud baseline at the same
`max_tokens`, and compare at equal *visible* output length. A reasoning model can spend the whole
budget on `reasoning` and return empty `content` at a low cap — that is truncation, not a
failure. Raise the cap (>=6000) and check `finish_reason` before scoring anything.

- Judge accuracy on a rubric tied to the real task — every required section present, every claim
grounded in the supplied evidence, gaps named rather than papered over — not on prose style.

- Keep the harness and both raw outputs somewhere durable; the scratch dir is pruned.

- Expect the local model to be a few times slower **per token**, and judge it on substance — but
do not assume it loses on wall clock. A local 27B running a real multi-tool task can be
substantively comparable to a frontier cloud model while looking "too slow" on a stopwatch;
and a local **MoE** (35B-A3B, ~74 tok/s vs the dense 27B's ~25 tok/s) beat a cloud *reasoning*
model outright on wall clock for the same visible answer (23 s vs 27 s), because the cloud
model spent its budget on hidden reasoning tokens. Compare at equal **visible** output, and
reach for the MoE whenever latency is the complaint — the speed gap between MoE and dense on
the same port is ~3x and easy to miss.

## 4. Keeping it alive

`launchctl bootstrap|submit|kickstart` and `hermes gateway restart` are **blocked inside a
supervised gateway session**, so a server cannot be made to auto-start from an agent session —
stage it and hand Richard the command.

- System daemon (boots before login, needs sudo): `sudo rapid-mlx service install`.

- User LaunchAgent (no sudo): write `~/Library/LaunchAgents/com.<x>.user.plist` (`RunAtLoad` +
`KeepAlive`), then the **user** runs
`launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/<x>.user.plist`.

- Otherwise run it as a tracked background process:
`terminal(command="…", background=true, persist_on_release=true)`. A `nohup` wrapper is refused,
and a process started in a session dies with it.

- **A plist edit does not take effect on ****`kickstart`****.** launchd caches the job definition it
loaded, so `launchctl kickstart -k …` restarts the process with the OLD argv. Changing flags
requires `bootout` then `bootstrap` (from a shell outside the gateway). Never treat the plist
file as proof of the running config: read the *loaded* definition
(`launchctl print gui/$(id -u)/<label> | sed -n '/arguments = {/,/}/p'`) and the serve log line
that reports the effective setting (`Memory-aware cache: N% of RAM`). A server can run for days
on defaults while a plist claiming otherwise sits on disk — and `ps` truncates argv without
`-ww`, so use `ps -ww` before concluding a flag is missing.

## Pitfalls

- **One LLM server at a time.** Two ~20 GB models will not both fit a 64 GB Mac. Both can appear
to run, but under a large prompt the non-primary one fails opaquely (LM Studio: `Compute<br>  error.`). That is unified-memory contention — when a job that worked starts erroring, check what
else is resident before touching the client.

- **A running process is not a working server** — probe the endpoint; a bound port can error
while the model loads.

- **No auth on ****`127.0.0.1`**** is expected**, not a hole — keep the bind on loopback.

- **GGUF is not universal** — Rapid-MLX cannot run it; for a GGUF-only model use LM Studio or
llama.cpp (reference).

- **Do not recommend a model the RAM cannot hold** — run `recipe`, not habit.

- **A name is not a spec — verify the model exists and read its real size before recommending.**
A "Flash" flagship variant can be 180B total (~97 GiB at 4-bit) and hopeless on 64 GB, while its
dense sibling is 15 GiB — and a version you expect may not exist at all (there is **no Qwen
3.7**; the line went 3.5 → 3.6 → 3.8). Check the size in `rapid-mlx models`, and for anything
uncached read the arch/params from the Hub (`curl -s https://huggingface.co/api/models/<repo>`
plus the raw `config.json`). Present size-vs-capability as a trade, not a win: `recipe`
typically offers a more capable slower model against a slightly weaker faster one.

- **oMLX is not a provider.** It is a quantisation toolkit (`jundot/omlx`, which produces the
oQ/oQe checkpoints) — do not go looking for an "oMLX server" or an oMLX route.

- **On a local model the tool-calling is the fragile part, not the speed.** The meta `tool_call`
tool takes a large, exactly-valid JSON argument; a smaller local model emitting kilobyte
payloads (page bodies, multi-item batches) mis-serialises them and the harness's no-progress
guard ends the run having produced nothing. Keep payloads ASCII-safe (a middle dot or em dash
inside a JSON string has broken the parse), split them into small batches, and prefer scripting
bulk writes behind ONE `terminal` call over making the model emit them.
**Before concluding a model cannot call tools, probe it** — send one small
`tools=[{...}]` request and check the arguments parse as JSON. If that returns valid JSON, tool
calling works and the failure is payload *size*, so fix the payload path rather than swapping to
a bigger model.

- **A brew upgrade can re-download the model.** A version bump can pin a new revision of the same
repo, so the next start reports "model weights are missing" and re-pulls the whole checkpoint
(tens of GB) — that is a slow first start, not a hang. The previous revision stays as dead
weight in the HF cache (`du -sh ~/.cache/huggingface/hub/models--*`). Run
`rapid-mlx upgrade --dry-run` first to see the method and target version; re-check the effective
flags afterwards, since a major bump can change the flag surface.

## Report shape

Give real numbers (RAM, capability %, tok/s), honest tradeoffs and one recommendation — not a
menu; name blockers (e.g. autostart needing his shell).

## References

- `references/apple-silicon-runners.md` — runner comparison, sizing table, the embeddings
container, and the GGUF / LM Studio path.