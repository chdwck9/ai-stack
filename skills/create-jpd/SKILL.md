---


name: create-jpd

uuid: 3c924dc8-ccd9-81b0-beae-fae190540a73

version: 6

description: "Create Jpd"

tools:

  - atlassian

  - notion

  - web_search

thinking: "Medium"

temperature: 0.3

resources:

  - "@BCaaS-OS"

  - "@Wally-OS"

  - "@DR-Confluence-Space"

  - "@Document-Standards"


---


# Create JPD

Research and populate a Jira Product Discovery (JPD) idea from either an existing ticket or a free-text concept. Pulls facts — internal (Jira/Confluence/Notion) and external (market research) — and drafts every descriptive field. Never sets or infers priority; offers suggested priority inputs as advisory notes only.

## Scope: sets vs. never touches

**Sets (factual/descriptive only):**

- Summary; Idea short description (`customfield_22338`)

- Description — Problem/Opportunity, Proposed Solution, Value & Impact, Supporting Evidence (Appendix 2 template)

- Idea Type (`customfield_22418`): New Product Idea / Feature Enhancement / Requests for Commitment

- Impacted Customers/Prospects (`customfield_22420`)

- Idea Region (`customfield_22419`), Country for Ideas (`customfield_23673`)

- Team (`customfield_12900`), Product Type(s) (`customfield_18937`)

- Link to RSD (`customfield_22422`) and Included in the Contract (`customfield_23839`) — RFC-type ideas only

- Customer Expected Date (`customfield_26764`) — only if a contractual/regulatory deadline is found

- Link to Salesforce Opportunity (`customfield_15173`) — only if research surfaces one

**Never sets as fields (advisory notes only — see Idea Owner Notes below):**

- Reach, Revenue, Impact, Confidence (`customfield_22414/22415/22416/22417`, detailed-stage counterparts `28452/19828`)

- Effort/T-Shirt (`customfield_22424`) — always left blank for the EM

- MoSCoW (`customfield_22293`)

- Planned roadmap quarter, Reason for rejection, More info needed?

- RICE/RRICE Score — Jira auto-calculates these

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Receive input** — a JPD ticket key/link (auto-write path) or free text (draft-only path). If free text lacks a clear problem statement, ask one clarifying question before researching.

1. **Internal research** — `searchJiraIssuesUsingJql` (project = IDEA) for duplicates/related ideas; `searchConfluenceUsingCql` for existing specs/RFCs; check @BCaaS-OS/@Wally-OS for conflicts or prior coverage. Every claim gets a source link.

1. **External research** — `web_search` for market context, competitor capability, regulatory drivers — only where it supports Problem/Opportunity or Value & Impact. Paraphrase, cite by name/link, never quote.

1. **Draft the description** — Appendix 2 structure exactly. Value & Impact states facts and outcomes, never a verdict ("high-value", "critical").

1. **Populate factual fields** — Type, Region, Country, Team, Product Type(s), Impacted Customers. Leave RRICE/MoSCoW/Effort null, not zeroed or placeholder'd.

  - **Team-reassignment guard**: if the ticket already has Team set to something other than what research suggests, do NOT overwrite it. Flag the conflict (current value vs. suggested value) and wait for confirmation — Team drives Jira's auto-assignment of the idea owner, so an unconfirmed change silently reassigns the idea away from its current owner.

  - **No-clean-fit guard**: some controlled-vocabulary fields don't structurally cover every idea. Product Type(s) is a loan/deposit product picklist — it does not apply to platform, infrastructure, or commercial-tooling ideas; state "Not applicable — platform/infrastructure capability" explicitly in the field table rather than silently omitting the field. For Idea Type, if none of the three options (New Product Idea / Feature Enhancement / Request for Commitment) cleanly fits (e.g. an internal cost or margin analysis), set the closest option but flag the mismatch in the field table so the EM can override rather than defer to a silent best-guess.

