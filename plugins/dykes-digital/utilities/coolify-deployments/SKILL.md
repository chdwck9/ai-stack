---


uuid: 41324dc8-ccd9-81ac-93b4-e37d772b2902
name: coolify-deployments
description: "Use when deploying an app through Coolify here."
version: 1.0.0
thinking: "Medium"
temperature: 0.2
author: Clarity
license: proprietary
metadata:
hermes:
tags: [coolify, deploy, docker, macos, ssh, root, dagu]
related_skills: [dagu-pipelines, docker-management, selfhosted-api-access]


---


# Coolify deployments (Studio, macOS host)

Publishing an app through Coolify on a Mac is not the Linux path. Coolify assumes a root-capable SSH
user and a Debian host; neither is true here. Read this before touching the UI or an app record.

## When to Use

- Publishing or deploying an app through Coolify.

- Deciding whether a deploy should go through Coolify at all.

- Coolify's [localhost](http://localhost/) server shows unreachable, or "Validate" does nothing.

## The estate (verify, don't assume)

- UI `http://localhost:7810`; `7811` = realtime, `7812` = terminal. All published on `0.0.0.0`.

- Container runs as `www-data`, unprivileged — **but ****`/var/run/docker.sock`**** is bind-mounted rw**, so
anything that drives Coolify is already host-root-equivalent. Judge proposals against that, not
against "it's only a container".

- Its Postgres is **`DB_HOST=supabase-db`** — the control plane lives on the supabase stack. Never
recreate that stack casually.

## Choosing the deploy path

The user's standing preference is **the fewest apps holding root**. Deploying with `docker compose` as
the login user needs **no** privilege escalation at all (Docker Desktop's socket is user-owned), so:

- **Default: ****`~/bin/deploy-app.sh <project>`**** + the Dagu ****`deploy-app`**** DAG.** No sudo, no SSH, retries
and run history in the Dagu UI. Protected projects (`coolify`, `supabase`, `portainer*`,
`studio-management`) are refused by name inside the script.

- **Coolify only when the user wants its UI/records.** Then it needs root SSH — Coolify prefixes
`sudo` on every remote command for a non-root user (`bootstrap/helpers/remoteProcess.php`:
`$server->isNonRoot() ? 'sudo ' : ''`). There is no setting that avoids it, and a narrow NOPASSWD
rule cannot work because the wrapper wraps *everything* (`ls /`, `mkdir`, `docker`).

Say which path is being taken and what it costs before building. If asked for fewer root holders, the
lever is the **docker socket** (Coolify + any Portainer agent + the agent itself are all root-equivalent),
not the sudoers file.

## Root SSH on macOS — three blocks, in order

Full commands: `references/macos-host-setup.md`. The shape:

1. Dedicated key (never reuse another app's key) into `/var/root/.ssh/authorized_keys`. macOS ships
`PermitRootLogin prohibit-password` by default, so **key-only root login needs no sshd_config edit
and no restart** — sshd re-reads its config per connection anyway.

1. **Root has no ****`docker`**** on PATH** (`/usr/bin:/bin:/usr/sbin:/sbin`, shell `/bin/sh`), and `/usr/bin`
is SIP-protected so you cannot symlink into it. Set `PermitUserEnvironment yes` plus
`/var/root/.ssh/environment` with the PATH.

1. **Root has no compose plugin** — Docker Desktop's cli-plugins live in *your* `~/.docker/cli-plugins`,
so root gets `docker: unknown command: docker compose`. Symlink the plugin directory into
`/var/root/.docker/cli-plugins`. Do **not** point root's `DOCKER_CONFIG` at the user's `~/.docker`:
that hands root their registry credentials.

Write the Coolify side yourself (private key record + server `user: root`) instead of asking the user
to paste a private key into a browser.

## Validation — never press "Validate" in the UI

`ValidateServer` reads `/etc/os-release`, which macOS does not have, so it throws and can flip
`is_reachable` back to false. It also leaves the server row looking broken.

- Check reachability with `$server->validateConnection()` (returns `['uptime' => true]`).

- Prove the real prerequisites with `$server->validateDockerEngine()` and
`$server->validateDockerCompose()` — these run Coolify's own `command -v docker`, `docker version`
and network check, and set `settings.is_usable` **from evidence**. There is no `is_validated` column
in current versions: validated = reachable + usable.

- Record why in `servers.validation_logs` so the next reader knows the state was established by hand.

## API recipes

Token, app creation, and the required-field traps live in `references/coolify-api.md`. Two that cost
real time:

- **`file://`**** git URLs are rejected** — Coolify validates `https://`, `http://`, `git://`, `ssh://`.
A local bare repo cannot be a source; the app needs a real remote before it can deploy.

- The `/applications/dockerfile` endpoint wants the Dockerfile **content, base64-encoded** — it is not
a "repo with a Dockerfile" endpoint. For a repo, use `/applications/public` with
`build_pack: dockerfile`.

- **No git remote? Use a service, not an application.** `POST /api/v1/services` with
`docker_compose_raw` (base64) creates a compose stack Coolify owns, no repo and no SSH. Recipe,
env-var handling and the Docker Desktop compose traps are in `references/coolify-api.md`.
Deploy a service with `POST /api/v1/deploy {"uuid": "<service uuid>"}` — the GET form is a 405 stub.

## Deploy contract layout

- `~/docker/apps/<app>/docker-compose.yaml` is **authoritative** if present; `deploy-app.sh` prefers it
over the path the running project reports.

- Keep it on **local disk**. API-triggered Dagu runs execute in the launchd process, which macOS TCC
denies network-volume access — a compose file on an NFS/SMB mount deploys from a shell and fails
from every trigger with `operation not permitted`.

- Only the compose file, `.env` and any `build:` context need to be local; data volumes can stay on the
NAS because the daemon does the bind mounts.

## Containerising an app that reads local state

Never bind-mount `~/.hermes` into a container to satisfy a dashboard: it exposes `.env`, `mcp-tokens/`
and every credential there to a web app. Build a compact snapshot instead — one `sqlite3` ATTACH
selecting only the tables/columns the app reads (144 KB vs the 184 MB live DB), refreshed by a Dagu
DAG, mounted `:ro`. Prefer env vars over a `.env` mount for keys, and make the app read
`os.environ` before any file.

## Verification

- `docker compose -p <app> ps` shows every service `running`/`healthy` after a deploy.

- Post-deploy check is a real HTTP probe of the app's health path, not just a container state.

- After any Coolify server edit, re-run `validateConnection()` and confirm `is_reachable`/`is_usable`
are still true.

## Pitfalls

- **Don't trust "port is open".** Coolify, a native process and Docker can each hold different bindings
on the same port; check both `localhost` and the LAN IP.

- **Coolify's UI reachability log spins forever** (`unreachable_count` in the thousands) and is
meaningless until SSH actually works — it is not evidence of anything else being wrong.

- **`docker compose up -d`**** deploys every service in the file**, including ones deliberately stopped.
Check what is defined before running it against a partial stack, and expect recreates when the
compose file moves (the project's config-files label changes).

- **A ****`www-data`**** container is not a sandbox** when it holds the docker socket. State that plainly when
weighing a security trade.

## Related

- `dagu-pipelines` — DAG authoring; the HTTP trigger and launchd/TCC caveats are recorded here because
they surfaced on the deploy path. That skill is user-owned, so `hermes curator adopt dagu-pipelines`
first if those rules should live there instead.

- `selfhosted-api-access`, `docker-management` — API access and container basics.

- `remote-mcp-servers` — when the thing being deployed is an MCP server for a hosted assistant
(transport Host allow-list, key auth, tunnel path routing).