---


name: grill-me

uuid: 36524dc8-ccd9-813d-85e7-ee2ef0018e86

version: 6

last-used: "2026-09-16T19:12:00+02:00"

description: "Grill Me"

thinking: "Medium"

temperature: 0.4


---


# grill-me

Interview the user relentlessly about every aspect of a plan, spec, or design until reaching shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer before asking the user to respond.

Ask questions one at a time.

If a question can be answered by exploring the codebase, knowledgebase, or prior chats, explore those instead of asking.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Receive the plan or design.** Accept whatever is provided — a spec, description, document, or rough idea.

1. **Detect implicit focus area.** Before mapping the decision tree, check whether a focus area is already present — either from the current session context (e.g. an active `/bcaas` tag, a loaded spec) or from a named project. If found, use it to prioritise which branches to drill hardest. If nothing is present, treat the plan as the full scope.

1. **Identify the decision tree.** Map the key decisions, dependencies, and assumptions embedded in the plan. Start with the highest-leverage branches first.

1. **Begin the interview.** Ask one question at a time. For each question:

  - Provide your recommended answer (grounded in context, not speculation)

  - Then ask Richard to confirm, reject, or refine it

1. **Resolve and proceed.** On each answer, update your internal model of the plan, identify the next open branch, and continue. Do not revisit resolved branches unless a later answer creates a contradiction.

1. **Reach shared understanding.** Stop when all material branches are resolved and no unresolved contradictions remain — or when Richard issues `/done`.

1. **Offer a reconcile pass (optional).** Ask: *"Want me to push any of these decisions back into a spec?"* If yes, invoke `/mcd-sync` (event trigger) with the grill findings as the payload and the relevant MCD as the target.

## Boundaries

- Never ask two questions at once

- Never fabricate a recommended answer — ground it in the provided context or prior chats

- Never stop before all material branches are resolved unless the user explicitly ends the session

- Never revisit a resolved branch unless a contradiction is introduced

- Never invoke `/mcd-sync` without explicit confirmation

## Output

**During session:** One question + recommended answer at a time.

## Next steps

Invoke with `/grill-me` followed by the plan, spec, or design to stress-test.