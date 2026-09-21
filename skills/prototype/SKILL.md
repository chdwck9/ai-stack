---


name: prototype

uuid: 38a24dc8ccd98172849ecf135ce6eafd

version: 8

description: "Prototype"

return: "Working prototypes with write-ups, service design blueprints, user test plans, and engineering bootstrap plans"

thinking: "High"

temperature: 0.4

tools:

  - notion

resources:

  - "@AI-Hub"


---


# Prototype

Design sprint-aligned prototyping skill. Takes a central brief with global success criteria, a set of prototype specs each with an exam question (HMW), user/customer context, and output medium. Produces working, pre-populated prototypes — rendered as JSX React artifacts where the medium is app/dashboard/UI — plus mandatory write-ups including a service design blueprint and engineering bootstrap plan for each.


---


## Invocation

```plain text
/prototype

brief: |
  [The central problem, opportunity, or goal you're designing around]

success_criteria: |
  [Global success criteria — how you'll know the overall sprint worked]

prototypes:
  - id: P1
    title: [short name]
    hmw: [How Might We question — the exam question this prototype answers]
    description: |
      [What the prototype is, what it does, and any key constraints]
    users: |
      [Who the primary users are and what matters to them]
    customers: |
      [Who the customers are (if different from users) and what matters to them]
    medium: [app | dashboard | jsx | doc | spreadsheet | docker-compose | figma | other]

  - id: P2
    ...

research: |
  [Optional: problem statement, HMW questions, selected/discarded ideas, user quotes, constraints]
```

Inline or conversational invocation is fine — the skill will extract the fields.

If invoked with no arguments (`/prototype` only), display the input template above as a code block and wait.


---


## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

### 0. Input template (no-args invocation)

Display the invocation template above as a code block. Do not proceed until the user returns a filled template or equivalent inline brief.

### 1. Parse and clarify

Extract `brief`, `success_criteria`, `prototypes[]`, and `research`. If `brief` or `success_criteria` is missing, ask once. If any prototype is missing `hmw` or `medium`, ask once — batch all gaps into a single question.

Do not proceed until brief + success_criteria + at least one complete prototype entry exists.

### 2. Research and augment

For each prototype, assess against the HMW question, medium, users, and customers declared. Produce:

**2a — Per-prototype confidence rating:** Strong / Moderate / Weak — one-line rationale each.

**2b — Suggested tweaks:** For Moderate or Weak, propose a specific improvement — sharper HMW, better medium, tighter scope.

**2c — Suggested drops:** Flag any prototype that is redundant, untestable in the declared medium, or unlikely to generate useful signal.

**2d — Suggested additions:** Based on research and design sprint methodology, propose 1–3 new prototype ideas not in the original list. Ground each in a specific research finding or user/customer need.

**2e — Discarded ideas check:** If `research` includes discarded ideas, flag any worth reconsidering.

Present the full assessment and **wait for a reply** before proceeding. This is the only input gate in the skill.

- `continue` → build original list unchanged

- `accept` → apply all suggestions, confirm revised list, then build

- Selective response → apply named changes only, confirm revised list, then build

### 3. Plan build sequence

Determine build order: simplest or most independent first, unless brief implies otherwise. State the order in one line. Proceed immediately.

### 4. Build prototypes

For each prototype in the confirmed list, invoke `/dt-loop` explicitly. `/dt-loop` is the execution engine — do not emulate it inline or fall back to `/loop`.

**Invocation pattern per prototype:**

```plain text
/loop prototype build [P-id] [full spec including brief, hmw, users, customers, success_criteria, medium]
```

**If /loop is not callable, emulate the full three-phase contract:**

Build a barebones, functional artifact. No styling required. All interactions must work. The HMW must be answerable from this artifact.

**Medium is a hard constraint.** `medium: app` or `medium: jsx` → JSX React component. Never substitute HTML for JSX. Never produce HTML and call it JSX.

**JSX requirements:** Default export, React hooks for state, Tailwind for layout (CDN class names), recharts/d3 if charts needed, pre-populated domain-appropriate demo data, no empty states, no lorem ipsum.

Tests: renders without error; all handlers wired to state; primary HMW answerable; core flow navigable without explanation.

User critique (adopt user persona): what works, what's confusing, what would stop them using it.

Self-critique: single biggest improvement for Phase 2.

Retain all Phase 1 functionality. Add styling, polish, completeness. It must look and feel like a finished product to a user unfamiliar with the build.

Tests: looks like a real product; user persona can complete success criteria without handholding; delivers on promises in the brief; simple and intuitive.

User critique: what delights, what would cause abandonment.

Customer critique (if different from user): value statement, objection.

Self-critique: single biggest viability risk and how Phase 3 will address it.

Fully operating prototype or MVP. Capitalise on Phases 1 and 2. Simplify the backend. Answer: how long and expensive would a production version be?

Tests: no dead states or broken flows; underlying logic explainable in one paragraph; engineer unfamiliar with this could upskill quickly; ROI case defensible.

Walk the global `success_criteria` step by step. Declare each step pass or fail. Only declare Phase 3 complete when all pass.

**Between phases:** write a compressed handoff block:

```javascript
[Phase N — Skeleton | Delighter | Money-Maker]
Artifact: [what was built]
HMW answered: [yes / partially / no]
User critique summary: [one line]
Self-critique carry-forward: [one improvement]
Open: [anything unresolved]
```

