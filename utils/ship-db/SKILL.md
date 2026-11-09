---


name: ship-db
uuid: 3fb24dc8-ccd9-8172-aa13-d15ce25bfabc
description: "Operate on Richard's Ship task database."
version: 8
last-used: "2026-10-26"
scope: local
author: Richard Dykes, Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
hermes:
tags: [ship, notion, tasks, gsd, ship-it, richard-os]
related_skills: [track-project, mind-dump, weekly-status-update, create-project]
thinking: "Medium"
temperature: 0.3


---


# Ship DB

Ship (`@Ship-It` / `@GSD` / `@Ship-It-DB`) is Richard's Notion database — the single source of truth
for tasks, projects, goals and rituals, and the task layer under Richard OS. It is the shared
substrate the whole persona stack reads: Kagetsu/mind-dump, Ari/Floki/Shin, Wayfinder, track-project,
weekly-status-update, and Clarity.

## When to Use

- Creating, reading or updating anything in Ship.

- Deciding what Richard should do next, or where a new item belongs in his system.

- Serialising a row so it actually lands on the intended views.

- Full property list and per-view filter rules: `@Ship-DB-Reference` (central; loaded on demand).

## Always-on rules

- **`Level`**** is the spine:** `Idea · Ritual · Goal · Project · To Do · Thing · Milestone`. It decides
which views a row is even eligible for — get it right first.

- **`Live`**** is effectively mandatory.** Most views filter on it. Set it to the pillar (`Craft` /
`Edge` / `Bonds`) in ~99% of cases; occasionally **also** add a company space (e.g. `@Mambu`) so
the item surfaces from the company page. `Live` may legitimately hold more than one relation.

- **`Archive?`**** must stay unset** for a row to appear on Backlog, Goals, Roadmap, Outcomes, Things
and To do list.

- **`This week`**** is derived — never set it by hand.** It auto-populates when `When?` start is set
correctly, and it is the sprint flag the n8n syncs (Habitica and others) key off.

- **Sprint membership** = Status ∈ {`Waiting`, `Do next`, `Doing`} **AND** `Priority` set **AND**
`When?` start inside the current week.

- **Status buckets:** `Waiting` = the *weekly* holding bucket and counts as in-progress (putting
something there means it must get done this week); `Do next` = the *daily* holding bucket
(1–3 items, in execution order, during intense periods); `Doing` = underway; `Backlog` = not this
week; `Defer` = **transient** — an automation returns it to `Waiting` deferred by a day, so never
park anything there deliberately; `LEAD` = **L**everaged / **E**liminated / **A**utomated /
**D**elegated, brownie points for work Richard did not do on purpose; `Shipped` / `Abandoned` =
done.

- **Priority:** `#1` (≈1/day) → `#3` (≈3/day) → `#5` (≈5/day) → `Everything else` (as few as
possible) → `Headache` (reserved for extremely critical periods; sorts above `#1`) → `Connect`
(meetings, 1:1s, social events).

- **Naming:** verb-first where natural, short, **phone-readable**. Consistency is not enforced — do
not burn effort regularising existing names.

- **Milestones are outcomes, not objectives — and a Weekly Milestone is week-bound, not dated.**
It answers "what outcomes am I targeting by the end of this week?", scoped to the whole week it
belongs to; a `When?` on one is not a day commitment, so **never filter or read Weekly Milestones
by date**. Weekly Milestones require only `Live` and carry **no** Priority — that is precisely what
routes them to Outcomes rather than Roadmap. Roadmap Milestones are dated to the 1st of the target
month and **do** carry Priority.

- **Task → project linkage is the self-relation, not a property.** Ship has **no ****`Project`**** column**; the only project link on a row is `Parent` (with the project row holding the mirror in `Children`). Attach a task to its project by setting the task's `Parent` to the project page — the same mechanism milestones already use. It is a **tracking** link only: allocation still goes through `Live`, and a task is never linked to a *Milestone*.

