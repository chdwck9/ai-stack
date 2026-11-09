---


name: clarity-capabilities
uuid: TBD
version: 1
description: "See Clarity's real runtime surface before claiming a gap."
last-used: "2026-10-20"
scope: local
thinking: "Low"
temperature: 0.2
author: clarity
license: proprietary
metadata:
hermes:
tags: [clarity, capabilities, probe, shell, runtime]
related_skills: [token-costing, handle-delegated-task]


---


# Clarity capabilities utility

Probe, don't assume. Clarity runs **on the host** with a shell, local files, the `hermes` CLI and the `hermes send` path. A run that reports "no shell / no send tool" is usually wrong about itself — probe first, then report only gaps that survive the probe.

## When to Use

- Before reporting a capability gap ("no shell", "no send tool", "no file access").

- At the start of a webhook / cron / delegated run, to confirm the surface you were given.

- Any time a session is unsure what it can actually do.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Probe.** `python3 ~/.hermes/scripts/clarity_capabilities.py` — prints host, shell (`python3`/`bash`/`git`), the `hermes` CLI path + version, the `hermes send` command, `state.db` / `cron` / `config` presence, the skills and scripts directories (with the script list), and the **names** of relevant env keys.

1. **Use the shell you have.** Reads, searches, renders, scripts, `git`, and `hermes send` for the home-channel ping are all available from this host. Reach for `terminal` before declaring something impossible.

1. **Report gaps only if the probe proves them** — and then name the missing tool, not a vague "no execution surface".

## Boundaries

- Prints env keys by **name only** — never read, print or transmit a value (no secrets).

- Read-only: writes nothing.

- A webhook/cron run may be given a narrower toolset than an interactive session; if the probe shows a tool genuinely absent, say so precisely — do not generalise "this session" into "Clarity cannot".

- This utility documents the surface; it does not grant capabilities.

## Verification

- The probe lists the `hermes` CLI and the scripts directory; if it cannot, the run really is restricted — say which line failed.

- Any capability you claim to lack must be one the probe reported missing.

## Disabled toolset ≠ missing capability

A toolset can be off in `config.yaml` (`agent.disabled_toolsets`, e.g. `image_gen`, `discord`, `video_gen`) while the underlying backend is fully usable — the bundled providers are importable Python and the credentials are already on the box. Probe the provider directly instead of reporting a gap:

- **Image generation** — `/Users/chdwck9studio/.hermes/hermes-agent/plugins/image_gen/<provider>/__init__.py`; `openai-codex` needs no API key (ChatGPT/Codex OAuth in `auth.json`), `openrouter` uses `OPENROUTER_API_KEY`. Load it with `importlib.util.spec_from_file_location` after putting the repo root on `sys.path` (it imports `plugins.image_gen._common` and `agent.*`), then call `Provider().generate(prompt, aspect_ratio="square")`. Results land in `$HERMES_HOME/cache/generated/images/`. **Prompt pitfalls:** OpenAI's safety filter rejects explicit franchise/character names ("R2 unit", "Star Wars", "mid-pose") with HTTP 400 — describe the object generically and it passes. Verify output with `vision_analyze` before delivering; the API reports `quality: low` even when `medium` was requested, so judge the pixels, not the metadata.

## Setting Clarity's own Discord avatar

The Discord bot user **is** Clarity (`id 1557116754243887144`, one bot per persona — no `profiles/` dir on this box). `PATCH https://discord.com/api/v10/users/@me` with `{"avatar": "data:image/png;base64,…"}` and `Authorization: Bot $DISCORD_BOT_TOKEN` (read the token from `~/.hermes/.env`, never print it). Reversible: send `{"avatar": null}` to clear. Verify by reading `avatar` back from `GET /users/@me` and fetching `https://cdn.discordapp.com/avatars/<id>/<hash>.png?size=256` with a browser User-Agent (the CDN 403s a default urllib UA).

## Pitfalls

- The most common error is asserting "no shell" without running `terminal` once. Probe first.

- `hermes send` needs the target chat id (Discord home `1557119812256145408`), not a channel name.

- New skills appear to a session only after it restarts (the loader is cached at start).