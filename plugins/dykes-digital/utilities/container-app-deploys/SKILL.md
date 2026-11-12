---


uuid: 41324dc8-ccd9-81ff-9621-d757e1d567c0
name: container-app-deploys
description: "Use when deploying a self-hosted app or stack."
version: 1.0.0
author: clarity
license: proprietary
thinking: "Medium"
temperature: 0.2
metadata:
hermes:
tags: [deploy, compose, docker, dagu, coolify, macos, selfhosted]
related_skills: [media-volume-management, dagu-pipelines]


---


# Container app deploys

Publish and update self-hosted apps on this estate: the Studio (macOS + Docker Desktop) and the NAS.
One contract per app, one deploy path, a trigger that can be handed to a scheduler.

## When to Use

- "Publish / redeploy / update this app or stack."

- Wiring push-to-deploy, a deploy webhook, or a scheduled redeploy.

- Deciding whether a panel (Coolify) can be the deployer on a given host.

## Core principle

**Deploying on macOS needs no root.** Docker Desktop's socket belongs to the login user, so
`docker compose up -d` runs as plain `chdwck9studio`. Tools that demand `sudo` are imposing an
assumption, not a platform requirement — check that before widening privilege anywhere.

## Procedure

1. **Write the contract** at `~/docker/apps/<app>/docker-compose.yaml`, with `.env` (mode 600) beside
it for secrets and `env_file:` in the compose for multi-service stacks. Pin `container_name`, the
published ports, `restart: unless-stopped`, and a `healthcheck:` hitting a real endpoint.

1. **Keep the contract on local disk.** Never on `/Volumes/...`: a scheduler- or API-triggered process
cannot read network mounts (macOS TCC), so an identical deploy works by hand and fails on a trigger.

1. **Add a health route** to the app (`/healthz` returning 200) — it is what the healthcheck, the
proxy and the next reader of the compose file all rely on.

1. **Deploy by script,** not by hand: `bash ~/bin/deploy-app.sh <project> [--pull] [--prune-orphans] [--check]`.
It resolves the local contract first, falls back to `docker compose ls --format json`, runs
`config -q`, then `up -d`, then reports real container state and exits non-zero if anything is not
running.

1. **Trigger it** with the dagu DAG (`deploy-app`):
`curl -X POST 127.0.0.1:8888/api/v1/dags/deploy-app/start -H 'Content-Type: application/json' -d '{"params":"APP=<project> PULL=1"}'`
A DAG-level `max_active_runs: 1` and `catchup_window: ""` are required — two concurrent `up -d` on
one project race, and a deploy that fires hours late is worse than one that never ran.

1. **Verify, then report:** `docker compose -p <project> ps --format json`, `curl -o /dev/null -w '%{http_code}'`
on the health path, and the actual bytes/behaviour of the real page — not the fact that `up` returned 0.

1. **Finish the first-run wizard headless.** A container that answers 200 on `/api/health` is *deployed*,
not *configured*: BI/dashboard tools, wikis, and media servers all sit behind a setup screen until
an admin account exists. Complete the wizard and the app's first data connection over its HTTP API
(`references/first-run-api-bootstrap.md`), then prove it with a real query through the app, not with
the API's 200.

## Rules and pitfalls

- **`up -d`**** starts every service in the file**, including ones deliberately left stopped. Point a
deploy at a project whose dormant services are welcome, or split them into another file.

- **Refuse control-plane projects by name** in the deploy script: the app that manages the daemon,
socket-bridge containers, and any project holding a *different* service's database. Recreating those
takes the control plane down with the deploy.

- **`{{ ... }}`**** never survives a scheduler.** Go-template formats (`docker compose ps --format '{{.Name}}'`)
get eaten by dagu and similar engines; use `--format json` plus a few lines of Python.

- **Stop the old instance before binding its port.** Two deployments of the same app on one port give a
`Bind for 0.0.0.0:<port> failed: port is already allocated` only after the whole build has run.

- **Data an app reads should be a snapshot, not a mount of a live secrets directory.** For a dashboard
reading `~/.hermes/state.db`, export only the tables/columns it needs with `sqlite3 … ATTACH` into a
small copy on a schedule, and mount that read-only.

- **A BI tool never shares a database with the data it analyses.** Give it its own app DB (users,
questions, dashboards) and connect the warehouse as a *read-only* data source: a dedicated login role
with `CONNECT`, `USAGE`, `SELECT` on the schemas it needs, plus `ALTER DEFAULT PRIVILEGES … GRANT<br>  SELECT ON TABLES` so tables created later are readable without a new grant. Never grant `auth`,
`storage` or `vault` schemas — those carry credentials and PII.

- **Report an empty warehouse as empty.** A validated connection to a database with zero user tables is
a real result, not a failure: say so, name the next ingestion step, and do not imply the tool is
populated.

- **Generate app secrets with ****`python3 -c "import secrets…"`**** and append them to the project ****`.env`****
(mode 600); never print the value.** Tell the user the file path and the variable name
(`grep MB_ADMIN_PASSWORD ~/docker/apps/<app>/.env`) — enough to retrieve it, nothing leaked into chat
or into a report.

- **Confirm the ****`.env`**** actually reached the container** instead of trusting compose's lookup
(`docker inspect <ctr> --format '{{range .Config.Env}}{{println .}}{{end}}' | sed -E 's/(PASS|KEY)=.*/\1=<set>/'`).
A password that silently resolved to empty surfaces later as an auth failure that reads like a broken app.

- **A UI panel is not automatically the deployer.** Verify it can complete a deployment on the target
host before promising it — Coolify on this Mac needs four fixes first, see
`references/coolify-localhost-macos.md`.

## Verification

- `dagu history deploy-app` shows a `Succeeded` row for the project.

- `docker compose -p <project> ps` shows the expected containers `running`/`healthy`.

- The published URL returns the real page (status **and** payload size/content), not just 200 from a stub.

## References

- `references/coolify-localhost-macos.md` — making Coolify deploy on a macOS host, and what still breaks.

- `references/first-run-api-bootstrap.md` — configuring a freshly deployed app headless (setup token,
admin account, data source, verification query), with the Metabase/Metabase-DB recipe.