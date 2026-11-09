---


uuid: 40524dc8-ccd9-81e9-af4c-f265790e3aac
name: docker-fleet-healthcheck
description: "Docker Fleet Healthcheck"
version: 1.4.0
last-used: "2026-10-27"
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
hermes:
tags: [docker, healthcheck, fleet, nas, studio, portainer, maintenance, cron, prune]
category: devops


---


# Docker Fleet Healthcheck

Recurring maintenance over every Docker container on the **Studio** (local Docker) and the **NAS** (Synology, via SSH). Detects unhealthy/exited/restarting containers, backs up their definitions, restarts the broken ones, and reports. Runs weekly as a cron job.

## When to Use

- The scheduled weekly fleet healthcheck fires.

- A container is unhealthy/exited and you need a safe, repeatable recovery routine.

- You need a snapshot of the compose projects/services running across both hosts.

- The user asks to prune Docker resources.

- The user asks to remove, rename, or migrate services between compose stacks (see *Surgery* in `references/destructive-operations.md`).

- A user reports **"I can't reach <service>"** — see `references/diagnosing-unreachable.md`; the app is often healthy behind a dead reverse proxy.

## Access model

A sudoers **NOPASSWD** rule grants passwordless root docker on the NAS (`(root) NOPASSWD: /usr/local/bin/docker, /bin/systemctl`). The socket is root-only (`srw-rw---- root root`), so a plain `docker ...` over SSH fails "permission denied"; always prefix `sudo -n`. Portainer (`http://192.168.2.6:9000`) is a fallback API but not required.

## Always-on rules (user guardrails — never violate)

- **Never remove** containers, images, or volumes. No `docker rm`, no `compose down -v`.

- **Only restart/start** existing containers. Prefer fixing over recreating.

- **Back up** compose files + container definitions before ANY change.

- **Volume data backups** only when recreation is explicitly approved.

- **Never print or store secrets** — redact env values (PASS/SECRET/TOKEN/KEY/CREDENTIAL/API/AUTH/PWD/BEARER).

- **Treat every container as production** — restart with `-t 10`, no long/unnecessary downtime.

- **Less is more** — do not create new containers unless absolutely necessary.

- **Image updates are reported, not auto-applied** — recreation needs explicit human approval.

- Keep the fleet visible: maintain/refresh a compose snapshot every run.

## Procedure

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Snapshot compose.** `docker ps -a --format '{{.Names}}\t{{.Label "com.docker.compose.project"}}\t{{.Label "com.docker.compose.project.config_files"}}'` → copy each project's compose file into a snapshot dir + write a manifest.

1. **Detect per host in ONE call.** `docker ps -a --format '{{.Names}}|{{.State}}|{{.Status}}'` (local plain; NAS via `ssh chdwck9NAS 'sudo -n /usr/local/bin/docker ps -a --format ...'`). Broken = state `restarting`/`dead`, or status contains `unhealthy`, or `exited` with a restart policy other than `no`.

1. **Per broken container:** `inspect` (redacted, saved to disk) → `logs --tail 60` → `restart -t 10` (or `start` if exited) → wait ~7s → re-list the host and re-check.

1. **Report:** per-host checked/restarted/still-bad + actions + a "needs a human" list. Exit non-zero if anything is still bad.

1. **Cron:** script attached, short summary delivered to origin. Set schedule and model with the `hermes cron` CLI — the `cronjob` tool cannot set a job's model/provider, so use `hermes cron edit <id> --model <model> --provider <provider> --pin` to pin the job to a local model (a pinned job does NOT follow `hermes model`). Convert an existing job rather than creating a near-duplicate.

The canonical implementation is deployed at `~/.hermes/scripts/docker_fleet_healthcheck.py` (also shipped as `scripts/docker_fleet_healthcheck.py`).

## Diagnosing "I can't reach <service>"

Check the layers in order — container, local service (curl port on `localhost` AND the host LAN IP), reverse proxy (**nginx-proxy-manager ****`npm`**** on the NAS is the entry point for most published services; check it FIRST**), then client/network (no VPN/tunnel unless configured, so off-network access fails by design). Full checklist (ports, `jellyfin-studio` 13380 note) in `references/diagnosing-unreachable.md`.

## Pitfalls

- **macOS has no ****`timeout`**** binary** — a `timeout ...` probe fails "command not found" and silently does nothing; guard long probes with a python `subprocess.run(..., timeout=N)` or a kill-after-N shell guard.

- **Running the healthcheck is NOT read-only** — it `docker start`s every `exited` container with a restart policy, waking the whole stopped stack; disclose and confirm scope first.

- **A running container can still be unhealthy** — check health status, not just state.

See `references/pitfalls.md` for the full list, `references/destructive-operations.md` for the mass-down signature, stack recovery, rename/recreate/remove surgery, and prune safety, and `references/nas-stack-topology.md` for the project map, ports, and dependencies.