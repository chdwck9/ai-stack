---


name: investigate

uuid: 3d824dc8-ccd9-81ab-b083-ea8b98692131

version: 2

description: "Investigate"

return: "investigation record"

tools:

  - notion

  - atlassian

thinking: "High"

temperature: 0.3

resources:

  - "@Resource-Index"


---


# Investigate

Root-cause investigation (P1) for anything behaving wrongly: a bug, a failing EOD job, a pricing mismatch, a CPQ/calculator divergence, drifted data, a broken workflow. Iron law: no fix without a named mechanism.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Verify the symptom is real.** Reproduce it or fetch primary evidence (the failing dashboard panel, the mismatched cells, the error). If it can't be evidenced, stop and say so — no investigating rumours.

1. **Freeze the blast area.** Note what must not be changed while investigating; no fixes, workarounds, or cleanups yet.

1. **Gather evidence (P3).** Pull from the sources this environment reaches — Grafana, sheets, Jira, specs, logs, Slack — targeted queries only (P15). Timeline the facts.

1. **Hypothesis ladder.** List candidate mechanisms; test in order of cheapest-most-discriminating first. Each test is a verifiable unit (P17) with a predicted result. Three consecutive failed hypotheses → stop, widen the frame, re-read the evidence; never brute-force.

1. **Name the mechanism.** The cause is a mechanism ("the p99 gauge persists after job completion"), not a category ("monitoring issue"). Trace it to where all affected paths route through.

1. **Fix once at the root — or hand off.** Within permissions: apply the single root fix plus a check that would catch recurrence. Outside them: package the mechanism, evidence, and proposed fix for the owner.

1. **Record.** Symptom → evidence → hypotheses tested → mechanism → fix → recurrence check.

## Boundaries

- Never fix a symptom while the mechanism is unnamed

- Never exceed three failed hypotheses without stopping to widen

- Never modify evidence sources during investigation

- Never blame a person — mechanisms only

- Fixes respect the universal write guard; external-system fixes are proposed, not applied, unless explicitly authorised

## Output

Artefact contract: investigation record with all six elements (symptom, evidence timeline, hypotheses + results, mechanism, fix/hand-off, recurrence check). Hand-off: $AI/artefacts/investigate/<yyyy-mm-dd>-<slug>/ or @Inbox; linked to the relevant Jira/MCD where one governs.

Self-check gate: verify every element before finishing; missing → do the work, do not finish.

## Examples

1. "check24 AUTHORIZATION_HOLDS shows 19.8h" → evidence: gauge vs counter → mechanism: stale p99 series with no recency gate → fix: increase() gating clause + alert-rule check; record linked to EOD MCD.

1. "CPQ and calculator disagree on DR Plus" → three hypotheses, second confirms: calculator updated, CPQ price rule not migrated → hand-off package to CPQ owner (write access out of scope), P16 flagged.

## Next steps

Invoke with the symptom and any evidence already in hand.