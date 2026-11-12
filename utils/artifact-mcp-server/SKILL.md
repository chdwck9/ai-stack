---


uuid: 41324dc8-ccd9-81b2-b8fd-d95f691ba0c5
name: artifact-mcp-server
description: "Use when pushing artifacts to [artifacts.dykes.digital](http://artifacts.dykes.digital/)."
version: 1.0.0
thinking: "Medium"
temperature: 0.2
author: clarity
license: proprietary
metadata:
hermes:
tags: [mcp, artifacts, coolify, cloudflare, react, jsx]
related_skills: [coolify-deployments, minimal-webservers, hermes-public-backend-exposure]


---


# Artifact MCP server ([artifacts.dykes.digital](http://artifacts.dykes.digital/))

A public Streamable-HTTP MCP server that lets a chat client publish HTML or JSX applets to a
Coolify-managed static site, plus an authenticated REST/paste fallback for plans that cannot add
connectors. Read this before changing the service, the tunnel route, or the JSX wrapper.

## Where it lives

- Code (local disk, not the NAS): `~/docker/apps/artifacts/` — `server.py`, `publish.html`,
`Dockerfile`, `nginx.conf`, `compose-site.yaml`, `scripts/`.

- Data volume: `~/docker/volumes/artifacts/{site,meta,versions,trash,conf}`.
`site/` is served, `versions/` archives every previous render, `trash/` holds deletes
(both reversible), `conf/` holds the nginx conf (mounted as a **directory**).

- Coolify services (project `ai-usage-dashboard`, server `localhost`): `artifacts-site`
(nginx :7861) and `artifacts-mcp` (image `artifacts-mcp:latest`, :7860). UUIDs in
`~/.hermes/artifacts-services.json`. API key in `~/.hermes/artifacts.env` (600,
`ARTIFACTS_API_KEY`) and mirrored into the mcp service env vars.

- Cloudflare tunnel ingress: `^/(mcp|health|api)` -> 7860, catch-all -> 7861 on
`artifacts.dykes.digital`.

## Surfaces

Key is accepted as `Authorization: Bearer`, `X-API-Key`, or `?key=` (query form is what
[claude.ai/ChatGPT](http://claude.ai/ChatGPT) connectors need — neither supports a static bearer token).

## Pitfalls that cost real time

1. **Pin ****`@babel/standalone@7`****.** Babel 8's preset-react defaults to the *automatic* runtime and
emits `import { jsx } from "react/jsx-runtime"`, a hard SyntaxError inside a plain
`<script type="text/babel">`. Babel 7 keeps the classic runtime (`React.createElement`).

1. **Auto-mount must live *****inside***** the babel script.** A separate plain `<script>` after the babel
block runs before standalone has transpiled it, so `App` is undefined.

1. **FastMCP returns 421 "Invalid Host header"** for any public hostname until you pass
`TransportSecuritySettings(allowed_hosts=[...], allowed_origins=["*"])` to `FastMCP(...)`
(defaults only allow [localhost](http://localhost/)).

1. **Coolify service creation** is `POST /api/v1/services` with `docker_compose_raw` (base64) and
**no** `type` field; `type` + `docker_compose_raw` together is a 422. Deploy is
`POST /api/v1/deploy {"uuid": …}` (GET returns post_required/405).

1. **`pull_policy: never`**** requires the image to already exist on the host.** Coolify will not pull;
a missing `nginx:1.27-alpine` fails with "No such image" and the service sits `exited`.

1. **Docker Desktop rejects a single-file bind mount** (`…/nginx.conf:/etc/nginx/conf.d/default.conf`)
with "not a directory", and silently creates the path as a directory. Mount a directory.

1. **Two services, not one compose.** Auto-deploy on push targets the *site* service so the mcp
container is never recreated mid-request; one compose would kill the MCP session.

1. **Cloudflare Error 1010 (****`browser_signature_banned`****)** blocks Python user agents here —
`python-urllib`, probably `python-httpx` (what a connector proxy may use). curl/browser/`Claude-*`
pass. Fix with a WAF skip rule for `http.host eq "artifacts.dykes.digital"`; the tunnel cert.pem
token can read `/zones` but is not a usable API token for WAF writes.

1. **psql does not interpolate ****`:'pw'`**** inside a ****`DO $$ … $$`**** block.** Use
`SELECT format('CREATE ROLE %I LOGIN PASSWORD %L', 'x', :'pw') \gexec` at top level instead.

1. **Coolify ****`pull_policy: never`**** also applies to base images you add later.** Pull them on the host
first; a missing image leaves the service `exited` with "No such image" in laravel.log — the UI
shows nothing useful.

1. **The Cloudflare 1010 block hits any Python UA**, so `scripts/mcp_client_test.py` sends its own
`User-Agent`; without one, every smoke test returns 403 and looks like an auth failure.

1. **The nginx ****`try_files`**** fallback must end in ****`=404`****.** Falling back to `/index.html` makes every
typo'd slug return the gallery with 200 and hides broken links.

## Warehouse + resource tools (v1.1)

- Schema `artifacts` in the Supabase Postgres (`supabase-db`), reached over **`edge-net`** — the mcp
container must join that external network (`networks: [edge-net]`) or use `host.docker.internal`
only for Coolify, not for PG. Roles `artifacts_rw` / `artifacts_ro`; DSNs in
`~/.hermes/artifacts.env`, mirrored as shown-once Coolify env vars. Re-apply with
`scripts/warehouse_init.py` (idempotent, rotates the password).

- Tables: `apps`, `versions`, `deployments`, `events`, view `registry`. Push/update/delete mirror into
them best-effort — a DB outage must never fail a publish.

- `deploy_stack(name, compose)` creates a Coolify *service* from compose (same
`POST /api/v1/services` + base64 `docker_compose_raw` path as `scripts/coolify_setup.py`), records a
`deployments` row, then deploys. `update_stack`, `application_status`, `application_action`
(restart/start/stop), `delete_application(confirm=true, protected-name guard)`.

- `about()` is the self-description tool: server/render/schema versions, Coolify version, PG version,
endpoints, tool list. Update `VERSION` / `RENDER_VERSION` there when behaviour changes.

- `query_warehouse` is read-only: single statement, must start `SELECT`/`WITH`, write verbs rejected,
`SET LOCAL statement_timeout = '5s'`, rows wrapped in `SELECT * FROM (…) LIMIT n`.

## Changing the server

Build **before** deploy: the compose pins `artifacts-mcp:latest` with `pull_policy: never`.

```bash
cd ~/docker/apps/artifacts && docker build -t artifacts-mcp:latest .
cd scripts && python3 coolify_env.py          # deploys both services
```

`scripts/coolify_compose.py <site|mcp> <compose-file>` patches a service's compose;
`scripts/mcp_client_test.py <base> <key> [tool] [json]` is the smoke-test client;
`scripts/coolify_setup.py` creates the services from scratch.

## Verification

- `POST /mcp` with the key returns 200 and an SSE `initialize` result; without a key, 401.

- A pushed artifact returns 200 at `/<slug>/`; a nonsense slug returns 404.

- JSX: fetch the page, extract the babel block, transpile with `@babel/standalone@7`, run against
stubs — output must contain no `import` and the mount must fire.

- Coolify shows a fresh deployment for `artifacts-site` per push.

## Related

`coolify-deployments` (service/API mechanics), `minimal-webservers` (why BaseHTTPRequestHandler vs
FastAPI), `hermes-public-backend-exposure` (tunnel + hostname exposure rules).