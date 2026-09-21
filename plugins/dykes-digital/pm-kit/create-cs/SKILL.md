---


name: create-cs

uuid: 3df24dc8-ccd9-8173-8f13-d6b25520304d

version: 3

description: "Create Case Study"

return: "A fact-grounded Career Project Evidence case study with updated evidence fields and cover-art brief"

last-used: "2026-09-19T10:23:00+02:00"

thinking: "Medium"

temperature: 0.3

resources:

  - "@AI-Hub"

  - "@career-coach"

  - "@cs-art"

  - "@unslop"


---


# Create Case Study

Interrogate and develop a Career Project Evidence case study from existing evidence. Reconstruct first, question second, write third. The goal is credible evidence, not polished storytelling at the expense of truth.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked skip: <reason> — never dropped silently.

### Voice rule

Use **we** in **Problem & impact** and **Solution & KPIs** when the evidence describes team/company work or does not explicitly establish Richard as acting solo. This also applies when Richard originated the work but delivery was collaborative. Use **I** in **Approach, role & key decisions** when describing Richard's personal contribution, decisions, ownership or leadership. Never use pronouns to inflate or diminish Richard's contribution: follow the evidence.

1. **Locate.** Identify the project in the Career Project Evidence database and load its existing properties, body, related evidence and relevant source material.

1. **Reconstruct.** Build the strongest factual version of:

  - **Why?** Problem, context and business/customer impact

  - **What?** Solution, scope and measurable outcomes

  - **How?** Approach, role, decisions, trade-offs and lessons

  Explicitly separate verified evidence, inference and unknowns.

1. **Gap-check.** Identify only the gaps that materially weaken the case study. Prioritise missing evidence around impact, scale, personal contribution, difficult decisions, constraints, outcomes and lessons. Do not ask for information already present in the evidence.

1. **Interrogate.** Ask targeted questions in small batches, adapting the next questions to the answers. Prefer specific prompts such as “What changed because of this?” or “What decision did you personally make?” over broad requests to “tell me more”. Do not turn the process into a giant questionnaire.

1. **Synthesize.** Incorporate the answers into a factual evidence model. Flag claims that remain unverified rather than smoothing them into plausible-sounding fiction.

1. **Draft.** Create a concise case study structured as:

  - Problem & impact

  - Solution & KPIs

  - Approach, role & key decisions

  - Lessons / evidence gaps where useful

  Write for a senior product/technology audience. Emphasise the problem, mechanism, decisions and evidence rather than chronology.

1. **Unslop.** Run $unslop on the drafted case study before finalising it. Remove AI tells, filler, redundant structure, repeated claims, unnecessary hedging and decorative wording while preserving the evidence, numbers, terminology, meaning and Richard's voice. Do not add content.

1. **Update evidence.** Update the project's Why?, What?, How? and Notes fields with the cleaned evidence. Preserve useful existing material unless it is redundant or superseded. Keep the database record factual rather than positioning-led.

1. **Create cover brief.** Use @cs-art to translate the project's distinctive mechanism or system into a cover-art concept. The visual should reinforce the case study rather than merely decorate it.

1. **Evaluate.** Check every important claim against available evidence, ensure Richard's personal contribution is clear, remove unsupported outcomes, and confirm that the case study explains why the work mattered. Re-run $unslop if the final prose has accumulated avoidable slop during synthesis or formatting.

## Examples

- **Existing project:** Mambu Pricing & Packaging → reconstruct the spreadsheet/manual-pricing problem, company-wide pricing system, calculator/CPQ, 1 hour to 10 minute deal estimation and later machine-readable Pricing Engine OS. Ask only for missing commercial impact, scale and concrete agentic usage before strengthening those claims.

- **Sparse project:** S3 Migration → reconstruct known migration scope and architecture first, then ask targeted questions about Richard's decisions, rollout constraints, customer impact, operational outcome and measurable cost/reliability effects.

## Boundaries

- Never invent outcomes, metrics, responsibilities, customers, decisions or technical details.

- Never convert an intended outcome into an achieved outcome.

- Never write a generic STAR story when the underlying evidence supports a richer product/technology narrative.

- Never ask questions whose answers can be recovered from existing evidence.

- Never overwrite useful evidence merely to make prose cleaner.

- Keep evidence, inference, aspiration and evidence gaps distinct.

- The case study is an evidence record, not a CV, LinkedIn profile or job-specific pitch.

- Do not claim autonomous/AI/agentic behaviour unless the evidence supports what actually happened.

- $unslop may subtract style and structure, but must not alter claims, numbers, commitments or domain terminology.

## Output

Produce:

1. Updated Career Project Evidence record.

1. A polished case study covering Problem & Impact, Solution & KPIs, and Approach, Role & Key Decisions.

1. Explicit remaining evidence gaps.

1. A @cs-art cover concept grounded in the project's actual mechanism.

1. Self-check: every material claim is evidence-backed or explicitly marked as an open gap.

Before finishing, verify every required element exists and passes. Anything missing → do the work; do not finish.

## Next steps

Start with existing evidence. Interrogate only the highest-value gaps, draft, run $unslop, then update the project record and produce the cover concept.