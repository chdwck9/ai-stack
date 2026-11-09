---


name: dagu-pipelines
uuid: 40524dc8ccd981b495efda35aba34550
version: 4
description: "Dagu Pipelines"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
author: Clarity
license: proprietary
metadata:
hermes:
tags: [dagu, automation, scheduling, webhook, alerts, n8n]
related_skills: [monday, hermes-services]


---


# dagu pipelines and alert webhooks

Move deterministic work off the LLM: schedule plain scripts in **dagu**, and deliver alerts through a
**Hermes webhook route**. Verified on dagu 2.22.0 / Hermes on macOS (Studio host).

## When to Use

- A recurring job is mostly mechanical (API calls, SQL, file writes) and keeps dying on a local model.

- You need a scheduled pipeline with per-step retries and visible run history.

- You need a chat alert that costs zero tokens and fires from a script.

## dagu DAG authoring (v2.22)

Author under `~/.config/dagu/dags/<name>.yaml`. **Always validate before trusting a DAG:**

```bash
dagu dry <name>          # simulate: catches schema errors AND shows the step tree
dagu schema dag          # root fields
dagu schema dag steps    # step fields (JSON schema)
dagu example 4           # working example of retries/continue_on
```

Gotchas that cost real time:

- **Step field name is version-dependent — check, don't assume.** dagu **2.16** uses `id:` + `run:`
(see the shipped `example-0N-*.yaml` in `~/.config/dagu/dags`); dagu **2.22** uses `name:` and
`command:`. Read an existing example DAG on the host before authoring, or the DAG validates but
silently does nothing.

- **Steps use ****`name:`**** (2.22) / ****`id:`**** (2.16)** for the human label, and `depends: [other-name]`. If you
do use `id:`, it must match `^[a-zA-Z][a-zA-Z0-9_]*$` — hyphens are rejected.

- **There is no ****`timezone:`**** key** — the scheduler uses host local time. Do not add one.

- **`run_condition`**** does not exist.** To always run a final step, use a DAG-level lifecycle hook:
`handler_on: { exit: { run: ... } }` (also `init`, `success`, `failure`).

- **Step failure aborts the DAG by default.** `continue_on: failed` lets it proceed; set it under
`defaults:` to apply broadly.

- **Retries:** `retry_policy: { limit: N, interval_sec: S }`, settable under `defaults:`.

- **`catchup_window`**** is inherited from ****`base.yaml`**** (6h default)**, so a restarted scheduler replays
missed ticks. Where a late run is *wrong* (a weekly reset firing hours late), set
`catchup_window: ""` in the DAG to disable it.

- Use `group:` and `labels:` for the UI; `max_active_runs: 1` to prevent overlap.

Paths: DAGs `~/.config/dagu/dags`; runs/logs `~/Library/Application Support/dagu/`; `dagu config`
prints them all.

### Running it durably

`dagu scheduler` only runs while the process lives. Install a LaunchAgent
(`~/Library/LaunchAgents/com.dykes.dagu-scheduler.plist`, `RunAtLoad` + `KeepAlive`, absolute
`/opt/homebrew/bin/dagu`) and `launchctl load -w <plist>` — that works from a supervised session where
`bootstrap` may be refused. Verify with `launchctl list | grep dagu` and `dagu ps`.

**Do not kill the scheduler mid-run** — it orphans in-flight runs that sit `running` and block
`max_active_runs: 1`.

## NAS share fallback: scheduled copy instead of a sync client

When a vendor sync client (Synology Drive) is unreliable, replace it with two scheduled DAGs over an
**SMB-mounted share** — a morning pull (share -> local) and an evening push (local -> share). A direct
mount is *more* live than a sync engine: always current, no queue, and structurally unable to wedge a
filesystem. Reference implementation: `workbox:~/bin/fallback-sync.py`.

Hard-won rules for the copy engine:

- **`os.walk`**** silently swallows directory-read errors** (`onerror=None`). A mid-walk SMB hiccup then
truncates the entire sync with *no* error anywhere — files simply never appear. Always pass an
`onerror` handler that records and fails the run. This one bug hid a 769-file shortfall.

