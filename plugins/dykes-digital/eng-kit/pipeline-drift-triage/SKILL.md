---


uuid: 41324dc8-ccd9-81f8-835f-e3eb5236e1c1
name: pipeline-drift-triage
description: "Use when a scheduled pipeline publishes wrong data."
version: 1
thinking: High
temperature: 0.3
author: Richard Dykes, Hermes Agent
license: MIT
metadata:
hermes:
tags: [cron, dagu, automation, debugging, drift, verification]
related_skills: [dagu-pipelines, ship-db, monday, morning]


---


# Pipeline drift triage

A recurring job (dagu DAG, Hermes cron, launchd) has been quietly publishing wrong data — wrong dates, wrong category, missing priority — for days and nobody noticed. Find the *deterministic* step that does the writing, prove it against the canonical spec, fix it, and heal the records already written.

The model is almost never the bug. Scheduled automations are two layers:

- a **mechanical half** — a plain script, zero LLM, whose output lands in a state JSON;

- an **agentic half** — a skill run on a schedule that reads that JSON and does judgement work.

Drift lives in the mechanical half. It is the layer with no one reviewing it, and the layer that gets "simplified" when someone rewrites a frozen list into a derived one.

## When to Use

- A scheduled job has been writing wrong values for days: dates shifted, wrong category or priority, rows missing or doubled.

- The user reports a recurring automation "has done some weird thing" — vague symptom, no stack trace.

- You are about to rewrite a frozen input list in a mechanical script into a derived one — the change that most often introduces drift.

## Steps

1. **Read the last runs before touching anything.** `~/.hermes/cron/output/<job_id>_<ts>.txt` (one file per run) and the DAG's state directory (`~/.hermes/state/<job>/summary.json` plus one `<step>.json` per step). The per-step JSON names *which* step wrote what, so the guilty step is usually obvious — it is the one whose output matches the symptom.

1. **Map the symptom to a step, then to a script.** Find the DAG (`~/.config/dagu/dags/<name>.yaml`) or job definition and read every `run:` line. Open the one script that writes the field that is wrong.

1. **"Some, not all" is the key clue.** When only a subset is wrong, two producers write the same field: one on spec, one drifted (commonly the 08:00 mechanical run vs rows the agentic phase adds later). Diff what the two write, not just what the wrong rows look like.

1. **Load the canonical spec skill** for that data and diff the script against it line by line. Mechanical scripts are simplified copies of a skill; the bug is a rule the simplification dropped — a hardcoded default where the spec says route by attribute, a missing branch, a guard written for the old data shape.

1. **Read the live data to confirm**, not just the code. Query the target (board/database) for the window and print the field distribution — every row `#5` where the spec says `Connect`, and each of those sitting 2–3 days late. The distribution tells you the rule; the individual rows only tell you the symptom.

1. **Fix the script, then dry-run it.** Every writer should support `--dry-run` that prints the full payload and writes nothing. On a settled period a correct script reports **zero** creates/refreshes/corrections; a nonzero create count is itself a finding (see pitfalls).

1. **Heal, then re-verify by reading the target back.** Run live, then re-query the same window and print the field values. A successful call is not a successful outcome.

1. **Leave the durable note where the next run cannot delete it** (see Storage).

## Pitfalls

- **A read that errors is not an empty result.** Notion (and most query APIs) answer a rate limit with an error string; code that does `res.get("results", [])` reads that as "nothing exists" and then **creates a duplicate of every row it was supposed to find**. Treat a non-list response as a failure: retry with a delay, then raise. Duplicate board rows are usually this, not a human.

- **A guard written for an older data shape silently stops guarding.** "Only touch rows still on the week's Monday (the sprint-entry default)" is true for alert rows and false once a calendar step writes real meeting dates — Monday is then a real date, and the rule becomes "push every Monday meeting to Thursday". Whenever a step's assumption is expressed as a value test (`date == Monday`), pair it with a property test that identifies the *origin* (`is_datetime = 1`, `Priority = Connect`).

- **Never let a mechanical step overwrite a judgement call.** Auto-correct only where the value is the mechanical default it wrote (e.g. `#5` → the spec's priority); anything a human could have chosen deliberately gets *reported* as drift, not rewritten.

- **Archived rows: keep them in the dedupe set, exclude them from reports and corrections.** Dropping them resurrects them; editing them undoes a deliberate decision.

- **Route by attribute, never by envelope.** An event's owner is its *calendar*, not the account it was fetched through; shared calendars make the account a lie.

- **Don't rewrite history quietly.** If the mechanical half was wrong for weeks, name the rows already written wrong and offer the heal; do not silently edit records the user may have curated.

## Storage: where a durable note may live

Skill directories are replaced nightly from the AI Hub, so **a ****`references/`**** file (or a script) kept inside a skill tree is lost** — that is how a documented rule vanishes while the skill still cites it.

- Rules and specs → `/Volumes/Live/@Edge/.ai/resources/standards/` (indexed as a handle in `resources.md`), or compiled inline into the [SKILL.md](http://skill.md/) body.

- The AI Hub page is canonical: publish after every create or edit, and re-publish after patching a skill whose files would otherwise be restored from the stale Hub copy.

- Scripts → `~/.hermes/scripts/`, referenced by absolute path from the DAG.

## Verification

- Re-read the target window; every corrected row shows the spec value.

- Dry-run over the settled period reports zero changes.

- The per-step state JSON for the run matches what you claim was applied.

## Output

Symptom → the step and script that caused it → the rule it broke → what you fixed → rows healed → what still needs the user.