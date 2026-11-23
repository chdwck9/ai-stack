---


uuid: 40d24dc8-ccd9-81a8-bba3-fff960d3a726
name: ats-cv-optimisation
description: "Use when tailoring a CV for a role, ATS or referral."
version: 4
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

- Richard is sending a CV to a contact or referrer for named or "earmarked" roles (see *Referral-route applications*).

- "Will this get past the ATS?" / "how do I customise my CV?" / "review my CV".

- Any application is about to be sent and someone wants it validated first.

Companion to `career-pipeline` (which owns the Notion Explore board, JD-to-evidence fit analysis, and the full ID-mode assessment). This skill owns the **screening layer**: how CVs are filtered before a human reads them, and how to make one survive that.

## First principles

- Never invent experience, metrics, dates, or qualifications. Evidence comes from the **Meta CV** (Richard OS, Notion). That is the source of truth; a CV is a derived view of it.

- **Reconcile every date and title against the Meta CV before the CV goes out.** Overlapping or contradicting date ranges are a verification flag and a real reason offers die — check them, do not trust the CV's own timeline.

- Separate verified evidence / plausible transfer / genuine gap. Do not let a desired claim imply evidence that does not exist.

- **Separate evaluation from implementation when the CV claims a tool.** Vendor analysis, contract negotiation and a decision *not* to adopt are real evidence, but they are not usage. Write "ran the analytics vendor evaluation and negotiation; the team chose Segment" rather than anything that implies the tool shipped, and source the hands-on claim only from where it genuinely exists (personal builds, a later role). The judgement not to adopt is a selling point with a product-led vendor, so give the reason instead of hiding the gap: "evaluated migrating, the stack was already saturated, so I did not propose it" reads as seniority. When the user corrects a tool claim like this, fix the Meta CV too and record the precise facts in its `agent_notes` — otherwise the next session re-derives the stronger, wrong version from a bullet that still says "implemented".

- **Never derive years-in-domain by summing role headings in the Meta CV.** One capability thread runs across several headings — an employer block titled "Data Science, 2013–2018" can sit inside a much longer data career, and a second heading for the same years gets read as a different job. Heading arithmetic therefore undercounts, and the undercount gets reported back to Richard as a gap he then has to correct. Establish the total from the Meta CV's `agent_notes` and evidence index first; if it is still ambiguous, ask one direct question ("how many years of that, and in what capacity?") instead of declaring a shortfall.

## How the gate works (short version)

- **Greenhouse** is not a black-box auto-rejecter: *Talent Filtering* searches parsed CVs by keyword, where recruiters toggle keywords between **Preferred (OR)** and **Required (AND)** — auto-suggested from the job post — and *Real Talent* matching **ranks** applicants without auto-rejecting. AI is never the final decision-maker.

- Employers stack Eightfold / SeekOut / HireVue / LinkedIn Recruiter AI on top.

- The real gate is: **lexical keyword filter → semantic/LLM ranking → human shortlist.** Optimise for both the AND-filter and the rubric grader.

- Depth, mechanisms and sources: `references/screening-stacks.md`.

## Always-on rules

1. **Make the CV rubric-mappable** — one explicit, quantified outcome per JD requirement. This satisfies the lexical filter *and* gives the semantic grader something to score. Titles + thematic tags + project-name chips score ~zero on evidence; this is the most common fatal flaw.

1. **Head the CV with the JD's exact job title** (e.g. `Senior Product Manager`). Never an inflated variant (Lead / Group / Director) against a lower-level req — seniority inference trips the filter. Two sub-rules for every other title on the page:

  - **In-body role titles lead with the noun the req screens for.** Where a role could honestly be described either as an entrepreneurial title (`Founder`, `Head of X Lab`) or a product title, use the product title on an IC-level req and carry the founder scope in the first bullet ("Founded X and ran it as a business…"). `Founder` reads as a different job family and invites an overqualified screen; the bullet preserves the same scope as evidence rather than as a label.

  - **Never put a parenthetical justification inside a title field** (`(before X was a thing)`, `(contract)`). Parsers and recruiters read the field literally, and an aside invites the reader to test the claim instead of accepting it. Move the point into a bullet, where it can be evidenced.

1. **Mirror the JD's own noun phrases verbatim, once each**, across the summary, a hard-skills / `AI & tooling` block, and 2–3 outcome bullets. Repetition adds no score and reads as keyword stuffing.

1. **Give both forms of every acronym once**: `Agent Client Protocol (ACP)`, `Model Context Protocol (MCP)`, `retrieval-augmented generation (RAG)`. Lexical AND-filters miss whichever form is absent.

