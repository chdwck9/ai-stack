# Ship — Notion bulk writes and queries (rebuilt standard)

**Rebuilt** 2026-11-09 after the original `references/notion-bulk-and-query.md` was lost to the
nightly Hub→local skill sync. Grounded in `~/.hermes/scripts/notion_bulk.py` as it actually is.

## Entry points

- `notion_bulk.py` — the library and a CLI: `query`, `props`, `archive`, `delete`, `loop`,
  `add-option`, `create`.
- `ship_add.py` — create rows: `--name … --live Edge|Mambu|Ship|<url> --status --priority --when`.
- `calendar_apply.py`, `monday_*.py`, `hub_push_one.py`, `hub_sync*.py` — all build on `notion_bulk`.

**Bulk operations go through `notion_bulk.py`, never a scatter of ad-hoc MCP calls.**

## Data sources

| What | URL |
| --- | --- |
| Ship | `collection://55b38845-c284-4e37-9212-55c8e289da97` |
| CRM (under @Bonds) | `collection://8c4c3ac6-e5f6-4191-9773-99e4cdd8d29e` |
| AI Hub | `collection://28424dc8-ccd9-801c-8439-000ba9845548` |
| Live (pillars) | `collection://c3ae031f-b61b-4430-a5c2-c37797cd3666` |

Two different id shapes, and mixing them is the classic failure:

- `notion-query-data-sources` wants the **`collection://` URL** as `data_source_urls[0]`.
- `notion-create-pages` wants the **bare UUID** as `parent.data_source_id` → `nb._ds_id(ds)`.

## Query rules

`nb.q(mcp, sql, ds)` → `{"results": [...], "has_more": bool, ...}`. Rows carry `url` (not `id`) and
property names exactly as in the schema (`"date:When?:start"`, `"Archive?"`, `"date:Next Connection:start"`).

- **Quote every property name**, including `?` and `:`: `SELECT "Name","date:When?:start" FROM "collection://…"`.
- Date filtering is **string comparison** on the start column: `WHERE "date:When?:start" >= '2026-11-09' AND < '2026-11-16'` (half-open; the column is `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`).
- `LIMIT n` works; a default page is ~100 rows — check `has_more` before treating a list as complete.
- Column names with spaces need the quotes: `"date:Last Connection:start"`, `"date:When?:is_datetime"`.

### The rate-limit trap (it has already bitten twice)

`notion-query-data-sources` returns an **error STRING**, not a dict, when Notion rate-limits
(`upstream_429`, retry ~30 s). Code that does `res.get("results", [])` turns that into **"no rows"** —
which in a create-if-missing loop means **a duplicate for every item in the window**.

Guard used in `calendar_apply.py` (copy it):

```python
def q_rows(mcp, sql, ds, tries=3, wait=31):
    last = None
    for _ in range(tries):
        res = nb.q(mcp, sql, ds)
        if isinstance(res, dict) and isinstance(res.get("results"), list):
            return res["results"]
        last = res
        time.sleep(wait)
    raise RuntimeError(f"Notion query failed after {tries} tries: {str(last)[:300]}")
```

Never let an errored query look like a clean empty run.

## Write helpers

- `do_props(mcp, urls, props)` — one `notion-update-page` per URL (`update_properties`). Not batched
  server-side, so ~1 call per row; keep loops under ~50 rows per run or expect 429s.
- `do_archive(mcp, urls)` — sets `Archive? = __YES__`, the reversible alternative to deleting.
- `do_delete(mcp, urls)` — Trash, chunks of 20. Only on Richard's explicit word.
- `loop_props` / `loop` — page through a `WHERE` clause `LIMIT n` at a time for large bulk changes.
- `create_pages(mcp, ds, specs, dry, capture)` — asserts the number of pages returned equals the
  number asked for; raise rather than assume.

## Bulk-change hygiene

1. `--dry-run` first for anything touching more than a handful of rows.
2. Count before and after; a declared total is an assertion, not a vibe.
3. Re-query the exact rows afterwards to verify (a 200 is not a success).
4. Log what changed and how to reverse it when the reversal is not obvious.
