---


uuid: 41324dc8-ccd9-819a-a751-d34ec54ac112
name: macos-selfhosted-deploys
version: 1.0.0
description: "Use when deploying self-hosted apps on a macOS host."
thinking: "Medium"
temperature: 0.3
author: Clarity
license: proprietary
created_by: agent
metadata:
hermes:
tags: [deploy, docker, compose, coolify, dagu, macos, ssh, root]
related_skills: [docker-management, dagu-pipelines, minimal-webservers]


---


# Self-hosted deploys on a macOS host

How to get an app from a repo or image to running containers on this Mac — and how to reason about
root while doing it. Two engines exist and both are supported: **Dagu** (no root, parameterised DAG) and
**Coolify** (control plane, needs root over SSH).

## When to Use

- Standing up, replacing or debugging the deploy path for any self-hosted app on this host.

- Wiring Coolify's "[localhost](http://localhost/)" server, or a deploy that must fire from a trigger/CI rather than a shell.

- Any question of the form "does this need root?" about containers, deploys or a control plane.

## Root accounting comes first

- **`docker`**** as the interactive user needs no sudo.** Docker Desktop's socket belongs to the login
user, so `docker compose up -d` runs unprivileged. A deploy script therefore has **no** legitimate
reason to ask for root; if one does, it is an assumption in a tool, not a property of the host.

- **The socket is the real root boundary, not the ****`sudoers`**** file.** Anything with `/var/run/docker.sock`
can start a privileged container and own the host. Count socket holders, not password-prompting apps:
the control plane, agent containers (Portainer etc.), and the agent itself. "Fewer apps with root" is
achieved by removing socket mounts, never by tightening sudo.

- **Never add ****`NOPASSWD`**** for the human's account** to satisfy a deploy tool: it silently grants root to
every process running as that user, including the agent and one-off scripts. If a tool demands root,
give it its own key and its own principal, so the blast radius is one revocable file.

- Read `~/.ssh/authorized_keys` and the sshd config before assuming a key is not installed. A previous
session often already installed it, and the real gap is elsewhere (user, PATH, sudo).

### sudo assumptions in the tool

Coolify prefixes `sudo` on **every** remote command when the SSH user is not literally `root`
(`bootstrap/helpers/remoteProcess.php`: `$server->isNonRoot() ? 'sudo ' : ''`) — including `ls /`. With
macOS password-sudo every check fails with `sudo: a terminal is required to read the password`, and no
UI setting fixes it. The only two coherent states are **root SSH** or **do not use that tool to deploy**.
Do not try to narrow-scope a sudoers rule for it; the command set is unbounded.

## Deploy contracts live on local disk

- **The deploy contract is the compose file + ****`.env`**** + any ****`build:`**** context, and it must live on local
disk.** macOS TCC denies `/Volumes` network mounts to launchd-spawned processes (HTTP triggers, CI,
scheduler), so a share-hosted compose file can be deployed by a human at a shell and by nothing else.

- **Bind mounts pointing at the share are fine.** The daemon performs those mounts; the deploy job never
reads the data. Only the files the deploy process opens must be local.

- Prefer one path per app (`~/docker/apps/<app>/docker-compose.yaml`) and make the deploy script treat a
local contract as authoritative over whatever path the running project reports — the running project
keeps reporting the old path in its labels after the move.

- Relative `./path` bind mounts and `build: ./dir` resolve against the compose file's directory: moving
the file without moving those directories silently changes what gets mounted or built.

## Dagu as the deploy engine (no root)

Author a parameterised DAG that calls one idempotent script; keep the script's decisions (path
resolution, protected projects, post-deploy truth check) out of YAML. Recipe and working shapes:
`references/deploy-dag-recipe.md`.

Rules that cost time:

- **`{{ ... }}`**** inside a ****`run:`**** block is dagu template syntax, not shell.** Any command carrying
`--format '{{.Name}}'` is expanded before the shell sees it and fails with `format value ... could not<br>  be parsed`. Request JSON (`--format json`) and parse in Python; audit usage/error strings too.

- **Params need defaults or a rich definition.** `params: "APP PULL=0"` is rejected at load
(`unknown parameter(s): "APP"`); declare a list of `{name, default|required, enum}` and read
`${params.APP}`. Only `dagu dry` surfaces this.

- **HTTP trigger:** `POST /api/v1/dags/<name>/start` with a JSON body — `{}` when the DAG has no params,
`{"params":"APP=ai PULL=1"}` otherwise. No body → **400**; `/api/v2/.../start` → **405**. A 200 is
acceptance, not success: verify with `dagu history <name>`.

- **Isolate a context problem with a throwaway probe DAG**, not by staring at the failing job. Print
`whoami`, an `ls` of the path, and a read of the specific file; then delete the DAG and its log dir.

- **`up -d`**** starts every service the file defines**, including ones someone had deliberately stopped.
Enumerate the file's services and compare with `docker ps` before a first deploy from a new path, and
say which containers the deploy will bring up. Recount afterwards rather than trusting the run result.

## Coolify as the deploy engine (root, by design)

Detail, including headless key registration and the PATH traps: `references/coolify-localhost-server.md`.

Headline rules:

- **A dedicated root key beats reusing an existing one.** Generate `<name>-root`, install only its `.pub`
into `/var/root/.ssh/authorized_keys`, and keep it separate so it can be revoked alone.

- **macOS already defaults to ****`PermitRootLogin prohibit-password`** — key-only root login, no sshd edit
and no restart. Check the config before "hardening" it.

- **Non-interactive SSH gets ****`PATH=/usr/bin:/bin:/usr/sbin:/sbin`**, so `docker` in `/usr/local/bin` is
invisible. For a zsh user a `~/.zshenv` export fixes it; for `root` (`/bin/sh`) use
`PermitUserEnvironment yes` plus `PATH=` in `/var/root/.ssh/environment`. You cannot symlink into
`/usr/bin` — SIP protects it. sshd re-reads its config per connection, so no reload is needed.

- **The full validator cannot pass on macOS**: `ValidateServer` reads `/etc/os-release` and dies. Prove
`docker version` over the SSH principal yourself, then set `is_validated` / `is_usable` explicitly —
and state in the closeout that those flags were backfilled by you because the validator is Linux-only.

- The container already holds the docker socket, so root SSH adds a second entrance to the same power
rather than a new class of privilege. Say that plainly instead of overselling the change.

## Verification

1. Real execution, not a dry run: one project deployed end to end, containers healthy afterwards.

1. The trigger path verified separately from the shell path — `dagu start` succeeding proves nothing
about an HTTP/CI trigger.

1. `dagu history` (or the control plane's own run record) shows a row with the expected params.

1. Deploy script exits non-zero when a container is not running, and the command you claim works was run.

## Pitfalls

- **Don't declare a tool "cannot deploy here" from one failure.** Separate the layers in order — auth,
PATH, privilege, file access — and say which layer failed. Each has a different fix, and the same
error string (`not found`, `operation not permitted`) appears at several layers.

- **A control plane holding the socket is already root-equivalent**, so "keep Coolify unprivileged" is
not a security claim you can make. Frame it as which interface gets root, and how revocable it is.

- **Presence of a key in ****`~/.ssh/authorized_keys`**** is not a working SSH path** — user, `IdentitiesOnly`,
PATH and sudo decide whether a deploy succeeds.

- Do not leave a private key on the clipboard or in a container `/tmp`; clear both (`pbcopy < /dev/null`,
`docker exec -u root <c> rm -f /tmp/<f>`) as soon as the key is registered.