- **`@Mambu`**** is the work-laptop sync boundary, not a workstream.** Only rows parented under `@Mambu` sync to Richard's work laptop, so that personal material never reaches his IT department. Never nest personal items there, and treat `@Mambu` as a container that legitimately sits at `Doing`.

- **`Who`**** marks delegation, not attendance.** A row with `Who` set belongs to that person; `Who` = the
Clarity user (`clarity@dykes.digital`) means the work is delegated to Clarity. **`Priority`**** = ****`Delegate`**
is the fast way to route a row into her queue without setting `Who`. (`Who's it for?` is unrelated —
prose describing the beneficiary.)

- **Delegated rows are executed by ****`$handle-delegated-task`**, fired by the `notion-ship` webhook. It
claims the row (`Status = Do next`, title prefixed `⏳ `), pings the Discord home channel, executes,
loop-verifies, then sets `Shipped` with a `✅ ` title (or `⚠️ ` if blocked). Never reset `Priority`,
`Live` or `When?` on pickup — and check the title marker before acting, so two triggers can't cause
duplicate runs.

- **Never create new Ship properties.** Use the existing schema; the only Ship relation defined
outside the DB itself is `Project` (from the AI Hub side).

- **Buttons are automations** (`Done`, `Add to Sprint`, `Add to Library`, `Clear it`) and are not
writable through the API — ignore them and set properties directly.

- **Verify writes by re-fetching.** A partial `When?` payload can silently default to "now" with
`is_datetime=1` instead of the intended date-only range; confirm `start`, `end` and `is_datetime`.

- **1:1s never become Ship rows.** A 1:1 is relationship building: it belongs in `@Bonds` and is managed in the **CRM** (Live → `@Bonds` → CRM) through that person's `Next Connection` — not in Get Shit Done. Setting `Next Connection` makes Notion auto-create a date-only Ship row under `@Bonds`; enrich that row with the real time, and never create your own.

- **Creating a missing CRM connection.** The CRM data source is reached at `Live → @Bonds → CRM`; its columns are `Name` (title), `Type` (multi_select — use `["Tribes"]`), `Active` (checkbox → `__YES__`), `Email` (email), `Company` (select, e.g. `Mambu`), and `Next Connection` (date, expanded as `date:Next Connection:start` / `:end` / `:is_datetime`). Create it with the minimal set (`Name`, `Type`, `Active`) plus `Email`/`Company` when the calendar supplies them, then re-fetch: the `Next Connection` write fires the automation that mints the date-only Ship row a few seconds later. Write this only under the weekly reset / `$monday` *Fill CRM gaps* step — standalone calendar syncs report the miss instead.

## Daily and weekly rhythm (context for how rows get used)

- **Daily:** work a kanban/list of the day's tasks — promote into `Do next` in the morning, progress
to done, or `Defer`. Habitica mirrors tasks→tasks, milestones→habits, rituals→dailies; Richard
works it on mobile and retires a milestone after 8–10 marks there.

- **Weekly (Mon AM):** incomplete prior-week tasks → `Backlog` or `Abandoned` → clear Habitica →
copy the week's meetings into the Notion calendar as Priority `Connect` → mind-dump → populate the
week's Milestones and tasks.

## Copying calendar meetings into Ship as `Connect`

The weekly rhythm names "copy the week's meetings as Priority `Connect`". The canonical procedure is the **`calendar-meetings-to-ship`** utility — follow it rather than improvising; the rules below are the Ship-side contract it depends on.

1. **Source — three calendars, not one.** Richard's "external calendar" is his own `richard@dykes.digital` Google Workspace account, read through the `gwork` wrapper (`~/config/google/gwork`), plus the Mambu work calendar (`richard.dykes@mambu.com`) shared into it as *reader*, plus the personal calendar (`chdwck9@gmail.com`, via `gpers`).

1. **Window.** Convert the requested range to ISO with an explicit UTC offset — `calendar list` otherwise defaults to the next 7 days only.

