---


name: setup

uuid: 3d824dc8-ccd9-811d-ba97-fd8d09cc15c8

version: 3

description: "Setup"

return: "environment profile + emitted files + memory delta"

tools:

  - notion

thinking: "High"

temperature: 0.3

resources:

  - "@Resource-Index"

  - "@Engineering-Principles"

  - "@Memory"

  - "@AGENTS"


---


# Setup

Bootstrap any environment into Richard's OS: detect the surface and its constraints, emit the governing instructions and resource file adapted to it, and seed memory. Run once per new environment, or after major OS changes.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Detect (probe, don't ask — P3).** Test: durable FS write access (ephemeral sandboxes don't count)? bash? subagents/tasks? Which MCPs (Notion, Drive, Atlassian, Slack)? Skill install mechanism (capabilities upload / skills folder / none)? Set mode: durable FS present → `mambu` (work paths / Mambu MCPs) or `local` (personal); no durable FS → `generic`. A mode is only valid if its endpoints are reachable — else fall back to `generic`. Record an environment profile.

1. **Emit governing file** — fetch @AGENTS from @AI-Hub first: it is the master copy of the eight sections. If present, adapt only the environment-specific parts — the §1 mode line and the §7 Model Mode Map — never regenerate the rest from scratch. If absent, generate from the section spec below and create @AGENTS from the result in step 6. Target: [CLAUDE.md](http://claude.md/) (Claude Code), [AGENTS.md](http://agents.md/) (other agent runtimes), or a project-instructions block to paste ([claude.ai](http://claude.ai/)). Exactly eight sections, adapted to the profile, ≤80 lines total:

  1. Resources — @Resource-Index pointer, detected mode, lazy row-fetch (never load the whole index), Master-write-only.

  1. Ethos — direct, no fluff; plan first; surface alternatives; lean everything; ask when the goal is unclear.

  1. Principles — pointer to @Engineering-Principles; cite P-IDs when a principle drives a choice.

  1. Guardrails — P15 token budget (rows not tables, compressed hand-offs, shortest complete output); universal write guard; halt conditions.

  1. Autonomy — P18 calibrated autonomy + the agent loop (goal → plan → execute → gate check → single summary).

  1. Skills — list what is installed here; anything else is invoked as $[skill-name] → fetch that [SKILL.md](http://skill.md/) from @AI-Hub by Name at run time and follow it.

  1. Model Mode Map — tier → model table for this environment's vendor(s); the only place tiers resolve to model names.

  1. Memory — @Memory pointer; when to run /memory export/import.

1. **Emit local resource file** (durable-FS environments only): derive $AI/[resources.md](http://resources.md/) from @Resource-Index — this mode's column as Handle | Endpoint | rw/ro | index version. On [claude.ai](http://claude.ai/): skip: no FS.

1. **Seed memory.** Run /memory import. If @Memory doesn't exist yet: skip: @Memory absent — recommend /memory export from the richest environment first.

1. **Verify (P3, P17).** Re-read the emitted files; prove resolution by resolving one handle end-to-end in this environment; report the environment profile, files written, memory delta.

1. **Sync @AGENTS.** Diff the emitted file against @AGENTS. Changes beyond the per-environment adaptations (§1 mode line, §7 map) are written back to @AGENTS with a version bump; if @AGENTS doesn't exist, create it (Type = Lookups, Visibility = private, patch UUID, register in @Resource-Index). No material changes → no write.

## Boundaries

- Never overwrite an existing [CLAUDE.md/AGENTS.md](http://claude.md/AGENTS.md) — diff, merge, and preserve user content; confirm before structural changes

- Never embed endpoints or UUIDs beyond the @Resource-Index pointer itself — everything else resolves at run time

- Never put vendor model names anywhere except the Model Mode Map

- Never ask what the environment is when it can be probed

- Never fork the governing content — @AGENTS is the single master; environments adapt §1 and §7, they never diverge on the rest

- Never skip the verify step; never emit a governing file over ~80 lines

## Output

Artefact contract: environment profile (surface, mode, capabilities); governing file with all eight sections; [resources.md](http://resources.md/) when durable FS exists; memory delta or explicit skip note; one end-to-end handle resolution proof; @AGENTS synced or an explicit no-change note. Hand-off: files written in place; a copy to $AI/artefacts/setup/<yyyy-mm-dd>-<surface>/ on FS environments; [claude.ai](http://claude.ai/) → workspace outputs + paste block.

Self-check gate: before finishing, verify every contract element; anything missing → do the work, do not finish.

## Examples

1. Fresh Claude Code on the work laptop → durable FS, bash, subagents, Notion+Drive MCPs → mode mambu. [CLAUDE.md](http://claude.md/) emitted (8 sections, 74 lines); $AI/[resources.md](http://resources.md/) derived (mambu column); /memory import writes 20+ entries; proof: @BCaaS-OS resolved to $AI/BCaaS OS/[index.md](http://index.md/) and read.

1. [claude.ai](http://claude.ai/) → sandbox FS is ephemeral → mode generic. Paste block emitted; [resources.md](http://resources.md/) skip: no FS; /memory import via memory store, unstorable categories skipped with note; proof: @Ship-It fetched via Notion.

## Next steps

Run in every environment once after installing. Re-run after @Resource-Index or @Engineering-Principles structural changes.