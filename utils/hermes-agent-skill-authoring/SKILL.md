---


name: hermes-agent-skill-authoring

description: "Author in-repo [SKILL.md](http://skill.md/) files: frontmatter and structure."

version: 2.0.0

author: Hermes Agent


---


# Skill Authoring

## Frontmatter Conventions

Every [SKILL.md](http://skill.md/) starts with a YAML header block:


---


name: <skill-name>

description: "<concise capability statement, under 60 chars>"

version: <major.minor>

scope: hub | local | synced

local-path: "<absolute path>" | omitted


---


## Body Structure

1. When to Use - trigger conditions (1-2 lines)

1. Steps - numbered, imperative instructions

1. Examples - Richard says X → route to Y

1. Boundaries - what never happens

1. Output - how user verifies completion

## Pitfalls

- One rule per line; never merge two rules into a single bullet.

- Do not invent a step without citing evidence (session excerpt, source link, or Richard's correction).

- If a step conflicts with authority boundaries, document the conflict explicitly.