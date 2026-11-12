---


uuid: 41324dc8-ccd9-8176-9760-d8f069a885f0
name: studio-app-deployment
description: "Use when deploying an app onto the Studio's Docker stack."
version: 1.0.0
author: clarity
license: proprietary
thinking: "Medium"
temperature: 0.3
metadata:
hermes:
tags: [docker, deploy, compose, coolify, dagu, macos, selfhosted]
related_skills: [dagu-pipelines, docker-management, minimal-webservers]


---


# Deploying apps on the Studio

One question decides everything here: **which process runs ****`docker compose`****, and can it read the
files?** Get that right and deployment is a five-second script; get it wrong and you spend an hour
fighting macOS permission models.

## When to Use

- Publishing a new app/service on the Studio (or the NAS) into the existing Docker estate.

- "Deploy this on Coolify" / "stand this up on a port" / "make it restart on reboot".

- A deploy that fails on permissions, ports, or a path the runner cannot read.

## Core rules (apply to every deploy)

- **A deploy contract is a compose file plus ****`.env`****, on LOCAL disk.** `~/docker/apps/<app>/` with
`docker-compose.yaml`, `.env` (600), and any build context. Never point the deployer at
`/Volumes/...`: launchd-spawned runners (Dagu's API-triggered runs, Coolify's jobs) are refused
network volumes by macOS, while an interactive shell is not — so the same DAG passes from your
terminal and fails on a trigger. Details: `references/dagu-http-trigger.md`.

- **Deploying needs no root.** On macOS with Docker Desktop the daemon socket is owned by the login
user, so `docker compose up -d` as yourself is enough. Any tool that demands sudo is demanding it by
design, not by necessity — Coolify prefixes `sudo` to every SSH command for a non-root user.

- **Never deploy the control plane from a trigger.** Keep a protected-prefix list in the deploy script
(`coolify`, `portainer*`, `supabase`, `studio-management`) and refuse by name. Coolify's own
Postgres is the supabase stack's `supabase-db` on this estate, so recreating supabase takes Coolify
down with it.

- **Every published port must be checked first.** A deploy that fails with `Bind for 0.0.0.0:PORT<br>  failed: port is already allocated` has already built and started — the port is the whole failure.
Check the port before deploying, and prefer `ports_mappings` over a proxy when the app is LAN-only.

- **Verify by hitting the app, not by reading the deploy exit code.** `curl -s -o /dev/null -w<br>  '%{http_code}' :PORT/healthz` plus a page-size/content check. Give every app a `/healthz` route —
Coolify and compose healthchecks both need one.

- **Secrets go in ****`.env`**** on the host, never in the image or the compose file's literals.** Pass them by
variable reference (`OPENROUTER_API_KEY=${OPENROUTER_API_KEY}`), and prefer env vars over mounting a
home directory into a container: a web app with `~/.hermes` mounted can read `.env` and every token
in it. Snapshot the one database it needs instead (see `references/dagu-http-trigger.md`).

## Procedure

1. **Locate the source.** A git checkout of the app, ideally already pushed to a repo — Coolify can
only clone from git (`file://` is rejected outright, `https`/`ssh`/`git://` only).

1. **Write the contract** at `~/docker/apps/<app>/docker-compose.yaml`: image or `build.context`, the
port mapping, `env_file`/`environment` from `.env`, volumes, `restart: unless-stopped`, and a
healthcheck. `templates/docker-compose.app.yaml` is the shape.

1. **Validate, then deploy** with `~/bin/deploy-app.sh <app> [--pull] [--check]<br>   [--prune-orphans]` (`scripts/deploy-app.sh` here is the same file). `--check` resolves the compose
project from `docker compose ls --format json`, validates config and prints the plan without
touching anything.

1. **Deploy via Dagu** when you want a trigger: `POST /api/v1/dags/deploy-app/start` with
`{"params":"APP=<app>"}`. The DAG runs `validate` then `deploy`, `max_active_runs: 1`,
`catchup_window: ""` (a late deploy is worse than none), one retry. Never trust the 200 — read
`dagu history` and the run log.

1. **Deploy via Coolify** only if the panel is wanted: `references/coolify-on-macos.md` has the whole
chain (API token, app creation, deploy + poll, and the four host fixes macOS needs).

1. **Report**: URL and port, what was verified (health + page content), what is protected, and how to
reverse whatever you stopped or replaced.

## Pitfalls

- **`docker compose ls`**** reports the path a project was CREATED with, so it keeps pointing at an old
(even NFS) compose file after you move the contract.** Prefer a local contract by convention
(`~/docker/apps/<app>/`) over trusting the live engine's `ConfigFiles`, and log which file was used.

- **`up -d`**** brings up every service in the file, not just the one you were looking at.** A compose
file with four services where one runs will start the other three on the first deploy. Diff the
service list against `docker ps` before you deploy, and say so when it happens.

- **A compose file that uses relative paths (****`build: ./svc`****, ****`./volumes/...`****) cannot be copied without
its context.** Move the whole directory, or the build/volume paths silently break.

- **Do not ****`docker compose up`**** a stack whose compose file lives on an unstable NFS mount.** Rewrites,
`git` operations and reads fail mid-command with `Device not configured` / `getcwd` errors; work on a
local clone and treat the share copy as a mirror.

- **Coolify on macOS is a special case, not a normal target.** `/data/coolify` is hardcoded in its
helpers and macOS's root volume is read-only, so it can never deploy without a patch. Read
`references/coolify-on-macos.md` before promising a Coolify deploy on this hardware.

- **A "validated" panel is not a working deployer.** Coolify's full `ValidateServer` is Linux-only
(`/etc/os-release`) and its real gate for deploys is `validateDockerEngine()` +
`validateDockerCompose()`. Prove deployment by deploying, then hitting the port.