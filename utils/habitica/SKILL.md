---


name: habitica
uuid: 3fb24dc8-ccd9-81be-aa2b-fcae34f8fe9d
version: 3
description: "Read and clear Habitica tasks and habits via the API."
last-used: "2026-10-19"
scope: local
thinking: "Medium"
temperature: 0.2
resources:

- "@Ship-It-DB"


---


# Habitica

Talk to Richard's Habitica account directly, without n8n: read the week's tasks and habits, and clear a finished week. Called by the weekly reset, and any ad-hoc Habitica question.

## Credentials

- Two values, **both** required — Habitica authenticates with a user id *and* an API key:

  - `HABITICA_USER_ID`

  - `HABITICA_API_KEY`

- They live in `~/.hermes/edge.env` (0600) and are read in-process. Never echo them, never paste them into chat, never copy them into a file that syncs.

- Source: Habitica → avatar/gear → **Settings → Site Data** → `User ID` and `API Key`. Both are 36-character UUIDs. **Regenerating the API key invalidates the old one immediately** — if a previously working key stops, that is usually why.

- Headers on every call: `x-api-user: $HABITICA_USER_ID`, `x-api-key: $HABITICA_API_KEY`, and `x-client: $HABITICA_USER_ID-Clarity`. All three are required.

- Base URL: `https://habitica.com/api/v3`.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays marked `skip: <reason>`.

1. **Load credentials** from `edge.env`, then **prove them** with one `GET /user` before doing anything else. Fail loudly if either is missing, and stop on `401 invalid_credentials` — that means the *pair* is wrong, not the headers (see Pitfalls). Never proceed on an unproven auth.

1. **Read the board** — `GET /tasks/user` returns todos, dailies and habits; split by `type`.

1. **Week clear** (the Habitica half of the Monday sweep): for every open **todo**, `POST /tasks/{id}/score/up`. That completes it and banks the reward; it does not delete. Count them.

1. **Milestone marks** — for each habit, read the week's history and count marks earned; pair with Ship's `Shipped` state before proposing a raise to 8 or 10.

1. **Verify** by re-reading `GET /tasks/user` and confirming no open todos remain for the cleared window.

1. **Report** the count cleared and the marks found; stay silent when there is nothing to change.

## Enchanted Armoire / gold burn

Ad-hoc sink for "spend all my gold" (e.g. before a class/account reset):

- `POST /user/buy-armoire` opens the mystery chest for **100 gp flat**; there is no bulk endpoint, so burning N gold is N/100 calls.

- The response carries the drop at `data.armoire` (`type`, `dropKey`, `dropText`) — `data.items.gear` is the whole owned-gear map, not the drop.

- Response omits gp: re-read `GET /user` → `stats.gp` every ~25 opens instead of every open (halves request count).

- Once every armoire gear piece is owned the chest returns only `food` and `experience` — expected, not an error.

- Remainder below 100 gp cannot be sunk here; there is no 100-gp-divisible way to reach exactly 0 (health potions are 25 gp, so a 61 gp residue still can't be cleared). Report the residue instead of inventing a sink.

## Boundaries

- Never delete a Habitica task — score it up instead (the reward is the point).

- Never write to Habitica without an explicit instruction or a scheduled sweep; it is a second writer alongside n8n.

- Never create, edit or reorder Habitica tasks from here unless asked.

- Never print or log the key; report variable *names*, never values.

- Never move Ship rows to `Backlog` as part of a Habitica-only task — that clears `Linked?` and severs n8n's map.

## Verification

- `GET /tasks/user` shows no open todos for the cleared window.

- No secret appears in any output, file or log.

## Pitfalls

- Habitica needs **both** headers, and they must belong to the same account. `401 invalid_credentials` ("There is no account that uses those credentials") means the **user ID and API key are a bad pair** — both values are well-formed 36-char UUIDs, so a malformed-looking value is not the clue; a stale/regenerated key, or a user ID copied from anywhere other than Habitica's Site Data, is. Re-copy both.

- `400 BadRequest "Missing x-client headers"` means the `x-client` header is absent — Habitica requires it on every call alongside the two auth headers. Format is `<user-id>-<app-name>`.

- Completing a todo is `POST /tasks/{id}/score/up` — there is no PATCH that sets `completed`.

- Ship's `Linked?` holds the Habitica task id, but scoring up does not need it: direct API access is independent of the n8n link, which is why a direct clear still works after a row moves to `Backlog`.

- **Rate limit is real**: Habitica v3 answers `429 TooManyRequests` above roughly 30 requests/minute per user/IP. Any loop of writes must pace itself (≥2.6s between requests) and honour the `Retry-After` header on 429. A tight buy loop with a `GET /user` per iteration trips it within seconds.

- Use one keep-alive `http.client.HTTPSConnection` (or a `requests.Session`) for loops — a fresh TLS connection per call is slow enough to matter over hundreds of calls.

- The account is shared with the n8n mirror; scope changes narrowly and report what was touched.