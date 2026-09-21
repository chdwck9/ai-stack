---


name: swarm

uuid: 3d824dc8-ccd9-81fb-87de-c5ae28b75589

version: 2

description: "Swarm"

return: "merged report"

tools:

  - notion

thinking: "Medium"

temperature: 0.3

resources:

  - "@Resource-Index"


---


# Swarm

Fan out one identical job across many independent units — one worker per unit, one merged report. Units: skills in the hub, tenants on a dashboard, sections of a spec, files in a folder, rows in a table.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Decompose.** Enumerate the units and write ONE brief every worker gets verbatim: task, inputs, required output shape. Units must be independent — no shared write targets, no ordering. If they aren't, stop: this is a sequence, not a swarm.

1. **Cap and confirm scope.** >20 units → propose a sample or batching before spending tokens (P18).

1. **Execute.**

  - Claude Code/Cowork: spawn one subagent per unit (batches of ~5), identical brief, `fast` tier where the unit job is mechanical.

  - [claude.ai](http://claude.ai/) (no subagents): run units sequentially in batches; after each batch, compress state to a hand-off block (results only, raw intermediates discarded — P15) before the next.

1. **Collect.** Reject worker outputs that don't match the required shape; re-run those units once; twice-failed units are reported as failed, not silently dropped.

1. **Merge.** One deduplicated report: per-unit result table + cross-unit patterns + failures. No per-worker narration.

## Boundaries

- Never swarm dependent units — decompose differently or refuse

- Never vary the brief between workers — one brief, verbatim (anti-drift)

- Never let workers write to shared targets; merge happens once, at the end

- Never exceed the cap without the Step 2 confirmation

- Worker failures are reported, never papered over

## Output

Artefact contract: unit inventory + the verbatim brief · per-unit result table · cross-unit patterns · failed units. Hand-off: $AI/artefacts/swarm/<yyyy-mm-dd>-<slug>/ or @Inbox.

Self-check gate: every enumerated unit appears in the table exactly once (result or failure); missing → do the work, do not finish.

## Examples

1. "/swarm: check all 54 installed skills for old model-field names" → 54 units, mechanical → fast tier, batches of 5 → table: 51 clean, 2 stale, 1 unreadable (reported); pattern: both stale files predate the Sep 4 migration.

1. "/swarm: rate each Tier 1 tenant's EOD health this week" → 9 units → [claude.ai](http://claude.ai/) sequential batches of 3 with compressed hand-offs → merged table + pattern (sonae latency outlier).

## Next steps

Invoke with the job and the unit set (or where to enumerate it from).