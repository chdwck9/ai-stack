---


name: weekly-status-update

uuid: 35024dc8-ccd9-8164-9c65-d77a4b08ba08

version: 6

description: "Weekly Status Update"

thinking: "Medium"

temperature: 0.3

resources:

  - "@BCaaS-MCD"

  - "@Tiago-OS"

  - "@Inbox"

  - "@Ship-It-DB"


---


# Weekly Status Update

Synthesizes the past week's Claude chat history — mind dumps, BCaaS/Wally project work, Cowork sessions, and referenced documents or transcripts — into two ready-to-use outputs: a concise Slack update for Tiago, and a structured 5-minute PMs Platform standup segment.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Establish time window** — default: Monday–Sunday of the previous calendar week. Confirm if a different window is needed.

1. **Pull Claude chat history** — use `recent_chats` to sweep the full 7-day window (paginate up to 5 calls). Then run targeted `conversation_search` calls for: `mind dump`, `BCaaS`/`DR`/`EaaS`/`BYOK`, `Wally`/`Arturas`/`platform`, `Tiago`/`Moreiras`, `cowork`/`transcript`, `pricing`/`commercial`/`NCC`/`Capital One`.

1. **Pull Granola meeting transcripts** (if Granola MCP is connected) — search for meetings from the target week involving Tiago, Wally team, or BCaaS stakeholders. Extract: decisions made, actions assigned to Richard, open items.

1. **Query Ship It DB — Weekly milestone progress** — query @Ship-It-DB for items from the target week where `Level = Milestone` or (`Level = To Do` AND `Cadence = Weekly`) and `date:When?:start` falls within the target window. Extract: Name, Status, Level, When? date. Tag all `Shipped` items as `[SHIPPED]`.

1. **Extract and tag signal** — for each chat or transcript, identify: `[DONE]`, `[MILESTONE]`, `[BLOCKER]`, `[QUESTION]`, `[ASK]`, `[LEARNING]`, `[FYI]`. Cross-reference: Ship It `[SHIPPED]` aligned with chat `[DONE]` = high-confidence completion. Discard: personal OS scaffolding, skill-building unrelated to BCaaS/Wally, family/health-related items.

1. **Load @BCaaS-MCD** (lazy) — to verify milestone names and PRD version.

1. **Load @Tiago-OS** (lazy) — to calibrate tone, confirm Tiago's active priorities. His lens: commercial progress, margin clarity, deal mechanics, scalability signals — not tooling or AI OS detail.

1. **Draft Output 1 — Tiago Update (Slack)** — Slack-ready bullets, no headers, no emoji unless requested. Max 6 bullets. Lead with most commercially significant progress. Include 1 blocker/ask bullet if any. 30-second read.

1. **Draft Output 2 — PMs Platform Segment (5 minutes)** — Four sections:

  - **Update** — 2–3 sentences on current domain, phase, and week's arc

  - **Progress & Milestones** — lead with Ship It `Shipped` items (ground truth), then augment with chat [DONE]/[MILESTONE]. Every bullet concrete and specific.

  - **Questions / Escalations / Requests** — bullet list directed at attending PMs. Omit entirely if no genuine asks.

  - **Interesting Learnings** — max 2 items, transferable value only.

1. **Present for review** — output both drafts in a single response, clearly labelled. Ask: "Any changes before I write this?"

1. **Optional — Write output** (explicit confirmation required) — if Richard confirms, create a new page under @Inbox titled `Weekly Update — [YYYY-MM-DD]` containing both outputs.

## Examples

**Example 1: Standard Monday morning invocation**

> "Generate my weekly update"

Expected: Sweeps last 7 days, pulls Granola if available, tags signal across BCaaS/Wally/mind-dump threads, drafts Tiago Slack message and PMs Platform segment. Presents both. Asks before writing.

**Example 2: Adjusted scope or window**

> "Generate my weekly update for the week of April 14th — focus on BCaaS pricing work only"

Expected: Adjusts window. Scopes searches to BCaaS, pricing, commercial, DR. Omits Wally signal.

**Example 3: No or sparse chat history**

Expected: Reports what was found. Asks Richard to supply context manually or confirm the week was light. Does not fabricate progress.

## Boundaries

- Never fabricate progress, milestones, or decisions not evidenced in retrieved history

- Never include personal OS content or AI OS scaffolding in either output

- Never write without explicit confirmation from Richard in the same turn

- Never include Slack @mentions or emoji unless explicitly requested

- Never surface [LEARNING] items in the Tiago update — Output 2 only

- Never exceed 6 bullets in the Tiago update

- Never skip Step 4 Ship It query — Shipped status items are the strongest completion signal

- Always confirm the time window before pulling history

## Output

**Output 1 — Tiago (Slack):** Bullets only. Max 6. No headers. Commercial and outcome-focused.

**Output 2 — PMs Platform (5-min standup):** Four sections: Update / Progress & Milestones / Questions & Escalations / Interesting Learnings. Structured markdown.