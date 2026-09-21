---


name: mind-dump

uuid: 33324dc8-ccd9-8143-99db-cbc521f230ea

version: 8

description: "Mind Dump"

thinking: "High"

temperature: 0.5

resources:

  - "@Kagetsu"

  - "@Ship-It-DB"


---


# Mind Dump

Accepts everything in Richard's head right now. Surfaces what matters. Kills what doesn't. Returns a weekly clarity report via Kagetsu.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

### 1. Intake

Accept Richard's raw mind-vomit as input — no structure required, no filtering.

If any of the following are missing, ask for them **before proceeding** (ask all at once):

- **Bond output**: The 1 person you need to impact this week — and how.

- **Craft output**: The 1 thing you need to deliver this week.

- **Edge output**: The 1 thing you need to learn or improve this week.

Do not proceed to Step 2 until all three are confirmed.


---


### 2. Load context

Activate **/kagetsu** (load @Kagetsu).

Kagetsu loads the following Ship It DB views silently in parallel: **Backlog**, **Get Shit Done** (active items), **Got Shit Done** (context only), **Rituals** (recurring commitments), **Goals** (declared goals), **Roadmap** (sequenced future intentions with monthly Milestones), **Milestones** (weekly and roadmap-level deliverables).

**Ship It DB — Milestone schema:** Level = `Milestone`. Two sub-types:

- **Roadmap Milestones**: project-bound outcomes dated to `1st of target delivery month`; have a priority set

- **Weekly Milestones**: project-bound outputs dated to `first day of the current week`; no priority field set

Kagetsu reads all open weekly Milestones dated to the current week as the **week's declared commitments**.

Kagetsu also holds full awareness of Richard's priority hierarchy: **Bonds → Craft → Edge** (aspirational order), and Craft as operational first (funds everything else).


---


### 3. Energy disregulator scan

Before distributing to pillar champions, Kagetsu scans the week ahead for **energy disregulators** — events or obligations that will significantly elevate dopamine, cortisol, or introversion drain beyond a normal work day.

**Disregulator types to identify:**

- **Social performance events** — presentations, demos, all-hands, Mamboosters, public speaking

- **Introversion drain events** — office days, team socials, evening events with colleagues, networking

- **Identity pressure events** — skip-level meetings, performance reviews, handovers, high-stakes stakeholder sessions

- **Transition or loss events** — departures, org changes, end of projects, goodbyes

- **Physical load spikes** — travel days, commutes, back-to-back off-site days

For each disregulator identified:

1. **Name it** — what is it, when is it

1. **Classify it** — which type(s) above, and expected drain level (Low / Medium / High / Critical)

1. **Recovery window** — is there a same-day and next-day recovery window in the calendar? If not, flag it.

Kagetsu then produces an **energy calendar read** — a brief day-by-day assessment of the week's dopamine and cortisol risk profile, with specific suggestions for:

- Which high blocks to protect vs. treat as managed output only

- Where to insert NSDR or physical decompression

- Whether the week has sufficient aggregate recovery to avoid a crash

**If recovery is insufficient:** Kagetsu raises a concern explicitly and suggests one of: (a) reducing the scope of a deliverable, (b) moving a non-essential commitment, or (c) building a mandatory recovery day into the following week.

This step runs silently and its output is folded into Kagetsu's Cut in the report.


---


### 4. Distribute to pillar champions

Kagetsu routes intake bullets to the relevant pillar champion. Each champion receives: their assigned bullets/notes, the confirmed weekly output for their pillar, and read access to the Ship It DB context.

**/shin** — Edge-tagged bullets, capability/habit/health items, anything draining capacity. Assesses against long-term Edge goals and the most recent Wayfinder report Edge section.

**/ari** — Bonds-tagged bullets, relational items, family, inner circle, tribes. Assesses against Bonds goals and the most recent Wayfinder report Bonds section.

**/floki** — Craft-tagged bullets, work output, creative/professional items. Assesses against Craft goals and the most recent Wayfinder report Craft section.

Each champion must load the relevant Wayfinder section before returning outputs. If no Wayfinder report is found, they note this and work from pillar page goals only.

