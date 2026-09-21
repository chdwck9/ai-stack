---


name: mcd

uuid: 3d724dc8-ccd9-81eb-876e-f5a2e9ff1099

version: 4

last-used: "2026-09-16T19:12:00+02:00"

description: "MCD"

return: "Manifest/node writes with delta summary, or routed retrieval answer"

tools:

  - notion

thinking: "Medium"

temperature: 0.4

resources:

  - "@MCD-Protocol"

  - "@AI-Hub-DB"

  - "@Inbox"


---


# MCD

Create, manage, update, and retrieve Master Context Documents per @MCD-Protocol. This is the single write/read surface for MCDs. Other skills, including `/mcd-sync`, `/loop`, `/dt-loop`, and MCD-aware agents, route MCD reads and writes through this skill rather than editing manifests or nodes directly.

The skill is optimized for Richard's preferred operating model: atomic context, explicit provenance, top-down graph traversal, surgical edits, minimal duplication, real migration rather than placeholder restructuring, and verified Notion state after structural work.

## Non-negotiable operating principles

1. **Protocol first.** Load `@MCD-Protocol` before any MCD write, migration, or structural decision. Treat it as the governing standard, not optional background reading.

1. **Inspect before mutate.** Fetch the target manifest and affected node(s) before editing. Never infer current structure from search snippets, memory, titles, or stale prior results when a fetch is available.

1. **Surgical by default.** Prefer the smallest exact edit that completes the task. Preserve unrelated wording, hierarchy, native mentions, source material, and child pages.

1. **Real migration, not empty architecture.** When refactoring an existing MCD, move/reuse substantive existing content into the new node structure. Do not create shells, summaries that replace source content, or duplicate pages merely to satisfy a template.

1. **No silent duplication.** A fact has one canonical home. Use inline mentions and routing instead of copying the same fact into multiple nodes. A resource registry records where something is, not what it says.

1. **No fabrication.** Unknown, contradictory, or unverified information becomes an ambiguity or remains explicitly unresolved. Never fill gaps with plausible prose.

1. **Top-down graph only.** `obsidian_links` is the explicit graph exception in node headers and MUST contain immediate child pages only. Never add parents, siblings, arbitrary descendants, or generic relationship metadata.

1. **Verify structural changes.** After moving, creating, nesting, splitting, or otherwise restructuring nodes, re-fetch the affected parent and child pages and confirm actual hierarchy, headers, links, and content. Do not assume a successful write means the structure is correct.

1. **Preserve history.** Never delete canonical knowledge merely because it is old. Supersede it, mark status appropriately, preserve provenance, and record the reason in the changelog where relevant.

1. **Use the existing graph before inventing a new branch.** For product MCDs, use `Systems` for substantive technical/operational structure and `FAQ & Memory` for interrogation, source-derived answers, timestamped Q&A, memory, and lifecycle context. Do not create new top-level buckets for concerns those branches already cover.

## Modes

Detect from input; if ambiguous, ask once: `Create, update, or retrieve?`

### CREATE

1. Accept a problem/opportunity statement or subject description.

1. Interrogate with up to 5 multiple-choice clarifying questions. Unanswered questions become ambiguity nodes, never blockers.

1. Load `@MCD-Protocol` and determine the profile: `product | system | project | person | business | feature`.

1. Inspect whether an MCD or relevant subject already exists before creating anything. Search is for discovery only when routing or direct lookup is insufficient.

1. Draft the minimum viable manifest and node set: manifest identity, routing, resource registry, changelog; then only the nodes required by the profile and known concerns.

1. For product MCDs, add `FAQ & Memory` as a first-class interrogation surface. Add `Systems` only when substantive technical/operational source pages or concerns exist. Never create branch placeholders just because the protocol permits them.

1. Reuse existing substantive pages where possible. If a legacy page already contains material knowledge, migrate or nest that knowledge rather than creating a second canonical copy.

1. Present the proposed structure and any consequential contract/identity changes for approval before creating or changing those gated surfaces.

1. Create the manifest and nodes in Notion. Register each actual node in the manifest. Set headers consistently and initialize `obsidian_links` only with actual immediate children.

1. Verify the resulting hierarchy and manifest routing after creation.

### UPDATE

1. Identify the target MCD and fetch its manifest first. Route from the manifest before searching.

1. Fetch only the affected node(s) and any parent/child page needed to understand the edit. Do not bulk-fetch the entire MCD without a reason.

1. Determine whether the incoming information is new, corrective, contradictory, superseding, or merely contextual.

1. Apply the smallest complete edit. Update the node body and its own `freshness`, `completeness`, and `status` header together when applicable.

1. If the concern is genuinely atomic but new, mint a new node and manifest row. Do not grow an unrelated node into a dumping ground.

1. If a node has accumulated multiple concerns or sustained internal structure, apply the promotion rule: branch it into a subject with its own manifest, and leave the original node as a concise pointer/stub.

1. Maintain `obsidian_links` as the top-down index of immediate children only. Whenever child nesting changes, update the parent's `obsidian_links` in the same structural transaction.

1. Touch manifest routing rows only when routing meaning changes: node added, renamed, retired, split, or materially changed in scope.

1. Contract-class nodes and manifest Identity require Richard's explicit approval before mutation. Context-class writes may proceed, but must produce a delta summary.

