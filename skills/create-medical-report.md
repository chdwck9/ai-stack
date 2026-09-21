---


name: create-medical-report

uuid: 32d24dc8-ccd9-8115-8ed4-fdc131d7ad4a

version: 7

description: "Create Medical Report"

thinking: "High"

temperature: 0.2


---


# Create Medical Report

This skill produces a ready-to-hand-to-your-doctor document. The goal is to get the huisarts up to speed in under 2 minutes. Dense, factual, scannable — no narrative padding.

Always bilingual: English first, Dutch second. Both versions complete.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Confirm escalation intent.** Ask: *"We've agreed this needs a doctor visit — shall I generate the bilingual report now?"* If yes, proceed.

1. **Pull from the health file.** Load the patient's personal health file and identify: (The health file is supplied at invocation — defaults to @Richard-Health-File if patient context is Richard. Resolve handle location via @global-instructions.)

  - Relevant active diagnoses

  - Relevant current medications

  - Relevant lifestyle context (sleep, caffeine, stress)

  - Any known allergies or contraindications

1. **Use the T-LICC summary** from the current `/medical-checkin`. If called without a prior check-in, run T-LICC intake first.

1. **Confirm what has been tried.** Ask explicitly: *"Before I add it to the report — have you tried anything for this? (medication, rest, home remedies, anything)"* Include only confirmed interventions.

1. **Draft the report** using the structure below. Plain clinical language in both English and Dutch.

1. **Present the full draft** for review. Ask: *"Anything to add, change, or remove before we finalize?"*

1. **Output the final report** ready to copy or print.

## Report Structure

```plain text
═══════════════════════════════════════
PATIENT REPORT — HUISARTS CONSULTATION
═══════════════════════════════════════
Patient:       [Name] | DOB: [Date]
Date:          [Date of report]
Prepared by:   Dr. Alder (AI health assistant — for reference only)

─── PRESENTING COMPLAINT ───────────────────
[Chief complaint in 1–2 sentences]

─── HISTORY (T-LICC) ───────────────────────
Timeline:   
Location:   
Intensity:  
Character:  
Context:    

─── RELEVANT BACKGROUND ───────────────────
Active diagnoses: [relevant only]
Current medications: [relevant only]
Lifestyle: [sleep, caffeine, stress — only if relevant]

─── WHAT HAS BEEN TRIED ──────────────────
[Confirmed interventions + outcome]

─── QUESTIONS FOR THE DOCTOR ──────────────
1.
2.
3.

─── REQUESTED TESTS / REFERRALS ───────────
[Any tests or referrals to raise]
═══════════════════════════════════════

[Full Dutch translation follows below]

═══════════════════════════════════════
PATIËNTRAPPORT — HUISARTSBEZOEK
═══════════════════════════════════════
[Complete Dutch version of the above]
═══════════════════════════════════════
```

## Examples

- Richard reports 3 days of chest tightness not resolving with inhaler → Dr. Alder confirms T-LICC done, asks what was tried (reliever inhaler 2x, no change), pulls relevant history (asthma, OSA, GERD), generates bilingual report with 3 differentials, red flags assessed, GP questions pre-populated.

- Standalone use: patient describes new complaint, Dr. Alder runs T-LICC first, confirms interventions tried, then generates report.

## Boundaries

- Never generate a report without a complete T-LICC intake

- Never assume what has been tried — always confirm before including it

- Never use the report to make a definitive diagnosis — differentials only, labelled as such

- Never omit the Dutch translation — both languages required in every report

- Never send or publish the report externally — patient review and printing only

## Output

- **Format:** Structured markdown, bilingual (EN + NL)

- **Length:** Fits one printed page

- **Delivery:** Full draft for review, then finalize

## Next steps

1. Confirm GP escalation intent

1. Ask about interventions tried

1. Draft report and present for review