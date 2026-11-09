---


name: notion-live-reports
uuid: 40324dc8-ccd9-8165-a120-d01501cd09a4
version: 2
description: "Notion Live Reports"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
author: clarity
license: proprietary
metadata:
hermes:
tags: [notion, report, dashboard, html, embed, scheduling]
related_skills: [openrouter-usage, token-costing]


---


# Notion live reports

Publish a self-contained HTML report into a Notion page and refresh it on a schedule. Notion renders
it inline in a sandboxed iframe — you are not limited to Notion's own block types.

## When to Use

- The user asks to embed a dashboard or report as an "HTML block" in Notion.

- A periodic report should live on a Notion page and update itself (wire the refresh into the
recurring job that already runs, rather than inventing a new one).

## Steps

1. **Build a self-contained HTML file.** Inline all CSS; no external scripts, no CDNs, no `fetch` —
the frame is sandboxed. Give it a generated-at stamp so a stale render is obvious.

1. **Upload it.** Notion MCP `create_attachment` with `filename: "<name>.html"` and `content:` the
file's text (inline path, ~200 KiB cap). It returns `suggested_markdown`, e.g.
`<embed src="file-upload://…">Caption</embed>`.

1. **Place it.** `update_page` with that markdown. On save the API resolves `file-upload://…` into a
permanent `notion-file-block://…` reference on the page.

1. **Refresh it on the next run.** Upload a **new** attachment and replace the existing
`<embed …>Caption</embed>` line. **Fetch the page first** and copy the current line verbatim — the
`src` changes on every upload.

  - `update_content` **cannot match an existing ****`<embed …>`**** block** — every variant of the stored
  markup returns `No matches found`, while plain text anchors on the same page match fine. Do not
  burn calls probing markup variants.

  - **Working refresh:** parse `<content>…</content>` out of a fresh `notion-fetch`, cut from
  `<embed` to `</embed>` in Python, splice in the new tag (keep the caption), and send the whole
  body as `command: "replace_content"` with **`new_str`** set to that body (`content` belongs to
  `insert_content`). Every `<page url="…">`, `<database …>` and `<column>` tag must be carried
  through verbatim; the tool lists any child page/database that would be deleted, so an unfaithful
  body fails safe instead of silently dropping content.

## Boundaries

- **Never put HTML in a code block or file block** — Notion shows the source, it does not render.
HTML goes through `<embed>` only.

- Uploads not placed promptly expire (~1 hour). Upload and place in the same run.

- The frame is sandboxed: no external assets, no network calls from the page.

## Pitfalls

- **Confirm the TARGET page id before writing.** A short Notion link normalises to a dashed uuid, and
two pages can differ by a single middle group. Take the id from a fresh read of the page you mean —
never from an earlier message or a neighbouring row — and read it back after the write. A
mis-targeted write lands the report on the wrong page and leaves the intended one untouched.

- **Match the stored text, not what you typed.** A no-match `update_content` returns a validation
error quoting the string it could not find. Notion stores escapes for some characters (`$` as
`\$`); when a verbatim line fails to match, remove it line by line, or target the
heading+separator together as one unique string.

- **Replacing an embed by appending a second one leaves orphans** — and the orphan cannot be deleted
(step 4). Splice the body once; never "add the new one and clean up after".

- **MCP calls whose content strings contain ****`$`****, ****`()`****, ****`-`**** break the JSON parser** — common in data
reports. Write the content to a file and call the Notion API directly, or use a string that avoids
the characters (spell out "zero dollars" instead of `$0.00`).

- **`replace_content`**** takes ****`new_str`****, not ****`content`****.** Read the `src` from whichever field
`create_attachment` returns: `markdown_source` carries the `file-upload://…` value even when
`suggested_markdown` is absent — parse both rather than assuming one shape.

## Verification

- Fetch the page and confirm the embed line is present and resolved to a `notion-file-block://…`
source.

- **Verify the bytes, not just the reference:** fetch with `include_file_urls: true`, download the
signed URL, and check the report's own generated-at stamp and expected section count. A resolved
reference only proves *an* upload landed there.

- Confirm the page's `page_last_edited_at` advanced and child pages/databases are still present.

- Confirm the rendered content is the latest revision, not a cached earlier upload.