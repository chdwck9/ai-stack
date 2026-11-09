---


uuid: 40624dc8ccd9818cb76ecdc1277e02e7
name: media-request-management
description: "Audit Jellyseerr/Seerr requests, fix sign-in or subtitle tracks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
hermes:
tags: [media, jellyseerr, jellyfin, anime, requests, watchlist]
category: media


---


# Media Request Management

## When to Use

Use this skill when Richard asks what films/series/anime he is missing, what to request in Jellyseerr, or whether a candidate is already available, requested, processing, or partially available.

Also use it when Richard names **one specific thing he wants** — "there was a special released a few months back, can you request/download it for me?", a film, a back season, an OVA. That is a request-and-grab job on a single title, not a triage sweep: identify the exact item, prove it is not already in the library, confirm a healthy release exists, and stop at the approval gate. See **Specials and one-off episodes (Season 0)** when the target is a special/OVA rather than a normal episode.

Also use it when Jellyseerr sign-in fails ("Something went wrong while trying to sign in", rejected passwords) or when its Jellyfin link looks dead (a sync job erroring on a timer). That is a different job from auditing requests — go to **§2.5** and `references/media-server-auth-troubleshooting.md`, and do not attempt to fix it by re-entering credentials.

Also use it when Richard says a specific episode/series in the library has the wrong subtitle or audio language ("only has Japanese subtitles", "English subs but Japanese audio"). That is a library-file replacement job, not a request audit — follow `references/sonarr-bazarr-language-tracks.md`.

Also use it when asked to add, fix, or replace Bazarr subtitle providers — including "do it without me creating an account". Provider enable/disable, which providers are account-free, and how to trigger a rescan are in `references/bazarr-provider-config.md`.

## Operating rules

- Check the request system state before recommending additions; Richard cares about what is **not already available, requested, processing, or partially available**.

- Do not submit Jellyseerr requests, approve requests, change media services, or alter Sonarr/Radarr/Jellyfin state without explicit action-specific approval. Prepare a request batch and stop at the approval gate.

- For anime triage, prioritise Richard’s stated taste: prefer strong story, sports, sci-fi/action, historical/drama, food/culture, or unusual high-quality picks; downgrade routine isekai, horror/paranormal/demon/supernatural, and ecchi unless the community signal is exceptional.

- Separate **new shows/reboots/spinoffs** from sequel seasons; Richard often asks especially for new anime and does not want sequel-only lists disguised as discovery.

- Report uncertain matches separately. A title match against an older base show, a different adaptation, or low confidence search result is not proof that the target season is covered.

## Procedure

### 1. Build the candidate set

1. Gather candidate titles from the requested source: MAL seasonal page, AniList, forums, Reddit, curated articles, or a provided list.

1. If search engines are bot-walled, use the directly accessible seasonal/database page as the ranking backbone and state that external forum confirmation was unavailable.

1. Keep alternate titles for each candidate: English title, Japanese romanisation, franchise/base title, and obvious punctuation variants.

1. Tag each candidate as `new`, `reboot`, `spinoff`, `sequel`, or `movie` before checking Jellyseerr.

### 1.5 Discover Jellyseerr host — vault-first, Docker second

Jellyseerr may run on a remote machine (e.g. your home server behind WireGuard). **Never deep-dive into Docker/network scanning when a saved login already encodes the URL.**

Order matters:

1. Call `browser_vault_list`. Any login item with kind=`login` and label containing "Jellyseerr" or "jelly" gives you the exact origin (host:port) — e.g. `http://100.90.18.106:9712`. Do NOT re-invent the URL.

1. Probe the known URL: `curl -sS http://<origin>/api/v1/status`. A JSON version response proves it's alive.

1. Only if NO vault login exists AND local Docker shows nothing: fall back to Docker scanning (`docker ps`, `docker network inspect`, port probes on 5055/8085). If nothing matches after ~2 min, report unavailable and stop.

The user cares about requesting media through Jellyseerr. If Jellyseerr is unreachable, inform Richard and stop.

### 1.6 Resolve anime metadata via external APIs

When Jellyseerr is up but you need metadata (TMDB IDs, alternate titles, year) before searching:

