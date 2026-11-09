---


uuid: 40524dc8-ccd9-810d-b835-d5cdda2b6c0a
name: jira-cloud-rest
description: "Use when pulling Jira Cloud data over the REST API."
version: 1
scope: local
author: Clarity
license: proprietary
metadata:
hermes:
tags: [jira, atlassian, rest, api, reporting]
related_skills: [monday, ship-db, remote-agent-kickoff]


---


# Jira Cloud over REST

Query Jira Cloud directly with the stored API token. This is the **deterministic** route: no LLM, no OAuth connector, no interactive login — so it runs from a script, a dagu step or a cron job, and it is the route to reach for whenever a connector-based Atlassian route is unavailable.

## When to Use

- A periodic Jira report: issues created, status transitions, comments of substance, blockers, due-date changes.

- Any "what happened in project X last week" question.

- When the connector-based route fails (see Pitfalls) and the data is still needed.

## Credentials

- `~/.hermes/keys/atlassian.env` (mode `600`): `ATLASSIAN_EMAIL`, `ATLASSIAN_TOKEN`.

- **Never print, log or paste the token.** Report variable *names*, never values. Read the file in-process.

- Auth is HTTP **Basic** — `base64(email + ":" + token)`.

## Site and endpoints

- Base: `https://mambucom.jira.com` (equally valid: `https://api.atlassian.com/ex/jira/<cloudId>`).

- **Prove the credential first:** `GET /rest/api/3/myself` must return a display name before you trust any other call.

## Search

`POST /rest/api/3/search/jql` with body `{"jql": …, "maxResults": 100, "fields": [...]}`.

- The legacy `GET/POST /rest/api/3/search` is retired on this instance — use `search/jql`.

- **Pagination is token-based, not offset.** Each response carries `nextPageToken` and no `total`. Loop, passing `nextPageToken` back under the same key, until it is absent. Never wait for or assert a `total` field.

- Request `fields` explicitly or the rows come back bare: `key`, `project`, `summary`, `status`, `created`, `updated`, `assignee`, `priority`, `duedate`, `issuetype`, `resolution`, `labels`.

## Two timestamp traps

- **Jira returns offsets without a colon** — `…T09:00:00.000+0100`. `datetime.fromisoformat` rejects that form. Normalise first:
`s = s.replace("Z", "+00:00"); s = re.sub(r'([+-]\d{2})(\d{2})$', r'\1:\2', s)`.

- **A windowed JQL has no upper bound unless you add one.** Filter client-side: convert `updated` into the reporting timezone and compare against the window's dates. Take the UTC offset from the date, not from habit — it changes on the last Sunday of October.

## History: transitions, comments, due-date changes

This is what turns an issue list into a report. Per issue:

- `GET /rest/api/3/issue/{key}/changelog?maxResults=200` → `values[].items[]`, where `field` is `status` (`fromString` → `toString`) or `duedate` (`fromString` → `toString`).

- `GET /rest/api/3/issue/{key}/comment?maxResults=100` → `comments[]` with `author.displayName` and an Atlassian Document Format `body`; flatten it with `body.content[].content[].text`.

- Filter both by their own `created` inside the window — the endpoints return the **full** history.

Volume is not a problem: a few hundred issues × 2 calls, with a small thread pool (≈6 workers) and retry-with-backoff on 429/5xx, finishes in well under a minute. A recorded `status` or `duedate` change is the evidence for a blocker — do not infer a blocker from a title.

## Pitfalls

- **`DR`**** and ****`MPO team`**** are the same Jira project under different names.** Never report them as two spaces.

- **Do not build scheduled work on a **[**claude.ai**](http://claude.ai/)** Atlassian connector.** It depends on a live per-connector OAuth grant that can silently lose its Jira scopes while the site still resolves — producing `403 The app is not installed on this instance`, which reads like an instance-level install problem and is not one. The token route has no such dependency.

- **Exclude bot/automation comments** when deciding what counts as "a comment of substance" — filter by author before quoting.

## Reporting shape

- **Flags** — only items needing the user's own perspective: customer/user requirement translation, expectation alignment, commitment-vs-record conflicts. **Exclude** EM/engineering-owned gates (sign-offs, approvals, access requests, ticket gates, routine engineering risk); those belong with the owning team. Escalating a routine approval is over-escalation.

- **Candidate tasks** — propose only, never write. Name, owner pillar, priority, and the week's Monday as the date.

- **Birds-eye** — one short paragraph per space: what happened and where the team stands.

## Verification

- `GET /rest/api/3/myself` answered before anything else.

- The collected issue count equals the sum of the per-space counts.

- Spot-check one changed issue's changelog against what you reported.

## Related

- `monday` — the weekly reset whose Jira leg this serves.

- `ship-db` — where the proposed rows would land.

- `remote-agent-kickoff` — the connector-based route and its scope-loss failure mode.