---


name: mcd-sync

uuid: 3d724dc8-ccd9-810c-a40e-cc00a70b79e6

version: 2

last-used: "2026-09-16T19:12:00+02:00"

description: "MCD Sync"

return: "Sync run summary with deltas, gated items, and integrity findings"

tools:

  - notion

thinking: "Medium"

temperature: 0.3

resources:

  - "@MCD-Protocol"

  - "@AI-Hub-DB"


---


# MCD Sync

Sync a source into an MCD (inbound, default) or an MCD into a target (outbound). Never writes MCD content itself — all MCD reads and writes go through /mcd; this skill owns signal extraction, delta computation, direction, bulk routing, and the integrity sweep.

## Invocation

`/mcd-sync [direction?] [all | mcd-list] [sources | target] [lookback_days=30] [dry_run?]`

Triggers: manual · timer (scheduled runs) · **event** (end-of-loop write-back from /loop and /dt-loop).

## Steps — inbound (world → MCD)

1. Invoke /mcd GET on the target manifest: routing table + each node's `sources:` lines define what to pull. No central sync config — nodes declare their own feeds.

1. Pull each declared source for the lookback window (Slack, Granola, Drive, Confluence, chats, URLs, event payload from a loop).

1. Extract a Raw Signal List: facts, decisions, numbers, ambiguities resolved/opened — each tagged with its source.

1. Compute deltas per node: net-new, contradiction, resolves-ambiguity, already-present (drop). Signals with no home → propose a new node.

1. dry_run: present Delta Report and stop.

1. Else hand deltas to /mcd UPDATE: context-class applied with delta summary; contract-class batched into one approval gate; contradictions always surfaced, never silently resolved.

1. Integrity sweep: manifest rows vs node headers (existence, freshness echo, dead links, orphans, routing misses logged since last run). Fix mechanical drift; report the rest.

## Steps — bulk mode (`all` or a list of MCDs)

Pull once, route many — never loop the single-MCD pipeline per target:

1. **Resolve target set** — one query against @AI-Hub-DB (Type = MCD, Archive = no), or the given list.

1. **Pull sources once** — the invocation's source list overrides per-node `sources:` for what gets pulled; one pull per source, one Raw Signal List.

1. **Route signals to MCDs** — fetch manifests only. Route on manifest identity + routing-table match; node-declared `sources:` act as affinity boosts. A signal may route to multiple MCDs — apply to each, same grounding.

1. **Unrouted signals** are dropped and listed — never forced. Recurring unrouted themes suggest a missing MCD or node.

1. **Per-MCD deltas via /mcd** as in inbound steps 4–6; node bodies fetched only for MCDs that received signals.

1. **One combined gate** — all contract-class items across all MCDs, grouped by MCD, one approval.

1. **Combined summary**; integrity sweep runs only on touched MCDs (full-estate sweep is a separate, explicit run).

## Steps — outbound (MCD → target)

1. /mcd GET the relevant nodes (source of truth).

1. Fetch target (KB article, Confluence page, doc). Diff, classify (add/update/delete/conflict), ground every change in a specific node.

1. Present change plan; execute on approval; report.

## Examples

- `/mcd-sync granola,slack_dm → bcaas 7d` → 11 signals, 4 deltas (3 context auto-applied, 1 contract gated), 1 ambiguity resolved, sweep: 1 stale manifest row fixed.

- `/mcd-sync all granola,slack_dm 7d` → target set of 7 MCDs resolved, 2 source pulls, 19 signals routed (3 to two MCDs each), 4 MCDs touched, 5 unrouted listed, one combined gate with 2 contract items.

- `/mcd-sync outbound bcaas → DR pricing KB article` → plan: 3 updates, 1 conflict flagged for instruction; applied on approval.

- Event: `/loop bcaas …` completes → /mcd-sync event payload → 2 learning nodes minted (1 anti-pattern), changelog appended, no gates hit.

## Boundaries

- Never write MCD content directly — /mcd is the only write path

- Never sync without a resolved target set (named MCD(s) or `all`)

- In bulk mode, pull each source once — never per-MCD

- Never force-route an unmatched signal — list it as unrouted

- Never silently resolve contradictions; never cite a change without source

- Never exceed the stated lookback

- Always produce a run summary, changes or not; always honour dry_run

- One gate per run — batch contract-class items, never ask per item

## Output

Run summary: sources scanned · deltas applied/gated/dropped · unrouted signals (bulk) · ambiguities opened/resolved · contradictions flagged · integrity findings · MCD links