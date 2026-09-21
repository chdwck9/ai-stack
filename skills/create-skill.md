---


name: create-skill

uuid: 31624dc8-ccd9-8032-8bdf-e3ee0f700ee2

version: 12

description: "Create Skill"

last-used: "2026-09-16T19:12:00+02:00"

thinking: "Medium"

temperature: 0.4

resources:

  - "@Skill-Template"

  - "@Resource-Index"


---


# Skill Creator

Translate a capability request into a production-ready [SKILL.md](http://skill.md/): precise steps, examples, boundaries, and an output contract. Complete, executable specifications only.

## Skill architecture

- [SKILL.md](http://skill.md/) is a router, not a manual: triggers, steps, boundaries, contract. Target 500–900 words.

- **Progressive disclosure:** content needed only at a specific step — templates, pattern lists, long examples, variant workflows — moves to sidecar files (`resources/`, `playbooks/`, `examples/` in the skill folder, or an @handle in @AI-Hub). The body carries a one-line pointer stating when to load each. A skill with 2+ variants of one workflow gets one playbook file per variant; [SKILL.md](http://skill.md/) matches the task and routes.

- All external references by @handle only, resolved via @Resource-Index. Never hardcode URLs, UUIDs, or paths. Lazy-load always.

- Subagent steps (Claude Code/Cowork): agent instructions live as sidecars with spawn conditions noted in the body; skipped on [claude.ai](http://claude.ai/).

## Build standards

Written into every skill drafted:

- **Anti-drift.** The Steps section opens with: "Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently."

- **Artefact contract** (skills whose output is an artefact — document, design, dashboard, dataset; e.g. loop, dt-loop, tokenise-brand). The Output section names the required elements (sections, fields, files) and ends with a self-check gate: "Before finishing, verify every required element exists and passes. Anything missing → do the work; do not finish."

- **Pipeline hand-off** (artefact skills). Declare emissions in `return:`. Write artefacts to the hand-off location — Claude Code/local: `$AI/artefacts/<skill>/<yyyy-mm-dd>-<slug>/`; [claude.ai](http://claude.ai/): workspace outputs, plus @Inbox on push. Downstream skills check there before regenerating.

## Steps

1. **Clarify.** Review concept and purpose. If vague, ask: concrete use case, who invokes and when, success criteria, autonomy level. Confirm before proceeding.

1. **Research prior art.** 2–4 keyword searches across public skill ecosystems ([skills.sh](http://skills.sh/), [agenticskills.io](http://agenticskills.io/), anthropics/skills, awesome-claude-skills lists) and @AI-Hub for existing coverage. Present max 3 matches — name, source, one line, what's worth borrowing — as optional inspiration, never a gate. Fold anything useful straight into Step 4.

1. **Load @Skill-Template** (lazy — now, not at activation).

1. **Draft.** Follow the template exactly, applying Skill architecture and Build standards above. YAML header — single atomic block, `---` delimiters, never a fenced code block: name, `uuid: TBD`, version, description (title-cased skill name only, no sentence), `return:`, `last-used:` (current timestamp when invoked/updated), tuning fields, resources (handle list only; omit if none). Do not include a `tools` property; resources and the execution environment define required capabilities. Assign the skill the most applicable AI Hub `Category` from the available kit options. Tuning defaults: `thinking: Medium` (High for heavy multi-step reasoning, Low for lookups) · `temperature: 0.7` (0.2–0.4 deterministic/technical, higher creative). No model-selection fields — model routing and loop escalation live in the environment's [CLAUDE.md/AGENTS.md](http://claude.md/AGENTS.md), never in the skill. Ask about overrides only if the user raises tuning. No `visibility` in YAML — Notion property only.

1. **Feedback.** Present the draft; incorporate without deviating from template structure.

1. **Test.** 2–3 prompts: typical, edge, boundary/refusal. Execute each against the draft, present prompt → output, review, iterate on affected cases. For artefact skills, run the self-check gate as part of the test. Confirm description is name-only. Optional blind A/B when iterations occurred and the user wants it.

1. **Publish.** Create the page in @AI-Hub (Type of P = Skills, Version = 1, Description = name only, full [SKILL.md](http://skill.md/) in the page body — never as attachment). Patch the returned UUID into the header (Notion + local). Write the final [SKILL.md](http://skill.md/) to workspace outputs and present for install; if the skill has sidecars, deliver the folder as a zip.

1. **Visibility.** Suggest private (personal OS/data) / mambu (work) / public (generic); confirm; update the Notion property.

## Examples

**"Create a skill that reviews docs against three different checklists"**

2+ variants of one workflow → [SKILL.md](http://skill.md/) router (~400 words) matching doc type, plus `playbooks/<type>.md` per checklist loaded on match. Anti-drift line in Steps; artefact contract naming the review report's required sections; hand-off to `$AI/artefacts/review/…`. Visibility: mambu.

**"Create a skill that turns a rough idea into a structured brainstorm"**

Step 2 finds a popular public analogue; its Socratic example structure is borrowed and translated into this template — never copied verbatim, never presented as install-ready. Single workflow, conversational output → no playbooks, no contract, no hand-off. Visibility: public.

## Boundaries

- Never write to Notion before test outputs are reviewed (a combined "push/proceed" counts as approval)

- Never exceed ~900 words in a [SKILL.md](http://skill.md/) body without moving content to sidecars or @handles

- Never deviate from @Skill-Template structure, omit Steps/Examples/Boundaries, or include fewer than 2 examples

- Never skip Step 2 research, require its findings to be adopted, or copy a found skill verbatim

- Never hardcode URLs, UUIDs, or paths — @handles only; never key-value pairs in resources; never eager-load without explicit instruction

- Never omit the anti-drift line, artefact contract, or hand-off from a skill that qualifies for them

- Never include model-selection fields (`model`, `model-mode`, `fallback-mode`, `loop-escalation-mode`) — model routing and escalation are environment concerns; never omit `thinking` or `temperature`

- Never attach the [SKILL.md](http://skill.md/) as a file to the Notion page — full content in the page body

## Output

Complete [SKILL.md](http://skill.md/) (plus sidecar files when split), matching @Skill-Template: real uuid, name-only description, @handle references throughout, contracts embedded. Delivered as Notion page in @AI-Hub + files in workspace outputs.

## Next steps

Invoke with a skill concept and purpose; vague concepts get clarifying questions first.