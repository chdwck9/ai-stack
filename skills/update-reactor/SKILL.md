---


name: update-reactor

uuid: 38824dc8-ccd9-8157-b73f-e93287808ba9

version: 4

description: "Update Reactor"

return: "updated Signal Taxonomy and Sources sections patched into the named reactor skill on Notion"

thinking: "Medium"

temperature: 0.3

tools:

  - web_search

  - notion


---


> Signal and source discovery tool for an existing reactor skill. Accepts a reactor skill name as input (e.g. `/update-reactor /disaster-reactor`), fetches it from Notion AI Hub, searches for new signals and sources not currently covered, proposes additions with evidence, and patches the skill on Notion after confirmation. Does not run the reactor, does not touch the status quo.


---


## Invocation

```javascript
/update-reactor /skill-name [focus: topic] [mode: gap-fill|expand]
```

- `/skill-name` — required. The name of the target reactor skill as it appears in Notion (e.g. `/disaster-reactor`)

- `focus` — optional. Specific topic, region, or domain to target (e.g. `focus: Africa signals`, `focus: submarine cables`)

- `mode` — optional. `gap-fill` (default): targets thin/missing domains. `expand`: searches broadly for signal categories outside current coverage


---


## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

**1. Fetch the reactor skill**

Search Notion AI Hub for the named skill. Fetch its full content. Extract:

- Current Signal Taxonomy section (all domains, entities, keywords)

- Current Sources section (all tiers, all URLs)

- Regions and infrastructure context (to calibrate relevance)

If the skill is not found, halt and surface the error.

**2. Map coverage gaps**

Read the Signal Taxonomy. Identify:

- Domains with thin coverage (fewer than 3 specific signals)

- Regions with no named sources in the Sources section

- Signal types plausibly relevant to the domain but absent (lateral/second-order signals, physical infrastructure, regulatory)

- If `focus` is set, target that area regardless of gap map

- If `mode: expand`, scan broadly for categories not covered at all

**3. Search**

Run targeted web searches based on the gap map:

- 1–2 queries per identified gap

- Prefer primary sources (regulatory bodies, status pages, official reports) over aggregators

- For each result: assess whether it introduces a new signal type, named entity, or source worth monitoring

- Do not re-surface signals already well-covered in the current taxonomy

**4. Assess and score**

For each candidate signal or source:

- **Relevance:** High / Medium / Low

  - High: directly affects the subject, credible primary source

  - Medium: second-order, plausibly relevant, secondary source

  - Low: tangential, speculative, poorly sourced

- **Domain:** which taxonomy domain it belongs to

- **Region:** if region-specific

- **Lateral flag:** if it is a second-order dependency signal

- **Evidence:** source URL + date

Discard Low relevance unless `mode: expand` and coverage is very thin. Cap at 15 proposed additions per run.

**5. Present for confirmation**

Output two proposed-additions blocks:

**Proposed signal additions** (for Signal Taxonomy):

- Grouped by domain

- Each: signal name · domain · region · lateral flag · one-sentence description · evidence URL · relevance score

**Proposed source additions** (for Sources):

- Each: name · URL · tier · signal types · region scope · rationale

- Only propose sources not already present

Ask: accept all, accept some, or reject?

**6. Patch the skill on Notion**

After confirmation:

- Fetch the current skill page again (to get latest content for safe str-replace)

- Apply `update_content` to patch only the Signal Taxonomy and Sources sections — do not touch any other part of the skill

- Increment the version number in the YAML header by 1

- Confirm: "Patched [skill-name] on Notion. Version now N."


---


## Examples

**Example 1: Targeted gap-fill**

> `/update-reactor /disaster-reactor focus: Africa signals`

Expected: Fetches disaster-reactor from Notion. Searches "Africa cloud infrastructure risk 2026", "AWS af-south-1 outage", "South Africa load-shedding data centre", "FSCA cybersecurity". Returns 4–6 new signal entries and 1–2 sources (Reuters Africa, AfricaNenda). Proposes additions. On confirmation, patches the skill and increments version.

**Example 2: Broad expand pass**

> `/update-reactor /disaster-reactor mode: expand`

Expected: Scans broadly for signal categories not currently in the taxonomy. Might surface: critical minerals supply chain (data centre construction), AI inference cost signals (hyperscaler margin pressure), or new APT group activity not yet named. Caps at 15 additions. Presents all for confirmation.

**Example 3: Source gap-fill for a new region**

> `/update-reactor /competitive-reactor focus: Latin America sources`

Expected: Searches for LatAm fintech/banking tech news sources not in current Sources section. Returns candidates: Contxto, LatAm List, Fintech Nexus LatAm. Proposes as Tier 2 additions. Patches on confirmation.


---


## Boundaries

- Never modify the reactor's Steps, Outputs, Boundaries, Examples, context block, artifact spec, or status quo — signal taxonomy and sources only

- Never propose a source without a live URL found in search results

- Never accept a signal with no evidence — every addition must cite a specific source URL

- Never re-propose signals already covered at High depth in the current taxonomy

- Never exceed 15 proposed additions per run — prioritise by relevance, discard the rest

- Always fetch the skill fresh from Notion before patching — never patch from a cached version

- Always increment the YAML version on patch

- Never patch without explicit user confirmation

## Output

- Proposed signal additions: grouped by domain, formatted for Signal Taxonomy section

- Proposed source additions: table rows formatted for Sources section

- Relevance scores and evidence citations for every item

- Notion patch applied after confirmation, version incremented