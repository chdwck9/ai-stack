---


name: career-pipeline

uuid: 3d424dc8-ccd9-81bb-b5c8-e4b93ed4f366

version: 6

description: "Capture interesting jobs from Notion Clipper, then assess and enrich them in ID mode with job-spec retrieval, fit analysis, company research, salary benchmarking, recruiter identification, automation assessment, thought-leadership opportunities, and a durable Notion record."

thinking: "Medium"

temperature: 0.3


---


# Career Pipeline

## Modes

### Save mode

Use when the user is saving a new, interesting job via the Notion Clipper. The Clipper creates the opportunity page in the Notion Explore database with only the automatic properties populated: title, Open Date, and URL.

Do not perform the full assessment in Save mode. The purpose of Save mode is capture, not analysis.

### ID mode

Use when the user explicitly invokes ID mode for the career pipeline. Find the newly saved/unpopulated job records in the Notion Explore database and enrich them using the full workflow below.

An unpopulated job is a record where the Clipper has supplied the automatic fields but the assessment/logging fields remain unfilled. Do not require the job to have been created in the current conversation.

## ID Mode Workflow

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. Identify the unpopulated job record(s) in the Notion Explore database. Use the automatic title, Open Date, and URL to determine which records require enrichment. Do not overwrite already assessed records unless the user explicitly asks for a refresh.

1. Retrieve the job posting from the page's supplied URL where possible. Use the actual source posting as the primary source. If the page cannot be retrieved, continue with the assessment using whatever reliable information is available, but explicitly mark the unavailable job-spec sections rather than reconstructing them from memory.

1. Perform JD-to-evidence fit analysis using Richard's current Master Resume / Master Portfolio as source assets. Compare the JD against Richard's evidence and identify strong matches, transferable evidence, missing evidence, hard blockers, addressable gaps, and positioning opportunities. Never silently compensate for a gap: if evidence is absent or ambiguous, label it explicitly and either ask a targeted question or preserve it as a gap. Where a material requirement may be satisfied by experience not explicit in the Meta CV, ask a brief L2 interview of up to 5 targeted questions rather than inferring evidence.

1. Assess fit:

  - Identify strong matches and transferable evidence.

  - Identify experience/qualification mismatches, missing evidence, and material risks. Do not reframe or infer missing evidence as a match; distinguish demonstrated evidence, plausible transfer, and genuine gap.

  - Distinguish hard blockers from addressable gaps.

  - Flag red flags in the role itself, including suspiciously broad scope, title/seniority mismatch, unrealistic expectations, excessive role stacking, or other concerns visible from the posting.

1. Research the company using current web sources, with particular attention to the last 18 months. Look for layoffs, restructuring, hiring freezes, executive churn, financial distress, major strategy changes, litigation/regulatory issues, culture concerns, or other credible hiring red flags. Also identify recent product/company momentum that materially affects the opportunity. Separate verified facts from inference and community sentiment.

1. Estimate a recommended salary range for negotiations in the relevant market. Provide the likely market range, recommended target/base range for Richard, negotiation anchor, assumptions, and confidence. Use current web research where salary data is needed.

1. Draft a concise cover letter in Richard's voice. Invoke `$unslop` and use its final output. Keep the letter specific to the company and role, avoid generic enthusiasm, and never invent experience.

1. Provide CV and career-surface guidance: assess whether the existing CV template/layout is sufficient; identify only sections that need changing; recommend the highest-value evidence and keywords to surface. Where requested, draft the full tailored resume, relevant LinkedIn sections, and cover letter from the Meta CV while maintaining factual integrity. Run consistency checks across dates, titles, technical claims, and achievements. Identify any new evidence that should be proposed for the Meta CV, but do not update the source of truth without approval. Do not rewrite the whole CV unless requested.

1. Identify the recruiter. Check the supplied job spec first. If not named, actively search the web and relevant professional sources for the recruiter or likely hiring contact. Clearly label confirmed vs likely matches.

1. Assess job-spec automation potential. Estimate what proportion of the role's stated activities could realistically be automated or substantially accelerated with current AI/software tooling. Separate: (a) highly automatable work, (b) AI-assisted but human-owned work, and (c) inherently human/context-dependent work. Give an overall percentage estimate, explain the assumptions, and identify the highest-value automation opportunities. Do not equate "AI-assisted" with "fully replaceable".

