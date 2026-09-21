---


name: sync-resources

uuid: 36624dc8-ccd9-81e1-898c-d60b6dce4801

version: 6

description: "Sync Resources"

thinking: "Low"

temperature: 0.1

tools:

  - notion

resources:

  - "@global-instructions"


---


# sync-resources

Write each local markdown file to its declared Notion page. One file at a time. Local is always the source of truth.


---


Copy the steps below verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

## Step 1 — Build candidate list

Load the handle table from @global-instructions. For each row, extract:

- `local_path` — first location starting with `/` or `~/`

- `notion_id` — first location starting with `notion://`, stripped to bare UUID (`8-4-4-4-12` format)

- `tool` — declared tool value

A row is a **candidate** if it has a local_path AND a notion_id AND tool = `notion`.

Skip silently: no local_path, or tool = `google-drive` or `atlassian`, or bare `https://` only.

**Path normalisation:** If a declared path begins with `/Users/[user]/Library/CloudStorage/SynologyDrive-Live/@Edge/`, also try the equivalent `/sessions/[session-id]/mnt/@Edge/` path. Use whichever is accessible.

**Scope note:** This skill only syncs top-level handle table entries. Child pages nested under a handle (e.g., BCaaS OS child pages under @BCaaS-MCD) have no handle table entry and are out of scope — maintain them via direct Notion API calls outside this skill.


---


## Step 2 — Process each candidate

Repeat Steps 2a–2d for each candidate, one at a time. Do not start the next until the current completes.

### 2a — Resolve file path

Try the declared local_path as-is. If not found, try appending `.md`. If still not found: log `SKIP @handle — not found` and move to the next candidate.

### 2b — Read file

Read the resolved file path.

### 2c — Resolve wikilinks

For each `[[...]]` pattern in the content:

1. Parse: `page_name` (everything before `|` or `#`), `display_text` (after `|` if present), `heading` (after `#` — discard silently)

1. Look up `page_name` in the handle table — match against any handle alias or the filename stem of any `local_path` (case-insensitive)

1. If found: build URL = `https://notion.so/` + notion_id with dashes removed. Replace:

  - `[[page_name]]` → `[page_name](url)`

  - `[[page_name|display]]` → `[display](url)`

1. If not found: replace with `display_text` or `page_name` as plain text

### 2d — Write to Notion

Call `notion-update-page` with:

- `page_id` = the candidate's notion_id

- `command` = `replace_content`

- `new_str` = the resource body text (resolved text from 2c)

Do not update title, properties, or metadata. Do not exit until the remote resource matches the local one.

Log: `✓ @handle` on success. `✗ @handle — [error]` on failure.


---


## Step 3 — Output summary

Print all log lines from Step 2.

**Total-skip diagnostic:** If every candidate was SKIPPED (none succeeded), output the following warning block instead of a bare SKIP list:

> ⚠ All candidates skipped — no local paths were accessible.

> 

> Likely cause: SynologyDrive is not mounted in this environment (Cowork sessions mount only the selected workspace folder; @Edge is unavailable). The path normalisation fallback to /sessions/[id]/mnt/@Edge/ also requires @Edge to be mounted.

> 

> Manual workaround: run this skill from a session where SynologyDrive is mounted. For child pages (e.g., BCaaS OS pages under @BCaaS-MCD), update via direct Notion API calls (notion-update-page with update_content or replace_content per page).


---


## Boundaries

- Never sync remote → local in upload mode or on scheduled runs — download mode is the only permitted Notion → local path, and it is manual-only

- Never run download mode on a schedule — halt if attempted

- Never update Notion page titles, properties, or metadata — body content only

- Never delete Notion pages

- Never attempt sync for `google-drive`, `atlassian`, or bare `https://` targets

- Always process one candidate at a time — complete 2a–2d before moving to the next

- If the handle table cannot be loaded: stop immediately


---


## Output

Brief log of results, one line per candidate processed. If all candidates were skipped, output the total-skip diagnostic block from Step 3.