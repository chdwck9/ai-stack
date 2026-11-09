---


name: remote-agent-kickoff
uuid: 40224dc8-ccd9-8179-beb4-c152ffa59108
version: 4
description: "Remote Agent Kickoff"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
author: Hermes Agent
license: MIT
metadata:
hermes:
tags: [agents, orchestration, herdr, t3, ssh, remote]
related_skills: [herdr-agent-runtime, hermes-multi-edge, service-api-mcp-research]


---


# Remote Agent Kickoff

Stand up a **remote control layer** so Clarity can start a coding-agent task on another machine
(Studio or the work laptop) and follow it to `done` or `blocked`. A locked-down laptop —
installers blocked, no OpenRouter — does not block this: the orchestrator never runs there.

## When to Use

- Wiring a remote coding-agent runtime so an orchestrator can start and monitor tasks.

- Choosing between herdr, T3 Code, SSH + headless Claude Code, or Claude Remote Control.

- Installing or operating herdr: host vs client, saved SSH machines, CLI/socket control.

## The model: three layers, never one thing

- **Runtime** — where agents execute (owns terminals/processes). **Control surface** — how your
agent drives it (CLI + socket API, MCP, SSH). **Client** — how a human watches.

- Split **host** (owns the terminals) from **client** (UI or API). Leave the laptop as a client;
install blocklists then stop mattering.

- The transport is *never* the binding constraint — entitlement and data are; ask where the work
tokens and repos live first.

## Step 1 — Confirm the tool exists before comparing it

Verify a named harness from primary sources, never from recall, and say plainly when a name
cannot be verified: GitHub REST (`/search/repositories`), `registry.npmjs.org/<pkg>`,
`pypi.org/pypi/<pkg>/json`, `raw.githubusercontent.com/<owner>/<repo>/<branch>/README.md`
(read the real branch first — often `master`).

## Step 2 — Pick the layer

Short version; full table in `references/harness-options.md`.

- **herdr** — a *runtime*: the server owns real terminals and every UI attaches. CLI + local
socket API returning JSON, semantic agent state (`working/blocked/done/idle`), first-class SSH
machines. Best when an agent must drive it. Ops: `references/herdr-operations.md`.

- **T3 Code** — control-plane app (desktop/web/mobile) with an MCP server.

- **SSH + headless Claude Code** — `ssh <host> 'claude -p "<task>" --output-format json'`.

- **Claude Remote Control** — Anthropic-native, gated by org policy.

- **ACP** standardizes *editor ↔ agent*, not orchestrator → agent. Wrong layer here.

## Step 3 — Preconditions (check before installing)

- **Inbound reach to the task host.** Test `ssh <target>` first. Without it that machine can only
be a *client* — the design changes.

- **Provider auth on the task host.** The agent CLI must be installed and logged in *where the
task runs*: `command -v claude codex pi hermes opencode`.

- **Unattended permissions.** A headless agent stalls on an unanswered approval — set a
permission mode; never blanket-apply `--dangerously-skip-permissions` unattended.

## Step 4 — Install, then verify the surface

- Prefer a package manager over `curl | sh`; else the official installer or binary.

- Start the server to outlive the session: `background=true, persist_on_release=true`.

- Verify with the tool's status command **and a read-only control call** — a running process is
not proof.

- Read-only probes (`list`, `status`, `schema`) are pre-approved; anything that spawns or prompts
an agent is a kickoff and follows Step 5.

## Step 5 — Route and guard

- Route: a work (Mambu) task → the work machine; otherwise the Studio.

- Autonomous execution on a **work** machine is human-impacting: hold at the approval gate unless
the user grants a **scoped standing authorization**, and state that scope.

- Prepare the exact command; confirm before anything that edits repos or sends messages.

## Pitfalls

- A *runtime* survives its client closing; a *control-plane app* loses work when its UI closes.

- A detached runtime restores layout after a restart but **not** the original processes.

- macOS ships no `timeout` binary — over SSH it fails with `command not found` and the wrapped
command never runs. Use the tool's own `--timeout`.

- `~/.claude/skills` on a remote is often a symlink into a shared brain — writing there publishes
to every machine sharing that folder.

- A remote agent's login can be near expiry; note it at kickoff so a stall is diagnosable.

## Report shape

Verdict first (works / doesn't; substitution or addition), then the deciding tradeoff, then what
to verify — one recommendation, not a menu.

## References

- `references/herdr-operations.md` — herdr install, host vs client, machines, CLI/socket API, the
verified Studio → work-laptop kickoff recipe.

- `references/harness-options.md` — decision table across herdr / T3 / SSH+headless / Remote Control.

- `claude-code` (autonomous-ai-agents) overlaps on the SSH+headless path.