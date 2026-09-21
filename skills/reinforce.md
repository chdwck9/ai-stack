---


name: reinforce

uuid: 35324dc8-ccd9-819f-aac0-e63f7a8cd6bb

version: 5

description: "Reinforce"

last-used: "2026-09-19T10:23:00+02:00"

thinking: "Medium"

temperature: 0.3

resources:

  - "@AI-Hub-DB"


---


# Reinforce — Skill Improvement Engine

Scans a conversation segment, assesses every skill used, invokes /create-skill to apply improvements and surfaces updated [SKILL.md](http://skill.md/) files for local install. Produces a light segment report and a session seed block.

No approval required — /create-skill is invoked autonomously per skill.


---


## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

### Step 1 — Define the segment

1. Identify the segment boundary: **Start** = timestamp of the last `/reinforce` call in this session, or session start. **End** = now.

1. Check for prior `/reinforce` reports in this session. If found, load them — they carry cross-segment signal (see Step 4c).

1. Label the segment: `Segment 1`, `Segment 2`, etc.


---


### Step 2 — Identify skills used in the segment

Scan for explicit invocations (`/[skill-name]`) and implicit activations (persona prefixes, skill-structured outputs). For each skill found, record: name, type (persona/task), invocation count, primary goal.

If no skills are identifiable, output: *"No skill invocations detected in this segment."* and stop.


---


### Step 3 — Fetch skill definitions

For each identified skill: search @AI-Hub-DB by name, fetch the full [SKILL.md](http://skill.md/) content, note the current version number.

If a skill cannot be found: flag under "Skills Not Found" — analyse it and present a proposed [SKILL.md](http://skill.md/) block in chat, but skip the /create-skill call.


---


### Step 4 — Assess performance per skill

Rate each skill 1–5 using the signal hierarchy (in priority order):

**Rating guide:** 5/5 = first pass, no corrections | 4/5 = minor refinement (≤1 correction) | 3/5 = meaningful iteration (2 corrections) | 2/5 = partial delivery | 1/5 = failed to deliver.

**Fallback:** If fewer than 3 meaningful exchanges, rate **3/5** and flag as low signal.

If prior segment reports exist for the same skill: compute weighted average (current = 60%, prior = 40%). Flag degradation as high-priority fix. Treat stable as baseline.


---


### Step 5 — Generate improvements per skill

For each skill, identify actionable changes: step gaps, resource additions (new @handles), optimisations, additions, boundary adjustments.

For persona skills additionally assess: tone fidelity, context loading, council behaviour.

Ground every change in specific evidence from the segment. Do not add speculative improvements.


---


### Step 5b — Audit referenced resources

For each skill with changes, inspect its `resources:` block. Determine whether any skill change implies a corresponding resource update. Queue resource updates alongside skill writes. Log all resource updates in the report under a clearly labelled **Resources Updated** block.


---


### Step 6 — Apply changes via /create-skill

Before applying any skill changes, update the skill's usage metadata: set its YAML `last-used` to the current timestamp and set the AI Hub `Last Used` property to the same timestamp. Also ensure its AI Hub `Category` is assigned to the most applicable kit.

For each skill with changes:

1. Apply all changes from Step 5 to produce the updated [SKILL.md](http://skill.md/) content.

1. Increment the version number in the YAML header by 1.

1. Invoke `/create-skill` with the full updated [SKILL.md](http://skill.md/) content.

1. Log: skill name, old version → new version, number of changes applied.

Skills with no changes: do not invoke /create-skill. Log as unchanged. No approval required — proceed autonomously.


---


### Step 7 — Produce the Reinforce Report

```javascript
## /reinforce — Segment [N]: [start label] → Now

### Segment Context
[2–4 sentences: what was worked on, what was produced, key decisions. Written as a session seed block.]

---

### Skills Assessed

| Skill | Type | Rating | Signal Basis |
|-------|------|--------|--------------|
| /name | persona/task | 4/5 | [one line rationale] |

---

### Changes Applied

#### `/skill-name` v[N] → v[N+1]
- **[Category]:** [What changed]
  *Reason: [Grounded in segment evidence]*

---

### Session Seed Block

[Paste this at the start of a new session to resume context]

---

*[N] skills updated via /create-skill. [M] skills unchanged.*
```


---


### Step 8 — Present updated [SKILL.md](http://skill.md/) files

For each skill modified in Step 6, output the full updated [SKILL.md](http://skill.md/) as a fenced markdown code block in chat, labelled `### skill-name — v[old] → v[new]`. Present these after the Reinforce Report.


---


## Examples

**Example 1: Single skill segment**

> Session used `/bcaas` once to retrieve context for a pricing discussion. Output used without correction.

Expected: Detects `/bcaas` (task skill, 1 invocation), rates 4/5, invokes /create-skill (v+1), presents [SKILL.md](http://skill.md/) block.

**Example 2: Multi-skill segment with rework**

> Session used `/jenny` (3 invocations, 1 correction) and `/doc-author` (1 invocation, 2 corrections).

Expected: `/jenny` 4/5 — optimises stakeholder message step. `/doc-author` 2/5 — adds heading format rule and required-sections checklist. Both updated via /create-skill.

**Example 3: Cross-segment degradation**

> `/reinforce` called earlier rated `/jenny` at 5/5. Current segment shows 2 rework cycles.

Expected: Rates 3/5 current segment. Weighted average: 3.8 → rounds to 4/5 overall. Flags degradation and adjusts the specific step that caused rework.


---


## Boundaries

- Never invoke /create-skill without having applied Step 5 improvements first

- Never rate a skill above 3/5 if 2 or more rework cycles were observed

- Never modify skills that were not used in the segment

- Every skill invoked in the segment must have its YAML `last-used` and AI Hub `Last Used` updated to the current timestamp, even if no content changes are made

- Never present the Reinforce Report before all /create-skill invocations are confirmed

- Never produce a Session Seed Block that includes personal data, sensitive financial details, or PII

- Never apply speculative improvements — every change must be grounded in segment evidence

- If signal is too low: default to 3/5, flag as low-signal, apply conservative improvements only

- Never write the Session Seed Block anywhere — chat-only, markdown code block


---


## Output

- **Reinforce Report**: structured markdown, inline in chat

- **Session Seed Block**: fenced markdown code block, inline in chat

- **Updated **[**SKILL.md**](http://skill.md/)** files**: one fenced code block per modified skill, inline in chat (after report)

- **Skill updates**: applied via /create-skill, version incremented — no user approval required


---


## Next steps

Invoke with `/reinforce` at any point in a session. The segment is automatically scoped from the last `/reinforce` call (or session start) to now. No parameters required.