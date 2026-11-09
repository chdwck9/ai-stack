---


name: handle-delegated-task
uuid: 3fe24dc8-ccd9-814d-a31a-ebaacf3efa52
version: 16
description: "Handle Delegated Task"
last-used: "2026-11-05"
thinking: "Medium"
temperature: 0.3
resources:

- "@Ship-It-DB"

- "@AI-Hub"

- "@Resource-Index"


---


# Handle Delegated Task

The procedure for a Ship task Richard has delegated to Clarity. Delegation is signalled by `Who` =
the Clarity user (`clarity@dykes.digital`), or `Priority` = `Delegate`. The `notion-ship` webhook
route fires on that change, but the payload carries **properties only** — the instructions live in
the page body.

**Two routing facts before you work:** capability is **edge-dependent** — probe with
`clarity_capabilities.py`, never assume the sandbox; and **workbox work goes to Mo, not Clarity** —
Richard pays Clarity's bill personally and the company pays Mo's, so running company work through
Clarity is a cost leak. See Pitfalls.

## When to Use

- A `notion-ship` webhook arrives (route `notion-ship`, delivery to the Discord home channel).

- Richard says a task has been assigned to Clarity.

- Any single Ship row that is explicitly hers to execute.

One task per invocation.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Resolve the task.** Take `page_id`/`url` from the normalised payload (`notion_task_intake.py`).
If `found=false`, post to the home channel asking for the task link and stop.

1. **Read the brief.** Fetch the page with the Notion MCP — **the body is the prompt**; the payload
never contains it. Empty body → ask in the home channel and stop.

1. **Claim it before working — only if this run will execute it.** `Status = Do next`; strip any
lifecycle marker from the title, then prefix `⏳ ` (idempotent). Leave `Priority`, `Live`, `When?`,
`Parent`, `Linked?`, `This week`, `Checked`, `Print`, `Phase` untouched. A triage-only run must NOT
claim (the intake sweep only picks up marker-less rows).

1. **Ping the home channel:**
`~/.hermes/hermes-agent/.hermes/bin/hermes send -t discord:1557119812256145408 "⏳ Picked up: <task name>"`.

1. **Open the conversation on the page.** Comment (`notion_create_comment`) at each gate: pickup ·
plan · each verified stage · close. Record the id:
`python3 ~/.hermes/scripts/notion_comment_intake.py --mine-add <comment_id>` — the MCP posts as
Richard's account.

1. **Watch for the answer.** The sweep (`~/.hermes/scripts/notion_comment_intake.py`) surfaces every
new Ship-page comment not in `~/.hermes/state/notion_comments_mine.json`. Treat a comment as an
instruction: reply and act in the same run.

1. **One-shot the brief.** Run `$one-shot` to compile the minimum sufficient context contract — write
the context and prompt yourself, expanding Richard's seed; **link** @AI-Hub Personas/Skills/MCDs
rather than copying. Ask in the home channel only when a gap materially changes execution (max 5
bundled questions).

1. **Plan, then execute.** Decompose into the smallest useful steps; state the plan in the page body
and task list; keep statuses current. Reads/searches need no approval; anything that communicates
with a human stays a **draft**.

1. **Loop and verify — on the execution host.** Produce, check against the brief's own acceptance
criteria, fix, repeat; never exit unverified; change approach after two failures.

1. **Close the moment a response comes back** — `✅ <name>` / `Status = Shipped`, with a closing
comment. **Do not hold a row open pending Richard's review.** Only a genuine failure or unanswered
question gets `⚠️ <name>` / `Status = Do next` plus a block comment in the same run.

1. **Report.** One brief home-channel message — what I did · outcome · next actions (omit if none).

## Pitfalls

- Never cost the Studio tokens for workbox-resident work — dispatch, verify returned evidence.

- The payload is not the brief; the body is a seed — expand it via `$one-shot`.

- A retitled row (`⚠️`/`⏳`) with no comment is a defect; comment at the gate where it
stopped, in that run. Off-board completion still closes the Ship row.

- Never guess a host or project; if unattributable, comment on the Ship page and wait.

- **Probe, don't assume the sandbox.** The `notion-ship` route's capability is edge-dependent: run
`python3 ~/.hermes/scripts/clarity_capabilities.py` first. If it proves a shell + `hermes send`,
the route IS execution-capable — run EXECUTE mode (claim, dispatch, close). Only a probe that
proves the shell missing means triage-only. Never report a sandboxed run as a broken machine or a
permissions problem.

- **On an unattended (webhook) platform ****`execute_code`**** is blocked** ("runs arbitrary local Python …
no user present to approve"), while `terminal` and the MCP tools work. Use `terminal` for shell work
here — a blocked `execute_code` is the platform gate, not a broken toolchain.

- **Large Notion body writes break the agent bridge.** `mcp__notion__notion_create_pages` or
`notion-update-page` with >~8 KB of markdown produce invalid JSON errors from the transport
layer. Write the content to a temp file first, then invoke the Notion MCP HTTP endpoint via a
short inline `python3 << 'EOF'` script through `terminal` (session-init, auth, SSE-framing handled;
see `references/notion-write-mechanics.md` for the full pattern and duplication scaffold for
new database rows).

- Notion pauses a webhook automation after a failed delivery; route secret `INSECURE_NO_AUTH`; two
triggers cause duplicate runs; route changes need a **gateway restart**.

- **Workbox work is Mo's, not yours.** When Richard assigns a task **for completion** and it is a
**workbox activity** (work laptop, `~/Library/CloudStorage/SynologyDrive-Ship/…`, Mambu work, or a
Claude/herdr session on the workbox), **dispatch it to Mo** (`$mo`, the workbox operator) and stop —
do not execute it as Clarity. Richard pays Clarity's bill personally and the company pays Mo's, so
running company work through Clarity is a cost leak. This does **not** apply to `$plan`
(decomposition only) or to personal/Studio work.

See `references/routing-and-hosts.md`, `references/authority-and-boundaries.md`,
`references/webhook-sandbox.md`, `references/reconciliation.md`.

## Verification

- The title carries exactly one lifecycle marker matching `Status` (`⏳`/`Do next`, `✅`/`Shipped`,
`⚠️`/`Do next`).

- The brief's acceptance criteria were exercised, not assumed.

- A pickup ping and a closing report both reached the home channel.

- A comment exists at each stage gate, including any block; the row was re-read.