After all prototypes are built, **proceed immediately to Step 5 without waiting for user input**.

### 5. Write-up per prototype

Mandatory and unconditional — never skip. Produce for each prototype:

**Section 1 — Prototype brief**

ID, title, HMW/exam question, medium, users, customers, key design decisions made across three phases.

**Section 2 — User testing plan**

- Testing method (moderated, unmoderated, A/B, guerrilla)

- Participant profile — separate user and customer profiles if declared

- 3–5 tasks or scenarios grounded in the HMW

- What to observe: success signals and failure signals

- Suggested tools (Maze, Lookback, Hotjar, in-person script)

**Section 3 — Service design blueprint**

A full service design blueprint as a Mermaid diagram covering:

- User/customer actions (front stage)

- Visible system responses (line of visibility)

- Backstage processes (data, logic, integrations)

- Support systems and tools

- Key evidence/touchpoints

Format:

```mermaid
flowchart TD
  ...
```

**Section 4 — Engineering bootstrap plan**

How to refine this prototype and hand it to an engineering team:

- Phase A (validate): minimum changes to test at scale — what to measure, what to watch

- Phase B (build): key engineering work, tech stack recommendations, data model sketch

- Phase C (scale): infrastructure, integrations, GTM considerations

- Handover checklist: what an engineer needs to pick this up cold

- Effort tier: S / M / L / XL with rationale

Deliver all write-ups as a single combined markdown file via `present_files`.

**Immediately after ****`present_files`**** returns**, auto-publish to Notion — do not wait for user input, do not treat file delivery as a session endpoint. Write to @AI-Hub without asking. Use the AI Hub DB as parent (`data_source_id: 28424dc8-ccd9-801c-8439-000ba9845548`). One page per prototype. Properties: `Name` = prototype title, `Description` = HMW, `Type` = Skills, `Visibility` = private.

### 6. Summary

```plain text
**prototype — session complete**

Brief: [restate]
Success criteria: [restate global criteria]
Prototypes built: [list with IDs, titles, HMWs, render modes, phase results]
Suggested but not built: [additions from Step 2 that weren't accepted]
Open items: [blockers, degraded outputs, missing data]
Next: [recommend which prototype to user-test first and why, grounded in HMW clarity]
```


---


## Agent mode

Sub-agents are spawned per prototype at Step 4 via `/dt-loop prototype build [P-id]`. Each prototype is an independent build unit.

### Permissions

### Halt conditions (per prototype)

- Three full phases without meeting success criteria → surface blocker, skip to next prototype

- Medium unsupported or tool unavailable → flag and propose nearest equivalent

- Domain too ambiguous to generate example data → ask once for sample data

### Mobile contract

Suppress plan confirmation and mid-run questions. Surface a single gate per blocked prototype only.


---


## Examples

**Example 1 — Full design sprint**

```javascript
/prototype

brief: |
  Mambu pricing is too complex for AEs to configure and for customers to understand

success_criteria: |
  An AE can configure a complete 3yr deal in under 5 minutes without reading a manual.
  A customer can read the output and explain what they're buying.

prototypes:
  - id: P1
    title: Dumb it Down
    hmw: How might we remove platform selection entirely and still produce an accurate deal?
    description: Simplified configurator with auto-platform, single discount lever, product toggles
    users: |
      AEs and deal desk — need speed and accuracy, frustrated by complexity
    customers: |
      Bank procurement teams — need to understand what they're buying at a glance
    medium: jsx

  - id: P2
    title: Customer View
    hmw: How might we produce a customer-facing summary that requires no internal knowledge to read?
    description: Read-only deal summary, plain English, no internal costs or margins visible
    users: |
      AEs generating the document — need it to look professional and be shareable
    customers: |
      CFO and commercial leads at prospect banks — need to forward it internally with confidence
    medium: jsx
```

**Example 2 — No-args invocation**

```plain text
/prototype
```

Expected: displays the input template as a code block and waits.


---


## Boundaries

- Never build before Step 1 parsing is complete

- Never proceed past Step 2 without user input — the assessment gate is the only input gate

- Never produce empty states — every prototype ships with domain-appropriate example data

- Never render infrastructure files as inline artifacts — always as files

- Never declare a phase complete without running all listed tests for that phase

- Never self-declare interactivity check passed without auditing every handler

- Never declare flow check passed without walking success criteria step by step

- Never skip the user and self-critique steps in any phase

- Never use lorem ipsum or placeholder text anywhere

- **Never substitute HTML for a declared JSX medium — this is a hard constraint and a known failure mode**

- Never execute `/dt-loop` logic inline — always invoke `/dt-loop` explicitly; `/loop` is not a valid fallback for prototype builds

- Never wait for user input between Step 4 and Step 5 — write-ups are produced automatically

- Never skip Step 5 write-ups — they are unconditional deliverables

- Never skip the service design blueprint or engineering bootstrap plan in write-ups

- Always auto-publish write-ups to Notion at Step 5 — no confirmation needed


---


## Output

- **Artifacts (inline JSX):** React components, default export, Tailwind, pre-populated demo data

- **Files:** Combined markdown write-up via `present_files`

- **Notion pages:** One per prototype, auto-published to AI Hub DB

- **Summary:** Single completion block at end of session