---


uuid: 40524dc8-ccd9-8154-b042-f71094bf1281
name: tech-landscape-research
description: "Use when asked what's current in AI/dev tooling."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
hermes:
tags: [Research, Models, Landscape, Primary-Sources, HuggingFace, Ollama, Versions]
category: research
related_skills: [service-api-mcp-research, grounded-citations, blocked-page-recovery]


---


# Tech Landscape Research

"Which model / harness / version is best right now?" is a currency question: the
answer changes faster than any training cutoff, so a remembered answer is a guess
dressed as fact. Answer it from a **primary-source registry**, fetch the
registry's **JSON API** (not its HTML page), and **date-stamp** the conclusion.

## When to Use

Trigger this for any "what's the current/best X" question about the fast-moving
AI/dev stack: open-weight or local models and MoE/quant choices, agent harnesses,
inference runners, library and CLI versions. It applies even when you feel
confident of the answer — the whole point is to replace a remembered guess with a
live, date-stamped check. Skip it only for stable, slow-changing facts.

## Procedure

1. **Establish "now".** Run `date` on the host and state the as-of date in the
answer. "As of Oct 2026" is part of the finding, not decoration.

1. **Pick the registry by object type** (exact endpoints in
`references/primary-source-apis.md`):

1. **Query the API, not the rendered page.** Registry HTML is JS-heavy and
bot-walled; the JSON endpoint is open, compact, and stable to parse.

1. **Drill to the object's own metadata.** For a model, read `config.json`
(`model_type`, `num_experts`, `num_experts_per_tok` → MoE vs dense) and the
`README.md` frontmatter tags (`moe`, `gguf`, `mlx`). Newer families use opaque
`model_type` strings — read the fields, don't pattern-match the name.

1. **Cross-check reality.** A model card proves a model exists, not that a
runner/quant for the user's hardware exists. Confirm a GGUF/MLX build and a
matching size before recommending it.

1. **Report** with the as-of date, named sources, and verified-vs-assumed kept
visibly apart. Download counts and recent `lastModified` are the currency
signal — an old library entry is context, not "current".

## Pitfalls

- **Never answer a landscape question from memory.** Verify against a live
registry even when confident; model naming (versions, MoE suffixes) drifts.

- **Search engines are the slowest route here.** `web_extract` can be configured
with a *search-only* backend that cannot extract — the fix is to set
`web.extract_backend` to firecrawl/tavily/keenable/exa/parallel; until then,
when generic-search results are low-relevance, stop fighting it and curl the
registry API directly.

- **HF models API quirk:** `?sort=trending` is rejected
(`Invalid sort parameter: trending`) even though the website uses it. Use
`sort=downloads&direction=-1`, or `search=<keyword>`.

- **Prefer a docs ****`llms.txt`**** index over crawling nav.** Many doc hosts publish a
flat list of every page slug; grepping it surfaces features (webhooks,
schedules, guided triggers) the rendered site buries.

- **One source is not currency.** Corroborate with a second registry and a
recency signal before calling something "the current best".

- **A name the user supplies is not proof it exists.** A tool or model you do
not recognise must be resolved against a registry (GitHub search, PyPI,
Homebrew) *before* you recommend or install it — never invent capabilities
for an unverified name. Verify *installability* too, not just existence: a
PyPI project page or Homebrew-core formula returning 200 is the green light.

## References

- `references/primary-source-apis.md` — exact endpoints, query params, and Python
parsing snippets for Hugging Face, Ollama, GitHub, and docs `llms.txt`.