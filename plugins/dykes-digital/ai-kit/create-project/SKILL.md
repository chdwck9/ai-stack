---


name: create-project

uuid: 38824dc8-ccd9-8195-a25e-fff22f31e2e3

version: 9

last-used: "2026-09-16T19:12:00+02:00"

description: "Create Project"

return: "Project Agent + MCD + Ship project + source wiring + install checklist"

tools:

  - notion

thinking: "Medium"

temperature: 0.3

resources:

  - "@Skill-Template"


---


# Create Project

Creates the complete project foundation: Project Agent, project MCD, Ship DB record, operational-source wiring, and install checklist.

## Inputs

Free-text project brief, existing spec/MCD, legacy project agent, or nothing. Gather only what is needed to create a usable project. Ask up to 5 questions; prefer inferring low-risk values.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays marked `skip: <reason>`.

### 1. Gather context

Extract name, outcome/scope, domain, timeframe, priority, stakeholders, milestones, constraints, decisions, desired skills/agent behaviour, and operational sources. Accept source links/handles such as Jira boards/filters, trackers, Grafana dashboards, GitHub, Slack and canonical docs. If an existing spec/MCD or additional source material is provided, read it first.

If timeframe is unclear, preferably ask duration; otherwise default `today → today+90 days`. Priority defaults to `#5`; use `#3` when explicitly urgent and `#1` when explicitly NB.

### 2. Build / update MCD

Create or update the project MCD using the current MCD standards. Register operational sources in the MCD's Resources section with enough metadata to retrieve and interpret them. The MCD is the durable context source of truth; do not duplicate source data into it.

### 3. Scope agent

Create the Project Agent from the current project-agent template. Publish it in AI Hub with `Type=Project` (format the page as a Skill). Include only relevant resources and skills; make the project MCD authoritative for scope, goals, constraints and decisions. Keep output `<60` lines. Define permissions from gathered context and preserve the global execution protocol.

### 4. Create Ship project

Create the project in the Ship DB. Required visibility fields:

- `Live` → `https://app.notion.com/p/chdwck9/Craft-1eb24dc8ccd98052846cd9ed921e2144`

- `Status` → `Doing`

- `Level` → `Project`

- `Priority` → assessed value, otherwise `#5`

- `When?` → supplied timeframe, otherwise today → today+90

- `Master Doc` → project MCD

- `Agent` → project Agent

Populate existing fields when supported by context: `Goals`, `Milestone`, `Phase`, `Milestones Achieved`, `Overall Progress`, `Risks & Mitigations`, `Stakeholders`, `Impact`, `Challenge / Opportunity`, `Approach / Solution`, `Who's it for?`, `Cadence`, dependencies, etc. Do not create new Ship properties.

For Mambu projects, set `Parent` to `https://app.notion.com/p/chdwck9/Mambu-31824dc8ccd980d18072dbe901d281c9`.

### 5. Source wiring

The MCD Resources section is the canonical source registry. Do not create a competing operational-resource property in Ship. Ensure the Project Agent can resolve the registered resources/handles. If a required operational source is supplied but cannot be connected, record the gap rather than inventing access.

### 6. Weekly tracking setup

For projects with a weekly cadence, state that `$track-project` will use the Ship project + MCD Resources + operational evidence and create dated child review pages under the Ship project. Review-window configuration belongs to the orchestrator, not Ship.

### 7. Verify

Re-fetch the created/updated MCD, Agent and Ship project. Confirm required Ship fields, relations, source wiring and Agent/MCD links. Repair only specific defects found; do not regenerate unrelated content.

### 8. Install checklist

Output:

- [ ]Project Agent published in AI Hub with `Type=Project` and Skill formatting, then installed in the intended agent/project environment

- [ ]MCD registered and linked as `Master Doc`

- [ ]Ship project created with required visibility fields

- [ ]`Agent` linked to the project Agent

- [ ]Operational sources registered in the MCD Resources section

- [ ]`$track-project` scheduled/invocable for the chosen cadence

- [ ]Any required connectors enabled

## Agent template

```yaml
---
name: [slug]
uuid: TBD
version: 1
description: "[Project Name] Project Agent"
tools:
  - [tools]
resources:
  - "@[handle]"
---
# [Project Name]
[One-liner.]
## Project instructions
[Constraints / behaviour overrides.]
## Permissions
**Always:** / **Ask first:** / **Never:**
## Resources
| Handle | Description | Location | Tool |
|---|---|---|---|
## Skills
| Skill | When to use | Load |
|---|---|---|
## Agent rules
- Resources are lazy-loaded unless marked eager.
- Resolve @handles from this table first.
- Treat the project MCD as source of truth for scope, goals, constraints and decisions.
- Maintain decision/rationale, risk/blocker, dependency, milestone and hand-off state where relevant.
- Use `$track-project` for weekly project review; use `$mcd-sync` for durable context synchronisation.
## Agent mode
**Auto-approved:** [read actions]
**Ask first:** [write/update actions]
**Never:** [hard stops]
```

Remove empty sections and keep `<60` lines.

## Boundaries

- Never write to Ship, MCD or Agent before context gathering is sufficient.

- Never fabricate resources, source locations, project relationships or permissions.

- Never create a parallel source registry or project-status database.

- Never create Ship properties; use the existing schema.

- Never omit required Ship visibility fields.

- Never treat operational systems as durable context; route meaningful findings through `$mcd-sync`.

- Never create weekly status files; `$track-project` uses dated Ship child pages.

- Never include irrelevant cross-project resources without explicit confirmation.

- Never exceed 5 clarification questions.

- Never exceed 60 lines in the generated Project Agent.