- **Skip regenerable trees**: `.venv`, `node_modules`, `__pycache__`, `.mypy_cache`, `.pytest_cache`,
plus `@eaDir`, `#recycle`, `.DS_Store`. These are the estate's documented stall cause and they are
also most of the volume (a 45 MB / 1,323-file `.venv` sat inside the shared agent brain).

- **Retry every copy** (4 attempts, linear backoff). SMB throws transient `ENOENT` / `EIO` under bulk
load; retries took a 1,246-failure reconcile to zero.

- **Adds and updates only — never delete.** Skip when destination size+mtime already match, and skip
when the destination is *newer*. Report overwrites; never `--delete`.

- **LAN-gate and mount-gate**: probe `socket.connect((nas, 445))` with a 3s timeout, then confirm with
`os.path.ismount()`. No-op and exit 0 when either fails, so roaming never marks the DAG failed.

- **A morning DAG wants ****`catchup_window: "24h"`** so a machine asleep or off at the tick still runs it
when dagu next starts. Leave the default 6h only where a late run is harmless anyway.

- **Authoring note:** a DAG that validates and appears in `dagu ls` can still never *run* — confirm
with `dagu history <name>` that a run row exists. A silently-failed `dagu start` leaves no row.

- **Never schedule a copy whose *****source***** is a FileProvider mount.** Reading through macOS FileProvider (Google Drive `My Drive`, iCloud, any `~/Library/CloudStorage/*`) blocks on non-materialised items exactly like the Synology wedge: the process sits alive with *no data file open*, size static, and never logs a completion. It got ~2.6 GB in before stalling for 18+ minutes. Force materialisation first (`brctl download <tree>`, or "Keep on this device" in Finder) or copy from a non-FileProvider path. A FileProvider source is only safe as a *destination* you write once to.

- **Bound directory-skeleton walks.** An unbounded `os.walk` of a 100 GB+ share over SMB produced `Errno 60` timeouts that *grew* with each retry (28 -> 174 -> 268 errors per pass) and never finished - two runs hit 14 and 22 minutes. A depth bound (3 gave the navigable top-level structure) made the same job 88 seconds and clean.

- **Nested-quoting trap:** do not put `(` or `)` in an `echo` string inside `ssh host 'bash -lc "…"'`.
The remote parser fails with `syntax error near unexpected token '('`, and because the failure is in
the *outer* command the DAG never fires — it looks exactly like a dagu problem. Keep echoed strings
bare alphanumerics and hyphens.

## Web UI — where it lives and how it starts

The UI is a **separate process** from the scheduler. `dagu scheduler` alone runs headless (it only
binds an internal service port); without a `dagu server` / `dagu start-all` there is **no UI at all**.

Both hosts serve the UI on **8888** at `http://127.0.0.1:8888`.

- **Port 8888, not the 8080 default, because 8080/8081 on the Studio are taken by ****`opencode2`****.**

- **Set the workbox port in ****`config.yaml`****, never in the Homebrew plist** — `brew services` regenerates
that plist from the formula, so a hand-edited `--port` silently reverts. `host` and `port` are valid
top-level `config.yaml` keys and `start-all` honours them. On the Studio the port is a plist flag
instead, because that LaunchAgent is hand-written.

- **The UI needs ****`auth.mode: none`**** to be usable.** With no `config.yaml`, auth defaults to `builtin`
with no admin account: the SPA loads but every `/api/v1/*` call returns **401**, and `/` + `/setup`
serve a first-run setup screen. Setting `auth: {mode: none}` in `~/.config/dagu/config.yaml` fixes it.
This is only acceptable because the listener is **loopback-bound**; if the UI is ever exposed beyond
127.0.0.1, set `auth.mode: builtin` back and complete `/setup` first.

