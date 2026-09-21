---


name: create-reactor

uuid: 38824dc8-ccd9-8131-b96d-c8b638a8eaa3

version: 5

description: "Create Reactor"

return: "disaster-reactor [SKILL.md](http://skill.md/) published to Notion AI Hub + first run as test"

tools:

  - notion

  - web_search

thinking: "Medium"

temperature: 0.4


---


> Setup wizard for a new Reactor. Interviews the user (or accepts a brief), generates a single self-contained [SKILL.md](http://skill.md/) in the /disaster-reactor pattern — signals, sources, context, execution logic, and artifact spec all embedded — publishes it to Notion AI Hub, and executes the first run as a live test. No separate knowledge files.


---


## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

**1. Interview or extract brief**

If the user passes a brief, extract answers from it. Otherwise ask in a single message:

- What domain does this reactor monitor? (e.g. platform risk, competitive landscape, regulatory)

- Who/what is the subject? (e.g. "Mambu's cloud platform", "our VC portfolio")

- Regions in scope?

- CSPs, SaaS tools, or infrastructure dependencies?

- Signal categories to prioritise or exclude?

- Dashboard output preferences? (heatmap, signal feed, scenario simulations)

- Cadence?

Do not ask questions already answered in the brief.

**2. Generate embedded Signal Taxonomy**

Build a compressed signal taxonomy for embedding directly in the skill body:

- Define signal domains relevant to the subject (use the six standard domains as a baseline; add domain-specific ones)

- For each domain: specific signals, named entities, keywords, lateral/second-order signals

- Include a keyword/entity index for search targeting

- Flag any domains with thin coverage for Step 3 gap-fill

**3. Generate embedded Sources**

Build a three-tier source table for embedding in the skill body:

- Tier 1: authoritative/real-time (status pages, regulatory bodies, primary news)

- Tier 2: secondary news and analysis

- Tier 3: specialist/deep-dive

- Include region → source mapping if multi-region

- Flag gaps — run targeted web searches to fill thin regions or domains before proceeding

**4. Draft the **[**SKILL.md**](http://skill.md/)

Compose a single self-contained [SKILL.md](http://skill.md/) following the /disaster-reactor pattern exactly:

- YAML header: name, uuid (TBD), version 1, description, return, tools

- Context block: domain description, infrastructure footprint, regions, region notes, key dependencies

- Signal Taxonomy section (embedded from Step 2)

- Sources section (embedded from Step 3)

- Steps 1–7: load status quo → fetch → classify → simulate → compose report → update status quo → build JSX

- Status quo format removed — no status quo file, no delta tracking

- Outputs section: REPORT + JSX artifact — both mandatory per run

- Artifact spec: D3 + TopoJSON choropleth, 6 panels, signal data contract, ISO ID mapping, pulse animation, severity colour coding

**5. Publish to Notion AI Hub**

Create a new page in the AI Hub DB (parent data source: `collection://28424dc8-ccd9-801c-8439-000ba9845548`):

- Properties: Name = skill name, Description = human-readable name, Type = Skills, Version = 1, Visibility = mambu (default; confirm with user if domain is generic/public)

- Content = full [SKILL.md](http://skill.md/)

- Retrieve the new page UUID and replace `uuid: TBD` in the YAML header

- Update the Notion page with the corrected YAML

**6. First run as test**

Invoke the new skill immediately:

- Run web searches across the signal taxonomy

- Fetch CSP and SaaS status pages

- Classify findings

- Produce REPORT block (two time horizons: Last 7 Days + Last 90 Days) + DisasterReactor.jsx artifact

- Present JSX via present_files

**7. Confirm and deliver**

- Confirm: "Your [name] reactor is live. Say `/[skill-name]` to re-run."

- Surface any fetch gaps or thin domains found during the first run as candidates for `/update-reactor`

**Example 1: Platform risk reactor**

> "Set up a Disaster Reactor for Mambu's cloud platform — AWS 90%, GCP 8%, Azure 2%. Regions: Europe, Middle East, North America, Latin America, SEA/APAC, Africa."

Expected: Generates embedded six-domain signal taxonomy, tiered sources with region mapping. [SKILL.md](http://skill.md/) published to Notion AI Hub. First run produces signals across all regions. Dashboard with D3 choropleth rendered.

**Example 2: Competitive reactor**

> "Set up a competitive reactor for our core banking platform. Monitor Thought Machine, Temenos, Finastra, 10x. Europe + North America. Weekly."

Expected: Signal taxonomy covers product launches, pricing signals, customer wins/losses, funding/M&A, leadership changes. Sources: Finextra, The Banker, company newsrooms, Crunchbase. Dashboard: competitor card grid with per-competitor signal feed.

**Example 3: Brief-driven, no interview**

> "Regulatory reactor for EU fintech. DORA, NIS2, EU AI Act, PSD3. Quarterly cadence. Audience: legal and compliance team."

Expected: Extracts all answers from brief, skips interview, drafts skill immediately. Signals taxonomy focused on regulatory milestones, enforcement actions, supervisory authority publications. Sources: EIOPA, EBA, ENISA, Politico EU.


---


## Boundaries

- Never proceed to Step 6 (first run) without the Notion page UUID confirmed

- Never leave template placeholders unfilled in the [SKILL.md](http://skill.md/)

- Never skip the Tier 1 source gap-fill in Step 3 — at least one authoritative source per region in scope

- Never generate an artifact without a confirmed signal data set from live searches

- Never run the first run without web_search enabled

- If the brief is ambiguous, generate a best-guess draft and surface questions at Step 5 confirmation — do not pause mid-generation

- Always embed signals and sources in the skill body — no separate knowledge files

## Output

- Single [SKILL.md](http://skill.md/) published to Notion AI Hub with real UUID

- First-run REPORT block, STATUS QUO seed, and JSX artifact rendered in chat