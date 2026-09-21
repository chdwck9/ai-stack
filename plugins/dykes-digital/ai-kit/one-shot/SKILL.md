---


name: one-shot

uuid: 3dd24dc8-ccd9-81ff-93fb-de35e0faef88

version: 1

description: "One-Shot"

return: "Executable context contract, optional hand-off target, and loop status"

last-used: "2026-09-16T19:12:00+02:00"

thinking: "High"

temperature: 0.3

resources:

  - "@AI-Hub"

  - "@Resource-Index"


---


# One-Shot Context Compiler

Transform a messy or underspecified request into the **minimum sufficient context contract** another agent needs for a strong first pass. Do not solve the underlying task unless explicitly asked. Optionally select a specialist and hand off through `$loop`.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Extract.** State the overarching instruction in one sentence. Identify goal(s), output(s)/decisions, audience, success criteria, constraints/deadline, and required inputs.

1. **Retrieve.** Search @AI-Hub and relevant connected sources for applicable Personas/Agents, Skills, Specs, Frameworks, Templates, Resources/source material, MCDs, Projects, and related work. Prefer current authoritative sources. Link rather than duplicate context.

1. **Resolve.** Infer low-risk gaps. Ask only questions whose answers materially change execution, preferably as one bundled question; maximum 5. Surface material assumptions.

1. **Contract.** Write the smallest self-contained brief that lets the receiving agent start without repeating discovery. Use the default structure below, trimming irrelevant sections and adding only execution-critical ones.

1. **Handoff.** If requested, select the narrowest suitable existing Persona/Agent, identify required Skills/resources, and hand off via `$loop`. Never invent a target. If no suitable agent exists, say what is missing.

1. **Check.** Verify that outputs, acceptance criteria, sources, assumptions, inputs, constraints, and boundaries are explicit; distinguish user facts, retrieved context, and inference. Remove instructions already owned by the receiving Persona/Skill.

## Contract

## [Title]

*Purpose / one-sentence instruction*

- **Goal** –

- **Outputs** –

- **Audience / User** –

- **Success criteria** –

- **Quality bar** –

- **Resources / Source material** – linked references

- **MCDs / Projects** – linked context

- **Inputs** – supplied or required

- **Constraints** –

- **Autonomy** –

- **Feedback / iteration** –

- **Checks / evidence** –

- **Boundaries** –

Only material assumptions, decisions, stakeholders, risks, dependencies, or background.

## Handoff modes

- **Contract:** return the contract for manual use.

- **Recommend:** return the contract + best Persona/Agent + required Skills/resources.

- **Execute:** build the contract, select the target, and invoke `$loop`.

- **Iterate:** incorporate downstream feedback/context and re-run `$loop`.

## Rules

- Minimum sufficient context > exhaustive context.

- Outcome > topic; specify what must be achieved, decided, produced, or changed.

- Link > duplicate; authoritative MCDs/resources remain the source of truth.

- Retrieve > invent; never fabricate sources, Personas, MCDs, links, requirements, or prior decisions.

- Assume carefully; surface material assumptions and preserve provenance.

- One-pass capable; the receiving agent should be able to begin useful work immediately.

- Specialist > generalist; select the narrowest suitable existing agent.

- Do not duplicate downstream Persona/Skill instructions.

- Do not ask more than 5 clarification questions.

- Never claim a `$loop` hand-off or execution that did not occur.

## Examples

**Contract:** `$one-shot Build a competitive analysis of X for our Q4 strategy review` → retrieve relevant strategy MCDs, company/product context and templates; produce a concise research contract with sources, decision questions and acceptance criteria.

**Execute:** `$one-shot then have the best agent execute this: audit the BCaaS ambiguity log` → build the contract, select the relevant agent/skill, and hand it to `$loop` rather than performing the audit itself.

## Boundaries

- Never block on information that can be safely inferred.

- Never turn assumptions into facts.

- Never broaden a focused request into an unnecessary project.

- Never modify source MCDs, projects, or other durable context merely while compiling a contract unless the user explicitly requests it.

- If a required specialist or source cannot be found, surface the gap rather than inventing one.

## Output

Return only the requested handoff mode: the final context contract, optionally followed by the selected Persona/Agent, required Skills/resources, and actual `$loop` status. Keep the compiler output concise; the receiving agent gets the context, not a dissertation about its construction.

## Next steps

Invoke with a goal and desired output. Add `Recommend` or `Execute` when a specialist hand-off is wanted.