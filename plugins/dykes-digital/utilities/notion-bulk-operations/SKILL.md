---


uuid: 41324dc8-ccd9-81dc-bb3e-d7747a2c22c0
name: notion-bulk-operations
description: "Use when bulk writing or querying Notion rows."
version: 1
thinking: "Medium"
temperature: 0.3
author: Clarity
license: proprietary
metadata:
hermes:
tags: [notion, bulk, database, idempotency, automation]
related_skills: [ship-db, notion-live-reports]


---


# Notion bulk operations

Writing or reading many rows in one pass — a weekly sync, a re-label, an estate-wide fix. The danger is
never the single call; it is the loop that runs unattended and either duplicates or silently skips.

## When to Use

- Creating/updating tens or hundreds of pages from a script, cron or DAG.

- Any create-if-missing loop over a data source.

- Recovering from a run that clearly went wrong (duplicates, untouched rows, silent no-op).

## Procedure

1. **Query first, and prove the query worked.** Read the exact window you are about to write
(`WHERE "date:When?:start" >= '...' AND < '...'`, half-open). If the response is not a row list, the
run must stop — see the error-shape rule below.

1. **Dry-run, then count.** Every bulk script takes `--dry-run` and reports planned creates/updates.
Compare that count to your expectation before the live run.

1. **Write through the helper, not ad-hoc calls.** One shared module per workspace (a
`notion_bulk.py`-style wrapper) so SQL quoting, id normalisation and retries live in one place.

1. **Read the rows back.** Re-query the exact ids you touched and assert every field you set. A 200 or a
returned URL is not a success.

1. **Report the delta**, and record how to reverse anything not obviously reversible.

## The id shapes are not interchangeable

- Queries take the **`collection://<uuid>`**** URL** as the data source argument.

- Page creation takes the **bare ****`<uuid>`** as `parent.data_source_id`, plus `allow_async: false` — or
the page does not exist yet when you verify.

- Page updates take the **bare 32-hex page id** — strip it out of the returned URL.

Mixing these fails as "created 0 rows" rather than an exception, so it reads like a quiet success.

## Errors arrive as values, not exceptions

A rate-limited or upstream-429 query comes back as an **error string** (or a dict with no `results`).
Code written as `res.get("results", [])` reads that as **no rows** — inside a create-if-missing loop
that means one duplicate per item in the window, with a report claiming all is well.

Wrap every query in a guard that retries on a non-result shape and then raises:

```python
def q_rows(mcp, sql, ds, tries=3, wait=31):
    last = None
    for _ in range(tries):
        res = nb.q(mcp, sql, ds)
        if isinstance(res, dict) and isinstance(res.get("results"), list):
            return res["results"]
        last = res
        time.sleep(wait)
    raise RuntimeError(f"query failed after {tries} tries: {str(last)[:300]}")
```

The same applies to writes: the update call returns a **text/error string** on failure rather than
raising. Check it before recording success.

## Targeted page edits: match the escaped text, and read the warnings

- `notion-update-page` with `command: "update_content"` takes an array of `{old_str, new_str}` operations and applies them as a batch. **A ****`warnings: [{code: "no_match"}]`**** entry means that one operation did nothing while the rest applied** — a half-succeeded batch that still looks like a 200. Read the warnings array, then re-fetch and assert every string landed.

- `old_str` must match the page markdown **including its escapes**: `agent\_notes`, `\|` inside table cells, and `<b>`/`<i>` tags rather than `**`/`*`. Quote the string from a fresh fetch rather than retyping it from memory — an underscore that is escaped on the page will not match an unescaped retype.

- The batch is the right shape for correcting a source-of-truth document in several places at once (version bump, a paragraph, a skills line, a standing note). Prefer it to `replace_content`, which rewrites the whole page and risks dropping child pages.

## A select property write can no-op while reporting success

`notion_bulk.py props <page_id> '{"Where": {"select": {"name": "Nike"}}}'` prints `ok` and changes nothing. Set select properties through the MCP tool instead — `notion-update-page` with `command: "update_properties"` and the plain value (`{"Where": "Nike"}`) — then query the column back. Same rule as everywhere else: the helper's own success message is not evidence the field persisted.

## SQL mode: the table name is the collection URL, and reserved columns need quoting

- The table is named by the full data-source URL: `SELECT ... FROM "collection://<uuid>"`. The bare uuid fails with `Invalid data source URL`; a made-up table name fails with `table <x> is not an allowed data source`.

- Columns whose names are SQL keywords must be double-quoted — `"Where"`, `"When"`, `"Jobs"`. Unquoted, the parser returns a long list of expected tokens that buries the actual cause.

- Date properties are expanded columns: `"date:Open Date:start"`, never `"Open Date"`.

- `%` wildcards go in the value, not the column: `WHERE Name LIKE '%Nike%'`.

## Dates are two properties, always

- Date-only: `{start: "YYYY-MM-DD", is_datetime: 0}`.

- Datetime: `{start: "<UTC ISO>.000Z", end: "<UTC ISO>.000Z", is_datetime: 1}` — store UTC, render local.

- A partial payload can silently default to *now*; read `start`, `end` and `is_datetime` back.

- Filtering is string comparison on the start column and matches on the `YYYY-MM-DD` prefix.

## Archive is not delete, and archived rows still exist

- **Archive** (`{"Archive?": "__YES__"}` via `update_properties`) is the reversible default; delete is
reserved for an explicitly erroneous page and needs the user's word.

- Archived rows still match queries, so **they must stay in the dedupe set** — drop them and the next
run resurrects the page you just archived.

- But never *correct* an archived row (dates, priority, category). Archiving is a decision, not drift.

## Do not overwrite derived or automation-owned fields

Formulas, rollups and anything a button or webhook maintains are read-only in practice: writing them is
rejected or silently ignored, and hand-fixing them fights the automation. Leave them and verify them —
an empty automation field means the automation did not fire, which is a finding worth reporting.

## Pitfalls

- **Order matters when steps share a field.** If step A clears a property that step B keys its dedupe
on, reordering them duplicates the estate. State the required order in the script header.

- Select options are schema, not values: adding one is an `ALTER COLUMN ... SET SELECT(...)` that must
re-send the **full** option list, or the others are dropped.

- Pagination: a default response is ~100 rows. Check the continuation flag before calling a result set
complete.

- One call per updated page — a 300-row loop will hit rate limits. Chunk, pace, and let the guard retry.