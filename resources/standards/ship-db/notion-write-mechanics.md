# Ship — Notion write mechanics (rebuilt standard)

**Rebuilt** 2026-11-09 after the original `references/notion-write-mechanics.md` was lost to the
nightly Hub→local skill sync. Grounded in `notion_bulk.py`, `calendar_apply.py` and observed API
responses.

## Create

```python
mcp.call("notion-create-pages", {
  "parent": {"data_source_id": "55b38845-c284-4e37-9212-55c8e289da97"},   # bare UUID
  "pages": [{"properties": {...}}],
  "allow_async": False,
})
```

- Always pass `allow_async: False` — async creation returns before the row exists and breaks the
  verify-immediately pattern.
- The response is `{"pages": [{"id":…, "url":…, "properties":…}]}`. **Assert the count matches** what
  you asked for; a partial create is silent otherwise.
- Page body, when needed, goes as `page["content"]` (markdown) in the same call.
- Minimum viable row: `Name · Level · Status · Live · date:When?:start` (+ `Priority` for real work).

## Update properties

```python
mcp.call("notion-update-page", {"page_id": pid, "command": "update_properties",
                                "properties": {"Status": "Doing"}})
```

- `page_id` must be the **bare 32-hex id** — strip the URL (`nb.pageid()`).
- **Dates are two properties, always together**:
  - date-only → `{"date:When?:start": "2026-11-13", "date:When?:is_datetime": 0}`
  - datetime → `{"date:When?:start": "2026-11-13T09:30:00.000Z", "date:When?:end": "…", "date:When?:is_datetime": 1}`
  - Ship stores datetimes in **UTC**; render local (Europe/Amsterdam) before showing them.
  - A partial date payload can silently default to "now" — always read `start`, `end` and
    `is_datetime` back after writing.
- Relations take a **list of full page URLs**: `{"Live": ["https://app.notion.com/dd0eacbf…"]}`.
- Selects take the plain option name: `{"Priority": "#5"}`. Checkboxes take `"__YES__"` / `"__NO__"`.
- **Write failures come back as a text/error string, not an exception.** Check the returned string for
  `error|invalid` before recording a success (see `calendar_apply.py`).

## Append content / comments

- Append to a page body: `{"command": "insert_content", "content": md, "position": {"type": "end"}}`.
- Project progress is appended **inline on the parent**, never as a child page.
- Comments: `notion-create-comment` with the page id + comment body. Richard delegating via comment is
  routed by the `clarity-comment` webhook (see `notion-triggers.md`) — the gate is an @-mention of
  Clarity's user id, because authorship is not separable (Clarity posts as Richard's own account).

## Archive vs delete

- **Archive** = `{"Archive?": "__YES__"}` via `update_properties`. Reversible, no approval needed,
  and the default for "this should not be on the board".
- **Delete** = `notion-delete-pages` (`user_confirmed: true`) → moves to Trash. **Only on Richard's
  explicit word**, and only for a clearly erroneous entry.
- Archived rows still exist and still match queries. Anything doing create-if-missing **must keep
  them in the dedupe set** or it will resurrect them, while leaving their date/priority alone.

## Select options

Adding an option to a select is a schema change, via `notion-update-data-source`:

```
ALTER COLUMN "Where" SET SELECT('a','b','c')
```

`nb.add_option()` reads the existing options off the data source schema first and re-sends the full
list — an `ALTER` with only the new option drops the rest. Quote-escape `'` in option names.

## Verify

- Re-read the exact rows you touched and confirm every field you set.
- `Linked?` is populated by a downstream automation **a few minutes later** — never write it, but do
  check it afterwards; empty means the automation did not fire.
