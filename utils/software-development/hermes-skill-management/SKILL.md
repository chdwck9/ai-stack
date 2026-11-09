---
name: hermes-skill-management
description: "Configure Hermes skill dirs and lifecycle write-back."
version: 0.1.0
author: Richard Dykes, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, skills, configuration, plugins, hooks, lifecycle]
    related_skills: [hermes-agent, hermes-agent-skill-authoring]
---

# Hermes Skill Management

Configure where Hermes reads and writes skills, and publish skill edits to an external hub on
every touch. Covers `skills.external_dirs` vs `skills.create_dir` and the `on_skill_lifecycle`
plugin hook. Does NOT cover authoring SKILL.md body/frontmatter (see
`hermes-agent-skill-authoring`) or the repo map (see `hermes-agent`).

## When to Use
- Relocating where Hermes stores/authoring skills ("move the self-improvement library").
- Wiring a skill directory that syncs to an external hub (Notion, git, S3, OWUI…).
- Publishing skill create/patch/delete events to an external system on every touch.
- Don't use for: writing SKILL.md content; installing hub skills.

## Directory model (the two knobs)
- `skills.create_dir` — where `skill_manage` (and the curator) **author** new skills; also scanned
  for loading. Set this to relocate the self-improvement library. Only ONE such dir.
- `skills.external_dirs` — extra roots, **live-read**. Read-only to *autonomous* curation; a
  foreground `skill_manage` **can** edit them (verified). Use for externally-owned/synced dirs.
- Precedence, lowest tier wins: trusted project > local `~/.hermes/skills` > `create_dir` > `external_dirs`.
- A dir that is BOTH `create_dir` and in `external_dirs`: drop it from `external_dirs` — otherwise
  `is_external_skill_path` classifies it read-only and the curator refuses to manage it.

## Procedure: relocate the authored-skill store
1. Ensure the target dir exists (create it if the path is a mount).
2. `hermes config set skills.create_dir <abs path>`
3. If it was also in `external_dirs`, drop it: `hermes config set skills.external_dirs '["<others>"]'`
   (a JSON list is accepted).
4. Verify `hermes config get skills`.
5. Verify a real author: `skill_manage(action='create', …)` a probe, confirm the file landed under
   `create_dir` (not `~/.hermes/skills/`), then delete the probe.

## Procedure: publish skill edits to a hub
1. Write a plugin `~/.hermes/plugins/<name>/{plugin.yaml, __init__.py}`; `register(ctx)` calls
   `ctx.register_hook("on_skill_lifecycle", cb)`.
2. In the callback, filter to `created`/`patched`/`edited` (+ `deleted` → archive signal); **ignore
   `loaded`** (fires on every skill use, not an edit).
3. Resolve the skill path, scope it to your hub dirs, and tag the payload with the target dir's
   external `Type`. Never publish skills resolving outside your targets (e.g. the local store).
4. POST the full SKILL.md on a daemon thread with a short timeout; fail open.
5. `hermes plugins validate <path>` then `hermes plugins enable <name>` (loads next session; the
   gateway hot-reloads hooks).
See `references/skill-lifecycle-publishing.md` for the hook payload and a minimal plugin.

## Quick Reference
```
hermes config get skills
hermes config set skills.create_dir /path
hermes config set skills.external_dirs '["/path/a","/path/b"]'
hermes plugins validate ~/.hermes/plugins/<name>
hermes plugins enable <name>
```

## Pitfalls
- **Test plugin/agent modules with the interpreter Hermes runs on, not a bare `python3`** — Hermes
  code uses `X | Y` type unions and fails to import on Python < 3.10 (a bare `python3` is often
  3.9). Use the install's venv python (`~/.hermes/installs/*/environments/*/venv/bin/python3*`).
- **"external_dirs are read-only" is about *autonomous* curation only.** Verify with a foreground
  `skill_manage` patch before designing around the assumption — do not report it as immutable.
- **Never hand-edit `config.yaml`** for these keys — a stray indent corrupts the live gateway. Use
  `hermes config set`.
- **`on_skill_lifecycle` does not fire for out-of-band edits** (editing a SKILL.md directly). If
  those must publish, add a filesystem watcher that POSTs the same payload.
- **`create_dir` on a flaky network mount makes skill *creation* fail when the mount is down.**
  Prefer a local path, or accept the coupling deliberately.

## Verification
- Config change: `hermes config get skills` shows the new value; a probe `skill_manage` create
  lands in the intended dir.
- Plugin: `hermes plugins validate` passes, `hermes plugins list` shows it enabled, and a probe
  edit fires the hook — point the webhook at a local HTTP listener and assert the payload
  (action, skill, notion_type, content).
