---


name: hermes-multi-edge
uuid: 40524dc8-ccd9-8196-9920-da4ccdbab423
version: 2
description: "Use when taking the agent to other machines/edges."
last-used: 2026-10-19
author: Hermes Agent
license: MIT
platforms: [macos, linux]
scope: local
thinking: "Medium"
temperature: 0.3
resources:

- "@hermes-agent"

- "@hermes-services"

- "@hermes-skill-library"
metadata:
hermes:
tags: [hermes, multi-machine, edges, gateway, connections, memory-provider, skills-sync, topology]
related_skills: [hermes-agent, hermes-services, hermes-skill-library, external-account-access]


---


# Hermes Multi-Edge

## When to Use

Taking the agent to a second machine (work laptop, home server, NAS, cloud) and deciding what is shared, what stays local, and how the machines reach each other. Triggers: "bring her to my other machines/edges", cross-machine memory or skills questions, or wiring a local-only account (work Slack, work email) into the agent.

## The model

One shared brain, one Hermes runtime per edge, the Desktop/Bot Mode roster as switchboard.

- **Runtime per edge** — each machine runs its own Hermes with the default `local` terminal backend, so `terminal`/`execute_code` hit that machine's shell and files.

- **Shared brain** — skills via `skills.external_dirs` / the Hub pull; memory via one server-side provider.

- **Switchboard** — Desktop → Settings → Gateways registers every backend; the roster is a union across them and agents message across machines with `message_agent`.

Reject the tempting shortcut: do **not** solve "run on the edge" by pointing the hub agent at `terminal.backend: ssh`. An agent has exactly one terminal backend, so that trades away local execution instead of adding remote.

## Steps

1. **Verify against the live docs, not memory.** Fetch the whole doc set once and grep it:

  ```bash
  curl -s -o ~/.hermes/cache/scratch/llms-full.txt https://hermes-agent.nousresearch.com/docs/llms-full.txt
  grep -n "^# " llms-full.txt | grep -i <topic>          # locate the section
  grep -n "<!-- source: website/docs/" llms-full.txt        # per-page boundaries
  sed -n '<start>,<end>p' llms-full.txt                      # read the page whole
  ```

  `curl` is the reliable path regardless of the configured web-extract backend. Check `hermes --version` too — connection kinds and roster behaviour change between releases.

1. **Inventory the edges and the transport between them.** For each machine: OS, whether it is always-on, and which of NFS share / Synology Drive / git / Tailscale it can actually reach. Off-LAN reachability and corporate network policy decide the design more than the agent config does.

1. **Pick the hub.** A laptop-class Mac sleeps, so an always-on hub is either the NAS running `hermes serve` in Docker, a Hermes Cloud instance (Portal sign-in, discovered from any Desktop, no networking to build), or nothing (adopt connections-only until an always-on host exists).

1. **Stand up a runtime per edge**, each in its own profile (`hermes -p <name>`) — never one profile drive-shared across machines.

1. **Share the skill library** by pointing every edge's `skills.external_dirs` at the same synced folder (`hermes config set skills.external_dirs '["/path"]'`). Keep `skills.create_dir` **local** on each edge — a down mount breaks skill *creation*, and the Hub pull is the reconciliation channel.

1. **Share memory with an external provider, not with files.** Built-in `MEMORY.md`/`USER.md` and `state.db` are per-profile files, so they do not follow the user between machines. Enable a server-side provider (`memory.provider: honcho` self-hosted in Docker, or another provider) so every edge reads and writes one store. Deployment, bootstrap order, auth, and the deriver's batching gate are in `references/honcho-selfhost.md`. Three settings decide whether sharing works at all:

  - `workspace` + `peerName` **identical on every edge** → one store, one user model. `aiPeer` is the per-agent identity; give each agent its own and separate workspaces when work context must not land in personal memory.

  - `pinUserPeer: true` for a single-operator install, so the user's own Telegram/Discord/Slack runtime IDs all resolve to `peerName`. Without it every platform ID mints its own peer and "she remembers" appears to fail while the store is actually fine.

  - `apiKey` set **explicitly in ****`honcho.json`**, never relying on the `HONCHO_API_KEY` env var alone: for loopback/RFC1918/Tailscale base URLs the plugin substitutes the placeholder key `"local"` for env-sourced keys, so an auth-protected server answers `401`.

1. **Register the connections** in the Desktop: Settings → Gateways → Add connection → **Local** / **Remote gateway** (HTTP(S), LAN/Tailscale/internet) / **SSH** (app opens the tunnel and starts the dashboard itself) / **Hermes Cloud** (Portal sign-in). SSH is the practical kind for a locked-down laptop because it needs no inbound LAN access. Give each a unique device name; handles disambiguate as `@name-device` when a profile name exists on several machines.