1. Create a durable job-posting snapshot in the opportunity page. Preserve the source as it existed at assessment time, prioritising the actual posting text for: role summary, responsibilities/activities, minimum/required qualifications, preferred qualifications, experience requirements, location/work model, compensation if stated, and application-specific questions or constraints. Preserve section headings and wording as closely as practical. Record the source URL and snapshot date. If the full posting cannot be retrieved, explicitly mark which sections are unavailable rather than reconstructing them from memory or secondary sources.

1. Identify 3–5 thought-leadership content opportunities based on the 3–5 problems the role is likely to need to solve in its first year. Find the intersection between those problems and Richard's demonstrated experience, interests, and credible opinions. For each piece include:

  - Working title / provocative thesis

  - First-year problem it signals understanding of

  - Richard's relevant experience / evidence

  - The opinion or distinctive angle he could credibly contribute

  - Best format

  - Hiring signal

  Prioritise useful judgment over generic career content. Do not imply Richard has solved problems he has not encountered; where evidence is indirect, frame the piece as a perspective, hypothesis, or proposed approach.

1. Enrich the Notion Explore database record. Set `Jobs` = `0 - Identified`; `Status` = `Identified`; `Last Connection` = today; `Next Connection` = tomorrow; `Actions` = `Reply to job spec`; `Where` = the company name from the job posting; `Tags` = best matching role type from the database, e.g. `Product Manager`; and retain the existing `Open Date` and `URL` values created by the Clipper. If the company is not already an option in the `Where` select, use the exact company name from the posting and create/use that select option where the Notion integration permits it; do not substitute a different label.

1. Before updating the Notion record, fetch the current database schema and use exact property names/options. Do not guess option names or property types.

1. The job must be moved to `0 - Identified` and `Identified` even if the job posting could not be retrieved. Failure to retrieve the source is not a reason to leave the job unclassified. Record the retrieval limitation in the page content and continue with all analysis that the available evidence supports.

## Output

For ID mode, return the assessment in this order: 1) Fit verdict, 2) Mismatches and red flags, 3) Company research and hiring risk, 4) Salary range and negotiation position, 5) Job-spec automation assessment, 6) Cover letter, 7) CV notes, 8) Recruiter lead, 9) Thought Leadership Content Opportunities, 10) Notion logging confirmation.

The Notion record must additionally contain clearly separated sections for `Assessment`, `Mismatches and red flags`, `Company research and hiring risk`, `Salary`, `Job-Spec Automation Assessment`, `Job Posting Snapshot`, and `Thought Leadership Content Opportunities`, plus the supporting cover letter, CV notes, recruiter lead, and logging context.

## Boundaries

- Never invent experience, qualifications, recruiter identity, salary data, or company facts.

- Use current web research for company, recruiter, and salary information.

- Treat salary ranges as estimates, not guarantees.

- Separate hard mismatches from addressable gaps.

- Keep the cover letter concise and human.

- Use Richard's current career context. Mambu is current; NavVis is previous.

- Tailored CVs and career surfaces must derive from the Meta CV and preserve factual integrity.

- Do not force AI/agentic-AI claims where Richard lacks direct evidence.

- In Save mode, do not perform the full assessment. The Clipper-created record is the intake state.

- In ID mode, preserve the Clipper-created `Open Date` and `URL` rather than replacing them.

- If the job link is absent, leave `URL` as-is/blank and note that the posting could not be retrieved.

- Never silently replace a missing job-posting section with invented or remembered wording. Mark unavailable sections explicitly.

- Treat the job-posting snapshot as evidence captured at the time of assessment, not as a live copy. Record the snapshot date.

- Automation percentages are estimates based on the activities actually stated in the posting, not generic assumptions about the profession.

- If the recruiter cannot be identified with reasonable confidence, say so.

- If Notion updating fails, report the failure and do not claim the opportunity was enriched.

## Resources

- `$unslop`

- Richard's Master Resume / Master Portfolio

- Notion Explore database

## Notion Logging Contract

The Notion Clipper is the intake mechanism. It creates the initial opportunity record with only automatic fields populated: title, Open Date, and URL. ID mode is the enrichment mechanism.

Every ID-mode run must leave the record in a deterministic identified state regardless of source retrieval success:

- `Jobs` = `0 - Identified`

- `Status` = `Identified`

- `Where` = company name when the company can be established

- `URL` = original Clipper URL, unchanged

- `Open Date` = original Clipper date, unchanged

- `Last Connection` = today

- `Next Connection` = tomorrow

- `Actions` = `Reply to job spec`

- `Tags` = best matching role type

- Page content = assessment, evidence-backed job snapshot, automation assessment, and thought-leadership opportunities

The database record is the durable system of record. Do not claim an opportunity is fully processed until the Notion update succeeds.