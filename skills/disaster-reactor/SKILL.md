---


name: disaster-reactor

uuid: 38824dc8-ccd9-8143-a2a3-f93fa8d89255

version: 4

description: "Disaster Reactor"

return: "REPORT block + DisasterReactor.jsx artifact"

tools:

  - web_search

  - web_fetch

  - bash_tool

  - present_files

thinking: "Medium"

temperature: 0.4


---


# Disaster Reactor

Forward-looking signal intelligence for Mambu's platform. Monitors cloud infrastructure, geopolitics, cybersecurity, macro-economics, AI lab health, and SaaS dependencies. Produces a structured report, updated status quo, and a live React dashboard artifact on every run.

**Cadence:** Weekly (Monday). On-demand for breaking events.


---


## Mambu Context

**Infrastructure footprint:** AWS ~90% (primary CSP globally) · GCP ~8% · Azure ~2% (ME-first)

**Regions in scope:** Europe (incl. UK) · Middle East · North America · Latin America · SEA/APAC · Africa

**Region notes:**

- UK: post-Brexit, outside DORA — FCA/NCSC applies

- Africa: AWS af-south-1 (Cape Town) primary; Eskom load-shedding leading physical risk; FSCA for regulatory monitoring

- Middle East: Azure-first despite global AWS dominance

**Key SaaS dependencies:** Salesforce (AWS/Hyperforce) · Intercom (AWS) · Atlassian Jira/Confluence (AWS) · Slack (AWS) · GitLab (GCP primary)


---


## Signal Taxonomy

Scan these domains. Backwards-looking metrics excluded — forward-looking and leading signals only.

**1. Cloud Infrastructure**

- CSP operational health: planned maintenance, capacity reservation changes, AZ additions/deprecations

- CSP holding company risk: AWS/Amazon earnings, Azure growth decel, GCP profitability, Anthropic/AWS partnership signals

- AI compute concentration: hyperscaler GPU allocation shifts, NVIDIA supply chain, data centre power grid stress (Northern Virginia, Dublin, Frankfurt, Singapore, Dubai)

**2. Geopolitical & Regulatory**

- Europe: EU AI Act, DORA enforcement, NIS2, Schrems III, ENISA advisories, Eurozone macro

- Middle East: UAE/KSA data residency, SAMA framework, GCC political instability, undersea cable routes, Azure UAE capacity

- North America: US EOs on cloud data handling, FTC/DOJ antitrust, CISA advisories, AI export controls, Fed/banking stress

- LatAm: Brazil LGPD/ANPD, Mexico data localisation, AWS São Paulo, political instability

- APAC: MAS TRM, APRA CPS 230, India DPDP, Philippines BSP, South China Sea cables, Taiwan Strait, TSMC supply chain

- Africa: FSCA, Eskom load-shedding, af-south-1 capacity

**3. Cybersecurity**

- APT activity targeting financial infrastructure (Russia/China/DPRK/Iran)

- Ransomware campaigns — banking/fintech sector

- Supply chain attacks on cloud-adjacent SaaS (Okta, Cloudflare, Datadog)

- Zero-days in hyperscaler infrastructure, Kubernetes, container runtimes

- CVSS ≥9.0 CVEs in AWS/Azure/GCP managed services or Mambu stack (Kafka, PostgreSQL, Java)

- BGP hijacking, DNS manipulation, DDoS — financial sector

**4. Macro-Economic & Financial Sector**

- Regional banking stress (SVB-pattern), central bank policy shifts (ECB/Fed/BoE)

- Fintech funding collapse — Mambu client viability

- DORA-driven vendor consolidation

- Competitor core banking outages (Thought Machine, Temenos, Finastra)

**5. Physical Infrastructure**

- Data centre power stress: us-east-1 (N. Virginia), eu-west-1 (Dublin), eu-central-1 (Frankfurt), ap-southeast-1 (Singapore), me-central-1 (Dubai)

- Submarine cable: FLAG/EIG (Europe–ME), SMW3/SMW5 (Europe–Asia), FASTER/Unity (Pacific), MAREA (Atlantic)

- Extreme weather affecting cloud regions

**6. SaaS Dependencies**

