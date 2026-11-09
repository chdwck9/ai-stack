# Ship — projects (rebuilt standard, partial)

**Rebuilt** 2026-11-09 after `references/ship-projects.md` was lost to the nightly Hub→local skill
sync. Grounded in `@Ship-DB-Reference` and `$create-project`; the **consolidation rules are NOT
recovered** — see Blanks.

## What a Project is

`Level = Project` in Ship. Used for **planning and roadmaps**, and it also **creates a folder in
Richard's documents** via an automation — so a project is the conceptual grouping of tasks,
milestones and knowledge, not just a label.

Tasks are no longer linked directly to milestones; they link to the pillar through `Live`.

## Visibility

- **Roadmap view** requires: `Level ∈ {Project, Milestone}` · `Archive? = false` ·
  `Status ∈ {Backlog, Waiting, Do next, Doing}` · `Priority ∈ {#1,#3,#5}` ·
  (`Parent` empty **or** `When?` set).
- `Live` is effectively mandatory (a project with no pillar is an orphan).

## Creating one ($create-project)

A project is a bundle, not a row — the row is step 4 of five:

1. Gather context (name, outcome/scope, domain, timeframe, priority, stakeholders, milestones,
   constraints, decisions, operational sources). Timeframe defaults to today → +90 days.
2. Create/update the project **MCD** — durable context of truth; do not duplicate source data into it.
3. Create the **Project Agent** (`Type=Project` in the AI Hub, formatted as a Skill, <60 lines).
4. Create the **Ship project row**, minimum:
   `Live` (pillar) · `Status = Doing` · `Level = Project` · `Priority` (default `#5`) ·
   `When?` = timeframe (default today → +90) · `Master Doc` → MCD · `Agent` → the agent.
5. Wire operational sources (Jira, Grafana, GitHub, Slack, docs) into the MCD's Resources.

Populate `Goals`, `Milestone`, `Phase`, `Milestones Achieved`, `Overall Progress`,
`Risks & Mitigations`, `Stakeholders`, `Impact`, `Challenge / Opportunity`, `Approach / Solution`,
`Who's it for?`, `Cadence`, dependencies when context supports them. **Never create new properties.**

## Reviewing one

`track-project` appends a dated block to the **project page body** (inline, never a child page):
Plan / Achieved / Missed / Why / Risks / Next / Evidence. `weekly-status-update` uses `Shipped` rows
as the completion ground truth.

## Consolidation — case by case (Richard, 2026-11-09)

There is **no automatic merge rule**. When two Project rows look like the same project, **highlight
both and let Richard decide**; don't merge, archive or re-parent anything on your own initiative.
Treat a suspected duplicate as a finding in the report, not a clean-up task.

## The documents folder (Richard, 2026-11-09)

Confirmed live: creating a Project runs an **n8n workflow in `n8n-prod` — "Second Brain"** — which
creates the folder tree on the NAS:

```
/volume1/Ship/[project parent]/[sub-projects or phases]
```

So the Project's hierarchy (parent → child projects/phases) is what makes the folder tree, not the
name alone. Don't create folders by hand; the automation owns them.

## Still open

- Whether `Project` rows are ever used without a Master Doc (legacy projects).
