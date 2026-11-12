---


uuid: 41324dc8-ccd9-81d4-9417-e172715cfacd
name: hermes-plugin-triage
description: "Use when evaluating Hermes marketplace plugins."
version: 1.0.0
author: clarity
license: proprietary
thinking: "Medium"
temperature: 0.3
metadata:
hermes:
tags: [hermes, plugins, marketplace, evaluation, install]
related_skills: [hermes-services, hermes-skill-library]


---


# Hermes plugin triage

"Which of these plugins should I install?" — confirm real catalogue names, read the disclosures, and answer against this machine's actual stack rather than repeating the source's ranking.

## When to Use

- A video, post or list of Hermes plugins comes in with "which are worth it for me?".

- Deciding whether a plugin replaces an existing skill, MCP server or script.

- Before installing anything that declares write access or new network egress.

## Steps

1. **Resolve names against the catalogue before discussing them.** Never repeat a name you only heard — speech-to-text mangles them and the popular-sounding ones often do not exist (the plan/verify family is not called what the video calls it).

  ```bash
  H=~/.hermes/hermes-agent/.hermes/bin/hermes
  $H plugins search "<term>" --json      # name, tier, description per entry
  $H plugins list                        # what is already installed
  ```

  `search --json` is the machine-readable path — parse it and filter in Python. If `browse --json` comes back empty, fall back to one `search --json` per term.

1. **Search by the description, not the name.** A video describes behaviour ("records you doing a browser job, then turns it into a skill"); the entry is `workflow-record`. Query the nouns in the behaviour: `record`, `wiki`, `phone`, `plan`, `usage`, `connect`.

1. **Read the FULL description of each candidate.** The table truncates at ~60 chars and the tail is where the **Disclosure** lives: what runs with your privileges, which port it opens, whether telemetry is on, what it writes, what it costs. That block decides the recommendation; the marketing line does not.

1. **Probe the prerequisite on this machine before calling anything applicable.**

  ```bash
  which claude codex                                  # subscription-backed providers need the CLI present AND logged in
  curl -s -m 2 http://127.0.0.1:9222/json/version     # browser-recording plugins need a Chromium on CDP
  pgrep -fl "Hermes.app"                              # Desktop-UI plugins are invisible in a chat-first workflow without it
  ```

  Also check whether the capability already exists (`skills_list`, `$H plugins list`, `hermes tools list`). Recommending a plugin for a job an existing skill already does well is a regression, not a win.

1. **Rank into three explicit buckets**: install now / conditional (name the prerequisite that makes it worth it) / skip (one clause each). The skip list is what makes the shortlist trustworthy.

1. **Install, then read the declared capabilities before trusting it:**

  ```bash
  $H plugins install <name>
  $H plugins capabilities <name>     # declared vs granted; check anything with write access
  $H plugins enable|disable <name>
  $H plugins remove <name>           # the undo — say so when recommending
  ```

## Pitfalls

- **Tier is the first filter, not the last.** `official` > `verified` > `community`; a Labs entry ("built by Nous Research, not supported") is fine for a narrow local tool and not for anything holding credentials. State the tier in the recommendation.

- **The disclosure is authoritative over the capability claim.** An entry can advertise something the runtime then refuses (an alias profile claiming spec-decode that the loader disables). When they disagree, believe the runtime and the disclosure, and say which one you verified.

- **Several entries do the same job.** Session-cost and quota families each carry 4-6 near-duplicates — same data, different UI surface. Recommend ONE and name the runner-up; installing three is churn.

- **Desktop-UI plugins need the desktop app.** Cost panels, wikis and status-bar chips do nothing for a chat-only session — confirm the app is running before spending the recommendation on one.

- **Subscription-backed model providers move spend, they do not remove it.** They bill every turn (cron included) against a personal plan allowance, inherit whichever account the CLI is logged into, and are usually experimental. Quantify against the user's stated spend goal and flag the cron interaction — an unattended job quietly eating a personal quota is the surprise.

- **A plugin that types into real accounts is the same risk class as an open automation editor.** Where local execution, real credentials and no approval gate meet, say so plainly and let the user accept it.

## Reporting shape (this user)

Ranked shortlist first, each with the concrete reason it fits *his* stack (name the machine, the job, the existing skill it complements). Then the skip list with one-line reasons. Then the disclosures, one sentence each: what it can touch, what it costs, what stops working. Offer to install the shortlist — do not install unprompted, and never present a plugin as suitable because it is popular.