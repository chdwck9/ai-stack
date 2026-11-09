---


uuid: 40d24dc8-ccd9-81a8-bba3-fff960d3a726
name: ats-cv-optimisation
description: "Use when tailoring a CV for automated screening."
version: 1
author: hermes-curator
license: MIT
metadata:
hermes:
tags: [career, cv, resume, ats, job-application]
related_skills: [career-pipeline, career-coach, job-search]


---


# ATS & CV Optimisation

## When to use

- Richard asks to check, tailor or improve a CV for a specific role.

- "Will this get past the ATS?" / "how do I customise my CV?" / "review my CV".

- Any application is about to be sent and someone wants it validated first.

Companion to `career-pipeline` (which owns the Notion Explore board, JD-to-evidence fit analysis, and the full ID-mode assessment). This skill owns the **screening layer**: how CVs are filtered before a human reads them, and how to make one survive that.

## First principles

- Never invent experience, metrics, dates, or qualifications. Evidence comes from the **Meta CV** (Richard OS, Notion). That is the source of truth; a CV is a derived view of it.

- **Reconcile every date and title against the Meta CV before the CV goes out.** Overlapping or contradicting date ranges are a verification flag and a real reason offers die — check them, do not trust the CV's own timeline.

- Separate verified evidence / plausible transfer / genuine gap. Do not let a desired claim imply evidence that does not exist.

## How the gate works (short version)

- **Greenhouse** is not a black-box auto-rejecter: *Talent Filtering* searches parsed CVs by keyword, where recruiters toggle keywords between **Preferred (OR)** and **Required (AND)** — auto-suggested from the job post — and *Real Talent* matching **ranks** applicants without auto-rejecting. AI is never the final decision-maker.

- Employers stack Eightfold / SeekOut / HireVue / LinkedIn Recruiter AI on top.

- The real gate is: **lexical keyword filter → semantic/LLM ranking → human shortlist.** Optimise for both the AND-filter and the rubric grader.

- Depth, mechanisms and sources: `references/screening-stacks.md`.

## Always-on rules

1. **Make the CV rubric-mappable** — one explicit, quantified outcome per JD requirement. This satisfies the lexical filter *and* gives the semantic grader something to score. Titles + thematic tags + project-name chips score ~zero on evidence; this is the most common fatal flaw.

1. **Head the CV with the JD's exact job title** (e.g. `Senior Product Manager`). Never an inflated variant (Lead / Group / Director) against a lower-level req — seniority inference trips the filter.

1. **Mirror the JD's own noun phrases verbatim, once each**, across the summary, a hard-skills / `AI & tooling` block, and 2–3 outcome bullets. Repetition adds no score and reads as keyword stuffing.

1. **Give both forms of every acronym once**: `Agent Client Protocol (ACP)`, `Model Context Protocol (MCP)`, `retrieval-augmented generation (RAG)`. Lexical AND-filters miss whichever form is absent.

1. **Parser-safe format**: single column; no tables, text boxes, columns, graphics, icons, headers/footers, or background images; standard headings (Summary, Experience, Skills, Education); dates as `MMM YYYY – MMM YYYY`; consistent title/company/date order; `.docx` or text-based `.pdf`.

1. **Two pages max** for senior IC/PM roles — length dilutes keyword density per screen and can push a required term outside the parsed window.

1. **Never** use hidden text, white-on-white keywords, or prompt-injection tricks. Screeners actively flag fraud; it is a disqualifier, not a shortcut.

1. Keep one designed/visual CV for portfolio use and a **plain single-column version for actual submissions** — do not try to make the designed one parseable.

## Procedure

1. **Source the requirement from the canonical posting**, not an aggregator. Prefer the employer's own board. Extract the JD's exact noun phrases and the "what success looks like" KPI language — that is the keyword set and the outcome rubric.

  - Greenhouse boards expose the full text via API: `curl -s "https://boards-api.greenhouse.io/v1/boards/<token>/jobs?content=true"` (HTML in `content`). Take the canonical req URL from `absolute_url` rather than trusting an aggregator link.

1. **Source live leads from Richard's job-alert mail** (his job-board signal lives in Gmail, not a scraped board): `~/config/google/gpers gmail search "...(from:jobalerts-noreply@linkedin.com...) newer_than:Nd"`. The **first ****`jobs/view/<id>`**** link in the alert body is the featured/primary job** matching the subject line. Verify the role↔URL mapping by `curl`-ing the public job page and reading `<title>` / `og:title` (works headless, no login). Aggregator URLs (Jooble, RocketHunt) go stale and hide the real req — always resolve to the employer's board.

1. **Read the CV as a parser would, before judging it.** Extract the text; if it is a designed PDF and extraction is empty or fragmentary, rasterise the pages and read them with vision. Report the parse failure as a finding — it is the reason the CV never reaches a scorer.

1. **Work the critique checklist** (below).

1. **Reconcile dates/titles to the Meta CV.**

1. **Deliver**: prioritised, specific corrections — name the exact line and the exact replacement. Then, if asked, produce the rewritten plain 2-pager mapped to the JD keywords (DOCX + text-PDF).

## Critique checklist

- **Evidence density** — quantified outcome per role, or only titles + thematic tags + project-name chips? (Most common fatal flaw.)

- **Parser-hostility** — designed layout, columns, rotated side rails, background logo walls, icons, CTAs.

- **Date integrity** — reconcile against the Meta CV; flag overlaps/contradictions.

- **Positioning** — does it lead with the target domain (e.g. platform + AI/agentic + data), or is it a generic "product leader" pitch?

- **Space allocation** — hobbies / "values" / "secret sauce" sections consuming page space that should carry achievements.

- **Hard-skills block** — present and matchable (SQL, Python, telemetry, Kubernetes, AWS, MCP, agentic, experimentation), not just thematic categories like "Strategy / Data / Leadership".

- **Header/contact** — specific location (`City, Country` — never a vague region); drop personal Notion links and "book a call" CTAs; LinkedIn + portfolio only.

- **Education** under a standard `Education` heading, not floating in the header.

- **Title alignment** — exact JD title, correct level.

## Pitfalls

- A designed/template CV (dark hero, logo wall, rotated rails, CTA button) usually has **no reliable text layer** — extraction fails or returns fragments. Confirm by extracting; then rasterise and read the pages with vision. Do not report empty extraction as "no content": the parse failure *is* the finding. Rasterise with PyMuPDF via `uv run --with pymupdf python ...` (`page.get_pixmap(dpi=170).save(png)`), which does not depend on a working system poppler.

- Aggregator job links (Jooble, RocketHunt, etc.) go stale and hide the canonical req — resolve to the employer's board before analysing or applying.

- **Do not re-run a full pipeline assessment on an already-assessed record.** Check the record first; if it was already assessed, treat the run as a *refresh* and change only what moved — do not reset its funnel stage.

- Intake/capture rows must stay unpopulated (title / Open Date / URL only). Pre-populating them with `Identified` status corrupts the funnel signal.

## references/

- `references/screening-stacks.md` — how Greenhouse and agentic/LLM screeners actually score, with evidence quality and sources.