- Status pages: [status.salesforce.com](http://status.salesforce.com/) · [intercomstatus.com](http://intercomstatus.com/) · [status.atlassian.com](http://status.atlassian.com/) · [status.slack.com](http://status.slack.com/) · [status.gitlab.com](http://status.gitlab.com/)

- Vendor financial health, M&A activity, security incidents, pricing/licensing changes

- Key cascade risk: AWS us-east-1 or eu-west-1 degradation → Salesforce Hyperforce impact

**7. AI Lab / Lateral Risk**

- OpenAI: funding, revenue vs burn, IPO, Azure GPU demand

- Anthropic: equity rounds, AWS partnership, IPO, export control actions

- Google DeepMind: GCP integral risk

- NVIDIA: export controls, fab capacity, allocation priority, new GPU generation transitions

**Entity index for search:** AWS · Azure · GCP · OpenAI · Anthropic · NVIDIA · Salesforce · Intercom · Atlassian · Slack · GitLab · DORA · NIS2 · EU AI Act · SAMA · MAS TRM · APRA CPS 230 · LGPD · DPDP · CISA KEV · APT28 · APT29 · Lazarus Group · Volt Typhoon · Killnet · LockBit · submarine cable · BGP hijack · data centre outage


---


## Sources

**Tier 1 — Real-time / Authoritative**

**Tier 2 — News & Intelligence**

**Tier 3 — Specialist**


---


## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

### 1. Fetch — live searches first, every run

Run web searches across the signal taxonomy before synthesising anything. Minimum search set per run:

- `AWS Azure GCP outage incident [current week]`

- `DORA enforcement 2026`

- `ransomware financial sector [current month]`

- `OpenAI Anthropic funding IPO [current month]`

- `NVIDIA GPU supply 2026`

- `[active geopolitical signal from status quo] latest`

- Region-specific searches for any elevated/high signals in current status quo

Fetch status pages (CSP + SaaS) directly. Flag any source returning nothing — do not invent signals.

### 2. Classify each signal finding

For each signal × source result:

- **Threat** — clearly negative, directional risk to Mambu

- **Opportunity** — clearly positive upside

- **Ambiguous** — dual-sided; split into threat and opportunity scenario

Do not force classification. Ambiguous is valid and useful.

Assign per signal:

- **Severity:** Critical · High · Elevated · Watch · Clear

- **Likelihood:** 0–100 (probability of materialising or escalating within 90 days)

- **Type:** `csp` · `cyber` · `geo` · `macro` · `physical` · `saas` · `ai-lab`

- **Status:** `emerging` · `established` · `resolved`

### 3. Simulate — top 3 scenarios

Pick the 3 signals most likely to develop further (priority: high-impact with predictable next move → ambiguous with meaningful divergence → weak signals accumulating evidence).

For each:

- **What it is:** one sentence

- **Most likely next:** one sentence

- **Threat branch:** if this goes badly for Mambu

- **Opportunity branch:** if this resolves well

### 5. Compose REPORT block

```javascript
## REPORT — Disaster Reactor
Run date: YYYY-MM-DD

### Executive Summary
[3–5 sentences. Net assessment. Top risk. Any resolved signals.]

### Signal Feed — Last 7 Days
[New and upgraded signals only. One paragraph per signal: what happened, why it matters to Mambu, source.]

### Signal Feed — Last 90 Days
[Active established risks. One paragraph each. Focus on trajectory, not recap.]

### CSP Status
AWS: [status + top signal]
Azure: [status + top signal]
GCP: [status + top signal]

### AI Lab / Lateral Risk
OpenAI | Anthropic | NVIDIA | Google DeepMind — one line each, status + key signal

### SaaS Dependency Status
[Table: System · Status · Signal]

### Scenario Simulations
[3 × scenario blocks from Step 4]

### Resolved / Superseded
[Any signals closed this run]

### Fetch Notes
[Sources that returned nothing or were inaccessible]
```

### 6. Update STATUS QUO

Two time horizons only. Merge new findings in. Remove resolved signals. Do not expand the structure.

```javascript
# status-quo.md — Disaster Reactor
Last updated: YYYY-MM-DD

---

## Last 7 Days — Active Signals
[Table: Region · Signal · Severity · Delta]
Free-text context per signal — 2–3 sentences max.

---

## Last 90 Days — Established Risks
[Table: Signal · Severity · Status · Last updated]
Free-text context per signal — 3–4 sentences max.

---

## Regional Summary
| Region | Status | Top signal |

## CSP Summary
| CSP | Status | Top signal |

## AI Lab / Lateral Risk
| Lab | CSP link | Signal | Status |

## SaaS Dependency Summary
| System | Status | Signal |
```

### 7. Build DisasterReactor.jsx

Write a React artifact to `/mnt/user-data/outputs/DisasterReactor.jsx`. Present via `present_files`.

**Tech stack:** React + D3 + TopoJSON. Load D3 and TopoJSON via `useEffect` + dynamic script injection (not import statements). Fetch world topology from `https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json`.

**Layout — 6 panels:**

1. **World map** — D3 choropleth, `d3.geoNaturalEarth1()`, dark background `#111`. Country IDs are ISO 3166-1 numeric strings. Active region = full opacity; inactive = `fill + "88"`. Clickable countries filter the region detail panel. Colour by severity: Critical=#ef4444 · High=#f97316 · Elevated=#eab308 · Watch=#3b82f6 · Clear=#22c55e.

1. **Region selector cards** — 6 cards (Europe · Middle East · North America · Latin America · SEA/APAC · Africa), sync with map click, show top severity badge.

1. **Region detail panel** — signals filtered to active region. Each signal card: hyperlinked name with ↗ (opens source URL) · delta badge · severity badge · type badge · status badge · description · source attribution · last-updated timestamp · likelihood bar (0–100%). Emerging signals: pulsing amber border (`animation: drpulse 2s infinite`).

1. **All-signals feed** — filter buttons: all / new / upgraded / unchanged / resolved.

1. **Right rail:**

  - CSP status row (AWS · Azure · GCP) with severity colour

  - AI lab / lateral risk panel (OpenAI · Anthropic · NVIDIA · Google DeepMind) — names hyperlinked ↗

  - Scenario simulation cards (3) with threat/opportunity branch toggle

1. **Footer:** delta summary (X new · Y upgraded · Z resolved) + fetch notes + run date.

**Signal data contract — every signal object requires:**

`id` · `name` · `regions[]` · `type` · `severity` · `status` · `likelihood` (0–100) · `updated` (YYYY-MM-DD) · `url` · `src` · `desc`

**Region → ISO 3166-1 numeric ID mapping:**

```javascript
eu: 276,250,724,380,620,528,56,40,756,752,578,208,246,233,428,440,372,616,203,703,348,642,100,191,705,300,826,831,832,833
me: 784,682,512,634,48,400,422,275,887,760,368
na: 840,124,484
apac: 356,360,458,702,764,704,608,50,144,586,524,410,392,36,554,156,344,446
latam: 76,32,858,152,68,604,170,218,862,591,188,340,222,558,320
africa: 710,566,404,818,12,504,288,231,800,716,686,729,646,508,834,450,480,175,706,24
```


---


## Outputs

Every run produces both — no exceptions:

1. **REPORT block** — structured text per Step 4, written to chat

1. **DisasterReactor.jsx** — React artifact written to `/mnt/user-data/outputs/DisasterReactor.jsx`, presented via `present_files`


---


## Boundaries

- **Always** run live web searches before synthesising — no run from memory alone

- **Always** produce all three outputs on every run

- **Always** include Africa and UK in scope

- **Always** hyperlink every signal name and AI lab card to its primary source URL

- **Never** invent source URLs — no URL = no signal card

- **Never** produce the JSX without running live searches first

- **Never** omit the fetch notes — log every source that returned nothing


---


## Examples

**Example 1: Weekly Monday run**

> `/disaster-reactor`

Expected: Searches all signal domains, fetches CSP and SaaS status pages, classifies findings, produces REPORT + DisasterReactor.jsx. Run completes with `present_files` presenting the JSX.

**Example 2: Breaking event mid-week**

> `/disaster-reactor` — AWS us-east-1 is having a major outage right now

Expected: Prioritises live AWS status fetch, escalates AWS signal to Critical, runs abbreviated signal sweep on other domains, produces REPORT + JSX with the outage as the lead signal. Scenario simulations focus on Salesforce cascade and Mambu client impact.

**Example 3: Quiet week, no new signals**

> `/disaster-reactor`

Expected: Searches return no material new findings. REPORT states net assessment is stable. JSX renders current signals. Fetch notes list any inaccessible sources.