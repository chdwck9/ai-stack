---


uuid: 40524dc8-ccd9-81d6-90fd-eabe027bd511
name: hermes-skill-library
description: "Hermes Skill Library"
version: 1.2.0
author: Richard Dykes, Hermes Agent
license: MIT
platforms: [macos, linux]
last-used: "2026-10-27"
metadata:
hermes:
tags: [hermes, skills, create_dir, external_dirs, plugins, hooks, notion, n8n, sync]
related_skills: [hermes-agent, hub-learning-governor]


---


# Hermes Skill Library

Configure which directories Hermes loads skills from and authors skills into, and wire the write-back
so skill edits reach the canonical hub (Notion).

## When to Use

- Relocating where Hermes authors and loads skills (`skills.create_dir` / `skills.external_dirs`).

- Wiring skill edits to publish to a hub (Notion) on every touch.

- A skill edit must reach an external system (an n8n webhook, a Notion page).

- Running a **consolidation pass** over one Hub `Type` — see `references/hub-consolidation.md`.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Pick the store.** Precedence (lowest tier wins): `trusted project > local (~/.hermes/skills) ><br>   skills.create_dir > skills.external_dirs`. `skill_manage(action='create')` writes only to
`skills.create_dir`. Table: `references/skill-stores.md`.

1. **Classify the content.** Workflows → `external_dirs` (Hub `Type=Skills`); reach-a-tool utilities →
`create_dir` (`Type=Utilities`); personas → `Type=Personas`. Detail: `references/content-classes.md`.

1. **Set config with ****`hermes config set`** (never hand-edit `config.yaml`): nested dotpaths and JSON
lists work, e.g. `hermes config set skills.external_dirs '["/a","/b"]'`,
`hermes config set mcp_servers.<name>.enabled false`.

1. **Move a skill in two verified steps** — never `cp … && rm -rf …` in one command. `cp` first,
confirm the destination `SKILL.md` exists and is non-empty, *then* remove the source in a separate
call. Verify a move by resolving the path: `get_skill_create_dir()` / `_resolve_skill_md(name)`.

1. **Write the Hub page body as the **[**SKILL.md**](http://skill.md/)** verbatim** — a plain `---` … `---` header, never a fenced
code block. Recipe: `references/notion-hub-skill-page.md`.

1. **Push local edits UP.** Run `~/.hermes/scripts/hub_sync_all.py` for the `~/.hermes/utils/**` store
(flags `--dry`, `--pull`, `--only`, `--include-local`, `--set-type`). It scans **only** that store —
a hub-scope skill living in the local store (`~/.hermes/skills/**`, e.g. `media/*`) is invisible to
it and silently stays local-only. Push those one at a time with
`hub_push_one.py <name> --path <SKILL.md> --type Skills --category <kit> --version N` (creates the
page when `Name` is absent, else replaces body + properties, and writes `uuid:` back). Check for a
newer writer first — a page `Version` newer than your file means do not push. Detail:
`references/hub-sync.md`.

1. **Do not rely on the lifecycle hook.** `skill-publisher` returns without POSTing (no
`SKILL_PUBLISH_WEBHOOK`, no `plugins.skill_publisher.webhook`); a healthy sink proves nothing about
whether Hermes fired the request.

## Pitfalls

- The Hub pulls back on a **midnight n8n timer**, not a hook — a Hub-side delete/rename is invisible
locally for up to a day; do not hand-delete what the timer will.

- A skill's Hub `Type` is the **directory its file sits in** (personas the one exception).
Reclassifying means moving the file, not just the page.

- Hub `Category` is a fixed kit list: `data-kit`, `eng-kit`, `pm-kit`, `design-kit`, `life-kit`,
`ai-kit`, `utilities` (no `creative`). An invalid Category fails the property write silently — the
body still updates. `Type` and `Category` are independent; set and read back both.

- `hub_sync_all.py` supersedes `hub_sync.py` (which only published its hardcoded `TARGETS`); it
preserves a page's `Type`/`Category` unless `--set-type` is passed.

- `hub_sync_all.py` derives its target list from `~/.hermes/utils/**/SKILL.md` **only**. A no-`scope`
skill stored in the local tier (`~/.hermes/skills/**`) never reaches the Hub through it — the script
and the midnight timer both look at the utils tree — so it stays local-only until you push it with
`hub_push_one.py`, which also lets you pass `--type Skills` explicitly (`hub_sync_all.py` would
path-classify a non-utils location as `Utilities`).

- Never blind-overwrite a page: re-fetch and check `Version` / `Last update`; prefer `update_content`
/ `insert_content` over `replace_content`.

- A rate-limited Notion reply is a plain STRING, not a dict — never read it as "not found" or you
create duplicates. A `notion-query-data-sources` SELECT silently caps at 100 rows — page it.

- Test plugins with the Hermes venv python (`~/.hermes/hermes-agent/venv/bin/python`), not system
`python3`. A bare `<name>.md` beside `<name>/SKILL.md` makes the skill unloadable by name.

- **Editing a skill file on the network-mounted store: write it in Python, not with the patch tool.**
The patch tool writes through a temp file (`<dir>/.hermes-tmp.<pid>`) and renames; on the NAS mount
that write can fail `No such file or directory` even though the directory is writable. Make the edit
as a read → replace → write (Python or `write_file`) and read the file back to confirm the new text;
a failed patch says nothing about permissions — verify those separately (`touch <dir>/.wtest`).

- **A stale entry in a hardcoded TARGETS map fails silently.** The legacy `hub_sync.py` prints
`SKIP <name>: no file at <path>` and keeps going when a target's path or `Name` no longer matches the
real directory — the skill is simply never published, and no error is raised. Confirm every entry's
path exists AND its `Name` matches the Hub page before trusting a run; prefer `hub_sync_all.py` /
`hub_push_one.py`, which derive the list from disk rather than from a map that drifts.

- **Publishing one skill out of a TARGETS list:** `hub_sync.py` has no name filter — import it and
narrow `TARGETS` to the single entry, then call `main()`. Running it whole also pushes every other
target it lists, which is almost never what you want mid-task.

`references/pitfalls.md` → full catalogue. `references/write-back-plugin.md` → the publisher.

## Verification

- `get_skill_create_dir()` / `_resolve_skill_md(name)` returns the new location after a move.

- The destination `SKILL.md` exists and is non-empty before the source is removed.

- After a push, re-query `Version` and grep the fetched page for a phrase you just added.

- No name exists in both `create_dir` and `external_dirs`.

- Read back any skill file you edited on the network store — writes there are less reliable than local
ones, and the publish target is the file on disk, not the edit you intended.