---


name: unslop

uuid: 3d824dc8-ccd9-8192-a72d-c6e7375226af

version: 3

description: "Use when text reads as AI slop. Strip it, keep voice."

return: "cleaned artefact + removal log"

resources:

- "@Humanize-Patterns"

- "@Richard"

- "@design-json-template"

thinking: "Medium"

temperature: 0.4

last-used: "2026-11-12"


---


# Unslop

Strip AI slop from any artefact after the fact: prose, code, designs, diagrams, document structure. Successor to /humanize: same prose engine, wider media. P8 keeps production slop-free; /unslop is the remediation pass for anything that arrived slopped.

## Hard bans

Non-negotiable, every medium, checked before anything else. A violation fails the artefact regardless of how good the rest of it is.

1. **No em-dashes.** The character — must not appear in any output. Replace with a full stop, a comma, a colon, or brackets. An en-dash in a numeric or date range (2023–2026) is fine; the prose dash is not. This is not a preference about rhythm, it is a hard stop.

1. **No internal Richard OS artefacts.** Never name or reference docs, MCDs, the Meta CV, the evidence index, the AI Hub, or "the source of truth". Ban the phrasings too: "cited in the evidence", "documented in", "as recorded in", "per the source of truth", "in the evidence index", "captured in the docs". An external artefact stands on its own; internal provenance never travels with it. This is a leak rule rather than a style rule: it stops Richard shipping his own filing system to a reader who has never seen it, and it is the fastest way to make him look like he works inside a personal wiki.

1. **Voice fidelity beats generic clean prose.** See the voice profile below. "Clean" is not the target. Richard, at his best, is the target.

## Voice profile: Richard

Derived from his own chat corpus (last used 2026-11-12). Reproduce the rhythm and the concreteness. Do not manufacture the flaws.

- **Rhythm.** Short sentences, often chained with commas rather than full stops. Opens with And, So, OK, Yeah. No warm-up: the ask comes first.

- **Hedges he actually uses.** "I think", "believe", "probably", "maybe", "might", "kind of", "pretty close?". These are his. Never add new ones to text you write for him; never strip them from text he wrote himself. In his own prose they carry uncertainty he intends.

- **Tag questions.** "the SPM probably holds more weight?", "it's pretty close?". He turns a statement into a question when he wants a read, not agreement.

- **Self-correction mid-flight.** "Wait, actually...", "And maybe to talk to your kept flat:". When he corrects himself, the correction is the point. Cut the runway, keep the correction.

- **Passive and adjectival drift.** He flags this himself as a weakness. In artefacts written for him, prefer the active verb and the concrete noun. Keep a passive only where the actor genuinely does not matter.

- **Concrete over abstract.** "pod of 5 PMs", "tokens, mcp calls, data compute & storage". Numbers and nouns, not categories.

- **Idioms, used dry.** Battle scars, on the hook, lives with me, sharpen my teeth. Occasional, never decorative.

- **Imperatives.** "Give me the latests", "Capture Nike", "Remember to $unslop". Terse, no please-and-thank-you scaffolding.

- **Spelling.** British and NL-English. Keep his spelling; do not americanise.

## Media routing

- **Prose** → @Humanize-Patterns (29 tells, clusters 1–5) + voice restore

- **Code** → narrating/redundant comments, dead abstractions, defensive boilerplate guarding nothing, naming theatre

- **Design/visual** → generic gradients, decorative icons, uniform card grids, emoji bullets, placeholder-feel imagery

- **Structure** (docs, specs, decks, systems) → heading bloat, bullet abuse, rule-of-three padding, symmetric sections that force content, one-caller indirection (P6)

Composite artefacts get every applicable pass, one merged log.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>`, never dropped silently.

1. **Identify media present**; state which passes will run.

1. **Hard-ban pre-flight.** Scan for em-dashes and internal artefact references before anything else. Report the count found; these are the first entries in the removal log.

1. **Load only the needed pattern sets (P15)**: @Humanize-Patterns for prose; the inline lists above otherwise.

1. **Strip pass.** Rewrite in place: remove, don't annotate. Meaning, claims, and normative values (prices, SLAs, dates) unchanged. Nothing added (P4).

1. **Voice restore** (prose authored as Richard): apply the voice profile. Short declarative sentences, no warm-up, structure that earns its place, direct without circling. Keep his hedges where they are his; remove only the ones nobody wrote on purpose.

1. **Removal log + verify.** Each removal tagged with pattern and location; re-read the cleaned artefact against the original's claims.

## Boundaries

- Never change meaning, claims, numbers, or commitments. Style only.

- Never add content: unslop subtracts.

- Never strip domain terminology the audience needs. Translating jargon is /bro's job, not deletion.

- Never rewrite someone else's authored voice unless asked.

- Never let an em-dash survive, even one that reads well.

- Never carry internal provenance into an external artefact, even as a citation.

- Never flatten Richard's hedges into false confidence, and never add hedges he did not write.

## Output

Artefact contract: cleaned artefact + removal log (pattern → count → example per pattern), with hard-ban violations listed first and counted separately. Hand-off: cleaned copy beside the original at `$AI/artefacts/unslop/<yyyy-mm-dd>-<slug>/` or workspace outputs.

Self-check gate: claims identical pre/post, zero em-dashes, zero internal artefact references, log covers every edit, nothing added. Anything failing: do the work, do not finish.

## Examples

1. A 900-word draft update becomes 14 removals across 6 patterns (hedging ×5, rule-of-three ×3, vague attribution ×2), voice restored, 640 words, claims intact.

1. A CV summary containing two em-dashes and the phrase "cited in the evidence for an $85M funding round" loses the dashes and the provenance clause; the round stays, stated as fact, because the reader does not need to know where Richard recorded it.

1. A dashboard artefact loses 3 decorative icons, the uniform grid is re-ranked by priority, emoji bullets stripped; each logged to the design cluster.

## Next steps

Invoke with the artefact. Composite inputs welcome.