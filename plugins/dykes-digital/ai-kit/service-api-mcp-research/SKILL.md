---


name: service-api-mcp-research
description: "Use when asked if a service has an API or MCP to connect."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
hermes:
tags: [Research, API, MCP, Integration, Feasibility]
related_skills: [external-account-access, selfhosted-api-access, mcp-server-onboarding, blocked-page-recovery]


---


# Service API / MCP Research

Answer "can we read X" / "can we connect to Y" with the route that actually
exists for THIS user's account type — verified against live sources, not
remembered. The central fact: **a service having an API is not the same as
that API being open to the user.**

## When to Use

Trigger this when asked whether a service can be connected or read
programmatically: "is there an API for X", "could you or $max connect to
Y", "can we read Z's data". Also when an existing integration needs to be
justified or replaced. Answer from the vendor's own live docs — never from
memory.

## Procedure

1. **Vendor developer portal first.** Look for `developer.<vendor>.com/docs`,
`<vendor>.com/docs`, or `/api`. Many doc hosts also publish a flat slug
index at `<docs-host>/llms.txt` — grep it to discover features and their
canonical page URLs before crawling the rendered nav. Read the *"who is this for"* sentence — the
decisive fact is usually *which parties* may use it (self-serve customer vs
business/enterprise account vs regulated third party). Personal accounts are
frequently excluded even when an API clearly exists.

1. **Map each API to a customer type.** Enumerate what the portal offers and
who each one is for. Never collapse "the vendor has an API" into "you can
use it."

1. **MCP ecosystem.** Search GitHub's REST API (the HTML search page is often
bot-walled):
`curl -sL "https://api.github.com/search/repositories?q=<svc>+mcp&sort=stars&per_page=5"`
then read the repo README raw with
`-H "Accept: application/vnd.github.raw" https://api.github.com/repos/<owner>/<repo>/readme`
— its **limitations** section usually names the exact account types the MCP
does NOT support.

1. **Support-doc check.** Query the vendor's help-centre API for terms like
`api`, `supported`, `developer`. This is often where the real integration
method is documented when there is no public API:
`curl -sL "https://<sub>.zendesk.com/api/v2/help_center/articles/search.json?query=<term>"`

1. **Gated official route → find the middleware.** If the vendor's own API is
closed to the user, identify the regulated/licensed aggregator that resells
access, and state what it covers and what it does not.

1. **Confirm the user's specific provider is in coverage** (published coverage
/ ASPSP list, or a product that demonstrably integrates it). If you could
not verify directly, present it as a signup-time check — never as fact.

## Fetching the sources

Vendor dev portals and doc sites are usually SPA/Cloudflare-gated; plain curl
returns the "Just a moment..." shell. Prefix the URL with `https://r.jina.ai/`
to get a rendered markdown copy — **anonymous access typically works with no
API key**, so try it before assuming it is unavailable:

```bash
curl -sL --max-time 40 "https://r.jina.ai/https://developer.vendor.com/docs/x"
```

Pitfall: for very large pages Jina may return a truncated body (~a few KB) —
if the result is short but the page is long, fetch the specific sub-URLs you
need rather than the index.

## Report shape

Verdict first (one line), then per-service findings, then the recommended
route, then honest caveats. State what you could NOT verify instead of
smoothing it over. Flag the safety property that matters — read-only vs
payment initiation — and any consent/expiry the user must plan for.

## Pitfalls

- **Account-type gating is the trap.** Read the eligibility sentence before
concluding an API is usable; "business accounts only" and "regulated TPPs
only" are common and decisive.

- **A product with no public API can still be the key.** If the product
connects accounts itself through a regulated middleware, that middleware is
the readable route — verify via the product's own "how it works" and
supported-list docs, not guesswork.

- **Never assert coverage you did not verify.** Separate what a source said
(a supported-list, the vendor's own docs) from what you assumed.

- Prefer the JSON API over the HTML page; bot-walled pages usually leave their
JSON endpoints open.

## Related

- `external-account-access` — wiring the connection once a route is chosen.

- `selfhosted-api-access`, `mcp-server-onboarding` — downstream setup.

- `blocked-page-recovery` — the full fetch-fallback ladder (note: its Jina
section is stale — it claims a key is required; anonymous works).

- `tech-landscape-research` — primary-source registries (HF, Ollama, GitHub,
docs `llms.txt`) for "what's current" model/tool questions.

Reference: `references/banking-apis.md` — UK/EU personal banking (Revolut,
Dyme, PSD2 aggregators, read-only finance MCP servers).