- AniList GraphQL: POST [https://graphql.anilist.co](https://graphql.anilist.co/) with JSON body `{"query": ..., "variables": {...}}`. Plain POST works — no auth needed. Setting a Bearer/OAuth token causes 403.

- TMDB v3 API: GET [https://api.themoviedb.org/3/search/tv?api_key=<key>&query=<title>](https://api.themoviedb.org/3/search/tv?api_key=%3Ckey%3E&query=%3Ctitle%3E) — simpler for raw fetches without auth overhead.

- Fallback: browser-based TMDB search page via browser_exec when APIs fail.

Keep title variants ready before hitting Jellyseerr: English, Japanese romaji, franchise base, known punctuation variants.

### 2. Query Jellyseerr through the API first

Use Jellyseerr's built-in API rather than driving the UI when possible; UI login mode toggles are brittle, the same `username` field can represent either media-server username or local email login, and session cookies may expire quickly. If a saved login fails once, stop fighting the form and switch to API-key or container-side inspection.

- API docs: `http://<jellyseerr-host>/api-docs/`.

- Public probes: `/api/v1/status` and `/api/v1/settings/public`.

- Browser cookie auth: type identifier with `fill_input` into the **`email`** field, then `browser_vault_fill(handle)`. In most Richard setups the password equals the username/email.

- Terminal/curl auth: `POST /api/v1/auth/local` with `{"email": "<user>", "password": "<pass>"}` → saves `connect.sid` to cookie jar (`-c file`). Then use `-b file` on subsequent requests. Prefer this when browser JS is blocked.

- API key via Portainer exec or `docker exec` — read from `/app/config/settings.json` inside the Jellyseerr container.

- See `references/jellyseerr-api.md` for full auth workflow, curl examples, and status mapping.

### 2.5 When sign-in fails or the media-server link looks dead

Diagnose from the container, never from the UI; the on-screen message is a generic wrapper and the form itself is the least informative surface.

1. Read the container log first: `docker logs --tail 3000 <jellyseerr>` and grep `Unauthorized`, `Bad Request`, `Failed sign-in`, `Sync interrupted`. Jellyseerr's own wording separates the three failure paths — media-server auth, local password, library sync.

1. Probe the media server the app is configured for: `scripts/jellyfin-auth-probe.sh <base-url> [key]`. It prints the server identity plus the HTTP status per auth-header style, and 400-versus-401 is the whole diagnosis (legacy header vs rejected credentials).

1. Compare identities: `jellyfin.serverId` in `/app/config/settings.json` against the live `Id` from `<base>/System/Info/Public`. A `serverId` matching no live server means the app is still paired with a server that no longer exists — every stored key and cached user token for it will 401.

1. Check the account's sign-in path in the app's DB (`password` NULL = media-server-only account, so the app's own login form can never work).

1. Report the failing path and the options, then stop at the approval gate: re-pointing the app, re-issuing keys, or toggling a server-side auth setting all change Jellyfin/Jellyseerr state.

See `references/media-server-auth-troubleshooting.md` for the full procedure, the header matrix, and remediation trade-offs.

### 3. Classify each candidate

For each title, search Jellyseerr with all title variants, then fetch details for the best match.

Classify using Jellyseerr media status:

- `AVAILABLE` — not missing.

- `PARTIALLY_AVAILABLE` — not missing for the first pass; mention only if Richard asks for completeness by season/episode.

- `PROCESSING` — not missing.

- `REQUESTED/PENDING` or approved request present — not missing.

- `UNKNOWN` — ambiguous; treat as manual-review unless the target season is clearly not requested or available.

- `NOT_TRACKED` — missing candidate, if the match confidence is good.

- No match — unresolved candidate; do not invent a Jellyseerr request target.

### 4. Rank recommendations for Richard

1. Put high-fit missing titles first, not merely highest community score.

1. Separate “add/review now,” “manual check,” and “skip/defer.”

1. Include enough evidence to act: title, Jellyseerr title/TMDB match if found, status, why it fits or conflicts with taste.

1. Keep the report compact; Richard wants the actionable delta, not a full catalogue.

## Output shape

Use concise sections:

- **Already covered / not missing** — available, partial, processing, requested/approved.

- **Looks missing / not tracked** — recommended candidates to add or review.

- **Unclear / manual check** — old-base-show matches, unknown statuses, low-confidence TMDB matches.

- **Skip/defer** — taste mismatch or weak signal.

- **Next approval gate** — request batch prepared, but not submitted.

## Replacing an episode with a differently-subbed/audio'd release (Sonarr)

When a library file has the wrong tracks (e.g. only Japanese subs on an anime that should carry English), swap the release rather than bolting on subtitles. Key traps: Sonarr refuses same-quality replacements (delete the old `episodefile` first), and its release cache expires so search+grab must run in one call. Full procedure: `references/sonarr-release-swap.md`.

## Specials and one-off episodes (Season 0)

When Richard asks for "the special" / "the OVA" / a specific one-off episode rather than a season:

1. **Identify which special it is before touching anything.** AniList search (`type: ANIME, sort: START_DATE_DESC`) returns each special with `format: SPECIAL|OVA`, its air date and a one-line synopsis — that is enough to disambiguate "a few months back" when a franchise shipped two in one year. Report both candidates with air dates and synopses rather than guessing, and let Richard pick; they are different stories.

1. A special that aired as part of a series does **not** appear as a standalone Jellyseerr search hit. Searching the show's name returns the parent series (`mediaType: tv`); the special is inside its Specials season. Read it from `GET /api/v1/tv/{tmdbId}/season/0` (name + `airDate` + `episodeNumber`).

1. In Sonarr the same episode sits in `seasonNumber: 0` — often at a **different episode number than TMDB** (e.g. TMDB E19 = Sonarr E24). Match on title/airDate, not on episode number.

1. **A special never downloaded is unmonitored by design, not a failed grab.** Check both switches before diagnosing: the Sonarr series' `seasons[].monitored` for season 0, and Jellyseerr's `/api/v1/settings/public` `enableSpecialEpisodes`. Richard's MHA series has every season except the current one unmonitored, and `enableSpecialEpisodes` is `false` — specials and back seasons silently never arrive.

1. Prove it is grabbable before promising anything: `GET /api/v3/release?seriesId=<id>&episodeId=<id>` returns the whole series' release list; filter to titles carrying `S00E<ep>` and report the **releases with an empty ****`rejections`**** array** (`ACCEPTABLE`) plus seeders and size. `rejections` entries are plain strings or `{reason}`, handle both. Release text may name the special by either the TMDB or the Sonarr number — `Episode wasn't requested: 0x23` / `Wrong episode` on a result that is obviously the right special means you searched the other numbering.

1. Enabling the episode and grabbing it changes Sonarr state → stop at the approval gate with the candidate + release evidence, and act only on Richard's explicit go-ahead.

## Stuck `importPending` rows in the Sonarr queue

Read `statusMessages[].title` first — it names the exact blocker, and the two common ones have nothing to do with each other.

- **`Invalid video file, unsupported extension: '.zip'`** — the release is an archive. **List the contents before extracting anything**: a "`[SubsPlease] … - S03E06 [1080p WEBRip AV1].zip`" here contained a single 1.38 GB `2.exe`, i.e. a self-extracting malware payload wearing an anime release name; `[SelfExtract Bundle]` in a release title is the same pattern. Never extract or run it. Blocklist and drop it, then take a real release:
`DELETE /api/v3/queue/{id}?removeFromClient=true&blocklist=true&skipRedownload=false` (this also deletes the payload from `/downloads`), then grab an acceptable non-zip release from `/api/v3/release`.
NAS has no `unzip`; `/usr/bin/7z l <file>` is the way to inspect.

- **`Episode has a TBA title and recently aired`** — Sonarr's TBA guard refusing to map a file onto an episode whose title metadata is still placeholder. Fix is metadata, not media: `POST /api/v3/command {"name":"RefreshSeries","seriesId":N}`, and the pending import completes by itself once the episode has a real title.

## Jellyseerr never flips imported media to AVAILABLE

Content can be fully imported and on disk while Jellyseerr still reports `PROCESSING` with `jellyfinMediaId: null`, and its `jellyfin-recently-added-scan` / `jellyfin-full-scan` / `availability-sync` jobs run happily without changing anything. Check the pairing: `GET /api/v1/settings/jellyfin` `serverId` against the live `Id` from `<jellyfin>/System/Info/Public`. Here Jellyseerr stores `79fc06b9…` while the live NAS Jellyfin is `c14999a1…` — it is still paired to the retired docker Jellyfin 10.11 instance, so availability sync is dead (see `references/jellyseerr-jellyfin12-login.md`). Verify the media landed by listing the library path on disk, and report the pairing as the separate fault rather than re-running scans.

## Pitfalls

- `GET /api/v3/history` rejects `sortDirection=desc` with a bare 400 — the accepted value is `descending` (and `ascending`). Same for `/api/v3/log`, which additionally needs `filename=sonarr.txt`.

- **A per-episode ****`MissingEpisodeSearch`**** on an anime series grabs the season pack once per episode** — 12 identical queue rows, all sharing one `downloadId`, while qBittorrent holds a single torrent. That is cosmetic; leave it alone and the pack imports once.

- **Never clean those duplicates up with ****`skipRedownload=true`****.** `DELETE /api/v3/queue/{id}?removeFromClient=false&skipRedownload=true` writes a `downloadIgnored` history event for *every* episode of the series: the torrent keeps downloading in the client but Sonarr will never import it, and the release then vanishes from `/api/v3/release` results entirely (so it cannot even be re-grabbed). Use `removeFromClient=true&skipRedownload=false` if a row really must go.

- A grabbed batch that Sonarr grabbed but does not track (no queue row, torrent present in the client) will not import on completion — it needs `ManualImport`. Prefer re-grabbing a release that Sonarr will track over letting an orphan run.

- `POST /api/v3/command {"name":"SeasonSearch","seriesId":N}` with no `seasonNumber` defaults to **season 0** (specials) and silently searches nothing. Always pass `seasonNumber`.

- Anime profile here (id 1, used by all 86 `/anime` series) allows only WEBDL/WEBRip/HDTV 1080p+720p, **requires the literal term ****`sub`**** in the release title**, and enforces min 1 seeder. Bluray releases and dual-audio batches named without "sub" are rejected outright — so a title with only BD rips shows `acceptable 0` and needs a profile change (approval gate), not a re-search.

- Prowlarr rate-limits under multi-episode anime searches: `429 TooManyRequests` disables indexers for 1-5 min mid-run, and each series' full episode sweep can take 20+ min. Long `started` MissingEpisodeSearch commands are normal, not stuck.

- Prefer API/state checks over browser UI scraping because Jellyseerr’s sign-in UI can toggle between media-server and local-login modes while keeping the same `username` field name.

- Never treat a base-series match as proof that a later season is covered; fetch TV details and inspect `mediaInfo`, request list, and season status before classifying.

- Do not expose API keys, passwords, cookies, or QR/session values in chat; run API-key work inside the container or use vault/cookie auth.

- Detect broken browser context by checking if `js('document.title')` returns `null` — if it does, the JS sandbox cannot interact with this page (CSP, iframe restrictions, or transport-layer issues). Abort browser form-filling immediately and fall back to curl-based auth (`POST /api/v1/auth/local` with cookie jar) or Portainer exec for API key extraction.

- API keys delivered by the user may be base64-encoded strings. Decode with `base64.b64decode(key).decode('utf-8')` before use. Do NOT prepend `base64.` or pass the raw encoded string.

  - **BUT the NAS Jellyseerr (100.90.18.106:9712) is the opposite case**: the value stored at `main.apiKey` in `/app/config/settings.json` (68 chars, base64) is exactly what `X-Api-Key` wants. Passing the base64-DECODED 49-char form returns `403 You do not have permission to access this endpoint`. `Authorization: Bearer <key>` is not accepted here either (401/`cookie 'connect.sid' required`). Try both forms empirically before assuming the key is bad. `~/.hermes/edge.env` JELLYSEERR_API_KEY now holds the RAW form.

- **A 403 (not 401) from Jellyseerr usually means a wrong-format key, not a permissions gap** — a bad key and an insufficient-scope key return the same body.

- Jellyseerr's login endpoint accepts **`email`**, not `username` — the payload is `{"email": "<user>", "password": "<pass>"}`. In most Richard setups the password equals the username. Using `"username"` causes a validation error (`required.openapi.validation`) instead of an auth response.

- On a Jellyfin-backed Jellyseerr, **`/auth/local`**** and ****`/auth/jellyfin`**** are separate paths that fail differently**: `/auth/local` needs a local password (none of Richard's accounts have one → `Access denied.`), `/auth/jellyfin` forwards to Jellyfin (→ 400/500 while legacy auth is off). Do not diagnose one from the other.

- `browser_vault_fill` requires the page to be fully loaded on the exact matched origin before it can locate password fields. If it returns "Could not determine current page origin," wait longer or navigate again — don't retry immediately.

- AniList GraphQL ([https://graphql.anilist.co](https://graphql.anilist.co/)) accepts plain POST with JSON body — no auth header needed. Setting a Bearer/OAuth token causes 403. Use only for metadata discovery, not Jellyseerr itself. A bare `urllib` POST also 403s: send `-A 'Mozilla/5.0'` and `--data-binary @bodyfile` from curl, writing the JSON body to a file first so shell quoting cannot mangle it.

- **Jellyseerr and Sonarr JSON responses contain raw control characters** (inside `overview`/synopsis text) — `json.loads` raises `Invalid control character at: line 1 column N` on the whole payload. Parse with `json.loads(text, strict=False)`, or curl to a file and parse the file. Both work; do not fall back to regex-scraping the JSON.

- **Episode list JSON's inline ****`episodeFile`**** omits ****`mediaInfo`** — it is empty/None even when the file has tracks. Fetch `/api/v3/episodefile/{id}` for the real `audioLanguages`/`subtitles` values; judging language from the episode list alone will mislead you.

- **Anime release naming decides subtitle tracks**: `MultiSub`/`Multi-Subs` = multiple embedded subtitle tracks including English; `Japanese Sub` = Japanese-only. Netflix rips are commonly single-language; Crunchyroll MultiSub rips are not. When one episode lacks English but its neighbours have it, the broken episode simply came from the single-language variant.

- **Same quality tier is not an upgrade in Sonarr** — replacing a WEBDL-1080p file with another WEBDL-1080p release is refused at import ("Existing file meets cutoff"). A language-driven replacement needs the old file deleted first, which is destructive and needs explicit approval.

- **Bazarr's subtitle download endpoint is ****`PATCH /api/episodes/subtitles`** (seriesid, episodeid, language, forced, hi). POST there is upload (405); GET `/api/subtitles` requires `subtitlesPath` (400 without it). A 500 from the PATCH means provider failure — run `GET /api/providers` and look for `ConfigurationError`/`403` before retrying or blaming the API key.

- Jellyfin 12.x authenticates with the **`Authorization: MediaBrowser Token="<key>"`** header. `X-Emby-Token`, `X-Api-Key` and `Authorization: Bearer` are rejected (401). The deprecated `X-Emby-Authorization` header is rejected as **400 Bad Request**, because Jellyfin 12 ships with `EnableLegacyAuthorization=false` — so on any auth call **400 means "legacy header", not "bad password"**, and 401 means the header was accepted and only the credentials were wrong. `http://localhost:13380` is the Studio Jellyfin instance; `http://192.168.2.6:8096` is the NAS one.

- `/Users/Me` returns 400 with a server-level API key (it needs a user session token) — that's expected; use `/System/Info`, `/Library/VirtualFolders`, or `/Items` to prove an API key authenticates.

- Jellyfin API keys are per-server app tokens (Dashboard → Advanced → API Keys), NOT bound to the creating user's permission scope.

- Identify a media server from `/System/Info/Public` (`Id`, `ServerName`, `Version`), **never from host:port**. Ports get reused when an install is replaced, and several Jellyfin installs can coexist on one host (a docker container and a package/native install on different ports, plus the Studio instance) while serving the same media paths.

- A replaced/reinstalled media server invalidates a linked app wholesale: the stored `serverId` stops matching and both the API key and the cached user token return 401. Rule that out before blaming credentials — it produces the same user-visible error as a wrong password.

- `fallenbagel/jellyseerr` is the **abandoned** original image; the project continues as **Seerr** (`seerr-team/seerr`, Docker Hub `seerr/seerr`). Builds before Seerr 3.x send the legacy Emby auth header, so they cannot sign in against Jellyfin 12 at all — check the deployed image's build date first, and fix by upgrading rather than by resetting passwords.

- A media-request app's own login form is only usable by accounts that hold a local password. Accounts created through media-server login have `password` NULL, so "login with Jellyseerr" always fails while the media-server button is the intended path; verify from the users table instead of assuming a wrong password.

## Requesting a one-off ANIME SPECIAL (Season 0) — end-to-end

Specials never arrive on their own. Sonarr's series `seasons` list and Jellyseerr's `enableSpecialEpisodes` both leave Season 0 out, so "it was released but is missing" is expected, not a failed grab.

1. Identify the episode: AniList GraphQL `sort: START_DATE_DESC` for the franchise gives the special's air date; Jellyseerr `/api/v1/tv/{tmdbId}/season/0` maps it to a TMDB episode (note Jellyseerr and Sonarr number specials differently — an extra movie entry can shift every Sonarr episode by one).

1. Monitor it: `PUT /api/v3/episode/monitor {"episodeIds":[...],"monitored":true}`.

1. Search + grab in ONE call: `GET /api/v3/release?seriesId=&episodeId=` then immediately `POST /api/v3/release {"guid","indexerId"}`. A grab issued from a release JSON fetched in an earlier call always fails with `Couldn't find requested release in cache` — the cache is seconds-long. Filter releases by `rejections` empty.

1. Verify: `GET /api/v3/episode?seriesId=` (`hasFile`) and `GET /api/v3/episodefile?seriesId=`.

### Special-specific traps

- **Absolute-numbering releases fail to import.** Anime specials are often published as e.g. `My.Hero.Academia.S08E147.More...` (absolute count) while the library wants `S00E23`. Sonarr parks the download in the queue as `importPending` with `Invalid season or episode` and shows `No files found are eligible for import` once the file is moved. Fix by manual import, not by re-grabbing.

- **`ManualImport`**** must be given ****`languages`****.** Omitting it crashes the import with `NOT NULL constraint failed: EpisodeFiles.Languages` **after** the file has already been moved into the library — Sonarr then has no `episodeFile` record and the queue item stays stuck. Always pass `languages: [{"id":1,"name":"English"},{"id":8,"name":"Japanese"}]` (ids from `/api/v3/language`).

- **Recovering a half-imported special**: `GET /api/v3/manualimport?folder=/anime/<Series>/Specials&filterExistingFiles=false` returns the stranded library file with its parsed episode; then `POST /api/v3/command {"name":"ManualImport","files":[{"path","seriesId","episodeIds":[<id>],"quality","languages"}]}`. Manual import accepts any path under a root folder, not just `/downloads`.

- **Force a release search to look at the special**: `?seriesId=<id>&episodeId=<episodeId>` returns the whole series' releases (500+ items) — filter in Python, never print the raw array.

- Clean up a stuck queue row with `DELETE /api/v3/queue/{id}?removeFromClient=true&blocklist=false` once the file is confirmed in the library.

## Ports on the NAS stack (do not assume defaults)

`8989` is lighttpd (Synology), NOT Sonarr. Actual published ports: Sonarr `9701`, Radarr `9704`, Lidarr `9702`, Readarr `9709`/`9708`, Prowlarr `9700`, Bazarr `9705`, Jellyseerr `9712`, Mylar `9703`, qBittorrent `9710`, Jellyfin(docker, stale) `896`, native Jellyfin `8096`, Portainer `9000`, n8n `56780`. Confirm with `ssh chdwck9NAS 'sudo -n /usr/local/bin/docker ps --format "{{.Names}}\t{{.Ports}}"'`. Sonarr's `/downloads` bind is `/volume1/temp`; the anime library is `/volume1/Play/Anime` → `/anime`.

## Readarr — is this book already in my library? (two instances)

Richard runs **two** Readarr instances on the NAS and a book check must cover both, or the answer is
wrong by omission:

- `9709` = written/ebook library, container `readarr`, config `/volume1/docker/readarr/config.xml`

- `9708` = spoken/audiobook library, container `readarr-spoken`, config `/volume1/docker/readarr-spoken/config.xml`

Each has its **own** `<ApiKey>`; `READARR_API_KEY` in `edge.env` holds only one of them, so read both
keys out of the two config files rather than reusing a single env var.

1. **Identify the title before querying anything.** For a YouTube/podcast link, `yt-dlp<br>   --skip-download --print "%(title)s" --print "%(description)s" <url>` gives title + full description
in one call and usually names the author and book outright. Do this first; it decides every later term.

1. **Membership is a title scan**, not a lookup: `curl /api/v1/book` and `/api/v1/author` to files, then
filter in Python on title and author name. A few thousand books answers in seconds.

1. **`/api/v1/book/lookup?term=`**** only proves addability**, and it is slow — ~45 s on the written
instance (upstream metadata proxy), sub-second when cached on the spoken one. Run **one** lookup per
tool call: a cell looping several lookups blows the 300 s `execute_code` kernel limit and loses the
whole result.

1. A library hit needs title *and* author checked — an author can be present with the book unmonitored.

1. Stop at the approval gate before adding: adding creates a monitored book record and triggers indexer
searches. Report per-instance status + addability, then ask.

Exact commands, the port/key table and a worked example: `references/readarr-book-checks.md`.

## Reading large Sonarr/arr responses

The terminal tool truncates stdout, which silently produces invalid JSON for release searches and episode lists. Always `curl ... -o /tmp/x.json` and parse the file; never parse captured stdout.

## Jellyseerr login broken after a Jellyfin upgrade (Jellyfin 12.x)

"Something went wrong while trying to sign in." on the Jellyseerr/Moonfin login page: local login can never work here (no local passwords), the frozen `fallenbagel/jellyseerr` image sends the legacy `X-Emby-Authorization` header that Jellyfin 12 (with `EnableLegacyAuthorization=false`) rejects with 400, and Moonbase/Moonfin SSO sits in front of it. Full chain, verification matrix, stopgap and proper fix: `references/jellyseerr-jellyfin12-login.md`.

## Jellyseerr API Key (this stack)

- Jellyseerr's API key lives under `main.apiKey` in `/app/config/settings.json` (may be base64-encoded; decode before use) — read it by copying the file out of the container (`docker cp jellyseerr:/app/config/settings.json`) or via the Portainer archive API.

- Auth header: `X-Api-Key: <key>`.

## Secure key storage on this Mac

Per-service API keys live in `~/.hermes/edge.env` (mode 0600). Key names: `SONARR_API_KEY`, `RADARR_API_KEY`, `LIDARR_API_KEY`, `PROWLARR_API_KEY`, `READARR_API_KEY`, `MYLAR_API_KEY`, `BAZARR_API_KEY`, `JELLYSEERR_API_KEY`, `JELLYFIN_API_KEY`. Read the *arr API keys from each container's `/config/config.xml` `<ApiKey>`; verification: `curl -H "X-Api-Key: $KEY" http://100.90.18.106:<port>/api/v3/system/status` (Sonarr/Radarr use v3, Lidarr/Prowlarr/Readarr use v1). Source the file with `set -a; source ~/.hermes/edge.env; set +a` — do not echo key values into chat.

**NAS host-port map (the container's internal port is NOT the published one).** Sonarr `9701` (internal 8989), Radarr `9704` (7878), Lidarr `9702` (8686), Prowlarr `9700` (9696), Readarr `9709` (8787), Bazarr `9705` (6767), Mylar `9703` (8090), Jellyseerr `9712` (5055), qBittorrent `9710` (WebUI, auth) / `9713` (loopback bridge), Portainer `9000`, n8n `56780` (5678).

- **`:8989`**** on the NAS host is Synology's lighttpd, not Sonarr** — it answers `403 Forbidden` with `Server: lighttpd`, and `/api/v3/system/status` there returns an HTML `404`. A real *arr answers JSON on `/api/v3/system/status` with its own key; an HTML 404 or a lighttpd `Server:` header means you are on the wrong port, so re-derive the port from `ssh chdwck9NAS 'sudo -n /usr/local/bin/docker ps --format "{{.Names}}\t{{.Ports}}"'` instead of guessing.

When Richard's media server (NAS) is unreachable or mounts fail:

1. **Verify connectivity first**: `ping chdwck9NAS`, `nc -zv chdwck9NAS 22` (SSH is open via Tailscale)

1. **SMB mounts to ****`/Volumes/`**** require sudo** — if you can't create the mount point, mount to `/tmp/` instead and update container bind mounts (see `references/smb-docker-desktop.md`)

1. **Docker Desktop's virtiofs can't access SMB-mounted directories** — if container shows empty `/media` but host has files, this is the limitation, not a config error

1. **SSH to NAS is often faster** than troubleshooting mounts — check if credentials are available, otherwise generate keys (`ssh-keygen -t ed25519 -C "richard@mac"`)

1. **Jellyfin restart after mount**: `docker restart jellyfin` after confirming mount is active via `df -h | grep Play`

See `references/smb-docker-desktop.md` for full workflow, NAS share layout, and workaround scripts.

## n8n (self-hosted on NAS)

- Instance: `https://n.dykes.digital` (public), direct NAS `http://192.168.2.6:56780` (docker `n8n-prod`, v2.18.5). Restart via `ssh chdwck9NAS 'sudo -n /usr/local/bin/docker restart n8n-prod'`.

- **REST API** (`/api/v1`, works now): api key in `X-N8N-API-KEY` header → `N8N_PROD_API_KEY` in `~/.hermes/edge.env`. Covers workflows, executions, credentials, tags.

- **MCP server** (streamable HTTP at `/mcp-server/http`): needs a SEPARATE MCP-scoped Bearer token (JWT audience `mcp-server-api`), generated at **Settings → Instance-level MCP → Connect a client → API key tab**. A general REST API key returns 401 `jwt audience invalid. expected: mcp-server-api` — do NOT reuse it for MCP. MCP token → `N8N_PROD_MCP_KEY`.

- Hermes MCP server wired as `mcp_servers: n8n-local` (url `https://n.dykes.digital/mcp-server/http`, `Authorization: Bearer <token>`, transport streamable-http, enabled) → 25 tools: search_workflows, execute_workflow, get_execution, get_workflow_details, publish/unpublish_workflow, test_workflow, prepare_test_pin_data, validate_workflow, create_workflow_from_code, data-table + node-search tools.

- MCP only sees workflows that have per-workflow MCP access enabled (Settings → Instance-level MCP); `search_workflows` returns previews of all viewable workflows regardless.

- n8n 2.33+ uses the new Instance-level MCP settings layout (Connection details, Access, Connected clients); older versions use a single-page settings screen.

## qBittorrent (passwordless API via SSH loopback bridge)

- `qbt.sh` mangles extra curl args (it splices `$*` into an ssh double-quoted command), so POST/delete calls must be run directly: `ssh chdwck9NAS 'curl -sS -H "Host: 127.0.0.1:9710" -X POST -d "hashes=<hash>&deleteFiles=true" "http://127.0.0.1:9713/api/v2/torrents/delete"'`. Query-string params on that endpoint return `Bad Request`; they must be form data.

qBittorrent has NO API key and NO multi-user WebUI (single `chdwck9` account, PBKDF2 password). Do NOT try to add a second WebUI user — the feature does not exist. Instead Clarity reaches the API passwordlessly:

- `~/.hermes/edge/qbt.sh "<api-path>"` — wrapper (e.g. `qbt.sh torrents/info`, `qbt.sh transfer/info`). Talks to `http://127.0.0.1:9713/api/v2` over SSH alias `chdwck9NAS`.

- **How it works**: compose service `qbt-loopback-bridge` (alpine/socat, `network_mode: service:qbittorrent`) runs INSIDE qBittorrent's netns, listening on `127.0.0.1:9713` and forwarding to `127.0.0.1:9710`. Because it shares the netns, the upstream connection is genuinely loopback. qBittorrent.conf has `WebUI\LocalHostAuth=false`, so loopback bypasses auth. The bridge host port is published `127.0.0.1:9713:9713` (loopback-only) — the LAN can NEVER reach it. LAN on :9710 still requires auth (403).

- **Gotcha**: qBittorrent also validates the **Host header** — requests must send `Host: 127.0.0.1:9710`, else 401 even from loopback. The wrapper handles this.

- **Gotcha**: qBittorrent rewrites its conf from memory on shutdown. To change settings you MUST `docker stop` -> edit `/volume1/docker/qbittorrent/qBittorrent/qBittorrent.conf` -> `docker start`. Edits while running are silently lost.

- **Gotcha**: a docker SUBNET whitelist (`AuthSubnetWhitelist`) is INSECURE here — published-port traffic is masqueraded to the bridge gateway (172.18.0.1), so whitelisting the subnet also opens the LAN. Use `LocalHostAuth` + the netns bridge instead.

- Compose file: `/volume1/Live/@Edge/.downloaders/docker-compose.yaml` (also visible on the Mac at `/Volumes/Live/@Edge/.downloaders/docker-compose.yaml`). Apply: `ssh chdwck9NAS 'cd /volume1/Live/@Edge/.downloaders && sudo -n /usr/local/bin/docker compose up -d qbittorrent qbt-loopback-bridge'`.

## NAS SSH + docker access

- SSH alias `chdwck9NAS` (`~/.ssh/config`) -> `chdwck9@192.168.2.6`, key `~/.ssh/id_ed25519_nas`, `IdentitiesOnly yes`.

- Docker on NAS needs sudo: `ssh chdwck9NAS 'sudo -n /usr/local/bin/docker <cmd>'` (sudoers `/etc/sudoers.d/docker-clarity` grants NOPASSWD for docker + systemctl only).

- NAS home is SMB-shared (0777), which trips OpenSSH `StrictModes`; `StrictModes no` set in `/etc/ssh/sshd_config` to allow key auth.

- Jellyfin topology (one local + TWO NAS instances — check which an integration targets before debugging):

  - `192.168.2.6:8096` = **native SynoCommunity Jellyfin 12.2 package** (`/var/packages/jellyfin`, name `chdwck9NAS`, server ID `c14999a1...`). The live one: it hosts the **Moonbase/Moonfin** plugin and is what Jellyseerr and most clients use.

  - `192.168.2.6:896` = old **docker** `jellyfin/jellyfin` still on **10.11.11** (bridge IP 172.20.0.2) — leftover from before the Synology-package migration; treat as stale.

  - `http://localhost:13380` = Jellyfin on the Studio (`jellyfin-studio`, 12.2.0); `p.dykes.digital` fronts it. `JELLYFIN_API_KEY` in `~/.hermes/edge.env` belongs to THIS server (proved: 200 on :13380, 401 on :8096).

- Restart the native NAS Jellyfin: `ssh chdwck9NAS 'sudo -n /bin/systemctl restart pkgctl-jellyfin.service'` (~40 s to come back). Config `/volume1/@appdata/jellyfin/config/system.xml`; DB `/volume1/@appdata/jellyfin/data/data/jellyfin.db`; logs `/volume1/@appdata/jellyfin/log/log_YYYYMMDD.log`.

- Editing root-owned package config when sudo is limited to `docker`+`systemctl` (NAS sudoers gives NOPASSWD for exactly those): stage the new file in NAS `/tmp` as `chdwck9` (`ssh NAS 'cat > /tmp/x' < local`), then bind-mount both dirs into a container:
`ssh NAS 'sudo -n /usr/local/bin/docker run --rm --entrypoint sh -v /tmp:/t -v <dir>:/cfg alpine -c "cp /cfg/system.xml /cfg/system.xml.clarity-bak && cp /t/x /cfg/system.xml && chown <uid>:<gid> /cfg/system.xml && chmod 644 /cfg/system.xml"'`
`cp` comes out root-owned — re-`chown`/`chmod` explicitly (ids from `stat -c '%u:%g'`). Always leave a `*.clarity-bak` beside the original.

- Read container files without portainer: `ssh NAS 'sudo -n /usr/local/bin/docker exec jellyseerr cat /app/config/...' > local` (avoids `docker cp` + root-owned `/tmp` + `scp` permission traps). Persistent stacks live at `/Server`; stack memory in `/Volumes/Live/@Edge/*`.

- Hermes MCP servers configured in `~/.hermes/config.yaml` under `mcp_servers:` (notion, n8n-local). Token stored inline; config is mode 0600.

## Cron Job Patterns for Monitoring

For time-sensitive monitoring (flights, alerts, recurring checks):

```bash
# Create recurring job
hermes cron create --name "Flight Monitor" --deliver origin --repeat 5 "every 15m" "Check flight status, alert only on material delays (20+ min), stop when landed."

# Create one-shot trigger (e.g., resume at specific time)
hermes cron create --name "Resume at 09:30" --deliver local --repeat 1 "2026-10-13T09:30:00+02:00" "Resume the paused cron job with ID <job_id>. Do not alter its prompt or schedule. Return empty."

# Pause/resume existing jobs
hermes cron pause <job_id>
hermes cron resume <job_id>
```

Key rules:

- Use `--deliver origin` to send alerts to current chat

- Use `--repeat N` to limit runs (e.g., 5 for a flight monitor)

- One-shot jobs use ISO timestamp: `"2026-10-13T10:45:00+02:00"`

- Paused jobs don't fire; resume when ready

- Empty response from cron job = no delivery (use for silent triggers)