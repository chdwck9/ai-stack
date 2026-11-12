---


uuid: 41424dc8-ccd9-81fd-acb8-c4cfc0089926
name: container-update-audit
description: "Use when auditing fleet images/apps for updates."
version: 1.0.0
author: Clarity
platforms: [macos]
metadata:
hermes:
tags: [docker, updates, upgrades, migration, ops, ai-stack]


---


# Container & AI-stack update audit

Monthly (and on-demand) read-only answer to "what is out of date in my fleet, and what breaks if I upgrade it". Pairs with `docker-fleet-healthcheck` (which asks *is it up*) — this asks *is it current*.

## Collector first, judgement second

Run the deterministic collector; never hand-inventory 140 images in an agent context.

```bash
python3 ~/.hermes/scripts/update_check.py           # ~1-2 min, read-only
python3 ~/.hermes/scripts/update_check.py --json    # machine-readable
python3 ~/.hermes/scripts/update_check.py --no-nas  # skip the NAS
```

It writes `~/.hermes/update-check/YYYY-MM-DD.json` and prints a summary covering:

- **Docker images on both hosts** (Studio local; NAS via `ssh chdwck9NAS` + `sudo -n /usr/local/bin/docker`).

- **Tag moved**: local repo digest vs the digest the registry serves now, for every registry-backed tag. Same tag + new digest = upstream rebuilt it (routine).

- **Version-pinned tags** with `same_major_newer` and `newest_other_major` for semver-looking tags.

- **Homebrew** outdated formulae/casks (rapid-mlx, dagu, cloudflared, opencode live here).

- **Git checkouts** (`~/.hermes/hermes-agent`, `/Volumes/Live/@Edge/.ai`) vs upstream, incl. dirty-file count.

- **launchd services** + installed versions + live rapid-mlx model/context.

- **Compose file path per container** (from `com.docker.compose.project.config_files`) — the file an upgrade actually edits.

Registry auth notes baked into the script: Docker Hub and [ghcr.io](http://ghcr.io/) use anonymous token flows; [**lscr.io**](http://lscr.io/)** takes its token from ****`ghcr.io/token?service=lscr.io`** ([lscr.io](http://lscr.io/)'s own `/token` 404s). HTTP 401/403/404 on a ref means locally built or private → report as "not in a public registry", not as a failure.

## Triage into three classes (do not blur them)

1. **Routine rebuild** — same tag, digest moved. No version jump, no migration. Risk = restart + smoke test.

1. **Same-major bump** — patch/minor. Low risk but read the changelog for behaviour changes.

1. **Major / cross-major jump** — postgrest v14→v16, mysql 8.4→newer line, imgproxy v3→v4, vector 0.28→0.36. These get migration steps, a rollback, and a downtime estimate.

## Plan in waves

- **Wave 1**: routine rebuilds + brew patches.

- **Wave 2**: same-major bumps, restart + smoke test each, one at a time.

- **Wave 3**: majors/migrations: backup (DB dump / volume snapshot) → migrate → verify → rollback path spelled out.

Dependency rules that bite:

- Supabase components move as a set (`supabase/postgres`, `postgrest`, `supavisor`, `postgres-meta`, `gotrue`, `storage-api`, `realtime`): a single-component bump creates version skew against `supabase-db` and is usually worse than the bug it fixes.

- Shared infrastructure (traefik/coolify-proxy, the shared Postgres/Redis) stops its dependents — schedule it alone.

- Any image major implies an on-disk format change (postgres, mysql, mariadb, mongo, metabase, qdrant) → dump first, and pin the *minor* line rather than jumping majors in the same month.

- `hermes-agent` sits thousands of commits behind its origin here; that is upstream history, not drift to hand-merge — upgrade with `hermes update`, and `launchctl` restarts must be handed to the user (blocked inside the gateway).

- Cap scope at ~12 actionable upgrades per month: security-relevant + AI stack + pinned majors first, media/arr `:latest` rebuilds last.

## Run lessons (from the first live run)

- **Docker Hub rate-limits the sweep.** ~100 manifest calls in a burst returns HTTP 429 on 20+ refs. The script now retries 429/5xx three times with backoff at 4 workers; if refs still come back unverified, report them as"unverified (rate limit)"and draw no conclusion — never read a 429 as "image missing".

- **`web_extract`**** is not available inside a cron run** (that platform ships a search-only web backend). Changelog research there has to go through `curl` against GitHub releases API / raw CHANGELOG files. Do not report "no breaking changes found" when the only real obstacle was the missing tool.

- The plan file is the durable artefact (`~/.hermes/update-check/plans/YYYY-MM.md`); the chat message is the index into it. Richard approves waves, not individual container restarts.

## Executing an approved wave — mechanics that bit

Before any pull: snapshot every target's `docker inspect` to `~/.hermes/update-check/rollback/<month>/`, note the old **image ID** (pulling the same tag retags the old image to `<none>` but keeps the layers, so rollback is `docker image tag <old_id> <ref>` + recreate), and back up any SQLite/LanceDB directory the service owns.

- **`up -d --no-deps <svc>`**** breaks any service using ****`network_mode: service:<other>`** — the sibling container is not part of the operation, so start fails with `network service:<name> not found` and the container is left in state `created`. Drop `--no-deps` for those; compose then starts the existing sibling (it is Running, so it is not recreated) and the link resolves.

- **Docker Desktop / macOS paths:** a standalone container recreated by hand must keep its exact `docker run` config (ports, `:ro` mounts, restart policy). Keep the old container stopped and renamed `<name>.rollback-<stamp>` instead of removing it.

- **`docker compose`**** from inside a ****`/Volumes`**** network-mount directory fails** with `error in parsing compose-spec.json: stat .: no such file or directory`. Run compose from `$HOME` with an absolute `-f`; relative bind mounts still resolve against the compose file's directory.

- **Portainer-deployed stacks: pass ****`-p <existing project>`****.** The project name comes from Portainer, not the directory (e.g. `/volume1/docker/portainer/compose/48/` runs as project `media` with `/data/compose/48/...` labels). Without it compose derives a new project, creates a fresh `<dir>_default` network and dies on `container name already in use` — no damage, but a stray network to remove.

- **Portainer agent containers are not safely upgradable from the CLI** — they are deployed by Portainer from a compose file that lives on the Portainer host, so a hand `docker run` recreation silently drops stack ownership. Redeploy from the Portainer UI instead (the API key in `~/.hermes/.env` may be stale and return 401).

- **A ****`:latest`**** rebuild is not always migration-free.** `jellyfin` and `jellyseerr` ran internal DB/settings migrations on first start after a digest-drift pull, so an image rollback alone does not revert them. Check the boot log for `Migrat` before calling a wave-1 item "routine".

- Verify with a probe that exercises the app, not just `docker ps`: NPM and Jupyter return 000/307 while still booting, and searxng needs `/search?q=test&format=json`.

## Boundaries

Read-only until approved. No `docker rm`, no prune, no `down -v`, no compose edits without an approved wave. Anything that recreates a container, changes a DB major, touches supabase, or restarts hermes-gateway/rapid-mlx needs Richard's explicit per-wave permission.

## Scheduled job

`79193c72732e` — "Monthly Container & AI-Stack Update Audit", `0 8 1 * *`, script `update_check.py`, delivers to Discord `#managers-stack` (1562010699331534899) with `attach_to_session` so Richard can reply "approve wave 1". Model pinned to a cloud model: the cron default is a local MLX model, and changelog research + planning on it runs for hours.