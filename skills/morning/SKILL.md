---


name: morning
uuid: 3ff24dc8-ccd9-811b-bc51-e251da9273bf
version: 7
description: "Morning Reset"
return: "Day report: day · mail · calendar · synced · blocks · Do next · remotes · Needs Richard"
last-used: 2026-10-27T12:00:00+01:00
thinking: High
temperature: 0.3
resources:

- "@Resource-Index"

- "@Ship-DB-Reference"

- "@AI-Hub-DB"
author: Richard Dykes, Hermes Agent
license: MIT
metadata:
hermes:
tags: [morning, daily, planning, orchestration, clarity]
related_skills: [triage-inbox, triage-tasks, monday, mind-dump]


---


# Morning Reset

Orchestration and taste for the daily reset. It does **not** do the work: the deterministic half has already run, and each judgement step is its own skill on its own model.

## When to Use

- Richard starts his day, or wants the next day prepped.

- Not the weekly close (`$monday`) or a brain-dump (`$mind-dump`).

## Run mode

Establish the target **before** step 1 — it changes every window read. **Morning** (default) → today; **night before** → tomorrow, so a late run preps ahead instead of reporting a spent day.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Read the mechanical summary first.** The dagu DAG `morning-mechanical` runs at **08:00**, an hour before this job: it fixed the window, created or refreshed every new/moved calendar row, archived the mail noise, refreshed the OpenRouter embed and verified the board. Read `~/.hermes/state/morning/summary.json`. A step it already applied is **reported, not repeated**. The two processes are divorced — if the summary is missing or stale, say so and carry on; never wait for the DAG and never redo it.

1. **Dispatch ****`$triage-inbox`** at a **day** horizon.

1. **Dispatch ****`$triage-tasks`** — the blocks, then the `Do next` moves they justify.

  Each step is **one run of its own skill**: `hermes chat -q "<step>" --skills <name>`. Pass the target window and nothing else — never restate a step's rules, add guidance, or run two steps in one context.

1. **Remotes.** `herdr machine list`, then per remote: `workspace create` → `agent start --kind claude` → `agent prompt "<brief>" --wait --until idle --until done` → `agent read`. Work (Mambu) items run on **workbox, always Claude Code**; everything else on the **Studio, local-model-first**. Headless Claude Code needs `--allowedTools` set first. Unreachable → skip, name once; `blocked` → **Needs Richard**, never answered for it.

1. **Report — short.** Emit the shape below. Verify every block traces to a calendar gap and a ranked goal, and every new/moved calendar entry has a board row.

## Examples

- **Free morning** — no meetings before noon → `09:00–11:30 · Pricing model — cost lines`; its tasks moved to `Do next`.

- **Moved meeting** — the 14:00 review slipped to 15:30; the DAG refreshed the row, no duplicate.

## Boundaries

- Never send, submit or post — draft and flag only.

- Never delete a message; archive and label are the maximum mutations.

- Never clear Habitica or move a row to `Backlog` — those are `$monday`'s.

- Never invent a goal, task, meeting or draft.

- Never treat a `Focus Block`/`Lunch` placeholder as busy, or place a block over a commitment.

- Never answer a remote's `blocked` prompt on Richard's behalf.

## Output

Day · Mail · Calendar · Synced · Blocks · Do next · Remotes · Needs Richard.

## Taste

*Richard-originated, grown by **`$reinforce`**. Signal → preference.*

## Next steps

Run it on a weekday morning, or the night before when prep needs to start early.