---


name: local-inference-apple-silicon
description: "Use when running local LLM inference on Apple Silicon."
version: 1
author: Hermes Agent
license: MIT
scope: local
thinking: "Medium"
temperature: 0.3
metadata:
hermes:
tags: [local-llm, apple-silicon, mlx, llama-cpp, ollama, inference]
related_skills: [token-costing, remote-agent-kickoff]


---


# Local Inference on Apple Silicon

Run LLMs locally on the Studio (Apple silicon, unified memory) — choose a model that fits the machine, stand up a server, and back agent harnesses with it.

## When to Use

- Choosing a local model or a local inference runner for a Mac.

- Installing, serving, or managing a local OpenAI/Anthropic-compatible endpoint.

- Sizing a model to a machine's unified memory.

## Sizing

- Usable budget ≈ 70–75% of unified memory for weights + KV cache; leave headroom. A 64 GB Mac tops out around a ~40–48 GB model at a good quant.

- **Prefer an MoE and size by ACTIVE parameters, not total.** At equal total size, a low-active MoE decodes far faster; a 30B-A3B behaves like a small dense model per token.

- Context grows the KV cache — a model that "fits" at 4-bit may not fit with a long context.

## Steps

1. **Pick the runner** — see `references/runner-selection.md`. Default: an MLX-based runtime for Apple-silicon speed; llama.cpp for GGUF breadth.

1. **Install from the package manager** (`brew install <tool>`) in preference to `curl | sh`; fall back to the official installer or a manual release binary when the package manager is blocked (locked-down machines).

1. **Size the model with the tool's own recommendation** if it has one (a `recipe` / `recommend` command) rather than guessing from a chart.

1. **Serve both API surfaces.** Many local servers expose OpenAI *and* Anthropic-compatible endpoints; because agent harnesses (Claude Code) speak the Anthropic Messages API, a server with `/v1/messages` can back a coding agent with **zero external tokens**.

1. **Verify with a real completion on BOTH surfaces** — `/v1/chat/completions` and `/v1/messages`. A listening port is not proof the server works.

1. **Make the server outlive the session:** `terminal(command="...", background=true, persist_on_release=true)` for a process that never exits. For a boot/login service prefer the tool's own manager; a supervised gateway session rejects `launchctl` bootstrap, so stage the plist and have the user bootstrap it from a normal shell.

1. **Wire agents to it:** point a coding agent at the local endpoint (e.g. the runner's own `launch <agent>` command) so its "model" is the local server.

## Pitfalls

- **Do not trust a frozen model list** — re-derive the current landscape from primary sources (see the reference) instead of repeating a remembered list.

- **Confirm you pulled the MoE variant, not a similarly named dense one** — check the repo's parameter/active-parameter tags or config, not the name alone.

- [Localhost](http://localhost/) endpoints usually need no auth but bind to loopback only — fine for same-machine agents, not for remote clients.

## References

- `references/runner-selection.md` — runner categories, when to pick each, and how to re-derive the landscape.