1. After any structural edit, move, split, merge, or branch change, re-fetch the relevant pages and verify actual hierarchy, child links, node headers, and preserved content.

1. Never silently trash or delete legacy source pages during cleanup. Prefer nesting, superseding, or explicit archive treatment; deletion requires a clear user instruction and preservation checks.

### GET

1. Fetch the manifest first, always.

1. Answer from the manifest if sufficient.

1. Otherwise batch-fetch the routed nodes, with a normal budget of ≤3 nodes and ≤2 hops from the manifest.

1. Follow inline mentions only when the routed nodes do not contain enough information.

1. Search Notion only when routing fails or the user explicitly asks for discovery. Treat the miss as a manifest/routing gap rather than silently normalizing search-first behavior.

1. Never let retrieval silently sprawl. If a routine question needs more than the expected retrieval budget, diagnose whether the MCD structure or routing is wrong.

1. Surface material freshness, contradictions, or unresolved ambiguity in the answer rather than presenting stale or conflicting context as canonical.

## Product branch rules

For product MCDs:

- `Systems` is for substantive architecture, product design, mechanics, requirements, schemas, infrastructure/environment, bootstrap/provisioning, and acceptance material.

- `FAQ & Memory` is for crafted FAQs, source-derived answers, timestamped Q&A, agent memory, interrogation history, and lifecycle context.

- Historical technical/source pages should be nested under the appropriate branch and retained as substantive pages when they still carry useful knowledge.

- Do not duplicate an MCD child page into `Resources` merely because it exists. The graph already provides that route.

- Use `Resources` for reusable or cross-cutting destinations that people/agents need to find: external docs, Confluence/Jira spaces, calculators, canonical documents, repositories, and stable internal source handles.

- Use `Artefacts` for concrete outputs/deliverables produced from or informed by the MCD.

- Treat `FAQ & Memory` as a knowledge lifecycle surface, not as a second generic notes bucket.

## Resource rules

Use the resource ladder from `@MCD-Protocol`: `sources:` → registry row → dedicated resource node when prose/state is needed.

A resource registry entry should identify the stable handle, destination, what it contains, and when to use it. Keep endpoints active and searchable. Do not invent URLs. If a destination is uncertain, record the source name and ambiguity rather than manufacturing a link.

## Node discipline

Every node should conform to the protocol:

```yaml
scope: [one line — what this covers and does not]
class: contract | context
freshness: [YYYY-MM-DD verified] · [YYYY-MM-DD source date]
completeness: full | partial | stub
status: active | superseded
sources: [feeds, if synced]
obsidian_links: [immediate child pages only]
```

Node types are `intent | constraint | decision | stakeholder | customer | contract | ambiguity | learning | resource`. Learning nodes must identify `pattern` or `anti-pattern` in their first line. One node = one concern.

## Approval and integrity gates

- Never write before loading `@MCD-Protocol`.

- Never mutate `class: contract` or manifest Identity without Richard's approval.

- Never create a duplicate canonical node when an existing node already owns the concern.

- Never create a placeholder page purely to satisfy the expected template.

- Never broad-replace a large manifest or node when a targeted edit will do.

- Never move or rename a page based only on title similarity; fetch and confirm identity/content first.

- Never assume a move succeeded because the tool returned success. Verify parentage with a fetch.

- Never delete a child page during replacement without an explicit instruction to delete it and a visible preservation/deletion check.

- Never use search as the default retrieval path when manifest routing exists.

- Never copy historical facts into current canonical nodes without resolving their status or provenance.

- Never conceal structural uncertainty. Report it and preserve the existing source until the hierarchy is proven.

## Retrieval integrity

When sources conflict:

1. Prefer the current canonical node and explicitly recorded decisions over legacy copies.

1. Prefer the authoritative source endpoint when the MCD identifies one.

1. Use freshness as a contextual signal, not proof of authority.

1. If the conflict cannot be resolved, preserve both histories and mint/update an ambiguity node.

1. Do not silently collapse materially different values into one “best guess”.

## Examples

- `/mcd create — new project: EaaS escrow automation for tier-2 banks` → inspect for an existing subject, ask up to 5 MC questions, create the project profile plus intent/resource/ambiguity nodes actually needed, and verify the hierarchy.

- `/mcd what constraints apply to BCaaS DR pricing?` → GET: manifest → relevant constraint/contract nodes → answer with freshness/ambiguity flags.

- `/mcd update — Tiago confirmed the 4-tier model is final` → route to the relevant decision/contract context, fetch existing nodes first, mint or update the decision as appropriate, mark superseded history, update routing only if needed, and gate contract mutation for approval.

- `/mcd refactor this legacy product MCD` → audit existing substantive pages first, define the new graph, migrate content into atomic nodes and branches, preserve source pages/history, update parent `obsidian_links`, and verify the final hierarchy. Do not replace rich pages with empty stubs or duplicate the same content across branches.

## Output

- CREATE: manifest URL + actual node list + open ambiguities + structural verification note

- UPDATE: delta summary with nodes touched, rows changed, superseded items, approvals/gates, and verification result

- GET: the answer, with routed node links and freshness/ambiguity flags where material

## Boundaries

- `/mcd` is the only MCD write/read surface.

- `/mcd-sync` may discover integrity deltas, but it must route actual MCD writes through `/mcd`.

- `/manage-spec` and `/reconcile-spec` are superseded for MCD operations.