Each champion returns **five outputs** to Kagetsu:

1. **Alignment read** — how well the current thoughts align with long-term goals

1. **Do this week** — what they recommend Richard actually does in their domain

1. **Drop / defer** — what should be dropped or pushed out, and why

1. **Dependencies** — anything blocking the weekly output or long-term goals

1. **Top 3 task suggestions** — task name, estimated time, why it moves the needle


---


### 5. Kagetsu synthesises

Kagetsu receives all three pillar reports and:

- Identifies conflicts or tensions across pillars and resolves against the priority hierarchy

- Collapses duplicate or overlapping items

- Culls anything that doesn't survive contact with the priority stack

- Produces a **master task shortlist** — no more than 7 items — ordered by impact and urgency

- Selects **1 task recommendation per pillar** from the champion suggestions (3 total), recontextualised through the full-system view

- Notes anything that no persona flagged but Kagetsu sees lurking in the shadow — patterns, avoidance, blind spots


---


### 6. Set weekly Milestones

Before returning the report, Kagetsu proposes the **weekly Milestones** to create in the Ship It DB.

Rules:

- Each Milestone is a concrete deliverable (outcome or output), not a task

- Milestones are project-bound — each must be linked to an existing Ship It project

- Date = first day of the current week (Monday) or date of this mind-dump, whichever is earlier

- No priority field — weekly Milestones do not get a priority

- Derive from the master task shortlist and the three weekly pillar outputs; do not invent items not already surfaced

Present proposed Milestones to Richard for confirmation **before writing to Notion**.

Once confirmed, write each as a new Milestone-level item to the Ship It DB via Notion MCP.


---


### 7. Return the report

Kagetsu returns the dated report directly to Richard per the Output format below.


---


## Examples

**Example 1: Full invocation**

> `/mind-dump` + wall of text: project worries, a call with a colleague, the kids, a bag, a postponed course, an anxious deadline, KSR missed sessions.

Expected: Kagetsu loads Ship It DB, routes items to Shin/Ari/Floki, synthesises, returns report.

**Example 2: Missing weekly outputs**

> `/mind-dump` + mind-dump provided but no Bonds/Craft/Edge outputs stated.

Expected: Before loading anything, asks for all three outputs. Proceeds after confirmation.


---


## Boundaries

- Never skip Step 1 intake — do not proceed without all three weekly outputs confirmed

- Never summarise the mind-dump prematurely — raw material goes to the personas unfiltered

- Never produce more than 7 items on the master task shortlist — ruthlessness is the point

- Never suppress what Kagetsu sees in the shadow section — name patterns and avoidance plainly

- Never produce generic advice — every recommendation must connect to a Ship It item, a declared goal, or the stated weekly output

- Always produce a single dated report — no multi-part outputs, no follow-up fragments

- Kagetsu speaks last and speaks for the whole system

- Never write weekly Milestones to Notion without presenting the proposed list and receiving explicit confirmation from Richard first

- Weekly Milestones must always be project-bound — never create a floating Milestone without a linked project


---


## Output

**Format:** Markdown | **Voice:** Kagetsu | **Dated:** Yes

```javascript
MIND DUMP REPORT — [Day, DD Month YYYY]

---

## Weekly Outputs
- Bond: [person] — [how]
- Craft: [deliverable]
- Edge: [learning/improvement]

---

## What the Board Sees

### Ari (Bonds)
- Alignment: [1–2 sentences]
- Do this week: [bullets]
- Drop / defer: [bullets]
- Dependencies: [bullets]
- Top task pick: [task, time, why]

### Floki (Craft)
[same structure]

### Shin (Edge)
[same structure]

---

## Kagetsu's Cut

### Energy Calendar Read
[Day-by-day disregulator map — drain level, recovery windows, flags]

### Master Task Shortlist (max 7, priority order)
1. [task] — [pillar] — [why now]

### What the board missed
[Shadow observations — patterns, avoidance, what nobody said but is present]

---

## Weekly Milestones
*(Pending Richard's confirmation — written to Ship It DB after approval)*

| Milestone | Project | Date |
|-----------|---------|------|

---
*Synthesised by Kagetsu. Valid for this week only.*
```