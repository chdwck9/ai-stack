---


name: review

uuid: 3d824dc8-ccd9-8177-b1df-e0e2088e97c7

version: 3

description: "Review"

return: "review report with verdict"

tools:

  - notion

thinking: "High"

temperature: 0.3

resources:

  - "@QA-Standards"

  - "@Design-Standards"

  - "@Document-Standards"

  - "@Spec-Standards"

  - "@Engineering-Principles"

  - "@Resource-Index"


---


# Review

One review entry point. Match the artefact type to its governing standard, lazy-load only that standard's Review notes, run the checks, produce a verdict. Standards are global resources — the same document governs production and review, edited in one place. Review-only by default; fixes applied only when invoked with `fix`.

## Routing

Ambiguous or composite → say which standards apply, run each, one merged report. No match → closest standard + note the gap for /reinforce.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Identify the artefact and stakes.** What is it, who consumes it, what does shipping it commit to?

1. **Route and lazy-load** the matched standard(s) via @Resource-Index — read the Review notes section (and skim the core standards for context); load nothing else (P15).

1. **Run the checks** against the real artefact (P3): open it, execute it, render it — never review from its description.

1. **Findings table.** Severity (BLOCKER / MAJOR / MINOR) · location · what's wrong · proposed fix. Every finding cites where it was observed; principle violations cite P-IDs.

1. **Verdict + fixes.** SHIP / SHIP-WITH-CONCERNS / BLOCK, one line of reasoning. With `fix`: apply MINOR fixes to the working copy, list what changed; MAJOR/BLOCKER fixes always stay proposals.

## Boundaries

- Never review from a summary or memory of the artefact — open the real thing

- Never review from a recalled standard — fetch the live standard's Review notes

- Never a findings list without a verdict; never a verdict without findings (or an explicit clean pass)

- Never apply MAJOR/BLOCKER fixes, or any fix without the `fix` flag

- Never soften severity to be polite — P7

## Output

Artefact contract — the report's final section is always: REVIEW REPORT: artefact · standard(s) applied · findings table · verdict line · fixes applied (or none). Hand-off: $AI/artefacts/review/<yyyy-mm-dd>-<slug>/ or @Inbox.

Self-check gate: confirm the report's last heading is REVIEW REPORT with table + verdict present; missing → do the work, do not finish.

## Examples

1. "/review the Mambooster DR deck" → @Design-Standards + @Document-Standards → 2 MAJOR (tier pricing contradicts pricing MCD; slide 7 slop scan), 4 MINOR → SHIP-WITH-CONCERNS.

1. "/review fix the draft PgM update" → @Document-Standards → 1 MAJOR (unsupported claim, proposal only), 6 MINOR applied (tells stripped, P8) → SHIP after MAJOR resolved.

## Next steps

Invoke with the artefact (or its location) and optionally `fix`.