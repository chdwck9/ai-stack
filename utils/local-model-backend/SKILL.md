---


name: local-model-backend
uuid: 40524dc8-ccd9-811e-8043-cc0eeafbb0c7
version: 1
description: "Use when benchmarking or serving a local LLM backend."
last-used: "2026-10-25"
scope: local
thinking: "Medium"
temperature: 0.2
author: clarity
license: proprietary
metadata:
hermes:
tags: [local-models, benchmark, lmstudio, rapid-mlx, routing, config]
related_skills: [hermes-agent, token-costing]


---


# Local model backend

Benchmark local models on Richard's real tasks, then wire the winner as Hermes' primary model with cloud delegation/fallback. Measure with real runs — never invent numbers.

## When to Use

- Richard asks to benchmark, compare, or pick between local models.

- Wiring a local LLM (LM Studio / rapid-mlx / Ollama) as Hermes' primary model.

- A local-model endpoint is down, or a local-primary setup needs cloud delegation / failover.

## Two local stacks (Studio)

GGUF models (e.g. 2-bit quants) can only run on the llama.cpp stack → a same-stack speed comparison against MLX models is impossible; only same-stack **quality** is. Say so instead of comparing apples to oranges.

### LM Studio

```bash
export PATH="$HOME/.lmstudio/bin:$PATH"
lms ls | ps | load <id> | unload --all
lms import -y --copy --user-repo User/Repo /path/model.gguf   # id becomes lower(User/Repo)
curl -s http://127.0.0.1:1234/v1/models | jq -r '.data[].id'
```

### rapid-mlx

```bash
rapid-mlx ls              # cached models (aliases -> HF repos)
rapid-mlx ps              # running servers
rapid-mlx serve <alias> --port 8001 --host 127.0.0.1 --yes   # long-running
```

Serve runs forever → start it with the terminal tool in **background** mode (`persist_on_release=true`), never foreground (it times out).

## Benchmark on real tasks

Use the rubric harness (never executes a tool; deterministic substring scoring):

```bash
python3 ~/.hermes/scripts/bench_models.py --models models.json --max-tokens 6000
# models.json = [{"name":..., "url":"http://127.0.0.1:1234", "model":"<id>", "key_env":null}]
```

Tasks live in `~/.hermes/scripts/eval_tasks.json` (16 tasks, 5 categories: mechanical / read-heavy / multi-tool / judgement / hallucination) sampled from Richard's real week. Prefer reusing prior artifacts over re-running: check `~/bench_rapid_mlx_results*.json` (throughput) and `/tmp/eval_smoke.json` (quality) first, and say what each covers.

**Pitfall — reasoning models and empty content.** Many models (Qwen flash lanes, Qwen3.8, Saluki) emit `reasoning_content` first. With a low `max_tokens` they hit `finish_reason: length` and return **empty ****`content`** → scored as a failure that is really truncation. Always set `--max-tokens` high (≥6000) before concluding a model is bad; check `finish_reason` + `reasoning_chars`.

## Wire a local model as Hermes primary

Provider `custom` + `model.base_url` + a non-empty `model.api_key`:

```bash
H=~/.hermes/hermes-agent/.hermes/bin/hermes
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak-$(date +%Y%m%d-%H%M%S)   # always back up
$H config set model.provider custom
$H config set model.default "mlx-community/Qwen3.6-35B-A3B-4bit"
$H config set model.base_url "http://127.0.0.1:8001/v1"
$H config set model.api_key "rapid-mlx"          # non-empty string; never a real key
$H config set model.context_length 262144
```

**Escalate/delegate + survive outages:**

```bash
$H config set delegation.provider openrouter
$H config set delegation.model deepseek/deepseek-v4.1-flash
$H config set fallback_providers '[{"provider":"openrouter","model":"deepseek/deepseek-v4.1-flash"}]'
```

- `delegation.*` = the local primary *choosing* to hand a complex/tool-heavy turn to a cloud subagent.

- `fallback_providers` (top-level list of `{provider, model}`) = automatic failover when the local server is down. `hermes fallback add` is an **interactive picker** — in a headless/gateway session set `fallback_providers` with `hermes config set` instead.

Verify: `hermes fallback list` shows Primary + chain; `hermes chat -q "Run the shell command 'date +%Y-%m-%d' and tell me only the output."` must show a real tool call.

## Hard constraints

- **Never hand-edit ****`config.yaml`** — use `hermes config set`. Back it up first; a stray indent breaks the live gateway. Changes take effect on **new sessions**, not mid-conversation (prompt caching).

- **`launchctl bootstrap`****/****`submit`**** is BLOCKED inside the gateway.** A LaunchAgent (e.g. `com.rapidmlx.user.plist`) can only be loaded from a shell *outside* Hermes. Inside the gateway, run `rapid-mlx serve` as a background process and hand the durable agent-load to Richard.

- **Check the port before binding.** `:8000` on the Studio is taken by Docker (`supabase-envoy`); rapid-mlx's launchd plist was pointed there and silently failed. Confirm with `lsof -nP -iTCP:<port> -sTCP:LISTEN`.

- A background-served model **dies with the host process**; only the LaunchAgent is durable. Flag the gap; don't imply it's permanent.