---


uuid: 41324dc8-ccd9-8136-a0da-f575617984fc
name: selfhosted-app-deployment
version: 1
description: "Use when deploying an app on the Studio or NAS."
thinking: "Medium"
temperature: 0.3
author: Clarity
license: proprietary
metadata:
hermes:
tags: [deploy, docker, compose, dagu, coolify, studio, nas]
related_skills: [dagu-pipelines, docker-management, minimal-webservers]


---


# Deploying apps on the estate

One contract, two engines. Get the contract right and the engine is a detail.

## When to Use

- Publishing a new app, or redeploying an existing compose project, on the Studio (Docker Desktop) or
the NAS.

- Someone asks "can Coolify deploy this?" or "make a trigger for deploys".

- A deploy "succeeded" but the container is old, missing services, or on the wrong port.

## The deploy contract (do this first)

Every app gets `~/docker/apps/<project>/` on **local disk**:

```javascript
~/docker/apps/<project>/docker-compose.yaml   # authoritative; lives on local disk, git-tracked
~/docker/apps/<project>/.env                  # 600; secrets never in the compose file
~/docker/apps/<project>/data/                 # host data the container mounts read-only or rw
```

Why local disk is not negotiable: a DAG run started by the scheduler or the HTTP API runs under
launchd, and macOS TCC refuses it any network mount (`ls /Volumes/<share>` fails, `open ...: operation<br>not permitted`). A compose file on the SMB/NFS share deploys fine by hand and *never* by trigger.

Deploy with `bash ~/bin/deploy-app.sh <project> [--pull] [--prune-orphans] [--check]`:

- resolves `<project>` from `docker compose ls --format json` when no local contract exists, and
prefers `~/docker/apps/<project>/` when it does;

- validates config, pulls, `up -d`, then reports what is **actually** running and exits non-zero if any
service is not;

- refuses `coolify`, `portainer*`, `supabase`, `studio-management` by name. `supabase` is in that list
because Coolify's own Postgres is `DB_HOST=supabase-db` — recreating that project takes the control
plane down with it.

Docker Desktop's socket is owned by the login user, so **this path needs no root at all**. Keep it that
way; reach for Coolify only when you want its UI, history or webhooks.

## Triggering a deploy (Dagu)

DAG `deploy-app` wraps the script; params `APP`, `PULL`, `PRUNE`. Two ways in:

```bash
dagu start deploy-app -- APP=ai-usage PULL=1
curl -X POST 127.0.0.1:8888/api/v1/dags/deploy-app/start \
     -H 'Content-Type: application/json' -H 'Accept: application/json' \
     -d '{"params":"APP=ai-usage"}'
```

- The endpoint is `/api/v1/dags/<name>/start`; `/api/v1/dags/<name>` is **405**.

- The POST **requires a JSON body even when empty** — `-d '{}'`, or the API answers
`400 Invalid request body`.

- Declare params as rich definitions (`- name: APP` / `required: true`), not a bare `params: "APP PULL=0"`
string; bare names are rejected at load time (`unknown parameter(s)`).

- A `run:` block is a Go template: `{{ ... }}` is dagu's syntax, not the tool's, so
`docker compose ps --format '{{.Name}}'` breaks with `format value ... could not be parsed`. Ask for
`--format json` and parse it in the script instead.

- Verify with `dagu history deploy-app`, not the HTTP 200 — a queued run can still fail.

## Coolify as the other engine

Coolify deploys over SSH and prefixes `sudo` on every remote command whenever the SSH user is not
literally `root`, so on a machine with password sudo it can only work as a root SSH target. Full chain,
including what to patch when upstream hardcodes `/data/coolify`:
`references/coolify-on-docker-desktop.md`.

## Pitfalls

- **`docker compose up -d`**** starts every service in the file, not just the running ones.** Deploying a
file whose other services were intentionally stopped silently brings them back (a media file went
from one container to four). Read the file before you deploy it, and say what will come up.

- **Changing the compose file's path recreates containers.** Compose records the config path in a
label, so moving a project from the share to `~/docker/apps/` forces a one-time recreate of every
service in it. Warn before you move, not after.

- **Check the port before the second deployer runs.** Two deploy paths for one app collide with
`Bind for 0.0.0.0:<port> failed: port is already allocated`, which reads like a broken deploy. Decide
which path is canonical and retire the other, or give one a different host port.

- **Never mount ****`~/.hermes`**** into an app container** to give it data. It hands a web app `.env`,
`mcp-tokens/` and every credential. Build a compact snapshot of the one or two tables it needs
(a 184 MB live SQLite became a 144 KB copy) and refresh it from a DAG.

- **Kill the ad-hoc copy before publishing the container.** A stray `python3 app.py` holding the port
makes the container fail to bind; find it with `lsof -nP -iTCP:<port> -sTCP:LISTEN` and say which PID
you stopped.

- **A protected-by-name guard is only useful if the list is honest** — add a project the moment it
becomes infrastructure for something else.