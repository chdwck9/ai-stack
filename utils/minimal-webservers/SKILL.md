---


name: minimal-webservers
version: 1
description: "Wrap scripts/tools into stdlib HTTP endpoints for demos."
thinking: Low
temperature: 0.3
author: clarity
license: proprietary
metadata:
hermes:
tags: [webservers, cli-tools, containers, packaging, http]


---


# Minimal Web Servers

When the user wants a simple HTTP-facing view/dashboard wrapped around an existing
script or data source — without installing frameworks or dependencies.

## When to Use

Phrases like "expose it as a web endpoint", "demo on a port", "stand up a page",
or dashboard/applet deployment requests.

Covers: wrapping CLI reports, status pages, health checks, admin consoles.

## Procedure

### 1. Assess scope — stdlib or framework?

- Single GET endpoint + refresh → `http.server` (stdlib)

- JSON APIs, POST, auth, concurrency → FastAPI + uvicorn

- Templates/static assets → FastHTML / Jinja + Flask

- Default: stdlib unless explicit feature request beyond its capability.

### 2. Build the handler

Use `BaseHTTPRequestHandler` (not `SimpleHTTPRequestHandler`) for full route control.
Handle `/`, `/refresh` routes manually. Set `Content-Type` explicitly.

### 3. Cache strategy

First request (or TTL expiry): run underlying command, save output to file.
Subsequent reads from cache. Avoids API hammering during demos, instant response times.
Default CACHE_TTL = 300 seconds.

### 4. Containerize

- COPY all needed scripts INSIDE the image — don't rely on host paths inside container.

- Fallback path logic in script: prefer container path, fall back to host path on bare run.

- Mount state/credentials as volumes (`~/docker/volumes/<name>:/root/.hermes:ro`).

- Connect to shared network (e.g., `edge-net`) for cross-service visibility.

- Only expose ports the user explicitly needs externally.

### 5. Register in Coolify (if applicable)

1. Open Coolify UI (`http://localhost:7810`).

1. Add Project → New.

1. Add Application → **Simple** deploy type.

1. Source: select **Docker Image** → enter image name.

1. Port: set mapped port. Network: choose shared network (`edge-net`).

1. Volumes: bind-mount state/credentials dirs.

1. Save & deploy.

## Pitfalls

- **Directory listing over content**: `SimpleHTTPRequestHandler` serves indexes instead of generated HTML when no file exists. Use `BaseHTTPRequestHandler` for manual route handling.

- **PATH resolution**: `~/.hermes/scripts/script.py` resolves on the HOST not inside container. Either COPY it into the image OR mount the entire parent dir as a volume.

- **Port conflicts**: Check `lsof -iTCP:<port>` before binding. Docker maps host ports even if nothing listens yet.

- **.env key lookup in container**: Scripts reading `~/.hermes/.env` need the dir mounted as volume inside container, not individual env vars.

- **Coolify networks**: Coolify manages its own network (`coolify`). Services on `edge-net` are reachable from Tailscale hosts and LAN. Apps registered in Coolify join their own network but can attach to `edge-net` for cross-service access.