---


name: mcd-sync

uuid: 3d724dc8-ccd9-810c-a40e-cc00a70b79e6

version: 4

last-used: "2026-10-02"

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

Sync sources into MCDs (inbound) or an MCD into a target (outbound). Never writes MCD content itself: all MCD reads and writes go through /mcd. This skill owns signal extraction, delta computation, mode routing, and the integrity sweep.

## Invocation

`/mcd-sync <mcd> [only:<source,…>] [window] [follow-links] [register-sources] [dry_run]` → **sources mode**

`/mcd-sync all <source> [only:<mcd,…>] [window] [follow-links] [register-sources] [dry_run]` → **all-MCDs mode**

`/mcd-sync outbound <mcd> → <target>` → outbound

Triggers: manual · timer · **event** (end-of-loop write-back from /loop and /dt-loop; runs as sources mode with the event payload as the source).

- **window:** `last week` = trailing 7d, `last month` = trailing 30d, `Nd`, or explicit dates. Rolling. Default 30d.

- **Two inbound modes. Each has one fixed axis and one open axis.**

- The fixed axis is never filterable to more than one. Many MCDs × many sources is not a mode: refuse and offer two runs.

## Steps — inbound (both modes)

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Parse and echo.** Resolve mode, MCD(s), source(s), filter, absolute start/end dates, flags in one line before pulling (e.g. `all-MCDs · slack · only: bcaas, wally · 2026-09-25 → 2026-10-02`). Missing or contradictory input → ask once.

1. **Resolve scope.**

  - Sources mode: /mcd GET the manifest. Sources = every `sources:` line in the manifest and nodes. `only:` names must be declared on the MCD; an undeclared source is refused and listed, never read.

  - All-MCDs mode: one query against @AI-Hub-DB, Archive = no, for pages that are MCD manifests. The marker is `mcd:` frontmatter plus an `# MCD Manifest` heading (the Hub `Type` is Product or Project; there is no MCD type). `only:` is resolved against that set; names matching an archived MCD or nothing are reported and skipped. List count and names. From each manifest read only Identity, routing table, aliases (from scope/identity prose and node names) and `sources:` lines; not changelog or ambiguity tables.

  - Filter names match on manifest identity and aliases. An ambiguous match is listed and asked once, never guessed. If the filter leaves nothing, stop and say why; never fall back to the default.

1. **Pull, window-bounded, named sources only.**

  - Sources mode: one pull per source.

  - All-MCDs mode: feed-like source (a channel, a meeting feed) → one pull. Search-like source (workspace search, Confluence) → one query per MCD per alias (keywords are ANDed, so never combine aliases), results deduped per MCD. Exclude bot/app and alert channels. Paginate until the window is exhausted or 100 results per MCD, whichever first; report any truncation. Unscoped source (no declared channels/spaces) = discovery pass: search the whole source.

  - Links found in content are listed as candidates, never fetched. With `follow-links`: one hop, same workspace, attributed in the summary.

1. **Extract a Raw Signal List.** Facts, decisions, numbers, ambiguities resolved/opened, each tagged with source ref and timestamp. Drop anything timestamped outside the window, including old content edited inside it.

1. **Route.**

  - Sources mode: signals map to the MCD's nodes via the routing table. Signals with no home → propose a new node.

  - All-MCDs mode: route on manifest identity + routing-table match; node-declared `sources:` act as affinity boosts. A signal may route to several MCDs. Unrouted signals are dropped and listed, never forced; recurring unrouted themes suggest a missing MCD or node.

1. **Compute deltas** (only for MCDs/nodes that received signals): net-new, contradiction, resolves-ambiguity, already-present (drop).

1. **dry_run:** present the Delta Report and stop.

1. **Apply via /mcd UPDATE.** Context-class applied with a delta summary. Contract-class and manifest Identity batched into one gate across the whole run, grouped by MCD. Contradictions always surfaced, never silently resolved.

1. **Register sources** (only with `register-sources`). For each channel, space or page that yielded accepted signals, propose it as a `sources:` entry on the node it fed and, where people would route to it, a registry row in the MCD Resources node. Apply via /mcd UPDATE (context-class). Never register a source that yielded nothing, a bot channel, or a personal DM. List all registrations in the summary.

1. **Integrity sweep** on touched MCDs only: manifest rows vs node headers (existence, freshness echo, dead links, orphans, routing misses). Fix mechanical drift; report the rest. A full-estate sweep is a separate, explicit run.

1. **Summary.**

## Steps — outbound (MCD → target)

1. /mcd GET the relevant nodes (source of truth).

1. Fetch target (KB article, Confluence page, doc). Diff, classify (add/update/delete/conflict), ground every change in a specific node.

1. Present change plan; execute on approval; report.

## Examples

- `/mcd-sync bcaas last week` → sources mode: manifest declares granola + slack_dm, 2 pulls, 11 signals, 4 deltas (3 context applied, 1 contract gated), sweep fixes 1 stale row.

- `/mcd-sync bcaas only:slack_dm last month` → sources mode, 1 of 2 declared sources pulled.

- `/mcd-sync all slack last month` → 14 non-archived MCDs, one feed pull (30d), 23 signals routed (3 to two MCDs each), 6 MCDs touched, 4 unrouted listed, 3 links listed unfetched, one gate with 2 contract items.

- `/mcd-sync all slack only:bcaas,wally last week` → filter resolves to 2 of 14 MCDs, one feed pull (7d), signals routed only to those 2.

- `/mcd-sync outbound bcaas → DR pricing KB article` → plan: 3 updates, 1 conflict flagged; applied on approval.

- Event: `/loop bcaas …` completes → sources mode with the event payload → 2 learning nodes minted, changelog appended, no gates.

## Boundaries

- Never write MCD content directly — /mcd is the only write path

- Never run all-MCDs mode with more than one source, or sources mode against more than one MCD

- Never read a source that wasn't named or declared; never follow links without `follow-links`; never go past one hop

- Never widen a filter beyond what was named; never fall back to the default when a filter resolves to nothing

- Never select an undeclared source or an archived MCD through a filter; a bad filter name is skipped and reported, the valid remainder runs

- Never use content outside the window

- Never register a source without accepted signals, and never register DMs or bot channels

- Never silently truncate: always report when a pull hit its cap

- Never touch Archive = yes MCDs

- Never force-route an unmatched signal; never silently resolve contradictions; never cite a change without a source ref

- One gate per run; always produce a summary, changes or not; always honour dry_run

## Output

Run summary: mode · resolved sources + window · filter (e.g. only bcaas, wally — 2 of 14) · MCDs in scope / touched · deltas applied/gated/dropped · unrouted signals (all-MCDs) · ambiguities opened/resolved · contradictions · links listed/followed · integrity findings · MCD links