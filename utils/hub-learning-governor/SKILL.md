---


name: hub-learning-governor

uuid: 3f224dc8-ccd9-8184-a570-e72ae422a729

version: 1

description: "Hub Learning Governor"

return: "Learning-route decision + applied-change delta"

last-used: "2026-10-07T20:46:19+02:00"

scope: synced

synced-version: 1

local-path: `/Users/chdwck9studio/.hermes/skills/hub-learning-governor/SKILL.md`

thinking: Medium

temperature: 0.3

resources:

  - "@AI-Hub"

  - "@Resource-Index"

  - "@Memory"

  - "@Local-Mode"


---


# Hub Learning Governor

Route learning signals from Hermes sessions into the correct governed destination. Use when asked to retain a preference, improve a skill, create a learned skill, reconcile local and Hub skill copies, or review continuous-improvement output. This skill governs routing; it does not replace `$reinforce`, `$create-skill`, `$memory`, or Hermes Curator.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Load context.** Search `@AI-Hub` for the named skill, resource, standard, project, or prior decision. Resolve the applicable source through `@Resource-Index`; load `@Local-Mode` before changing a skill. If no canonical record exists, state that explicitly.

1. **Classify the signal.** Use exactly one primary route:

  - Richard-originated gut or aesthetic correction → `$reinforce` and the producing skill's `## Taste`.

  - Evidence-backed execution gap, repeat failure, or missing boundary → `$reinforce`, which applies the change through `$create-skill`.

  - New reusable workflow or source-derived method → `$create-skill`; `$learn` output is a candidate, never a governed publication.

  - Durable cross-session fact or preference → `$memory`; `@Memory` remains the superset and Hermes memory receives only an approved compact projection.

  - Use count, inactivity, archive, backup, or duplicate telemetry → Hermes Curator only.

  - One-off task state, transcript detail, or unverified inference → do not retain.

1. **Apply the route.** Ground every skill change in the active segment or cited source. Keep Taste lines terse, Richard-originated, and free of personal data. For memory, use the native pending-memory approval flow and then `$memory export` or `$memory import` to merge it with `@Memory`. Do not write credentials, account identifiers, health, or family data unless the governing memory workflow was explicitly invoked for that category.

1. **Synchronize governed skills.** Apply scope before every write. `hub` has one Hub copy; `local` has one local copy and receives no Hub write; `synced` compares both copies against `synced-version`. If both changed, show the diff and stop for Richard's decision. If one changed, it wins; update the other copy and set both `version` and `synced-version` to the new identical version. Update Hub `Last Used` only for `hub` and `synced` skills.

1. **Constrain Curator.** Keep `curator.consolidate` off unless Richard explicitly opts in for a bounded review. Curator may report, back up, mark stale, archive, or restore agent-created skills. It must not make semantic edits to AI-Hub-governed skills, alter Taste, or publish a skill.

1. **Verify and report.** Read back every changed Hub page and local `SKILL.md`. Report source evidence, route selected, destination, version transition, synchronization result, and items deliberately not retained.

## Examples

- Richard says, "This is too corporate; make it more direct," after `/weekly-status-update` → route to `$reinforce`; update only that skill's Taste or the step evidenced by the correction. Do not add a generic Hermes preference.

- A new source produces a broadly useful workflow → `$learn` may make a candidate; `$create-skill` researches, tests, and publishes the governed Hub skill. For a synced skill, write the identical local copy only after the Hub record is verified.

- Curator reports an unused skill → retain the Curator state transition only. Do not infer that the workflow is poor or remove its Hub page.

## Boundaries

- Never treat Hermes memory, Curator telemetry, or a `$learn` candidate as the source of truth for a skill.

- Never create a Taste line without Richard's explicit correction.

- Never publish, merge, or overwrite a conflicting synced skill without the `@Local-Mode` comparison.

- Never auto-run `$reinforce` on old sessions without attributable evidence from those sessions.

- Never enable Curator consolidation as a substitute for governed review.

## Output

Return a compact markdown delta: **Signal / Route / Evidence / Changed or prepared / Sync state / Not retained**. For writes, include the Hub page URL, local path, version, and read-back verification. Before finishing, verify every required element exists and passes. Anything missing → do the work; do not finish.

## Next steps

Invoke when a session generates a learning signal, before promoting a `$learn` candidate, or when reconciling a governed skill between AI Hub and Hermes.