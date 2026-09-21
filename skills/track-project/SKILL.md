---


name: track-project

uuid: 36824dc8-ccd9-81c1-bea5-cf56c46a6ddd

version: 5

last-used: "2026-09-16T19:12:00+02:00"

description: "Weekly Project Review"

tools:

  - notion

  - Read

  - Write

thinking: "Medium"

temperature: 0.2


---


# Track Project

Reconstructs a project's current state each review cycle from its Ship record, registered operational sources, and MCD. Writes a dated child update to Ship and routes durable findings to `$mcd-sync`/`$mcd`.

## Source of truth

- **Ship DB:** personal project registry, current human-facing state and review history.

- **Operational sources:** company systems such as Jira, trackers, dashboards, GitHub, Slack and docs; evidence only.

- **MCD:** durable project context, decisions, risks, ambiguities and resources.

- **Agent/orchestrator:** cadence and review window; do not store review-window configuration in Ship.

Never create a competing project/task database or duplicate operational data into the MCD.

## Review flow

1. Resolve the Ship Project page. If none is specified, use active `Level=Project` records with a due/active timeframe and the configured cadence; do not invent projects.

1. Read the project's current properties, previous dated child update, linked MCD (`Master Doc`) and Agent.

1. Read the MCD Resources section to discover registered operational sources. Do not use a separate Ship resource registry unless explicitly configured.

1. Determine the review window from the orchestrator/previous review date. Prefer `previous review → now` so missed runs do not create gaps.

1. Search **Ship DB** for activity in the review window, not just the Project row. Include `Level=Milestone` and `Level=To Do` items. Milestones may have a parent Project relation, but may also be parentless. To Do items are not parent-linked, so assess likely project ownership from the item name and other available fields/context. Treat these as candidate evidence, not definitive attribution: use naming/context, MCD, project terminology and timing to decide relevance; flag ambiguous matches rather than silently attaching them.

1. Query registered operational sources for meaningful changes in the window. For Jira, inspect planned/targeted work, completed/reopened/blocked/overdue items, milestone movement, scope changes and significant decisions/comments. Adapt to other sources according to their purpose.

1. Reconcile the Ship activity with operational evidence and reconstruct **Plan → Achieved → Missed → Why → Risks/Decisions → Next**. Use Ship Milestones/To Dos to recover intended or completed work that may not be represented in the operational source, while avoiding duplicate reporting. Distinguish observed facts from interpretation. Never infer a missed item without evidence.

1. Update the Ship project's existing state fields only where justified: `Status`, `Phase`, `Milestone`, `Milestones Achieved`, `Overall Progress`, `Risks & Mitigations`, and other existing project fields when a durable change is evidenced. Do not add new properties.

1. Create a child page under the project, named `YYYY-MM-DD`, containing:

  - **Plan** — what was expected this period

  - **Achieved** — material outcomes

  - **Missed** — planned work not achieved

  - **Why** — evidence-based causes

  - **Risks / decisions** — emerging risks or decisions required

  - **Next** — next meaningful actions/milestones

  - **Evidence** — links/references to sources consulted

  Keep it concise; this is a historical snapshot, not a ticket dump.

1. Classify findings before MCD hand-off:

  - **Noise:** no durable context change; do not sync.

  - **Signal:** meaningful project-context change; route to `$mcd-sync`.

  - **Decision / risk / ambiguity / learning:** route to `$mcd-sync` for appropriate MCD update.

  Never write raw ticket activity into the MCD.

1. If no meaningful evidence exists, write a dated child update stating that the period was quiet and leave state unchanged.

## Output

Return the updated Ship page, dated review child, source evidence used, and any MCD hand-off. If a source could not be queried, state which one and why; do not fabricate results.

## Boundaries

- Never create local `status.md` files or folders.

- Never overwrite prior dated updates; append a new child page.

- Never treat ticket counts or completion percentages as project health by themselves.

- Never update Ship state without evidence.

- Never update the MCD directly when `$mcd-sync` is the required routing layer.

- Never invent source locations, project relationships or missing activity.

- Never create Ship properties; use the existing schema.

- If the project is ambiguous, ask rather than guessing.