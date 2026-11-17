---


uuid: 41924dc8-ccd9-8148-8c9d-faa1a44f330f
name: agent-runtime-exit-review
description: "Use when surveying Hermes' agent-runtime competitors."
version: 1.0.0
author: Hermes Agent (Clarity)
license: MIT
platforms: [macos, linux]
metadata:
hermes:
tags: [Competitors, Landscape, Hermes, BuildVsBuy, Monthly]
category: research
related_skills: [tech-landscape-research, competitor-news-monitor]


---


# Agent Runtime Exit Review

Monthly check of whether a commercial personal-agent product has overtaken this
self-hosted Hermes setup, and whether a trial is worth the switching cost. The
client is Richard; the subject includes **me**. Report that honestly: a
competitor that is genuinely better at his work is a finding, not a threat to
manage.

Watch contract (watchlist, rubric, verdict rules, last run, open questions):
`~/.hermes/competitor-watches/agent-runtime-exit.json`. Read it first, update
it last.

## When to Use

- The monthly cron fires for `agent-runtime-exit`.

- Richard asks "should we still be running Hermes?", "what do the labs ship now?",
"is X worth trying?" where X is a hosted personal-agent product.

## Procedure

1. **Establish now** (`date`) and read the watch contract. Diff the watchlist
against last month before searching, so stable entries are skipped.

  **`human_decisions`**** in the contract overrides the rubric.** When Richard has
  already ruled on a product, the run does not re-propose it — it reports
  whether the named re-entry triggers have landed. Anything he has deferred
  stays deferred until the trigger is evidenced by a primary source.

1. **Fetch primary sources per vendor.** One launch/changelog page per product
beats a search sweep: positioning, platform support, pricing tier, and the
limits section ("what it doesn't do yet") are all on it.

1. **Verify every price and tier on the vendor's own page.** A pricing claim from
a search snippet is unverified — mark it, or leave it out.

1. **Score against the rubric**, not against feature checklists. The rubric is
ownership, autonomy surface, persistence/RSI, integrations, upkeep, cost,
lock-in. A vendor winning on UX but losing on ownership is a `MONITOR`, not a
migration.

1. **Price the exit explicitly** before any migration is recommended: memory,
skills, cron jobs, gateway/channel plumbing, integrations and credentials that
would have to be rebuilt. Hosted agents cannot be migrated *from*; the memory
stays with them.

1. **Return a verdict per entry** — `THREAT / TRIAL / MONITOR / PASS` — plus one
`Needs Richard` line. Then update the state file (last_run, verdicts, open
questions, cutoff).

## Report shape

```javascript
As of <date>. Baseline: Hermes (owned) vs <N> products.

Per product: name | what changed this month | strongest thing about it |
weakest thing about it | verdict.

Signal / Why it matters / Recommendation / Needs Richard.
```

Keep it under ~40 lines for Discord. Detail belongs in the state file or a
scratch note, not the message.

## Pitfalls

- **`web_extract`**** fails on this box** (`OpenAI Native Web Search ... is a<br>  search-only backend and cannot extract`). Use
`curl -sL "https://r.jina.ai/<url>"` instead; [x.ai](http://x.ai/) returns 403 to plain curl
but renders fine through Jina.

- DuckDuckGo HTML search is bot-walled to plain curl; `r.jina.ai/https://html.duckduckgo.com/html/?q=...`
works and its `## [title](...)` lines are enough to resolve a product name to a
vendor page.

- **A product name from a chat message is a search key, not evidence.** Resolve
"dots" -> OpenAI, "Nod" -> n8n Labs, "Muse" -> Meta, "Duet" -> Anthropic
before writing anything about them.

- Do not mistake "included in their $200 plan" for free. State which plan the
user would actually need to hold.

- Do not treat one vendor's benchmark number (e.g. LongMemEval 93.2%) as
comparable across products; note it as vendor-reported.

- Feature parity is the wrong test. The question is upkeep Richard stops paying
versus control he stops owning.

## Verification

- [ ]Every claim traceable to a primary URL fetched this run, or marked unverified.

- [ ]Every price/tier quoted appeared on the vendor page, not a snippet.

- [ ]Each verdict carries an exit-cost line if it says TRIAL or THREAT.

- [ ]State file updated; no silent skip of an unreachable source.