---


uuid: 41324dc8-ccd9-81c0-9eb0-db44c3fa7f72
name: remote-mcp-servers
description: "Publish your own MCP server to [Claude.ai](http://claude.ai/) or ChatGPT."
version: 1.0.0
thinking: "Medium"
temperature: 0.3
author: clarity
license: proprietary
metadata:
hermes:
tags: [mcp, fastmcp, cloudflare-tunnel, api-key, coolify, self-hosted]
related_skills: [coolify-deployments, minimal-webservers, mcp-integration, hermes-services]


---


# Running your own MCP server for [Claude.ai](http://claude.ai/) / ChatGPT

Hosting an MCP server so a hosted assistant can call it is a *deployment* problem with three failure
surfaces that all look alike from the client side: the transport Host header, the edge/WAF, and the
client's own HTTP signature. Work them in that order — a "connection failed" in Claude is almost never
the Python code.

## When to Use

- Publishing a tool/applet server for [Claude.ai](http://claude.ai/) custom connectors or ChatGPT developer-mode connectors.

- Any Streamable-HTTP MCP server that must sit behind a public hostname, an API key, or a tunnel.

- "The MCP server works locally but the connector can't reach it."

## Procedure

1. **Write the server with FastMCP over Streamable HTTP**, stateless so concurrent clients don't fight
over sessions. `templates/fastmcp-key-auth-server.py` is a working, key-authenticated starting point.

1. **Bind the public hostname into the transport-security allow-list** (see pitfalls — this is the 421).

1. **Containerise** (`python:3.12-slim`, `pip install mcp uvicorn`), build the image on the host, and
deploy with `pull_policy: never` if Coolify owns it — see `coolify-deployments`.

1. **Publish through the tunnel** with path routing so one hostname can carry both MCP and a UI:
`- hostname: X, path: ^/(mcp|health)` → MCP port, then a second `- hostname: X` rule → the static
port, then the existing rules, `http_status:404` last. `cloudflared tunnel ingress validate` before
restarting, and `cloudflared tunnel route dns <tunnel> <host>` for the CNAME.

1. **Verify from outside** (never from `127.0.0.1` alone): initialize, `tools/list`, one real write,
then fetch the artefact the write produced over public HTTPS, then fetch a path that must 404.
`scripts/mcp_client_test.py` does the RPC half.

1. **Hand over the connector URL** with the key in it (`https://host/mcp?key=…`) and say plainly that
OAuth was not implemented if it wasn't.

## Auth that actually works with hosted clients

Hosted connectors do not reliably let you paste a static header, and OAuth is a much bigger build.
Accept the key in three places, in this order, and compare with `hmac.compare_digest`:

1. `Authorization: Bearer <key>` (clients and curl)

1. `X-API-Key: <key>`

1. `?key=<key>` on the URL — the pragmatic option that makes [Claude.ai](http://claude.ai/) and ChatGPT work today

Always leave one unauthenticated route (`/health`) for tunnel and container probes, and answer 401 with
the accepted forms — a 401 that explains itself saves a round of debugging.

## Pitfalls

- **421 "Invalid Host header" behind a tunnel is the MCP SDK, not the tunnel.** FastMCP/Streamable HTTP
runs DNS-rebinding protection and only allows `localhost`/`127.0.0.1` by default. Set
`transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=True,<br>  allowed_hosts=["<public host>", "localhost", "127.0.0.1"], allowed_origins=["*"])`. The tell: your
own extra routes answer 200 while every `/mcp` POST returns 421 — which reads as a broken tunnel.

- **Cloudflare error 1010 ****`browser_signature_banned`**** blocks Python UAs.** `python-urllib` and friends
are blocked by a browser-signature rule; curl, browser and `Claude/1.0` UAs pass. Test the same URL
across several user agents before blaming the server, and tell the user the real fix is a WAF skip
rule for that hostname (owner action) — hosted assistants fetch connectors from their own infra and
will not look like a browser.

- **`app.route(...)`**** does not exist on the Starlette app FastMCP returns.** Add your own endpoints with
`app.router.routes.insert(0, Route("/health", handler, methods=["GET"]))`, and add the CORS middleware
*after* the auth middleware so preflight is answered before the key check.

- **A ****`try_files … /index.html`**** fallback makes every probe succeed.** Any URL returns 200, so "the
artefact is live" passes on a page that was never written. Use `try_files $uri $uri/ $uri/index.html<br>  =404;` and serve the index page from `index index.html`, then check a deliberate unknown path.

- **Editing ****`~/.cloudflared/config.yaml`**** needs a restart, and the restart is the dangerous part.**
`launchctl kickstart -k` on the tunnel job can leave it dead (exit 78 / `needs LWCR update`) and
re-`bootstrap` is blocked inside the gateway, which takes every tunnelled host down at once. Validate
the config first, confirm you can restore the job, and if you cannot, run `cloudflared … tunnel run`
as a supervised background process to restore service and flag the re-registration to the user.

- **A push that writes a bind-mounted file is live immediately.** If Coolify also owns the site, trigger
`POST /api/v1/deploy` for the deployment record, but don't tell the user the bytes waited for the
deploy — and don't redeploy the container that is serving the MCP session itself.

- **JSX needs no build step.** Wrap a bare component in React 18 UMD + Babel standalone
(`<script type="text/babel" data-presets="react">`) and append a `createRoot` mount only if the
source doesn't render itself. Verify by screenshot — a syntax error inside Babel renders a blank page
with a console error and still returns HTTP 200.

## Verification checklist

- `POST /mcp` `initialize` → 200 over the public hostname, with and without the key (401 without).

- `tools/list` returns the expected tool set; one write tool returns a URL.

- The written URL returns 200 **and** a neighbour path returns 404.

- Container/service status `running` in Coolify, health path green from outside.

## Files

- `templates/fastmcp-key-auth-server.py` — key-guarded FastMCP server with `/health`, host allow-list
and a shared data volume; copy and fill the tools in.

- `scripts/mcp_client_test.py` — stdlib Streamable-HTTP client: `initialize`, `tools/list`, or a
`tools/call` from the command line.