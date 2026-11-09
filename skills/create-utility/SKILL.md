---


name: create-utility

uuid: 3fb24dc8-ccd9-814e-b5c1-e6dc2078ba5c

version: 2

description: "Create Utility"

last-used: "2026-10-16T14:24:11+02:00"

thinking: "Medium"

temperature: 0.4

resources:

- "@Skill-Template"

- "@Resource-Index"


---


# Utility Creator

Translate a capability request into a production-ready **Utility** — the small, Clarity/Hermes-local skill class — and route it to the Utilities store and the Hub. Complete, executable specifications only.

## Utility or Skill

Decide first: the two are different stores, formats, and Hub types.

If the capability transfers to another person or agent, it is a Skill — route to `$create-skill`. A Utility only matters inside this agent: tool wiring, an operating procedure, a local convention.

## Process

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Clarify.** Extract the concrete use case, who invokes it and when, success criteria, and autonomy level. Confirm it is a Utility, not a Skill. Ask at most one clarifying question, and only when genuinely necessary.

1. **Check coverage.** Search `@AI-Hub` for an existing Utility that already covers the capability; extend it rather than duplicating. No public prior-art survey is needed at Utility scale.

1. **Load @Skill-Template** (lazy — now, not at activation) for the shared header conventions only.

1. **Draft.** Apply the Utility format. YAML header — single atomic block, `---` delimiters, never a fenced code block: `name` (= directory name), `uuid: TBD`, `version`, `description` (a capability statement, ≤57 chars, ends with a period), `last-used` (current date), `scope: local`, `thinking` (Low|Medium|High), `temperature` (0.2–0.4 deterministic/technical, higher creative), `resources` (handle list; omit if none). Body keeps only the sections the procedure needs — `## Steps`, `## Boundaries`, `## Verification`; add `## Pitfalls` / `## Quick Reference` only when useful. No model-selection fields — resources and the environment define capability.

1. **Feedback.** Present the draft; incorporate without inflating it.

1. **Test.** Run 2–3 prompts — typical, edge, boundary/refusal — against the draft; present prompt → output; iterate on the affected cases.

1. **Publish.** Write `<name>/SKILL.md` into the Utilities store (`skills.create_dir`). Leave `uuid: TBD` until the write-back returns the Hub page id; write that id back into the header on the next edit. Bump `version` and set `last-used` on every edit.

1. **Hub page body.** The Hub page body is the **full **[**SKILL.md**](http://skill.md/)**, verbatim** — frontmatter written as a plain `---` … `---` header, **never inside a fenced code block** (the sync pulls the page body down verbatim as `.md`; a fence breaks the file every agent reads). The rest of the body is normal markdown; never attach the [SKILL.md](http://skill.md/) as a file.

1. **Confirm Hub.** The `skill-publisher` plugin POSTs each edit to n8n → Notion AI Hub as `Type = Utilities`, `Category = utilities`. Verify the page exists, the properties match, and the body round-trips as `.md`. Publishing is unconditional and has no review gate: never leave a utility local-only. The same rule governs every skill and persona you create.

## Updating an existing Utility

Read the current file first; never rewrite from memory. Extend or split rather than duplicate — if two variants emerge, split into two Utilities. Bump `version`, set `last-used` to today, and keep the existing `uuid`. Publish exactly as for a create (step 7); the write-back upserts the existing Hub page.

## Rules

- Utility format only — never the full `$create-skill` ceremony.

- One workflow per Utility; if two variants emerge, split into two Utilities.

- `name` = the directory name = the skill name. Lowercase, hyphens, ≤64 chars.

- No hardcoded paths, UUIDs, or URLs — reference by @handle via `@Resource-Index`; the store is `skills.create_dir`, never a literal path.

- Utilities may hold sensitive content: default to private; the Hub is the sharing boundary, never beyond it.

- Verify, never invent — no fabricated tooling, paths, or capabilities.

- Never overwrite an existing Utility without bumping `version` and `last-used`.

- Never attach the [SKILL.md](http://skill.md/) as a file to the Hub page — full content in the page body.

- Never wrap the frontmatter in a fenced code block in the Hub page body — a plain `---` header only; a fence breaks the synced `.md`.

## Taste

*Richard-originated, grown by ****`$reinforce`****. Signal → preference.*

- Hub page body = the [SKILL.md](http://skill.md/) verbatim. → Use plain `---` header delimiters, never a fenced code block (a fence breaks the file the sync pulls down).

## Examples

**"Create a utility that mounts my SMB shares for the media containers"** → single-workflow Utility, header trimmed, `## Steps` = mount → verify → unmount on failure, `## Verification` = a mount check; `scope: local`; lands in `skills.create_dir`, Hub `Type=Utilities`.

**"Codify how Clarity connects to a service via API"** → carries a credential, so sensitivity applies: reference the secret by env/handle, never inline; instructions only; confirm no secret is copied into the file.

## Output

Complete Utility `SKILL.md` (header + `## Steps` / `## Boundaries` / `## Verification`), written to `skills.create_dir` and mirrored to the Hub as `Type=Utilities`. Present the file and the three test results.

## Next steps

Invoke with the capability to codify, e.g. `$create-utility mount SMB shares for media`. A transferable capability routes to `$create-skill` instead.