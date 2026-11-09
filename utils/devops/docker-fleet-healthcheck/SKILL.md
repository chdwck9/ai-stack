---
name: docker-fleet-healthcheck
description: "Weekly Docker fleet healthcheck: Studio + NAS containers."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [docker, healthcheck, portainer, nas, studio, maintenance, cron]
    category: devops
---

# Docker Fleet Healthcheck

Weekly maintenance pass over every Docker container on the **Studio** (local Docker) and the **NAS** (via the Portainer API). Detects unhealthy/exited/restarting containers, backs up their definitions, restarts them, and writes a report. Runs as a cron job Friday 00:00.

## When to Use

- The scheduled weekly fleet healthcheck fires.
- A container is reported unhealthy/exited and you need a safe, repeatable recovery routine.
- You need a snapshot of what compose projects and services are running across both hosts.

## Hard guardrails (never violate)

- **Never remove** containers, images, or volumes. No `docker rm`, no `docker compose down -v`.
- **Only restart/start** existing containers. Prefer fixing over recreating.
- **Back up** compose files + container definitions before ANY change (script does this).
- **Volume data backups** only when recreation is explicitly allowed (`--allow-recreate`).
- **Never print or store secrets** (env values are redacted on capture).
- **Treat every container as production** — no long, unnecessary downtime; restart with `-t 10`.
- **Less is more** — do not create new containers unless absolutely necessary.
- **Image updates are reported, never auto-applied** — recreation/upgrade needs explicit human approval.

## Access model

| Host | Method | Notes |
|---|---|---|
| **Studio** | local `docker` CLI | Docker Desktop socket, works directly. |
| **NAS** | Portainer API (`PORTAINER_URL` + `PORTAINER_API_TOKEN` in `~/.hermes/.env`) | Synology Docker socket needs root; SSH `sudo` needs a password, so Portainer API is the automation path. |

If `PORTAINER_API_TOKEN` is empty the script **skips the NAS gracefully** and reports it. Create a token in Portainer: **My account → Access tokens → Add access token**, then put it in `.env`.

## Procedure

Run:
```bash
python3 ~/.hermes/scripts/docker_fleet_healthcheck.py --mode weekly
```
The script:
1. Snapshots every compose project's file + service manifest to `~/.hermes/docker-healthcheck/compose/`.
2. Checks Studio containers; for each broken one backs up `docker inspect` (redacted) and logs, then `docker restart -t 10` (or `start` if exited), re-checks.
3. Checks NAS containers via Portainer; restarts broken ones the same way.
4. Writes a JSON + Markdown report to `~/.hermes/docker-healthcheck/reports/<run_id>.md`.
5. Exit code `0` = all healthy/fixed; `2` = issues remain needing a human.

Then deliver a **short** summary: what was checked, what was restarted, and anything still broken. Do not remove anything. Flag image updates for approval.

### Escalation (only with human approval)

If a container keeps crashing after restart, do NOT recreate it blind. In the report, list the container, its log tail, and the recommended fix. Only then, with explicit approval, back up volumes first (transient helper container: `docker run --rm -v <vol>:/data -v <backupdir>:/backup alpine tar czf /backup/<vol>.tgz -C /data .`) and recreate from the compose file.

## Pitfalls

- **`docker inspect` env values** carry credentials; always redact keys matching PASS/SECRET/TOKEN/KEY/CREDENTIAL/API/AUTH/PWD/BEARER before saving.
- **SMB-mounted compose paths** (`/Volumes/Live/@Edge/...`) can hang on `find`/`grep`; read specific files, don't recurse broadly.
- A container can be `running` yet `unhealthy` — check the health status, not just the state.
- Restarting a healthy container is churn; only touch broken ones.
- The NAS Docker socket is root-only (`srw-rw---- root root`); do not waste time on `docker` over SSH without sudo.

## Output

A compact report: hosts checked, containers checked, containers restarted, and `Needs a human` items. Saved to `~/.hermes/docker-healthcheck/reports/`. Delivered by the weekly cron.
