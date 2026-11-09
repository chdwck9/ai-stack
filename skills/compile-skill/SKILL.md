---


name: compile-skill

uuid: 3a024dc8-ccd9-81d0-a0fb-f43c32873776

version: 6

description: "Compile Skill"

thinking: "Medium"

temperature: 0.3


---


# Compile Skill

Takes a [SKILL.md](http://skill.md/) file and produces a self-contained, portable package: all referenced resources are pulled and written as local `.md` files, tool dependencies are scrubbed, personal or environment-specific references are generalised, and the whole thing is zipped for sharing or migration to another account.

Invoke with a path or pasted content of a [SKILL.md](http://skill.md/). Output is a `.zip` file.


---


## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

### Step 1 — Ingest the skill

Accept the [SKILL.md](http://skill.md/) via one of:

- A file path (e.g. `/path/to/SKILL.md`)

- Pasted raw content in the prompt

- A handle (e.g. `@BCaaS-OS`) — resolve to its [SKILL.md](http://skill.md/) first

Parse the YAML header and body. Extract:

- `name` — used as the zip folder name

- `tools:` block — record all declared tools

- `resources:` block — record all `@RESOURCE-NAME` handles

- All `@RESOURCE-NAME` references in the body text

- Any inline URLs, UUIDs, or file paths in the body

Flag any discrepancy between resources declared in the YAML header and those referenced in the body. Resolve the union — compile all of them.


---


### Step 2 — Identify compilation targets

Scan the full skill (header + body) for:

**2a — Resources to fetch:**

All `@RESOURCE-NAME` handles (from YAML and body). These become `.md` files in `/resources`.

**2b — Tool calls to scrub:**

- `tools:` entries in the YAML header (e.g. `- notion`, `- google-drive`)

- Any step instructions that require a specific MCP tool (e.g. "call notion-fetch", "search @AI-Hub-DB", "use google-drive to retrieve", "invoke Notion:notion-search")

- Lazy-load or eager-load instructions tied to a specific tool

**2c — Personal/environment-specific references to generalise:**

- UUIDs (Notion page IDs, database IDs)

- Hardcoded account names, workspace names, or email addresses

- Handle definitions that point to personal data stores

- Preference-specific instructions (e.g. hardcoded output folder paths)

- Any path rooted at a personal home directory

**2d — Examples, tests, scripts to split:**

- If the full [SKILL.md](http://skill.md/) body exceeds 1000 words: move `## Examples` content to `/examples/examples.md`

- Any fenced code blocks with a declared test purpose: move to `/tests/` with appropriate extension

- Any fenced code blocks that are standalone scripts (bash, python, js, etc.): move to `/scripts/` with appropriate extension and a boilerplate shebang/header

**2e — Sub-skills to embed (recursive):**

Scan the full body for `/skill-name` invocations (e.g. `/reconcile-spec`). These are callable sub-skills that a user of the portable package will also need. For each found:

- Locate the sub-skill's [SKILL.md](http://skill.md/) (via skill registry search or filesystem)

- Apply the full compilation pass to it: tool-scrub (Steps 4a–4c), personalisation-generalise (Step 5), UUID replacement — exactly as done for the main skill

- Then scan that sub-skill's body for its own `/skill-name` invocations and compile those too, placing all of them flat in the same `sub-skills/` folder (no nesting)

- Recursion depth limit: 2 levels. Beyond that, write a placeholder and note the chain in the manifest

- If a sub-skill cannot be located at any level, write a placeholder stub with the skill name and a note that the user must supply it

Present the compilation manifest to the user as an informational summary (no confirmation required — compilation proceeds immediately after):

```javascript
Compilation manifest for: [skill-name]

Resources to fetch (N):
  - @Handle-1 → resources/handle-1.md  [flat — no child pages]
  - @Handle-2 → resources/handle-2/  [hierarchical — N child pages at L1, M at L2]

Sub-skills to embed (N):
  - /skill-name → sub-skills/skill-name.md
  - /other-skill → sub-skills/other-skill.md  [NOT FOUND — placeholder will be written]

Tool calls to scrub (N):
  - YAML tools: notion, google-drive
  - Body: [list step references being scrubbed]

References to generalise (N):
  - UUID abc123 → [REPLACE: your-uuid]
  - Path /Users/... → [REPLACE: your-path]

Content to split out (N):
  - Examples → examples/examples.md  [reason: body > 1000 words]
  - Script in Step 4 → scripts/setup.sh

Optimisation opportunities (confirmation required before applying):
  - [Any redundancies or structural improvements spotted]
```

If optimisation opportunities are found, list them in the manifest and pause only on those — ask before applying. All other compilation steps proceed without confirmation.


---


### Step 3 — Fetch and write resources

For each `@RESOURCE-NAME` handle:

**3a — Resolve the handle:**

Use whatever tool is available in the current environment to fetch the resource content. If no tool is available, write a placeholder file:

```markdown
# [Resource Name]

> **Placeholder — resource not fetched.**
> Original handle: `@RESOURCE-NAME`
> Source: [URL or UUID if known]
>
> To populate this file: retrieve the content from the source above and paste it here.
```

**3b — Write to ****`/resources`****:**

- Filename: kebab-case version of the handle name, `.md` extension (e.g. `@BCaaS-OS` → `bcaas-os.md`)

- Strip any personal metadata from the fetched content (author names, personal UUIDs, account-specific paths) before writing

- If the resource is itself a [SKILL.md](http://skill.md/), write it as-is (it is a reference document, not being compiled)


---


### Step 4 — Rewrite the skill body (single pass)

Perform all body rewrites in one pass:

**4a — YAML header:**

Remove the `tools:` block entirely from the compiled [SKILL.md](http://skill.md/) header.

**4b — Handle references + tool-specific instructions:**

For each step that calls a named MCP tool or tool-specific method, and for every `@RESOURCE-NAME` reference:

- Remove the tool call instruction

- Replace with a generic instruction that achieves the same goal using the local `/resources` files instead

Examples of replacement patterns:

Every tool-specific instruction has a portable equivalent. Rewrite it as the intent, not the mechanism.

**4c — Validate:**

After scrubbing, re-read the compiled body. Confirm no tool names remain (notion, google-drive, slack, atlassian, granola, etc.). If any remain, flag them to the user.


---


### Step 5 — Generalise personal references

For each item identified in Step 2c:

- **UUIDs:** Replace with `[REPLACE: descriptive-label]` placeholder

- **Personal paths:** Replace with `[REPLACE: your-path-to-X]`

- **Account/workspace names:** Replace with `[REPLACE: your-workspace-name]`

- **Personal handles pointing to private data:** Replace the handle reference with a note: `<!-- COMPILED: @Handle was personal data. Describe your equivalent here. -->`

- **Preference-specific instructions:** Rewrite as a general instruction with a note indicating the original was a personal preference

Do not remove content — generalise in place so the compiled skill remains structurally complete.


---


### Step 6 — Split examples, tests, and scripts

**6a — Examples (if body > 1000 words):**

- Move `## Examples` section content to `/examples/examples.md`

- Replace in [SKILL.md](http://skill.md/) body with: `## Examples\n\nSee [examples/examples.md](examples/examples.md)`

**6b — Tests:**

For each fenced code block identified as a test:

- Write to `/tests/test-[n].[ext]` with a boilerplate header comment

- Replace in [SKILL.md](http://skill.md/) body with a reference

**6c — Scripts:**

For each standalone script block:

- Write to `/scripts/[name].[ext]` with appropriate shebang and boilerplate

- Replace in [SKILL.md](http://skill.md/) body with a reference


---


### Step 7 — Assemble and zip

Build the following folder structure under a root folder named `[skill-name]/`:

```javascript
[skill-name]/
├── SKILL.md
├── resources/
│   ├── flat-resource.md          ← single-page resource
│   └── hierarchical-resource/    ← resource with child pages
│       ├── index.md              ← L0 content
│       ├── s1-overview.md        ← L1 child
│       ├── s2-scope.md           ← L1 child
│       └── s3-constitution/      ← L1 child that itself has children
│           ├── s3-constitution.md
│           └── s3a-sub.md        ← L2 child
├── sub-skills/
│   └── skill-name.md      ← one per /skill-name invocation found in body
├── examples/
│   └── examples.md        (only if body > 1000 words)
├── tests/
│   └── test-1.[ext]       (only if tests present)
└── scripts/
    └── script-name.[ext]  (only if scripts present)
```

Omit empty folders. Write a `README.md` at the root if more than 3 resource files are present, listing what each file is and how it maps to the original handle.

Zip the folder and present to the user for download.


---


## Examples

**Example 1: Simple skill, flat resource**

> `/compile-skill` invoked on a 400-word skill with one resource (`@Document-Standards`, a single Notion page with no child pages) and one declared tool (`notion`).

Expected behaviour: Fetches `@Document-Standards` — no child pages found → writes `resources/document-standards.md` (flat). Scrubs `tools: notion` from YAML. Body under 1000 words — examples stay inline. Outputs `skill-name.zip` with `SKILL.md` + `resources/document-standards.md`.

**Example 4: Hierarchical resource (Notion index page with child sections)**

> `/compile-skill` invoked on a skill with `@Mambu-Pricing-Engine-OS`, a Notion page that has 18 child section pages (§1–§18), each of which is a leaf (no further children).

Expected behaviour: Fetches L0 index → finds 18 `<page url>` child links → creates `resources/mambu-pricing-engine-os/`. Writes `index.md` (L0). Fetches all 18 children → writes `s1-overview.md`, `s2-scope.md`, … `s18-cpq-interface.md` (all L1, all flat). Appends links from `index.md` to each child file. No L2 children found — stops. Manifest shows: `@Mambu-Pricing-Engine-OS → resources/mambu-pricing-engine-os/ [18 child pages at L1, 0 at L2]`.

**Example 2: Large personal skill**

> `/compile-skill` invoked on a 1800-word skill with 4 resources, tools `notion` and `google-drive`, personal UUIDs in the body, and a bash script in one step.

Expected behaviour: Fetches all 4 resources (strips personal metadata). Scrubs both tools from YAML. Rewrites tool-specific step instructions to use local files. Replaces personal UUIDs with `[REPLACE: ...]` placeholders. Splits examples to `/examples/examples.md`. Moves bash script to `/scripts/setup.sh`. Surfaces optimisation opportunities before zipping. Outputs zip with full folder structure + `README.md`.

**Example 3: Skill with unfetchable resource**

> `/compile-skill` invoked in an environment where no fetch tools are available.

Expected behaviour: Writes placeholder `.md` files for each resource. Notes in manifest that resources were not fetched. All other steps proceed normally.


---


## Boundaries

- Never apply optimisations without explicit user confirmation

- Never delete content — generalise or replace with placeholders, never remove

- Never include personal UUIDs, email addresses, or private paths in compiled output

- Never zip before Step 4c validation confirms no tool names remain in the body

- Never fetch resources eagerly at invocation — resolve only when Step 3 is reached

- Never write a `README.md` if the resources folder has 3 or fewer files

- If the input [SKILL.md](http://skill.md/) has no resources, tools, or personal references: flag it in the manifest as "may already be portable" and proceed — do not block

- Never modify source files — compiled output only; originals are never touched

- Never apply optimisations without explicit user confirmation; all other steps run without a gate


---


## Output

- **Compilation manifest**: inline in chat before compilation begins

- **Zip file**: `[skill-name].zip` containing `SKILL.md`, `/resources`, `/sub-skills`, and any applicable `/examples`, `/tests`, `/scripts` folders — presented as a downloadable file

- **Chat artefact mode**: if the user requests the compiled skill as a chat artefact (e.g. "output as artefact" or "embed in chat"), present the compiled `SKILL.md` content as a markdown artefact instead of (or in addition to) the zip


---


## Next steps

Invoke with a [SKILL.md](http://skill.md/) path, pasted content, or handle. Compile Skill will present a manifest, then immediately build the package.