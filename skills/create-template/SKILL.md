---


name: create-template

uuid: 37324dc8-ccd9-8121-ba98-f801566db215

version: 6

description: "Create template"

tools:

  - web_search

  - notion

thinking: "Medium"

temperature: 0.4

resources:

  - "@AI-Hub-DB"

  - "@Templates"

  - "@global-instructions"


---


# Create Template

Creates a new template in the AI Hub and registers it with a global @handle.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Identify archetype** — Infer the ideal template builder from the template's purpose. Examples: idea proposal → Head of Product Strategy; PRD → Head of Product Management; runbook → Principal Engineer; editorial brief → Editor-in-Chief. State the chosen archetype in one line, then reason from that perspective through all subsequent steps.

1. **Research** — Web-search best practices for the template type, framed through the archetype's lens. Summarise 3–5 recommended sections with brief rationale. Present findings and proposed structure. Wait for confirmation before proceeding.

1. **Draft template** — Build the template in Markdown using the confirmed structure. Keep it lean — every section must earn its place.

1. **Write to Notion** — Create a new page in @AI-Hub-DB with `Type = Templates`. Set Name, Description. Write the template as the page body. Capture the returned UUID.

1. **Register handle** — Propose an `@handle` name following the pattern in @global-instructions. Add a row to the global resource table inline with: handle, description, Notion URL (using the UUID from Step 4), and Tool = notion. Present the updated row for confirmation before writing.

## Boundaries

- Never register a handle without user confirmation of the name

- One template per invocation

## Output

Notion page URL + updated resource table row, ready to paste into @global-instructions.

## Taste

*Richard-originated, grown by **`$reinforce`**. Signal → preference.*

- Hub page body = the file verbatim. → Plain `---` header delimiters (`---` / `name:` / `description:` / … / `---`), never a fenced code block — a fence breaks the file the sync pulls down.

- Never wrap the header in a fenced code block when writing a page to the Hub — plain `---` delimiters only; a fence breaks the synced `.md`.