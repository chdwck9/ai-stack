---


name: why

uuid: 3d824dc8-ccd9-8135-b33e-c2fe8371662f

version: 2

description: "Why"

return: "decision narrative with evidence"

tools:

  - notion

  - atlassian

  - google-drive

  - slack

thinking: "Medium"

temperature: 0.3

resources:

  - "@Resource-Index"


---


# Why

Decision archaeology: answer "why is X the way it is" with evidence, not recollection. X can be a spec section, a pricing rule, a DR tier, a process, a Jira epic's scope — anything with a history.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Frame.** Restate the question as a falsifiable claim to trace ("Escrow verification is annual because …"). Ask only if X is genuinely ambiguous.

1. **Discover sources (P3).** Enumerate what THIS environment can reach — don't assume: MCD changelogs, decision logs and AZ registers in Notion; Jira issues and comments; Confluence pages; Drive doc comments and version history; Slack threads; web for external constraints (regulation, vendor changes). Skip unreachable categories with a note.

1. **Query in parallel.** One targeted pass per evidence category using X's distinctive terms. Fetch rows and threads, not whole spaces (P15).

1. **Reconstruct.** Order the evidence into a decision narrative: what was decided, when, by what reasoning, what alternatives were rejected, what has changed since. Every claim carries its source (page, ticket, thread + date). Unknowns stay unknowns — no invented rationale.

1. **Assess.** Confidence (evidenced / inferred / unknown per element) and gaps worth closing. If the answer contradicts current documentation, flag the drift and the page it lives on.

## Boundaries

- Never assert a motive without a citation — inference is labelled inferred

- Never fill evidence gaps from general knowledge of "how companies work"

- Never quote private Slack/doc content beyond the minimum needed

- Read-only: never edit the artefacts being investigated

## Output

Decision narrative in chat: claim → evidence timeline → rejected alternatives → confidence + gaps. Offer @Inbox push only if substantial.

## Examples

1. "/why is DR priced as % of ACV rather than flat fee?" → Notion pricing MCD changelog + Jira + a Slack thread → narrative: margin-management intent (evidenced), tier-simplification driver (inferred), original modelling owner unknown; flags stale % on one Confluence page.

1. "/why does Wally migration exclude region Y?" → WAZ register + Jira → evidenced constraint chain; confidence high; no drift.

## Next steps

Invoke with the thing and, optionally, where to start looking.