1. **Parser-safe format**: single column; no tables, text boxes, columns, graphics, icons, headers/footers, or background images; standard headings (Summary, Experience, Skills, Education); dates as `MMM YYYY – MMM YYYY`; consistent title/company/date order; `.docx` or text-based `.pdf`.

1. **Two pages max** for senior IC/PM roles — length dilutes keyword density per screen and can push a required term outside the parsed window.

1. **Never** use hidden text, white-on-white keywords, or prompt-injection tricks. Screeners actively flag fraud; it is a disqualifier, not a shortcut.

1. Keep one designed/visual CV for portfolio use and a **plain single-column version for actual submissions** — do not try to make the designed one parseable.

1. **The submission artifact is a text-layer ****`.pdf`**** or ****`.docx`****; never ****`.md`****, never a design-tool export alone.** Applicant portals accept pdf/docx/txt — a `.md` upload fails the file-type check or parses to near-nothing, scoring zero before a human reads it. A Figma/Canva export degrades parsing even when it carries a text layer. Hold the split explicitly: the `.md` is the canonical source, the PDF is what gets submitted, and the designed version is the portfolio link or a second attachment where the portal takes several files.

1. **Frame in-flight work so the claim cannot become false.** Write "leading the commercial model for X" rather than "launched X" until launch is confirmed, and switch to the past tense only once it has shipped. A CV assertion that goes stale when a date slips is worse than a softer one that stays true, and interviewers ask how the launch went. Same rule for unreleased product names: use the generic description ("a usage-based credit unit") in any external document unless the name is already public — naming someone else's unlaunched product is not the candidate's call. Apply the same precision to what actually shipped: "launched the commercial model for the platform" is not "launched the platform" — widening the object to the larger thing it sits inside is a claim the interviewer will test against that thing's own timeline.

1. **Decline to tailor when the req fails a stated hard requirement — deliver the fit verdict instead.** Producing a CV for a req the candidate cannot clear converts effort into a rejection, and on a large board it also burns the employer: most ATSs enforce a re-application cooldown (often 6–12 months), so a speculative application costs the next real opening there. Grade the qualification language before deciding: "ideally", "a strong advantage", "bonus points", "or equivalent practical experience" are soft and never block; an unqualified "N+ years of …", a named framework or credential, or a required domain ("IATA BSP/ARC", "GCP in production", "2+ years managing PMs") does. Quote the failing requirement verbatim, name the cooldown risk, and offer the reusable master CV plus a watch on the board rather than a tailored file. Adjacency is not a qualification: a genuine analogy to the candidate's evidence does not clear an explicitly required domain.

1. **No em-dashes, and no internal provenance, in any career surface.** The em-dash character is banned outright in CVs, cover letters and referral notes: use a full stop, comma, colon or brackets, and keep the en-dash only inside a numeric or date range. Strip every reference to the machinery that produced the document too: "the Meta CV", "the docs", "the MCD", "the evidence index", "cited in the evidence", "documented in", "as recorded in". The reader has never seen that system, and a provenance clause makes a CV read as a personal wiki leaking into a job application. State the underlying fact instead ("its reporting was instrumental in the case for an $85M round") and leave the source where it belongs. `scripts/render_cv.py` fails loudly on both.

1. **Write tighter than Richard talks.** He is wordy: stacked clauses, runway before the claim, qualifications tacked on after it. Halve it. One idea per bullet, active verb, concrete noun, no warm-up. The eccentricity budget is about 10% per document: one dry aside or one unusual concrete phrase, never in the summary's first sentence and never once per bullet. If a reader notices the personality before the evidence, it is over budget. His verbal hedges ("I think", "probably", "kind of") belong in conversation, not in a CV: do not add them, and do not strip them from text he wrote himself.

## Procedure

1. **Source the requirement from the canonical posting**, not an aggregator. Prefer the employer's own board. Extract the JD's exact noun phrases and the "what success looks like" KPI language — that is the keyword set and the outcome rubric.

  - Greenhouse boards expose the full text via API: `curl -s "https://boards-api.greenhouse.io/v1/boards/<token>/jobs?content=true"` (HTML in `content`). Take the canonical req URL from `absolute_url` rather than trusting an aggregator link.

  - **Re-verify the req is live at tailoring time, and match on title + location rather than a remembered job ID.** Postings get pulled and re-listed under a *new* ID, so a saved "appears closed" verdict can be wrong and a stored ID silently returns nothing. Fetch the whole board once (a large employer runs 200–300 open reqs), filter `title` and `location` in Python, and take the ID and `absolute_url` from that response. Report the check in the answer: "job X is no longer on the board; the same title is live as job Y" is a finding the user needs *before* any tailoring.

  - Strip the JD HTML to text before extracting keywords (`<li>` → `- `, block-level tags → newline, drop remaining tags) so the "What you'll do" / "Who you are" bullets survive as separate lines rather than one paragraph.

