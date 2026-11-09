---


name: create-cs
uuid: 3df24dc8-ccd9-8173-8f13-d6b25520304d
version: 5
description: "Create Cs"
return: "A fact-grounded Career Project Evidence case study, updated evidence fields, and a square cover image matching the established visual system"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
resources:

- "@AI-Hub"

- "@career-coach"

- "@unslop"


---


# Create Case Study

Create a fact-grounded Career Project Evidence case study from existing evidence, then generate its cover image. Reconstruct first, question second, write third; illustrate last. The goal is credible evidence and one strong visual idea — not polished storytelling, and not a presentation slide.

**This is a hand-off to a frontier model.** A specific, non-routine creative operation — run it on a frontier reasoning + image-generation model. Keep the order: writing before interrogating, or illustrating before the evidence is settled, produces polished fiction.

## When to Use

- Build, strengthen or evidence-check a case study in the Career Project Evidence database.

- Turn sparse project evidence into a credible, KPI-bearing narrative.

- Produce the accompanying square cover art for a Career Project Evidence page.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

### Voice rule

Use **we** in **Problem & impact** and **Solution & KPIs** when the evidence describes team/company work or does not explicitly establish Richard as acting solo. This also applies when Richard originated the work but delivery was collaborative. Use **I** in **Approach, role & key decisions** when describing Richard's personal contribution, decisions, ownership or leadership. Never use pronouns to inflate or diminish Richard's contribution: follow the evidence.

### Phase 1 — Case study

1. **Locate.** Identify the project in the Career Project Evidence database and load its existing properties, body, related evidence and relevant source material.

1. **Reconstruct.** Build the strongest factual version of **Why?** (problem, context, business/customer impact), **What?** (solution, scope, measurable outcomes) and **How?** (approach, role, decisions, trade-offs, lessons). Explicitly separate verified evidence, inference and unknowns.

1. **Gap-check.** Identify only the gaps that materially weaken the case study. Prioritise missing evidence around impact, scale, personal contribution, difficult decisions, constraints, outcomes and lessons. Do not ask for information already present in the evidence.

1. **Interrogate.** Ask targeted questions in small batches, adapting the next questions to the answers. Prefer specific prompts such as "What changed because of this?" or "What decision did you personally make?" over broad requests to "tell me more". Do not turn the process into a giant questionnaire.

1. **Synthesize.** Incorporate the answers into a factual evidence model. Flag claims that remain unverified rather than smoothing them into plausible-sounding fiction.

1. **Draft.** Create a concise case study structured as **Problem & impact**, **Solution & KPIs**, **Approach, role & key decisions**, and **Lessons / evidence gaps** where useful. Write for a senior product/technology audience. Emphasise the problem, mechanism, decisions and evidence rather than chronology.

1. **Unslop.** Run `$unslop` on the drafted case study before finalising it. Remove AI tells, filler, redundant structure, repeated claims, unnecessary hedging and decorative wording while preserving the evidence, numbers, terminology, meaning and Richard's voice. Do not add content.

1. **Update evidence.** Update the project's Why?, What?, How? and Notes fields with the cleaned evidence. Preserve useful existing material unless it is redundant or superseded. Keep the database record factual rather than positioning-led.

1. **Evaluate.** Check every important claim against available evidence, ensure Richard's personal contribution is clear, remove unsupported outcomes, and confirm that the case study explains why the work mattered. Re-run `$unslop` if the final prose accumulated avoidable slop during synthesis or formatting.

### Phase 2 — Cover art

1. **Understand.** Identify the project's core subject, mechanism and distinctive visual metaphor. Prefer concrete product, technical, data, commercial or workflow imagery over generic business imagery.

1. **Reference.** Inspect existing Career Project Evidence cover art when available and preserve the established visual language. Do not reinvent the visual system for each project.

1. **Compose & illustrate.** 1:1 square canvas, focal point on the centre horizontal row, one central project-specific object/system plus a small number of supporting elements suggesting the problem, mechanism, relationships or outcome; must survive both Notion gallery cropping and full-page viewing. Simplify aggressively — communicate the idea, do not document every component or process step. Apply the visual contract below.

1. **Text.** A few short handwritten labels only where they aid comprehension; never titles, paragraphs, exhaustive labels, metric dumps or diagram documentation.

1. **Generate.** Use the image-generation tool and iterate against composition, simplicity and subject rather than accepting a generic first pass.