1. **Meetings only.** An event is a meeting when it has **attendees**. Exclude the zero-attendee blocks (`Focus Block`, `Lunch`, all-day `Home` markers) **and daily/standup recurring meetings** (`DR daily`/`DRDaily`, `Platform eng AWS daily`, …) — Richard attends the dailies without tracking them and adds one back explicitly only when he wants it on the board.

1. **Serialise each meeting:** `Level = To Do`, `Priority = Connect`, `When?` = the event start→end as a **datetime range** (`is_datetime = 1`, stored in **UTC** — subtract the local offset), and `Live` = the pillar for that calendar: Mambu/work → `@Craft`; Dykes Digital and Personal → `@Bonds` (family, relationships, social) or `@Edge` (health, habits, self-development). Leave `This week` alone — it derives.

1. **Name short**, matching existing rows: person's first name for a 1:1, compact name for a recurring sync (`DRDaily`, `Platform Weekly`, `EOD Weekly`).

1. **Status:** a meeting still ahead → `Waiting` (the weekly holding bucket the n8n sync picks up); one Richard has promoted for today → `Do next`; `Shipped` only for a meeting that actually happened. Never mark a future meeting `Shipped`.

1. **Verify** by re-querying (`start`/`end`/`is_datetime`) and **report the list** — name, local time, status — flagging any gap (e.g. earlier days of the week not yet copied) instead of silently filling it.

**1:1s are the exception — they never become a ****`Connect`**** task.** A two-person meeting with one connection is relationship building: update that person's `Next Connection` in the CRM (Live → `@Bonds` → CRM, among the **Active** connections) to the meeting's date. Notion then auto-creates a *date-only* Ship row under `@Bonds` — wait a few seconds and set its `When?` to the real start→end, because the automation carries the date but not the time. If the person is not an active connection, report the miss; create nothing.

Pitfalls specific to this flow:

- **The wrapper's ****`calendar list`**** only queries the primary calendar** — a shared/secondary calendar (the Mambu one) returns nothing that way. Enumerate calendars (`calendarList`) and query every `calendarId` in the window. `scripts/calendar_week.py --account work|pers --start <ISO> --end <ISO> [--json]` does the full sweep in one command (all calendars, de-duped recurring instances, per-event attendee count) — run it once per account (`work` = `dykes.digital`, `pers` = `chdwck9`).

- **Take the pillar from existing rows, not intuition.** Work meetings sit under `@Craft`; same-day travel and personal Connect rows sit under `@Edge` / `@Bonds`. Fetch a sample of `Priority = Connect` rows before choosing `Live`.

- **Locating the CRM is not obvious — it is a non-inline linked database under ****`@Bonds`****, not a child page.** Fetching the `@Bonds` Live page lists its inline view databases only; the CRM appears as a `<database … inline="false">` tag whose data source carries the title `CRM`. When the fetch is too large to read directly, search Notion for a *known connection's first name* (`Najat`, `Rytis`) — the automations leave person-named Ship rows whose `Live = @Bonds`, which confirms the person exists without opening the database. Resolve the CRM by the **data source title ****`CRM`**, never by a hardcoded id.

## Projects in Ship

Ship holds the project *record*; durable project context lives in its MCD and its Agent. When creating or updating a project, follow **`$create-project`** — it owns the full foundation (Agent + MCD + Ship row + source wiring). Ship-side essentials it enforces:

- `Level = Project`, `Status = Doing`, `Live` = a pillar (usually `@Craft`), `Priority` assessed (default `#5`), `When?` = the project window (default today → +90 days).

- `Master Doc` → the project MCD; `Agent` → the project Agent. **A ****`Doing`**** project with no ****`Master Doc`**** is unfinished, not merely thin** — flag it.

- Mambu projects set `Parent` = the `@Mambu` page.

- Populate only *existing* fields (`Goals`, `Phase`, `Milestone`, `Overall Progress`, `Risks & Mitigations`, `Stakeholders`, `Cadence`, …) — never create new properties.

