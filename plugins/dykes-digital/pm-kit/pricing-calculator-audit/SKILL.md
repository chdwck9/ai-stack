---


name: pricing-calculator-audit
uuid: 41c24dc8-ccd9-8113-9b6a-f3984a12298b
version: 6
description: "Pricing Calculator Audit"
return: pricing-audit-report
last-used: "2026-11-18T15:10:00+01:00"
thinking: High
temperature: 0.2
resources:

- calculator: [https://docs.google.com/spreadsheets/d/17aoou9UJVnCLg6I60PY0IY_S5OeFnhjTO8eiiHL4y78/edit?gid=1765971382](https://docs.google.com/spreadsheets/d/17aoou9UJVnCLg6I60PY0IY_S5OeFnhjTO8eiiHL4y78/edit?gid=1765971382)


---


# Pricing Calculator Audit

Audit a Mambu pricing calculator version: what is broken, questionable, or needs a decision. Every finding is reproducible and numbered.

## Steps

Copy into the task list; mark skips `skip: <reason>`.

1. Open the calculator (header link) via the Sheets connector; pull formulas. A supplied export is audited instead, labelled not-master. Neither available → ask.

1. Read Current Version, Last Updated and Version owner from the Change Log header, by label. If the version differs from the one named, ask which.

1. Find the prior audit (user link, Docs, past chats): re-audit (steps 8–9 apply) or full.

1. Map the flow once: Deal Config → Year sheets → Deal Spec → Deal Review. Skip Quote Preview (not implemented).

1. Trace every family below, reading formulas.

1. Classify each candidate: By design → drop; Decision → Decisions table; else Finding, acknowledged items included, every run. Set Type and Priority per Rules.

1. Recompute one example per finding; reproduce each P1 on a copy.

1. Re-audit: diff old against new export cell by cell. Status from the diff, never release notes. Tag new problems Introduced or Late find.

1. Carry standing decisions until answered.

1. Write the Output as a Claude Docs page (Status a dropdown chip per row), then self-check the gate.

1. Fixes, only when the owner names them this session: apply exactly those to the master, re-read each changed cell, set Status Fixed and Comments `Automated through Claude`.

## Example

Header: `Pricing Calculator v19.2.11 Audit`, then `v19.2.11 · Owner <Version owner> · Last updated 2026-11-13 · Audited 2026-11-18`. Row:
`F4 | Bug | Bundle discount ignores volume | Year n!E27 | Five 1-account products unlock 30% off: −€266k/yr at 1M accounts | Count a product only at its card minimum | P1 | Open | |`

## Boundaries

- Read-only. Edit the master only for fixes the owner names this session (Step 11); never otherwise.

- No audit without sheet or export.

- Never report By design items; never set Status to Planned (the owner marks it).

- State each finding once; elsewhere cite its ID.

- Name no people or customers, except the Version owner in the header.

## Output

1. Title and header line, linked to the master; re-audit adds `vs vA.B.C`.

1. Verdict, ≤3 sentences: headline defects; counts by priority and Type; re-audit adds fixed, open, new.

1. Scope, one line: formula trace of the export, not recalculation.

1. Release changes (re-audit): ≤6 bullets, price or approval movers only.

1. Findings register, sorted by priority then impact: ID | Type | Issue | Where | Impact | Fix | Priority | Status | Comments. Where ≤2 refs; Impact ≤20 words with a number; Fix ≤12 words (the planned fix if known) or `Decision Dn`. Status dropdown: Open, Planned, In progress, Fixed, Changed; default Open. Comments empty, except `Automated through Claude` on rows fixed in Step 11. P3s last, one line each.

1. Decisions: Decision | Today | Recommendation | Findings | Comments. Standing and new.

Gate: header from Change Log; counts match rows; every row has Type, number, one-action Fix; no By design item; no Planned pre-set; no repeats or names.

## Rules

- **Type.** Bug: broken formula or clear defect. Error: bug under conditions (bad selection → #N/A; hard-code not updating with currency or location). Logic: questionable practice or uneven logic (e.g. Year 0); goes to Decisions or owner, P2 at most.

- **Priority.** P1: wrong price, approval route or confidential exposure on live deals, reproduced. P2: distorts margin, misleads policy, breaks a downstream view; advisory-flag gaps and overage defects cap here (CPQ enforces approvals and calculates overages). P3: latent or cosmetic.

- Release regressions are expected (weekly cadence): state the pattern once, not per row.

- **False positives.** Each finding needs an openable cell, its trigger condition and a reproduced number. Owner intent beats inference; unsure → Decision or drop.

## Families

- **Approval:** thresholds on every band; averages including empty years; discounts netted against uplifts; bundle discounts ignoring volume or card minimums; margin 100% at zero revenue; missing red rules.

- **Pricing:** hard-codes not converting across currency; typed prices where siblings look up; uneven or double uplifts; wrong location index; cheapest-tier defaults; reversed lookups; placeholder tables; allowances differing from spec.

- **Flow:** inputs with no Deal Spec row; options doing nothing; wrong SUM ranges; broken refs; offset lookups shifting on row insert.

- **Margin:** zero costs; cost of sales missing or applied to cost; label mismatches returning 0%.

- **Data:** customer data in copies; validation gaps giving wrong non-zero prices.

- **Year 0:** inconsistent price and cost rules; wrong defaults; billing without volume.

- **Release:** renamed labels breaking lookups; new defaults; moved rows, #REF! names.

## Taste

- Margin shown as 100% on a zero-revenue year → Logic, not Bug.

- Two counts feeding one discount that disagree → Error, not Logic.

## Business context

Early-warning tool in Sheets. AEs and CSMs use Deal Review; Deal Spec takes line items, not subtotals.

**By design (drop):** PS valued before discounts; legacy add-ons; discounts and flags not reaching Year sheets; missing Core Banking subtotals; terms over 5 years; fixed Deal Spec offsets; bad inputs zeroing prices; static FX; Sheets limits (unlockable copies, no update mechanism); template sheet; Change Log breaking-change logic; Business Lending priced as Mortgages; placeholder credit bundles; headline ACV spanning the whole year; typed base prices on product cards (final price converts by currency and location; costs mix formula and typed values); TAM cost of sales of 0 (row kept for visibility).

**Acknowledged (report; owner marks Planned; planned fix goes in Fix):** Mambu Credits bundled/additional split; Agents default to cheapest tier; Payments base subscription typed (currency conversion applied); MCP/Agents allowance mismatch (Mambu Intelligence Platform sheet is official); zero product and connector costs; no Payments cost of sales (Agentic Platform has one: lookup header must equal the Deal Review section label); scratch sheets; unused named ranges; unwired Year totals.

**Standing decisions (carry):**

- D1: Payments location pricing: actual rate or simplified premium.

- D2: Exclude service-level fees from discount metrics (only PS today).

- D3: Year 0 billing policy, one standard across Payments, Core Banking, Agentic.

- D4: Service-level uplift: product fee only, or all software.

- B2: Product and Engineering control over Payments pricing and cost.