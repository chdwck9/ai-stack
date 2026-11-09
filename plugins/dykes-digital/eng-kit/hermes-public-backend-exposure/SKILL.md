---


uuid: 40524dc8-ccd9-816d-88b0-df95f6a3ce57
name: hermes-public-backend-exposure
description: "Use when exposing the Hermes backend at a public host."
version: 1.0.0
metadata:
hermes:
tags: [hermes, dashboard, tunnel, cloudflare, security, auth]


---


# Exposing the Hermes dashboard / serve backend publicly

Goal: make a Hermes backend reachable at a public HTTPS hostname (remote desktop
app, remote chat) without leaving agent control open to the internet.

The Hermes backend the desktop app and remote clients use is the **web
dashboard / ****`hermes serve`**** process on port 9119** (loopback by default). A
messaging gateway (`hermes gateway run`) is a *different* process — do not
conflate them.

## Order matters: auth gate FIRST, route SECOND

**A loopback-bound dashboard has NO authentication** (`/api/health` reports
`"auth_required":false`). Tunnelling it as-is exposes full agent control
(files, terminal, every session) to the internet. Never create the public route
before the gate is on and verified.

### 1. Check current state

```bash
lsof -nP -iTCP:9119 -sTCP:LISTEN          # is the backend up, on which bind
curl -s http://127.0.0.1:9119/api/health   # look at auth_required
```

### 2. Configure an auth provider (fail-closed)

The gate engages when `dashboard.public_url` is a **non-loopback** hostname, even
on a loopback bind. Without a provider the dashboard **refuses to start**
(SystemExit) — so configure the provider in the same step.

Password provider (no IDP needed):

```bash
# hash without leaking plaintext into logs/history; run from the hermes-agent root
<venv>/bin/python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('PW'))"
hermes config set dashboard.basic_auth.username <user>
hermes config set dashboard.basic_auth.password_hash 'scrypt$...'
hermes config set dashboard.basic_auth.secret "$(python3 -c 'import secrets;print(secrets.token_urlsafe(36))')"   # else sessions die on every restart
hermes config set dashboard.public_url 'https://<host>'
```

OAuth alternative: `hermes dashboard register --redirect-uri https://<host>/auth/callback`
(writes `HERMES_DASHBOARD_OAUTH_CLIENT_ID`; requires a **Nous Portal** login).
If the user is only logged into e.g. openai-codex, register is unavailable —
use the password provider or Cloudflare Access.

### 3. Restart the dashboard and VERIFY the gate

```bash
launchctl kickstart -k gui/$(id -u)/ai.hermes.dashboard   # macOS
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:9119/api/sessions   # expect 401
curl -s http://127.0.0.1:9119/api/auth/providers                              # expect provider listed
# prove the credential works so the owner isn't locked out:
curl -s -H 'Content-Type: application/json' -d '{"provider":"basic","username":"<user>","password":"<pw>"}' http://127.0.0.1:9119/auth/password-login
#   -> {"ok":true,"next":"/"}   wrong password -> 401
```

Abort and fix before exposing if any of these are wrong.

### 4. Tunnel route + ingress

```bash
cp ~/.cloudflared/config.yaml ~/.cloudflared/config.yaml.bak-$(date +%Y%m%d-%H%M%S)
cloudflared tunnel route dns <tunnel-name> <host>
# add to ~/.cloudflared/config.yaml ingress, BEFORE the http_status:404 catch-all:
#   - hostname: <host>
#     service: http://127.0.0.1:9119
launchctl kickstart -k gui/$(id -u)/digital.dykes.cloudflared   # restart to pick up ingress
```

### 5. Verify from outside

```bash
curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' https://<host>/   # expect 302 -> /login, NOT 200
```

## Gotchas

- Full launchd/tunnel layout, command list, and the DNS→TLS→tunnel→origin
diagnostic ladder: `references/cloudflare-tunnel.md`.

- Setting `dashboard.public_url` also makes **local** dashboard access require
login (the gate is global once engaged). Tell the user.

- Never put the plaintext password in chat. Write it to a `chmod 600` file
under `$HERMES_HOME` and give the user the path.

- The public hostname is *not* the messaging gateway; webhooks are a separate
ingress host/port.