- Re-fetch after writing `When?` and confirm `start` / `end` / `is_datetime`.

Consolidation rules (used by the weekly reset and any project clean-up):

- Two projects covering the same delivery → keep the one that has the MCD, archive the other; re-point `Parent`/relations first.

- A `Project` with **no ****`Live`**** relation is invisible on every pillar view** — give it a pillar or archive it.

- Hobby or long-dormant "projects" (no MCD, no activity for months) are `Idea`-level; archive them rather than leaving them in `Backlog`.

- Archiving = `Archive? = __YES__` (reversible). Deleting moves the page to Trash (recoverable) — **only on Richard's explicit word.**

## Bulk operations

Never hand-issue dozens of tool calls for a bulk change — it is slow, token-expensive and error-prone. Use the parameterised helper and reuse/adapt it rather than writing a new one:

- `~/.hermes/scripts/notion_bulk.py` — verbs: `query`, `delete`, `archive`, `props`, `sql-delete`, `sql-archive`, `sql-props`. The `sql-*` verbs loop `SELECT … LIMIT n` → act → repeat until the WHERE matches nothing, so **one command clears or re-tags thousands of rows**; `sql-props` applies an arbitrary properties JSON to every match (use it for bulk `Parent` linkage, status sweeps, archiving).

- **`notion_bulk.py query`**** truncates its output at 8000 characters** — it prints `[:8000]`, so any result set past that is cut mid-JSON and `json.loads` fails. Never read a whole week/pillar/data source through `query`. Paginate instead: `SELECT … LIMIT 100 OFFSET n` until a short batch, dump the concatenated rows to a file, then aggregate in Python — `~/.hermes/scripts/ship_query.py "<SQL>" <out.json>` does exactly this (imports `notion_bulk`'s MCP client, no truncation). Count and filter programmatically; never eyeball a partial list.

- `~/.hermes/scripts/ship_query.py` — paginates a Ship query and writes the full JSON to a file; use it when `notion_bulk.py query` truncates (its print is capped at 8000 chars, so a bulk read can be silently cut mid-row).

- **The board holds thousands of rows (~9k) — never pull it whole to cross-check a subject.** `ship_query.py` also stops paginating past ~5000 rows, so a full-board read is slow *and* silently partial. To answer "does a row already exist for X", run a **targeted keyword query** instead: build the `WHERE` from an OR-list of `"Name" LIKE '%kw%'` clauses over the candidate keywords, read the (small) result set, and match in Python from that — never from a board dump.

- **Writing rows: copy the payload shape from ****`~/.hermes/scripts/hub_sync.py`****, never guess it.** Over the MCP, `notion-create-pages` takes `{"parent": {"data_source_id": "<32-hex>"}, "pages": [{"properties": {...}}]}` and `notion-update-page` takes `page_id` + `command` — `update_properties` carries `properties`, while `replace_content` carries **`new_str`** (the markdown body), NOT `content` or `properties` (`content` returns `validation_error: The "replace_content" command requires a "new_str" parameter`). The property values are **not** Notion-REST shapes: a relation is a JSON **string** of page URLs — `"Live": json.dumps(["https://app.notion.com/<pillar-id>"])` — a checkbox is `"__YES__"` / `"__NO__"`, and a date is three keys, `"date:When?:start"`, `"date:When?:end"` (ISO `…Z`, converted from local by subtracting the offset) and `"date:When?:is_datetime": 1|0`. Page ids come from `url`, and **`url`**** only appears on a ****`SELECT *`** — a narrow projection like `SELECT "Name","Status" …` silently drops it, so a helper that does `nb.pageid(row["url"])` on a projected result raises `KeyError: 'url'`. Select `*` (or add `url` to the projection) whenever you need to act on the rows it returns.

- **Never hardcode a pillar id.** Read it off an existing row of the same kind (`WHERE "Priority" = 'Connect'` for meeting rows) and confirm it with `notion-fetch` (its `title` is `@Craft` / `@Bonds` / `@Edge`), then reuse that URL.

- **Resolve a pillar/relation page by fetching it and reading its ****`title`**** — never by id-prefix.** Two pages can share a hex prefix (an active pillar and an archived sibling both matched `LIKE '%1eb24dc8%'`), so a prefix filter can silently select the wrong page; fetch and confirm the title before reusing the URL.

- **Creating rows: ****`~/.hermes/scripts/ship_add.py`** — `ship_add.py --name "…" [--name "…"] --live Edge|Mambu|Ship|<url-or-id> --level "To Do" --status "Do next" --priority "#5" --when YYYY-MM-DD`. It writes synchronously (`allow_async:false`) and prints the created page ids. Use it instead of hand-building the `notion-create-pages` payload. It resolves only the shortcut names `Edge`/`Mambu`/`Ship`; any other pillar (`Craft`) must be passed as its **full page URL or id** — a bare `--live Craft` writes the literal `https://app.notion.com/Craft` and fails `validation_error: Invalid relation value … for property Live` (resolve it first with `notion-search`). It has **no body option**: to add page content, follow up with `notion-update-page` + `command:"replace_content"` + `new_str`.

- **In the data-source SQL, every date column is a compound name that MUST be double-quoted:** `"date:When?:start"`, `"date:When?:end"`, `"date:When?:is_datetime"`. Bare `date:When?:start` in a WHERE raises `unexpected character`, and guessing `"When?"` raises `no such column: "When?"` — neither is a permissions or token problem. Run `SELECT * FROM "<collection>" LIMIT 1` once to read the real column keys (they come back exactly as `date:When?:start`), then build the filter as `WHERE "date:When?:start" >= '<yyyy-mm-dd>' AND "date:When?:start" < '<yyyy-mm-dd+1>'`. `.hermes/scripts/ship_query.py` only takes the SQL through unchanged, so a syntax error there is always the quoting.

- **Quote *****every***** property name that contains punctuation, not just the date columns.** A bare `Archive?` in a WHERE (or any other `?`-bearing name) raises `Expecting token of type --> EOF <-- but found --> '?'`; write it double-quoted — `WHERE "Archive?" = '__NO__'`. The same applies in any `FROM`/`SELECT` projection.

- **Always name the collection in ****`FROM`****, and pass the ****`data_source_urls`**** argument unquoted.** A `SELECT` with no `FROM` returns `query must reference at least one allowed data source`, so the table is the full `"collection://<id>"`. The helper's `data_source_urls` list wants that URL **bare** (`collection://<id>`); wrapping it in quotes yields `Invalid data source URL`.

- **A database page id is not its data-source id.** To query an arbitrary database reachable by name (`notion-search`), fetch the *database* URL and read the `collection://<id>` out of the response — grep the fetch text for `collection://`. Querying by the database's own page id fails with `Invalid data source URL`. **And the data source id must match the table you query:** the helper's `data_source_urls` list is what the SQL is allowed to touch, so querying the CRM while still passing the Ship DS returns `table "collection://<crm-id>" is not an allowed data source` — pass the *target* database's own `collection://<id>` as the second argument (`nb.q(m, sql, crm_collection)`), not the Ship collection.

- It drives the Notion MCP HTTP endpoint directly; the OAuth token in `~/.hermes/mcp-tokens/notion.json` is MCP-scoped (it is rejected by `api.notion.com`) and Cloudflare 1010-blocks non-browser clients, so it must send a browser `User-Agent`. Tool names on that endpoint are **hyphenated** (`notion-query-data-sources`, `notion-fetch`, `notion-update-page`, `notion-delete-pages`, `notion-update-data-source`) — the underscore forms used in this file's prose are the agent-bridge names and will 404 as "tool not found" over raw JSON-RPC. Handlers must also tolerate the SSE framing: responses arrive as `event: message` + `data: {…}` lines, not bare JSON.

## Comments and closeout reconciliation

A page comment is the human-visible log; `Status` is only the machine state. Post with `notion-create-comment` (`page_id` + `markdown`, inline Markdown not HTML), **then record the returned id** with `notion_comment_intake.py --mine-add <id>` — the MCP connection is Richard's own account, so his replies and the agent's comments are indistinguishable in authorship, and the intake sweep keys only off that recorded set. Retitle and re-status in one `update_properties` write (`"Name"` takes the full new title). Reconciling a row that finished off-board is retitle → `Status` → comment naming where it happened → re-fetch and confirm, in the run that learns the outcome. Exact payloads and traps: `references/notion-write-mechanics.md`.

## Pitfalls

- **Fetch the *****database***** URL, not the data source, to read view definitions.** The database fetch
carries the `<views>` block with each view's full filter JSON; the data source fetch does not. That
block is the only reliable answer to "what does a row need to appear on view X".

- **Setting ****`Status`**** to ****`Waiting`**** rewrites ****`When?`**** into the current week** — that is the "add to sprint" behaviour, not a bug. For a *future-dated* reminder, re-apply the future `When?` after the status change (so it sits in its own future sprint, not this one), then re-verify `start` / `is_datetime`. A future-dated `Waiting` row is invisible to the current week's timeboxed sprint and does not sync to Habitica until its week arrives.

- **Do not trust prose descriptions of Ship over the live schema** — the Operating System MCD has
drifted before (it named status `DEALt With` and priority `1/3/5`; the live values are
`Defer`/`LEAD`/`Abandoned` and `#1`/`#3`/`#5`). Re-read the schema when precision matters.

- **An over-full ****`Do next`**** is reported, not silently trimmed.** `Do next` is a 1–3 row daily bucket; when it already holds more, promoting more tasks makes the day unusable and demoting rows to `Backlog` is `$monday`'s call, never a side effect of a triage. Count the bucket first, list the rows dated before today as stale, and leave them for Richard's decision.

- **A ****`To Do`**** with no Priority is invisible to Get Shit Done**, and a row with no `Live` is an
orphan on Goals / This week / Got Shit Done / Things.

- **A Status bucket is not a window.** `Waiting` / `Do next` / `Doing` are holding buckets that
accumulate across time and carry legacy rows with no `When?` at all — reading a whole bucket for
"this week's work" surfaces dozens of years-old rows as if they were live. Filter triage on the
quoted column `"date:When?:start"` falling inside the window; sprint membership already requires it.

- **`track-project`**** owns project review pages** — it appends a dated update block inline to the project page body (Plan / Achieved / Missed / Why / Risks / Next / Evidence). Do not create a
parallel status file or a competing project database.

- **A backfill is a record, not a plan.** When capturing work already done, the pillar capacity guard
does not apply (report the count rather than trimming the list), `Priority = Everything else`, and
`When?` = the day the work happened — only rows dated inside the current week reach the sprint.

## Taste

*Richard-originated, grown by **`$reinforce`**. Signal → preference.*

- Future-dated reminders are `Waiting`, not `Backlog`. → `Backlog` requires an explicit move into the sprint; a reminder should already sit in its (future) sprint. Its future `When?` keeps it out of the current timeboxed week and out of Habitica until that week.

- The sprint is timeboxed to the **current week** only. → A row dated outside this week is expected to be invisible in this week's board and Habitica; that is not a fault to fix.

## References

- `references/notion-triggers.md` — Notion API webhooks vs in-app database automations, and how to wire a board-row event into a ping: setup, delivery guarantees, and the dedupe/idempotency guards.

- `references/notion-write-mechanics.md` — comment/retitle/closeout payload shapes, the two-half shape of `notion-fetch`, and the traps (no `created_by`, macOS has no `timeout`, hyphenated tool names).

- `@Ship-DB-Reference` — every property, the ten views and their filter rules, the status/priority
semantics, the automations and the write-authority contract. One shared copy; never keep a local
duplicate in sync by hand.