---


name: how

uuid: 3d824dc8-ccd9-814a-949c-d2eef25e1fbe

version: 2

description: "How"

return: "grounded walkthrough"

tools:

  - notion

  - atlassian

  - google-drive

thinking: "Medium"

temperature: 0.3

resources:

  - "@Resource-Index"


---


# How

Grounded walkthrough: explain how X actually works by reading the governing artefacts — spec sections, configs, sheets, tickets — never from memory alone. X can be a system, process, pricing mechanism, or integration.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Set altitude.** Infer the audience and depth from the ask (exec summary / working level / mechanism level). State the altitude chosen.

1. **Locate ground truth.** Resolve the governing artefacts via @Resource-Index and this environment's tools; read the relevant sections only (P15). If no artefact governs X, say so — the walkthrough is then explicitly unverified.

1. **Walk through.** Follow one concrete instance end to end (a deal, a failover, a request) rather than describing components in the abstract. Each step cites where it's defined. Note where observed behaviour and documentation diverge.

1. **Map the edges.** Boundaries, failure modes, and the 2–3 most common misconceptions, each grounded.

1. **Offer a visual** (flow or sequence) when the path has branches; skip for linear flows.

## Boundaries

- Never present an unverified explanation as grounded — label which parts were read vs recalled

- Never paraphrase-degrade normative content (SLAs, prices, RTO/RPO) — state exact values with their source

- Read-only on all sources

## Output

Walkthrough at the stated altitude: concrete instance traced end to end, per-step citations, edges and misconceptions, divergence flags. Visual when branching warrants it.

## Examples

1. "/how does EOD batch monitoring decide a job is late?" → reads the Grafana dashboard JSON + EOD MCD → traces one tenant's job through thresholds, cites the 3.5h rule and its gating query, flags the wrapper-exclusion regex as commonly misread.

1. "/how does a DR tier land on a customer invoice?" → pricing MCD + calculator → one worked deal from tier selection to line item.

## Next steps

Invoke with the thing and, optionally, audience or altitude.