1. **Source live leads from Richard's job-alert mail** (his job-board signal lives in Gmail, not a scraped board): `~/config/google/gpers gmail search "...(from:jobalerts-noreply@linkedin.com...) newer_than:Nd"`. The **first ****`jobs/view/<id>`**** link in the alert body is the featured/primary job** matching the subject line. Verify the role↔URL mapping by `curl`-ing the public job page and reading `<title>` / `og:title` (works headless, no login). Aggregator URLs (Jooble, RocketHunt) go stale and hide the real req — always resolve to the employer's board.

1. **Read the CV as a parser would, before judging it.** Extract the text; if it is a designed PDF and extraction is empty or fragmentary, rasterise the pages and read them with vision. Report the parse failure as a finding — it is the reason the CV never reaches a scorer.

1. **Work the critique checklist** (below).

1. **Reconcile dates/titles to the Meta CV.**

1. **Deliver**: prioritised, specific corrections — name the exact line and the exact replacement. Then, if asked, produce the rewritten plain 2-pager mapped to the JD keywords (DOCX + text-PDF).

1. **Render and verify, do not describe.** Generate the PDF/DOCX from the `.md` with `scripts/render_cv.py`, then confirm the page count with `pdfinfo` and read the rendered pages with vision before handing it over. Layout defects that only appear at render time are normal — italic role sub-lines and education lines collapsing into the preceding paragraph, a wrapped contact line, a third page — and they are invisible in the markdown.

## Referral-route applications

A referral is a different channel, not a better CV. The first reader is a human, but the application still has to be filed against a req in the ATS with the referral attached — a CV emailed to a contact starts no process.

- **Get the exact req ID from the referrer before tailoring.** "Earmarked roles" is not a target, it is a guess that spends the referral. Ask which req(s), and confirm they are still live and funded.

- **One CV per req.** A single file tailored to three roles reads as tailored to none, and duplicate applications on the same board get flagged.

- **The referrer's note to the recruiter outranks the CV.** Offer to draft it: req ID, three lines on fit, one proof metric, and the logistics the recruiter will ask about (location/commute, work-model acceptance).

- **The file you send is the file that gets parsed.** A referral does not bypass the ATS, so the same parser-safe, rubric-mapped version goes into both places.

- **Keep constraint arguments out of the CV.** Comp bands, office-first vs remote, and level mismatches belong in the referrer note or the cover letter. Apology lines inside the CV read as a weak candidate — instead surface the mismatch to Richard as a decision *before* he spends the referral.

## Master CV and per-req variants

Applying to a *class* of roles (several AI/platform PM reqs, several fintech reqs) does not mean hand-writing one CV per application. Keep **one master ****`.md`** and override exactly three fields per req:

1. the H2 title line under the name — the req's exact title, verbatim;

1. the first sentence of the summary — name the req's domain in its own words;

1. the order of the hard-skills blocks — put the req's core domain first.

Everything else (employer blocks, dates, education) stays fixed. Re-authoring the body per application is how dates and claims drift apart between versions, and a recruiter comparing two of them finds the inconsistency. Record the three override fields in the master's frontmatter so the next session does not rediscover them.

The designed version is a **rendering of the same source**, not a parallel document. When Richard builds a Figma/portfolio CV he builds it from the master `.md` after the overrides are set, so the content has one owner and the design pass cannot reintroduce a stale date or a claim the master does not carry.

**Converting a designed CV back into a working source** (asked for as "convert this into .md"): transcribe faithfully — preserve the printed order, headings and wording — and record every discrepancy against the Meta CV (dates, titles, typos) in the file's frontmatter rather than silently correcting them in the body. The body stays a true copy so Richard can see what the document actually said; the frontmatter carries the correction list that drives the next revision.

## Cover letters

Many EU portals require one alongside the CV and say so in the posting; treat that as a requirement, not an invitation. One page, rendered in letter mode. Shape, ordering and the traps: `references/cover-letters.md`.

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

- **Level calibration** — executive-positioning advice does not transfer down. For senior IC / Head-of reqs, demote "innovation and transformation" to a single line of evidence (a lab or a zero-to-one build), because an innovation theme plus coaching or teaching roles reads as a consultant or portfolio career rather than an operator; drop authority language ("decision-making authority", "influence beyond the product function") because on an IC req it screens as overqualified or as someone who will not do the work. The honest asset is *programme scope without the title* — state the scope, not the authority. Peer scope is not people management: "one of five domain PMs, each owning a domain and its engineering team" is cross-functional delivery, so never render it as "led a team of five PMs" — that fabricates exactly the line-management evidence a Group/Director-level req would probe.