1. **Unslop.** Apply `$unslop` as a final visual cleanup pass — remove generic, decorative, repetitive or over-explained elements and unnecessary text without changing the project's meaning or visual system. A result that fails the quality gate is regenerated, not decorated around.

1. **Evaluate.** Run the quality gate; a failing result is regenerated, never shipped.

## Non-negotiable visual contract

Lock these before generating; if a result violates any hard requirement, reject it and regenerate.

- **Format:** square 1:1.

- **Background:** solid/dark `#1E1E1E` charcoal.

- **Drawing:** white hand-drawn/sketch/chalk linework only.

- **Colour:** none — no gold, yellow, green, blue or grey highlights, coloured fills, gradients or brand colours.

- **Logos:** none. **Title:** none by default.

- **Subject:** one central project-specific object, system or metaphor, focal point on the centre horizontal row.

- **Density:** restrained — an illustration, not documentation.

- **Text:** at most a few short handwritten labels, only where they clarify the visual.

- **Style:** rough, tactile, hand-drawn chalk/sketch, not polished corporate infographic art.

- **Composition:** primarily central/radial, not a left-to-right presentation narrative — communicate the mechanism at a glance.

## Generation protocol

Construct the image-generation prompt from the project evidence only. The prompt MUST begin with the visual contract:

"Square 1:1 cover illustration. Solid #1E1E1E dark charcoal background. White chalk/hand-drawn linework only. No colour. No logos. No coloured fills. No presentation-slide layout."

Then describe only: (1) the central subject; (2) the project's distinctive mechanism; (3) 2–4 supporting visual cues; (4) at most 2–4 short handwritten labels. Never add branding, decorative landscapes, coloured accents, headings, KPI lists, timelines, component lists, client panels, outcome checklists or invented components. Full protocol: `references/cover-art-system.md`.

## Examples

- **Mambu Pricing & Packaging:** reconstruct the spreadsheet/manual-pricing problem, company-wide pricing system, calculator/CPQ, 1 hour → 10 minute deal estimation, and the later machine-readable Pricing Engine OS. Ask only for missing commercial impact, scale and concrete agentic usage before strengthening those claims.

- **Sparse project — S3 Migration:** reconstruct known migration scope and architecture first, then ask targeted questions about Richard's decisions, rollout constraints, customer impact, operational outcome and measurable cost/reliability effects.

- **Cover art — Pareto:** central metaphor is **a modular stack of reusable AI capabilities being composed into different solutions**; labels and anti-list in `references/cover-art-system.md`.

## Boundaries

- Never invent outcomes, metrics, responsibilities, customers, decisions or technical details.

- Never convert an intended outcome into an achieved outcome.

- Never write a generic STAR story when the underlying evidence supports a richer product/technology narrative.

- Never ask questions whose answers can be recovered from existing evidence.

- Never overwrite useful evidence merely to make prose cleaner; keep evidence, inference, aspiration and evidence gaps distinct.

- The case study is an evidence record, not a CV, LinkedIn profile or job-specific pitch.

- Do not claim autonomous/AI/agentic behaviour unless the evidence supports what actually happened.

- `$unslop` may subtract style and structure, but must not alter claims, numbers, commitments or domain terminology.

## Output

1. Updated Career Project Evidence record.

1. A polished case study covering Problem & impact, Solution & KPIs, and Approach, role & key decisions.

1. Explicit remaining evidence gaps.

1. Self-check: every material claim is evidence-backed or explicitly marked as an open gap.

1. The final square cover image, returned only as the image itself — it should feel like one strong visual idea captured in a sketchbook, not a consulting slide compressed into a square.

Before finishing, verify every required element exists and passes. Anything missing → do the work; do not finish.

## Next steps

Start with existing evidence: interrogate the highest-value gaps, draft, run `$unslop`, update the project record, then generate the cover from the settled evidence — one square image, one strong idea.

## References

- `references/cover-art-system.md` — full generation protocol, the Pareto worked example (metaphor, labels, anti-list) and the complete quality gate (reject and regenerate on any failure).

## Taste

*Richard-originated, grown by **`$reinforce`**. Signal → preference.*

- Hub page body = the file verbatim. → Plain `---` header delimiters (`---` / `name:` / `description:` / … / `---`), never a fenced code block — a fence breaks the file the sync pulls down. Writing a page to the Hub: plain `---` delimiters only.