1. **Keep local-only logins on their own machine.** If an account can only be signed in on one device, the agent that touches it must run on that device, in its own profile, with its own credential store. Reach it as a peer (`message_agent`, group chat, or an `@name-device` mention) — never as a copied token.

1. **Verify end to end**: the connection tests `Reachable`; a skill resolves from the synced `external_dirs` path on the edge; the agent's `terminal` tool reports the edge's hostname, not the hub's; a message from the hub agent lands on the edge agent and returns.

1. **Design the unreachable-edge case explicitly.** A machine that is asleep or off cannot run a delegated turn — a local-only login is genuinely unreachable in that moment, and no tooling changes it. Say so, then give the reachable design: the hub writes the request as a queued task (task DB / inbox note) addressed to that edge, and the edge agent picks it up on next boot. Do not imply the hub executed it.

## Boundaries

- Never copy a credential, session cookie, or login token between machines to make a local-only account reachable. It breaks device trust, usually breaks SSO, and is an access-control change — the edge has to host the agent.

- Treat an employer-owned machine as a policy gate before a technical one. Say plainly that a work laptop running an agent with shell access, and the ability to install Tailscale/Synology Drive, are the user's/IT's decisions; a local-only account is unreachable if the machine may not run the agent at all.

- Memory, sessions, and credentials are per-machine by design; do not promise seamless continuity that the built-in files cannot deliver.

- Do not put `$HERMES_HOME` (or `state.db`) on a network share; see Pitfalls.

- Routing to `$create-utility` vs a full skill: build the local procedure here; a capability that transfers to another person or agent belongs in the Skills library instead.

## Verification

- `hermes config get skills.external_dirs` on each edge returns the synced path, and `hermes skills list` shows a skill that only exists there.

- `hermes memory status` reports the external provider active on each edge, not `off`.

- The provider can actually answer from stored content: `memory status` showing `available ✓` proves only that the plugin loaded. Ask it something whose answer exists only in a turn you just stored (Honcho: `POST /v3/workspaces/<ws>/peers/<peer>/chat`) and check the synthesized answer reflects it. Confirm ingestion separately by watching the work unit flip to `processed = true`.

- Desktop → Gateways shows every connection with `Reachable` after **Test**.

- Each edge's agent reports its own `hostname`/`whoami` from the `terminal` tool.

## Pitfalls

- **One terminal backend per agent.** `terminal.backend: ssh` does not give a hub agent local-plus-remote; it replaces local with remote. Keep `local` on each edge and let the machines talk as peers.

- **SQLite over a network mount.** `state.db` uses WAL, which is unsafe on NFS/SMB; Hermes forces `journal_mode: delete` for fresh databases there and logs an error for existing WAL ones. Keep `$HERMES_HOME` local per edge — share a synced *folder*, not the home.

- **Built-in memory does not travel.** `MEMORY.md`, `USER.md`, and session search are per-profile files. Expecting "she remembers the other machine" without an external provider produces a confusing half-memory; either enable the provider or state the limitation.

- **A NAS folder is reachable by more than one path.** The same shared folder commonly appears as an NFS mount on the LAN and as a cloud-sync path off it (`~/Library/CloudStorage/<SyncClient>-<share>/...`, or `/sessions/<id>/mnt/...` in hosted sessions). Resolve the path that actually exists on that edge before reporting a file missing; a path that works on the LAN is not evidence it works on the laptop.

- **`git`**** on a network-mounted repo can refuse with "dubious ownership".** Fix with `git config --global --add safe.directory <path>` rather than copying the repo elsewhere.

- **A smoke test of the memory provider writes real memory.** A test turn is not inert: it lands in the provider *and*, through the memory tool, in the local `MEMORY.md`/`USER.md`. Purge both sides before finishing — delete the test sessions on the server (and flush its cache, since a derived representation survives row deletion) and strip the injected lines from the built-in memory files — or the next session starts believing a fabricated fact.

- **"Multi-location agent manager" tools are a different product.** T3 Code and its peers are control surfaces for *coding-agent harnesses* already installed on your machine (Claude Code, Codex, Cursor, Grok Build, OpenCode, Antigravity) — no shared memory, skills, or identity. See `references/edge-inventory.md` before recommending one.

## References

- `references/edge-inventory.md` — the user's actual edges, mounts, existing stack, and the adjacent-tool comparison.

- `references/honcho-selfhost.md` — self-hosting the shared memory provider: compose shape, the migration/embedding-dimension bootstrap, JWT minting, TOML keys, the deriver batching gate, and the Hermes wiring traps.