- **Distinguish a real API 200 from the SPA fallback.** An unknown path returns the Dagu HTML shell with
status **200**, so a bare status check lies. Send `Accept: application/json` (an unauth'd API returns
**401**, not HTML) and check the response body parses.

- **API key is lowercase ****`dags`****, and it is version-specific.** `GET /api/v1/dags` → `{"dags":[{dag:{name...},<br>  suspended, latestDAGRun:{statusLabel}}]}` on 2.16.1/2.22.0. `/api/v2/*` exists on 2.22.0 but 404s back
the SPA shell on 2.16.1.

### Restarting a host's service

`dagu start-all` (workbox) and `dagu server` (Studio) can be restarted freely. `start-all` embeds the
scheduler, so restarting it kills any in-flight run — check `dagu ps` is empty first. `brew services<br>restart dagu` reports the new label as `sh.brew.dagu`; that is normal.

**A restart replays catchup ticks and the retry scanner replays failures, so a restart can start work.**
`start-all` re-applies `catchup_window` (6h default, 24h on `workbox-morning-pull`) and replays missed
cron intervals; the retry scanner (`retry_failure_window`, 24h) separately re-enqueues recently failed
runs every 30s. Expect a restart on a host with a failing DAG to immediately spawn another attempt —
verify `dagu ps` after, and do not read a fresh run as evidence the restart misfired.

If an in-flight run must be cleared to restart, **`dagu stop <dag>`**** gracefully** (SIGTERM, cleanup
handlers run, no orphaned `running` row) rather than `kill`ing the scheduler. A run stuck in `U`
(uninterruptible SMB I/O on a NAS sync) only ends when its I/O returns, so a stop can take minutes.
`dagu stop` on a failed run also cancels its pending DAG-level auto-retry.

## Hermes alert webhook (zero LLM)

```bash
hermes webhook subscribe <route> --deliver discord --deliver-chat-id "<channel-id>" \
  --deliver-only --prompt "{text}" --description "..."
```

`--deliver-only` forwards the rendered prompt verbatim with **no agent run**. The subscription's
secret lands in `~/.hermes/webhook_subscriptions.json` (read it from scripts; never hardcode it).

### Signing an incoming POST

A generic caller must sign. The gateway accepts (see `gateway/platforms/webhook.py`):

- **`X-Webhook-Signature-V2`** = hex HMAC-SHA256 of `"<timestamp>.<raw body>"`, with
**`X-Webhook-Timestamp`** in the same request. *Use this.*

- Legacy `X-Webhook-Signature` = hex HMAC-SHA256 of the body alone.

- Also accepted: `X-Hub-Signature-256`, `X-Gitlab-Token`, Linear, Svix.

Body must be JSON `{"text": "..."}` when the prompt template is `{text}`. A 401
`Invalid signature` means the signature/secret pair is wrong, not that the route is missing.

Pitfalls:

- The webhook binds `platforms.webhook.extra.host` (**default ****`127.0.0.1`**). Only loopback and the
Cloudflare tunnel reach it; other LAN hosts get connection-refused. Widening the bind is a security
change — explicit approval + a gateway restart.

- `hermes` CLI reads `$HERMES_HOME`. An inline `HERMES_HOME=... cmd` on its own line **persists in
the shell session** and makes later `hermes` calls target the wrong profile (e.g. "webhook platform
is not enabled"). Run `unset HERMES_HOME` before debugging.

## n8n (hosted) constraints

Name-resolution limits, the shared-brain mount, secret handling, the SDK build order and the `jsCode`
newline trap: `references/n8n-hosted-constraints.md`.

## Verification

- `dagu dry <name>` passes; the DAG appears in `dagu ls`; a real `dagu start <name>` succeeds in
`dagu history`.

- The alert path is proven by a real delivery: check `~/.hermes/logs/gateway.log` for
`direct-deliver ... route=<route>` and the returned `delivery_id`.

- De-duplicate alerts (fingerprint + re-alert window) or a persistent fault pings on every tick.

## Related

- `monday` — the weekly reset these DAGs serve. `hermes-services` — gateway, dashboard, cron lifecycle.