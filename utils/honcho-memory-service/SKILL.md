---


uuid: 40524dc8-ccd9-81c1-847c-e992dc29c6df
name: honcho-memory-service
description: "Honcho Memory Service"
version: 2.0.0
last-used: "2026-10-27"
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
hermes:
tags: [honcho, memory, selfhosted, docker, scopes, workspaces, memory-provider, edges, postgres, pgvector]
category: devops


---


# Honcho Memory Service

> **DECOMMISSIONED 2026-10-28 — do not rebuild without being asked.** Honcho was removed: containers and volumes deleted, `config/honcho/config.toml` and the `HONCHO_*` secrets removed, the service + volume blocks stripped from `docker-compose.yaml`, and Hermes set to built-in memory (`memory.provider: ""`). Its memory was migrated to markdown at **`@Edge/.ai/Memory/`** (peers, sessions, 1,247 derived documents, raw dump) and is read with `search_files` or Obsidian. Keep this skill for the *method* — costing and safely tearing down a shared-key sidecar.

Richard's server-side memory: a self-hosted Honcho instance in the Studio `ai` docker stack, shared by every agent he runs. Covers provisioning, the data model, and pointing clients at it. Deploy: `references/deployment.md`; client wiring: `references/client-wiring.md`; workspaces/scopes: `references/workspaces-and-scopes.md`; pitfalls: `references/operations-and-pitfalls.md`; cost and teardown: `references/cost-and-teardown.md`.

## When to Use

- Standing up or rebuilding Honcho (or another server-side memory provider) in the `ai` stack.

- Wiring Hermes — or another harness (Codex, Claude Code, OpenCode, Kilo) — to one shared memory.

- Designing workspaces / scopes / peers (pillars `bonds`, `craft`, `edge`).

- Minting/scoping Honcho keys, or confining an edge device to a subset of memory.

- Memory appears empty, stale, or not shared across two agents.

## Always-on rules

- **One workspace, many scopes.** A workspace is a HARD boundary — nothing crosses it, *including the peer*; split only for a real confidentiality/compliance fence. Group by topic/confidentiality with **scopes**.

- **Scope names are permanent** (no delete endpoint) — settle the taxonomy first. **Sessions are the unit scopes enforce** — recall is bounded by *where*, not what, was said. A scope constrains only queries that name it; an unscoped request still sees everything (confinement is the *key*, not the scope).

- **Probe with facts you're willing to keep** — prefer read-only checks; a write probe must delete its sessions, flush the cache, confirm derived state gone, and remove any `MEMORY.md`/`USER.md` line.

- **Never put a secret in chat** — mint keys in-process, print only length/name, write a `0600` file; credentials live in `~/.hermes/edge.env` (0600).

- **Verify against the live service, never config** — client connection, a real recall round-trip, scope enforcement (`401` outside).

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Add the services to the stack compose** — project `ai` at `@Edge/.ai/docker-compose.yaml`, `780x` host ports (memory API `7806`, embed `7807`), per-service config under `@Edge/.ai/config/<service>/`, secrets in `@Edge/.ai/.env` (gitignored), join `edge-net`.

1. **Start datastores first, then migrate, then fix the vector dimension, then start the API.** Skipping it leaves the API in a crash-loop that reads like an auth/DB fault — ordering/repair: `references/deployment.md`.

1. **Confirm health on the host** (`curl` the API `/health`), then confirm the worker is *processing*, not merely running — a healthy API with a pending queue looks like success.

1. **Demonstrate one real end-to-end recall** and report that output, not container status.

1. **Wire a client:** install/activate the provider, point it at the service (`references/client-wiring.md`); use the **same workspace *****and***** same user peer on every host** — plugins default to a workspace named after themselves, so an unconfigured harness stays isolated.

1. **Verify** with the client's status command, a representation read-back, and a real recall round-trip. An MCP-only harness gets tool-based recall unless hooks exist — pair it with a memory skill.

## Data model

Workspace vs scope vs session-allowlist, boundary strength, named-scope key limits and the two hard blockers are in `references/workspaces-and-scopes.md` — read it before creating workspaces/scopes (both effectively permanent).

## Pitfalls

- **A named-scope key cannot initialise the standard SDK** — `honcho-ai` calls `POST /v3/workspaces` at the head of nearly every accessor, correctly refused for a scope key, so the client errors out. Confinement and the stock plugin are mutually exclusive.

- **The Hermes provider plugin has no scope support** — scopes on the primary agent are organisational, not enforced; bounded reasoning there is a plugin change.

- **Never point embeddings at a desktop app** — closing it silently stops new embedding while old recall works; serve them from a headless `embed` container (`ghcr.io/ggml-org/llama.cpp:server`, `--embeddings`, `http://embed:9931/v1`).

- **The reconciler heals failed embeddings only after a 10-minute ****`SYNC_BACKOFF`** — let the 300 s cycle fire or enqueue `{"reconciler_type": "sync_vectors"}`, then check `message_embeddings.sync_state` → `synced`.

- **Honcho bills the LLM key for its own work** — `honcho-api` and `honcho-deriver` both take
`LLM_OPENAI_API_KEY=${OPENROUTER_API_KEY}`, and the deriver, summariser and every dialectic level run
paid calls. The shipped config derives **every message immediately** (`FLUSH_ENABLED = true`,
`REPRESENTATION_BATCH_WORK_UNIT_TARGET_TOKENS = 0`) plus scheduled dreams, so it is a real,
easy-to-miss line on a shared key. Cut it by restoring batching, disabling `dream`, and capping
`DEFAULT_MAX_TOKENS` — or point `[deriver]` / `[summary]` / `[dialectic.*]` at a local
OpenAI-compatible server to make it free. Attribute it like any other consumer (shared-key steps in
`token-costing`).

- **Other gotchas:** `docker compose up -d --no-deps` defeats health-gated `depends_on`; the worker batches by default and looks broken; migrations seed a vector width that can mismatch your model; store the DB on a local named volume, never the network share. Full prose: `references/operations-and-pitfalls.md`.

## Reporting

Close with: what's running and where, the route verified, evidence of a real round-trip, what was cleaned up, open decisions, and anything minted not yet in `edge.env`.