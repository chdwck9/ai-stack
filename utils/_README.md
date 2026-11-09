# Utilities — format & pipeline

**Location:** `/Volumes/Live/@Edge/.ai/utils/` (live, written by Hermes)
**Hub mirror:** Notion AI Hub DB — `Type = Utilities`, `Category = utilities`
**Direction of truth:** Notion is the single source of truth. Hermes writes its local copy
*and* pushes the change to Notion on every touch; the nightly sync converges every endpoint
to the Notion version.

This file is a spec, not a skill (only `*/SKILL.md` is loaded), so it can sit here safely.

---

## What a Utility is

A small, Clarity/Hermes-local skill: an operating procedure, tool wiring, or preference that
only matters inside this agent. May be sensitive. Not a domain-transferable Skill.

| | Skills (transferable) | Utilities (this dir) |
|---|---|---|
| Hermes dir | `skills.external_dirs` | `skills.create_dir` |
| Hermes access | live read/write | live read/write |
| Hub Type | `Skills` | `Utilities` |
| Hub Category | per-skill kit (`ai-kit`, `eng-kit`, …) | `utilities` |
| Format | full `create-skill` ceremony | this spec |

Both dirs are **live** in Hermes and both are **writable** by a foreground `skill_manage` call.
Only *autonomous* curation (the curator) treats `external_dirs` as read-only; *new* skills
authored by Hermes land in `create_dir`.

---

## Multi-endpoint model

Skills are used on several endpoints (Hermes, Claude, Open WebUI, Perplexity, …). Every
endpoint's edit writes back to Notion as it happens; the nightly sync pulls Notion back down
to every endpoint's files. So:

```
   endpoint edit ──write-through──▶ Notion  (one version)
                                      │
                          00:00 nightly sync (Notion → all files)
                                      ▼
                         every endpoint converges to that version
```

- **Best case:** Hermes' write-through already put its edit in Notion, so the midnight pull is
  a no-op (same bytes overwritten).
- **Worst case:** another endpoint edited the same skill in Notion; the midnight pull replaces
  Hermes' local file with theirs. Hermes' own edit is not lost — it is in Notion history, and
  the local file simply takes the converged version.

---

## Format

Inherits the `create-skill` YAML header, trimmed. Body is Hermes-native and kept light —
write only the sections the procedure needs.

```markdown
---
name: kebab-case-name
uuid: <notion-page-uuid | TBD until first publish>
version: 1
description: "<capability statement, <=57 chars, ends with a period>"
last-used: "YYYY-MM-DD"
scope: local
thinking: "Low | Medium | High"
temperature: 0.3
resources:
  - "@handle"
---

# Title

One or two sentences: what it does and when it activates.

## Steps
1. ...
2. ...

## Boundaries
- Hard rules only.

## Verification
- How to prove it worked.
```

### Inherited from `create-skill`
- `---` delimiters, single atomic block (never a fenced code block).
- `name`, `uuid`, `version`, `last-used`, `thinking`, `temperature`, `resources`.
- `scope` field — always `local` for a Utility (file is the working copy; Notion is the hub copy).
- `## Steps` / `## Boundaries` sections.

### Left to Hermes
- `description` is a **capability statement** (Hermes' skill index truncates at 57 chars),
  not the name-only string the Skills format uses.
- No mandatory 2-example minimum, no research step, no `visibility` property.
- Section depth is discretionary — add `## Pitfalls` / `## Quick Reference` only when useful.
- Tuning fields default `thinking: Medium`, `temperature: 0.3`.

### Rules
- `name` = the directory name = the `uuid`-bearing skill name. Lowercase, hyphens, ≤64 chars.
- Bump `version` and set `last-used` on every edit (the publisher reads these for the Hub row).
- `uuid` stays `TBD` until the n8n workflow creates the Hub page and returns the real id;
  write it back into the file's header on the next edit.
- One workflow per Utility; if two variants emerge, split into two Utilities.

---

## Pipeline (write-back on every touch)

```
skill_manage (create/patch/edit)
        │  on_skill_lifecycle hook
        ▼
skill-publisher plugin   ──POST──▶  n8n webhook  ──▶  Notion AI Hub
  (Skills dir  → Type=Skills)                    └──▶  Open WebUI (optional)
  (Utilities   → Type=Utilities)
```

- **Plugin:** `~/.hermes/plugins/skill-publisher/` (this profile). Fires on skill lifecycle
  `created` / `patched` / `edited` for any skill under a configured target dir; `deleted`
  publishes an archive signal. `loaded` (a use, not an edit) is ignored.
- **Targets** (`plugins.skill_publisher.targets`, or auto-derived): each maps a dir to a Notion
  `Type` (+ optional `Category`). Default: every `skills.external_dirs` → `Skills`;
  `skills.create_dir` → `Utilities` / `utilities`. Skills resolving to none are never published.
- **Payload:** `{event, action, skill, provenance, session_id, path, notion_type,
  notion_category, ts, content}` where `content` is the full SKILL.md.
- **Config:** webhook from `SKILL_PUBLISH_WEBHOOK` (`.env`) or
  `plugins.skill_publisher.webhook` (`config.yaml`). Disable with
  `plugins.skill_publisher.enabled: false`.
- **Out-of-band edits** (editing a SKILL.md directly, not through Hermes) are **not** caught by
  the hook. If those must write back too, add a filesystem watcher that POSTs the same payload.

## Notion mapping
- `Name` ← frontmatter `name`
- `Type` ← target dir (`Skills` or `Utilities`)
- `Category` ← target config (Utilities) or preserved by n8n on update (Skills)
- `Description` ← frontmatter `description`
- `Version` ← frontmatter `version`
- `Last Used` ← frontmatter `last-used`
- Page body ← the full SKILL.md