- **Domain-years gap** — only after establishing the real total from the Meta CV (see first principles): if the JD's N years genuinely exceeds it, never reconcile with arithmetic. Raise outcome density per year and pull the earlier genuine domain roles into one continuous thread; a years claim is checked against the dates on the same page. State a genuine shortfall once and move on — repeating it in every draft wastes the user's attention on a gap they cannot change.

- **Constraint leakage** — comp or work-model objections, or apology lines, written into the CV instead of the cover letter or referrer note.

## Pitfalls

- A designed/template CV (dark hero, logo wall, rotated rails, CTA button) usually has **no reliable text layer** — extraction fails or returns fragments. Confirm by extracting; then rasterise and read the pages with vision. Do not report empty extraction as "no content": the parse failure *is* the finding. Rasterise with PyMuPDF via `uv run --with pymupdf python ...` (`page.get_pixmap(dpi=170).save(png)`), which does not depend on a working system poppler.

- Aggregator job links (Jooble, RocketHunt, etc.) go stale and hide the canonical req — resolve to the employer's board before analysing or applying. The same applies to your own saved snapshot: a req recorded as closed can come back under a new ID, so re-check the live board before advising or tailoring rather than trusting the last assessment.

- **When a "gap" turns out to be a recording failure in the Meta CV** — a capability thread split across role headings, a role recorded under a weaker title, a product or launch not yet logged — fix the source of truth first, then re-derive the CV. Add the fact to the Meta CV and, where the same false gap has already been raised once, a standing never-flag note in its `agent_notes`; correcting only the CV leaves the next session to rediscover the same shortfall and spend the user's attention on a gap they have already disproved.

- **Do not re-run a full pipeline assessment on an already-assessed record.** Check the record first; if it was already assessed, treat the run as a *refresh* and change only what moved — do not reset its funnel stage.

- Intake/capture rows must stay unpopulated (title / Open Date / URL only). Pre-populating them with `Identified` status corrupts the funnel signal. `notion_bulk.py create --ds "collection://<id>" --file <spec.json> --capture` writes exactly that shape; set `Where` afterwards (add the select option first, then write it through the MCP tool — the helper's `props` command no-ops silently, see `notion-bulk-operations`).

- **A role captured and then rejected is marked, not deleted.** Keep the capture date, set `Status = Abandoned` with `Jobs = 0 - Identified`, and say why in the page. Deleting it destroys the record that it was considered and rejected, which is the signal that stops the next sweep re-surfacing it as new.

- **Fresh prose fabricates; editing does not.** Writing new bullets from an evidence file is where invented numbers and invented antecedents enter, because a plausible figure is easy to produce and nothing in the source contradicts it. Every number and every "replaced X" claim must trace to a line in the source; a round quantity that sounds right ("a hundred people now quote the same way") and a plausible predecessor ("the spreadsheets and dashboards it replaced") are the two easiest fabrications to commit and the two easiest for an interviewer to open up. If the source gives no quantity, write the qualitative outcome. Re-read your own draft against the source before rendering, not just the source against the draft.

## references/

- `references/screening-stacks.md` — how Greenhouse and agentic/LLM screeners actually score, with evidence quality and sources.

- `references/cover-letters.md` — the one-page cover letter: required-not-optional, the seven-move structure, and what makes a letter read as a real person.

- `references/job-board-apis.md` — identifying a company's ATS from its careers page and pulling the live board as JSON, so req IDs and open/closed status are verified rather than remembered.

## scripts/

- `scripts/render_cv.py` — renders a CV or cover letter markdown file to single-column, parser-safe HTML → PDF + DOCX, and gates the output: it prints a banned-prose report (em-dashes, internal provenance phrases) and flags a page count over budget (two for a CV, one for a letter). Run `uv run --with markdown python scripts/render_cv.py <cv.md> "<output basename>"` and add `letter` as a third argument for a cover letter. The PDF is printed by a Chromium-class browser, because LibreOffice's HTML import ignores `text-indent` and `padding` on block elements (wrapped bullet lines collapse to the left margin) and drops `<li>` markers on some items; the DOCX is still converted by LibreOffice, but in a local temp dir and copied in, because it writes unreliably straight into a mounted network share. If no Chromium is installed it falls back to LibreOffice and says so, in which case read the rendered pages before delivering. Tune only the CSS block (font size, line-height, page margins) to land on budget; do not restructure the content to make it fit.