1. **Draft Idea Owner Notes** (advisory only — never written to fields):

  - **Suggested Reach/Revenue/Impact/Confidence** — a proposed score per the RRICE rubric, each tied to a specific fact (e.g. "Reach: 3 — moderate, affects the 4 customers on the Tier 1 Escrow waitlist per [source]").

  - **Suggested Effort (T-shirt)** — directional only, explicitly labeled "non-binding, EM to confirm."

  - **Suggested MoSCoW category** — with the specific criterion it's closest to.

  - **Why this skill isn't setting these itself** — one line: RRICE/Effort/MoSCoW require judgment on cross-functional priorities and capacity trade-offs that sit with the vertical lead/EM, not with a research pass.

  - **What would have to be true for Must Have / Accelerated now** — a short gap list of the specific facts (contractual deadline, revenue threshold, customer count, regulatory date) that are currently missing or unconfirmed, which — if confirmed — would push this idea up. Framed as "not yet confirmed: X, Y, Z," never as a verdict.

1. **Output**:

  - **Ticket key supplied** → write factual fields directly via `editJiraIssue` (auto-approved for this skill), then post the Idea Owner Notes as a Jira comment (`addCommentToJiraIssue`) clearly labeled "Suggested — not set as fields, confirm before applying." Report what was written, what's pending on Team (if flagged), and what's left for EM/vertical lead.

  - **Write-failure fallback**: if `editJiraIssue` or `addCommentToJiraIssue` fails (permission error, app-not-installed, or similar) on the first ticket of a batch, don't retry per-ticket — treat it as systemic, flag it once clearly (what failed, the exact error), and fall back to presenting the full drafted content (description + field table + Idea Owner Notes) per ticket in copy-paste-ready format for manual entry. Continue the research and drafting work for every remaining ticket in the batch regardless of the write failure — the failure blocks the write step only, not the research/draft value.

  - **Free text supplied** → present the full draft (fields + Idea Owner Notes) in chat; create the idea and post the comment only after Richard confirms.

## Examples

- *"Fill in IDEA-1256, it's about supporting AWS China as a DR region"* → fetches the ticket, researches AWS China DR precedent (internal + regulatory), writes Description/Type/Region/Team/Product Types directly, posts Idea Owner Notes as a comment with suggested RRICE/Effort/MoSCoW and a "what's missing for Must Have" gap list, reports what's still pending for EM.

- *"Rough idea: customers want self-serve escrow reconciliation reports"* (no ticket) → researches, drafts full field set + Idea Owner Notes, presents for confirmation before creating.

- *"Fill in IDEA-980 and set it Should Have"* → populates factual fields, declines to set MoSCoW as a field, but includes the requested category in the Idea Owner Notes as a suggestion, and points to Front-Door Review as the actual decision venue.

- *"Fill in IDEA-732, Team should be Escrow"* but the ticket's Team is currently set to "Wally" with a different assignee → flags the conflict, shows current vs. suggested Team, waits for confirmation before changing.

## Boundaries

- Never set Reach/Revenue/Impact/Confidence/Effort/MoSCoW/roadmap quarter/rejection reason as fields, even if explicitly asked — offer them only as labeled, non-binding suggestions in the Idea Owner Notes comment.

- Never invent customer names, ARR, or adoption figures — state "not found" rather than estimate.

- Never quote external sources — paraphrase with citation, one source-attribution per claim.

- Never create a new idea without explicit confirmation of the drafted content.

- Never auto-link candidate duplicates — surface them, let Richard confirm the link.

- Never silently overwrite a populated field on a supplied ticket without flagging the conflict first — this applies especially to Team, which drives auto-assignment.

- Never frame the "what would have to be true for Must Have" gap list as a recommendation to accelerate — it's a factual gap list, not a verdict.

## Output

- Format: mixed. Sources checked (internal/external, linked) → drafted Description in full → field table (field → drafted value → source/confidence) → Idea Owner Notes block (suggested RRICE/Effort/MoSCoW + rationale + Must Have gap list) → explicit line: "Left as fields for vertical lead/EM: Reach, Revenue, Impact, Confidence, Effort, MoSCoW."

## Resources

- @BCaaS-OS, @Wally-OS — coverage/conflict check for BCaaS/Wally ideas

- @DR-Confluence-Space — DR-specific internal docs

- @Document-Standards — description tone/structure

## Next steps

Invoke with a JPD ticket key/link or free text. Thin free text triggers one clarifying question before research starts.

## Taste

*Richard-originated, grown by **`$reinforce`**. Signal → preference.*

- Hub page body = the file verbatim. → Plain `---` header delimiters (`---` / `name:` / `description:` / … / `---`), never a fenced code block — a fence breaks the file the sync pulls down.

- Never wrap the header in a fenced code block when writing a page to the Hub — plain `---` delimiters only; a fence breaks the synced `.md`.