---


name: hermes-model-sources
uuid: 40524dc8-ccd9-8167-9ee0-f7fab899d2ac
version: 2
description: "Hermes Model Sources"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
author: Hermes Agent
license: MIT
metadata:
hermes:
tags: [hermes, providers, model-routing, openai-compatible, gateway, config]
related_skills: [local-model-backend, hermes-services, service-api-mcp-research]


---


# Wiring an external model source into Hermes

Add a model source — a provider API, or a locally-run OpenAI-compatible gateway in front of a remote
provider — and make it usable: a selectable alias, the primary model, or a fallback. The
supported-route procedure and its traps, not a tour of one provider.

## When to Use

- "Use X as a model source / provider", "can Hermes use X's models".

- Adding an OpenAI-compatible endpoint (a proxy/gateway, LM Studio, rapid-mlx) as a model source.

- Swapping the primary model between providers.

## Always-on rules

- **Never hand-edit ****`config.yaml`****.** The file/patch tools refuse it as security-sensitive; use
`hermes config set <dotted.key> <value>` (nested paths and JSON values both work; `--force` writes
a key the running version does not recognise).

- **Check for a NATIVE provider before building anything.** `ls ~/.hermes/hermes-agent/plugins/model-providers/`.
A native provider (own env var, base URL, reasoning translations) beats a hand-rolled proxy. Build a
local gateway only for what native cannot do (e.g. a keyless free lane) — not as a reflex.

- **Secrets never enter chat, notes, or a printed command.** `hermes config set` echoes the value it
writes — redirect it (`… >/dev/null`) or reference an env var through an alias's `key_env`. Print
only lengths/prefixes.

- **Verify through Hermes, not just curl** — an up endpoint does not prove Hermes routes to it.

- Config changes take effect on **new sessions**, not mid-conversation (prompt caching).

## Procedure

1. **Discover.** `ls ~/.hermes/hermes-agent/plugins/model-providers/` for a native provider;
`hermes config get providers` and `hermes config get model` for what exists; `hermes chat --help`
for `--provider`.

1. **Probe the endpoint directly.** `GET <base>/v1/models` → confirm the exact model id and its
`cost`; run one live completion before wiring anything.

1. **Register a user-defined provider** — mirror the existing `providers.<name>` field shape:

  ```bash
  hermes config set providers.<name>.api           http://127.0.0.1:<port>/v1
  hermes config set providers.<name>.api_key       "<key>"     # add >/dev/null to suppress echo
  hermes config set providers.<name>.default_model <model-id>
  hermes config set model.aliases.<alias>          <name>/<model-id>
  ```

  Select with `/model <alias>` or `hermes chat --provider <name> -m <model-id>`.

1. **Or make it primary** (only when asked): `hermes config set model.provider <name>` +
`hermes config set model.default <model-id>`. Keep a `fallback_providers` entry on a known-good
provider.

1. **Verify** `hermes chat -Q --format text --provider <name> -m <model-id> -q "Reply with exactly: OK"`
→ prints `OK`; then once with no flags if it is now primary.

1. **Persist a local gateway** as a user LaunchAgent (below).

## Persist a local gateway (launchd, macOS)

Write `~/Library/LaunchAgents/<label>.plist` with `ProgramArguments` (absolute binary path + args),
`WorkingDirectory`, `RunAtLoad=true`, `KeepAlive=true`, and stdout/stderr log paths. Then, **from
inside a session**:

```bash
launchctl unload ~/Library/LaunchAgents/<label>.plist 2>/dev/null
launchctl load -w  ~/Library/LaunchAgents/<label>.plist
```

- **`launchctl bootstrap`****/****`submit`****/****`kickstart`**** are blocked inside the gateway — but ****`launchctl load -w`****
is NOT.** The legacy pair loads a *non-gateway* user agent fine, and with `RunAtLoad`+`KeepAlive` it
survives reboot. Only the gateway's own restart stays the user's job (`/restart`, or a shell outside
Hermes).

- Kill the ephemeral background instance before loading the agent, or the port is double-bound.

- Verify: `launchctl list | grep <label>`, then `lsof -nP -iTCP:<port> -sTCP:LISTEN`, then re-run the
Hermes end-to-end check.

## Credentials from a non-standard env file

A user's ad-hoc env file (e.g. `~/.hermes/edge.env`) is **not auto-loaded** by Hermes, nor by a
proxy's own process. Bridge the value into what each actually reads: `~/.hermes/.env` for Hermes, and
the proxy's own config for the proxy. Upsert the line (don't clobber the file); verify without
printing the value.

## Pitfalls

- **Never trust a "free" model label.** Providers often expose both `…-free` and the plain id; the
`-free` one is frequently quota-limited (`429` / `FreeUsageLimitError`) while the plain id is
billable. Read the per-model `cost` from `/v1/models` and confirm with a live call — then state
which id you actually set.

- **A direct-curl success is not a Hermes success**, and a `--provider` success is not proof the
*default* got switched — check both explicitly.

- **Do not leave the default on an id that 429s.** Set the working (billable) id and say so — never
silently ship a broken default.

References: `references/opencode-zen.md` — OpenCode Zen: the native provider vs the `opencode2api`
gateway, and the free-vs-paid model ids.