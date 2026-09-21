---


name: create-shortcut

uuid: 35e24dc8-ccd9-8187-8c35-f6d1877e6b3a

version: 7

description: "Create Shortcut"

tools:

  - notion-fetch

  - notion-create-pages

thinking: "Medium"

temperature: 0.3

resources:

  - "@AI-Hub-DB"

  - "@Skill-Template"


---


# create-shortcut

Creates prompt shortcuts — a lightweight, LLM-agnostic instruction format. No YAML frontmatter, no tool-specific syntax, no platform UUIDs. Any LLM in any tool (Claude, Gemini, GPT, Copilot) can read and follow a Recipe without configuration.

A Recipe has five sections: a header, a Context block (with a Resources h3 inside it), numbered Steps, Boundaries, and Examples.

Invoke via `/create-shortcut`.


---


## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

### 1. Determine mode

Identify which of four modes applies:

- **New** — user provides a brief or description; build from scratch

- **From skill** — user provides a [SKILL.md](http://skill.md/) source (pasted text, Notion UUID, or URL); convert it

- **From gem** — user provides a Gemini Gem instruction block; convert it

- **From chat **— user asks to reverse engineer the current chat as an efficient prompt.

If unclear, ask one question: "Are you creating a new recipe, or converting an existing skill or Gem?"

### 2. Ingest the source (conversion modes only)

**From skill:**

- Accept pasted [SKILL.md](http://skill.md/) text, or a Notion UUID/URL — if a link is provided, fetch via Notion MCP

- Identify: skill name, description, steps, resources, boundaries, tools

- Note all @resource-name handles and their current UUID values

- **Identify invocation argument patterns**: look for template switches, mode flags, or argument-driven branches in the source skill's Invocation block (e.g. `doc-author prd`, `skill new|update|delete`). These must be preserved in the recipe as a switch table in the Context section — do not collapse them into a single default path.

**From gem:**

- Accept pasted Gem instruction block

- Identify: trigger, task blocks, resource handles, boundaries

- Map task-and-output blocks back to plain sequential steps

**New:**

- Confirm: recipe name, purpose, and any known resources or context documents

### 2b. Resolve resource locations (conversion modes only)

For each `@resource-name` entry in the source skill's `resources:` frontmatter block:

- If a UUID or URL is present **and** Notion MCP is available: fetch the page. Extract the human-readable title and the ancestor path (database name, Type tag). Compose a plain-language description: `"[Page Title]" in [Database] (Type: [Type]); search for "[Page Title]" to locate it`.

- If no tool is available to look up the resource: derive a plain-language description from the resource name and surrounding context in the skill. Use the pattern: `search [system] for "[inferred name]"`.

- If the UUID is empty or the fetch returns nothing: flag the resource as unresolved and note it inline in the recipe: `@resource-name: location unknown — ask the user to provide this`.

The goal is that every resource entry in the final recipe is **actionable**: a human or LLM reading it cold should be able to locate the resource without additional context. A bare `@resource-name` with no location is not acceptable output.

### 3. Strip platform-specific notation

Remove or neutralise all of the following:

Preserve:

- Logical step sequence — do not reorder

- All @resource-name handles (clear UUID values, keep names, apply locations from Step 2b)

- Boundaries (rewrite as plain "Do not..." rules)

- Examples (preserve structure; strip platform references)

### 4. Rewrite skill calls as explicit prose

Any step that invokes another skill or sub-agent must be written as an explicit numbered instruction, not a slash command:

**Format:** `Run the skill '[skill-name]' with [input description] — find it at @[resource-location].`

Examples:

- `Run the skill 'mcd-manager' with the project context — find it at @ai-hub.`

- `Run the skill 'micro-edit' over the drafted section — find it at @ai-hub.`

This ensures the instruction is executable in any tool without assuming slash-command support.

### 5. Assemble the shortcut document

Output the shortcut using this exact structure:

```javascript
# shortcut-name

> One-line description of what this recipe does and when to use it.

## Context
[Sets up how the LLM should operate. Includes: role or persona framing ("You are..."),
domain background, conventions or standards to apply, and tone. Omit if nothing meaningful to add.

If invocation argument patterns were identified in Step 2, include a switch table here:

**[Switch name]** — resolve before Step 1:

| Argument / context signal | Behaviour |
|---|---|
| `skill arg1` | [what to do] |
| `skill arg2` | [what to do] |
| No argument | [default behaviour] |
]

### Resources
- @resource-name: [human-readable location from Step 2b]
- @resource-name: [human-readable location from Step 2b]

## Steps

1. Step one.
2. Step two.
   - Sub-note or clarification if needed.
3. Step three.

## Boundaries
- Do not [X].
- Always [Y].

## Examples

**Example 1: [scenario]**
[Input] → [Expected output or behaviour]

**Example 2: [scenario]**
[Input] → [Expected output or behaviour]
```

Rules:

- `### Resources` is always h3 (not h2) and lives inside `## Context`

- Resources are listed as `- @resource-name: [actionable location]` — one per line; a bare name with no location is not acceptable

- If there are no external dependencies, omit the Resources h3 entirely

- Invocation switches go in `## Context`, above `### Resources`, as a named table

- Steps are always numbered; sub-notes use a single indent with `-`

- Boundaries are a flat plain-language list — no platform jargon

- Minimum 2 examples are required

- **Multi-path operations:** When the source skill has sequential steps for variants of the same operation (primary path + fallback), collapse them into a single recipe step. Describe the primary approach as the main instruction; note the fallback as an indented sub-note. Do not give each path its own numbered step — that overloads the recipe with technical branching the reader doesn't need to see at the top level.

### 6. Review and iterate

Present the draft. Ask: "Does this capture the intent? Anything to adjust?"

Incorporate feedback. Do not restructure unless explicitly asked.

### 7. Write to Notion and present file

Once approved:

**7a — Write to Notion AI Hub DB:**

- Create a new page in @AI-Hub-DB

- Properties: Name, Description (one-liner from recipe header), Type = `Recipes`, Version = `1`

- Write the full recipe as the page body

**7b — Present as file:**

- Write the recipe to the outputs folder: `/sessions/[workspace]/mnt/outputs/[recipe-name]/RECIPE.md`

- Present the download link


---


## Examples

**Example 1: Convert a skill with resources and argument switch (doc-author)**

Input: doc-author [SKILL.md](http://skill.md/) — has resources with Notion UUIDs, has invocation arguments (`prd`, `bc`, `proposal`, `one-pager`)

Expected output:

- Step 2b runs: each UUID fetched from Notion, titles and locations resolved (e.g. "@Opportunity-Template: 'Opportunity Template' in AI Hub (Type: Templates); search Notion for 'Opportunity Template'")

- Invocation argument switch captured as a table in the Context section

- All MCP calls rewritten as plain-language instructions

- Output: clean [RECIPE.md](http://recipe.md/) with actionable resource locations and a template switch table

**Example 2: New recipe from brief**

Input: "I want a recipe for running a weekly team status update — check Jira, summarise sprint progress, post to Slack"

Expected output:

- Context explains the cadence and audience

- Resources: `@jira-project: team Jira board — ask the user to confirm the project URL`, `@slack-channel: #team-updates — ask the user to confirm the channel name`

- Steps include explicit prose: "Run the skill 'micro-edit' over the draft message — find it at @ai-hub"

- No MCP tool names, no slash commands

**Example 3: Convert a skill with multi-path operations (pe-review)**

Input: pe-review [SKILL.md](http://skill.md/) — has separate steps for primary (.docx) and fallback (HTML) comment extraction

Expected output:

- Steps 3 and 4 (primary and fallback extraction paths) collapsed into a single recipe step: "Read the document body and comments" with the .docx path as the main instruction and the HTML path noted as an indented fallback sub-note

- Result is a 5-step recipe, not 7 — the technical branching is present but not visually dominant


---


## Boundaries

- Never include YAML frontmatter, `---` delimiters, or `uuid`/`visibility`/`tools` fields in recipe output

- Never include MCP tool names, Claude Code syntax, or slash commands in recipe output

- Never hardcode Notion UUIDs, `notion.so` URLs, or `collection://` references in recipe output

- Always use `### Resources` (h3) inside `## Context` — never as a standalone h2

- Never output a resource entry with just a name and no location — always resolve to an actionable description in Step 2b

- Never use slash-command syntax for skill calls in recipe output — always explicit prose

- Never reorder the logical sequence of steps when converting from a source

- Never give each variant of a multi-path operation its own numbered step — collapse to one step with fallbacks as sub-notes

- Never skip Step 6 (user review) before writing to Notion

- Never produce a recipe with fewer than 2 examples

- Never collapse invocation argument patterns into a single default — preserve all branches as a switch table


---


## Output

- Format: Markdown [RECIPE.md](http://recipe.md/) using the structure defined in Step 5

- Sections: name, description, `## Context` (with optional switch table and `### Resources` h3), `## Steps`, `## Boundaries`, `## Examples`

- No frontmatter, no UUIDs, no platform-specific notation

- Delivered as: Notion AI Hub page (Type = Recipes) + `/sessions/[workspace]/mnt/outputs/[recipe-name]/RECIPE.md`


---


## Resources

- @AI-Hub-DB — Notion AI Hub DB; target for writing recipe pages (Type = Recipes)

- @Skill-Template — reference for understanding source [SKILL.md](http://skill.md/) structure during conversion


---


## Next steps

Invoke with `/create-recipe`. Paste a source skill or gem to convert, or describe the new recipe you want to build.