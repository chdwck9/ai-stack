---


uuid: 40524dc8-ccd9-8133-9b88-d6a6f17886f1
name: mcp-server-onboarding
description: "MCP Server Onboarding"
version: 1.2.0
last-used: "2026-10-27"
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
hermes:
tags: [mcp, oauth, config, verification, connectors]
category: productivity


---


# MCP server onboarding

Taking an MCP server from "the provider gave me a URL or a launch command" to "Clarity can call its tools and I have proved it returns real data": config write, auth hand-off, in-session verification. Hosted (URL + OAuth) servers take the Steps path; **stdio** (command-launched) servers take the section below. Provider-specific OAuth failures (CIMD vs DCR, pre-registered clients, WAF blocks) belong to `mcp-oauth-setup`.

## When to Use

- Richard says "connect to <service>" for something that ships an MCP endpoint — hosted/OAuth or a stdio launch command.

- A configured MCP shows `✗ disabled`, `401 Unauthorized`, or zero tools.

- After re-auth: proving an existing connection still returns data, not just `Connected`.

## Catalog first

Before hand-wiring anything (cloudflared routes, raw DNS, bespoke OAuth scripts) run `hermes mcp catalog` and `hermes mcp list`. A Nous-approved entry means `hermes mcp install <name>` (then `hermes mcp login <name>`) *is* the integration; hand-plumbing is the fallback.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Discover the provider and read its auth metadata first** — MCP vs API pages, plan gates, key-vs-OAuth, tool list, `.well-known` auth metadata (see `references/discovery.md`).

1. **Do not rely on ****`hermes mcp add`**** from an agent session.** It aborts the OAuth step (`non-interactive environment and no cached tokens found`), then defaults the `Save config anyway? [y/N]` prompt — nothing is written and the probe fails `401`. Write the entry directly:

  ```bash
  cd ~/.hermes && cp config.yaml config.yaml.bak-<name>
  hermes config set mcp_servers.<name>.url https://<host>/mcp
  hermes config set mcp_servers.<name>.auth oauth
  hermes config set mcp_servers.<name>.oauth.cimd false
  hermes config set mcp_servers.<name>.oauth.redirect_port 27893
  hermes config set mcp_servers.<name>.enabled true
  ```

  The agent's patch/write tools refuse `~/.hermes/config.yaml` by design; `hermes config set` is the sanctioned write. Use a free port inside **27890-27894** (Hermes' callback range).

1. **Start with DCR, escalate only on evidence.** `oauth.cimd: false` lets Hermes register dynamically (most hosts accept it); add a manual `client_id` only after DCR or the authorize/token endpoint rejects it.

1. **Hand consent to Richard, but keep the flow alive.** Run `hermes mcp login <name>` as a pty background process (`pty=true, background=true`) — it prints the authorize URL *and opens his default browser*, then blocks on the loopback callback (`127.0.0.1:<port>/callback` — no paste needed). Poll (`process_manage action=poll`) for `✓ Authenticated — N tool(s) available`. Never type or ask for his credentials.

1. **Verify two ways:** `hermes mcp test <name>` → `✓ Connected`, transport, auth type, tool list; plus one real **read-only** call via `scripts/mcp_smoke_test.py <name> <read_tool>` (server tools aren't in the agent toolset until a new session).

1. **Establish identity and ceiling.** Call an identity tool (`get_account_info`, `whoami`, `list_workspaces`): the browser session may be in a different account/workspace, and free/paid plans silently change visible data. Report the limit as a fact.

1. **Close the loop in the record that owns the task.** Update it (status + a connection block: endpoint, auth mode, port, verified identity, plan ceiling, how to re-auth) and read it back. State that `/reload-mcp` or a new session is needed before Clarity can use the tools.

## Stdio (command) servers

A stdio server launches as a subprocess: no URL, no OAuth, no callback port — non-interactive and agent-safe. The Steps 2 `config.yaml` route is hosted-only; **do not use it here.** Full loop (launch contract, `hermes mcp add --command … --args …`, version pinning, reconnect, smoke test) in `references/stdio-servers.md`.

## Verification

Done means all four hold: `hermes mcp test <name>` connects and lists tools; the smoke test returns real content from a read tool; the identity tool reports the intended account/workspace; the task record carries the connection block, read back after writing.

## Pitfalls

- **`hermes mcp add`**** in an agent session looks like it worked** — it prints the failure, prompts, and exits without saving; check `hermes mcp list` / grep the config first.

- **`✓ Connected`**** is not proof of data** — discovery succeeds against an empty account, wrong workspace, or free plan; always run a read call and the identity tool first.

See `references/pitfalls.md` for the rest (session-start tool binding, pty login, vendor installers, `oauth.scope` precedence, scope/WAF blocks, unauthenticated discovery); `references/granola.md` for Granola.