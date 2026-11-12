---


uuid: 41324dc8-ccd9-8109-8b79-e20007656d42
name: self-hosted-app-deployment
description: "Use when deploying a self-hosted app or its deploy path."
version: 1.0.0
author: clarity
license: proprietary
thinking: "Medium"
temperature: 0.3
metadata:
hermes:
tags: [deploy, docker, compose, coolify, dagu, ci, root, macos]
related_skills: [docker-management, dagu-pipelines, hermes-services]


---


# Self-hosted app deployment

One deploy path per app, executed by a normal user, with a real run history.

## When to Use

- "Deploy X", "ship this", "publish app on Coolify", "redeploy after the image change".

- Setting up or repairing the deploy path itself: Coolify SSH/key/server wiring, a Dagu deploy DAG,
a CI runner, a deploy script.

- Any question of the form "should this have root / sudo / a key?" — answer it from the root
accounting below before changing anything.

## Root accounting — decide this before touching anything

- **Deploying Compose apps on macOS needs no root.** Docker Desktop's socket is owned by the login
user, so `docker compose up -d` works from a plain shell. Confirm with a bare `docker ps` before
designing anything privileged.

- **Coolify demands root for a self-imposed reason.** It prefixes `sudo` on *every* remote command
when the SSH user is not literally `root` (`bootstrap/helpers/remoteProcess.php`, `isNonRoot()`),
so even its reachability probe (`ls /`) runs under sudo. On a host with password sudo that cannot
succeed — the error surfaces as a *connection* failure and looks like a bad key.

- **The real lever on "fewer apps with root" is the docker socket, not sudoers.** Every container or
agent holding `/var/run/docker.sock` rw is root-equivalent (it can start a privileged container
with `/` mounted). Count socket holders, not sudo entries: the panel, any Portainer agent, and the
agent shell itself all qualify.

- Therefore: keep **one** deploy path that runs as the login user, and treat "give X root" as "add
another door to a room X can already enter". Say that trade in exactly those terms when asked.

## The deploy contract

`~/bin/deploy-app.sh <project> [--pull] [--prune-orphans] [--check]` — a copyable template lives at
`templates/deploy-app.sh`. Rules it encodes, keep them in any rewrite:

1. **Resolve the compose file from the engine**, never from a hardcoded path:
`docker compose ls --format json` → match `Name` → use its `ConfigFiles`.

1. **Validate, then act**: `compose config -q` before `up -d`; `--check` must change nothing.

1. **Refuse control-plane projects by name** (`coolify`, `portainer*`, `studio-management`). A bad
compose in the panel takes down the panel; a Portainer agent is a socket bridge. Deploy those by
hand, deliberately.

1. **Report truth after the fact** — list containers and exit non-zero if any is not running. "up -d
returned 0" is not a deployment.

1. **JSON only.** Never pass a Go-template format string (`--format '{{.Name}}'`) into a command that
may run under Dagu — its step parser eats double braces. Parse `--format json` in python.

Log to `~/Library/Logs/deploy-app.log`; keep the script idempotent so a retry is safe.

## Trigger layers — pick one primary, not three

- **Build in CI, deploy on the host.** Building on the Studio competes with local inference for
memory; push to a registry and let the host pull.

- **Push-to-deploy wants a self-hosted runner**, not a tunnel: it dials out, runs as the login user,
needs no inbound port and no public route. A loopback-only scheduler API (Dagu `:8888`) can never be
called by a cloud CI directly — that is the whole reason for the runner.

- **Deploy contracts belong on local disk.** A compose file (or `.env`) on an NFS/SMB share deploys
fine when you run it by hand and fails when anything triggered runs it (see
`references/dagu-deploy-trigger.md`). Move the stack to `~/docker/apps/<app>/` and point the script
at that checkout — it also kills the drift between "what's on the share" and "what's deployed".

Coolify wiring on a macOS host (key registration, server user, PATH, ports, DB inspection):
`references/coolify-localhost-macos.md`. Dagu params, HTTP trigger shape and the execution-context
trap: `references/dagu-deploy-trigger.md`. Live Coolify state reads:
`references/coolify-tinker-recipes.md`.

## Verification

- Script: `--check` passes, then one real run, then `compose ps` shows every service `running`.

- Dagu: a run row in `dagu history <dag>` (a dry run proves nothing) plus the `OK <app> — deployed`
line in the log.

- Coolify: the platform's own connection test returns uptime, not "reachable but sudo failed".

## Pitfalls

- **A sudo error is not an authentication error.** If a remote check reports *connection* trouble,
read the actual stderr first: `sudo: a terminal is required` means SSH worked and privilege
escalation did not. Reporting it as a key problem sends you to the wrong fix.

- **Never claim a deploy from a dry run or a zero exit code.** Both succeed while nothing moved.

- **Don't duplicate compose files to get around a mount problem** — move the stack once and keep one
source of truth, or the next deploy silently uses the stale copy.