---


name: webhook-debugging

uuid: 41324dc8-ccd9-8134-9b76-cdccd09ef147

version: 1

description: "Debug failed webhooks: tunnel, auth, paused automations."

thinking: Medium

temperature: 0.3


---


# $webhook-debugging

Diagnose why a webhook integration failed to deliver.

## Steps

### 1. Confirm network path

Test the public-facing URL directly:

```javascript
curl -s --max-time 3 https://hooks.dykes.digital/webhooks/<route_name>
```

If Cloudflare returns JSON or a page instead of timing out/refusing, the tunnel is live.

Test locally:

```javascript
curl -s http://127.0.0.1:8644/webhooks/<route_name>
```

Both should return `{"error": "..."}` or `{"status": ...}`, never a timeout.

### 2. Check gateway log for the actual failure reason

```javascript
grep '\[webhook\]' ~/.hermes/logs/gateway.log | tail -30
```

Look for these patterns:

- `Invalid signature for route <name>` — signature mismatch (see pitfall below)

- `Unknown route: <name>` — route doesn't exist or has a typo

- `Route disabled: <name>` — subscription has `enabled: false`

- `Rate limit exceeded` — too many requests in 60s window

- No lines at all for the expected timestamp range — the request never reached the gateway

### 3. Diagnose signature rejection (most common)

The gateway accepts only these signature header families:

**PITFALL:** If the incoming service sends NO header from this list (e.g., Notion's `x-notion-webhook-secret`), the gateway returns 401 "Invalid signature" regardless of the secret value. Third-party webhooks that don't sign payloads will ALWAYS fail against a route with a real secret.

**Fix:** Set `secret: "INSECURE_NO_AUTH"` on the route in `~/.hermes/webhook_subscriptions.json`. Over HTTPS tunnels this is safe — Cloudflare terminates TLS, so the payload is encrypted in transit.

To change without restarting the gateway:

```python
import json
path = "/Users/chdwck9studio/.hermes/webhook_subscriptions.json"
with open(path) as f:
    subs = json.load(f)
subs["<route_name>"]["secret"] = "INSECURE_NO_AUTH"
with open(path, 'w') as f:
    json.dump(subs, f, indent=2)
```

The gateway hot-reloads dynamic routes on every inbound request.

### 4. Test after fix

```javascript
curl -s --max-time 3 https://hooks.dykes.digital/webhooks/<route_name>
  -X POST -H 'Content-Type: application/json'
  -d '{"test": true}'
```

Should return `{"status": "accepted", "route": "<name>", ...}` with HTTP 202, not 401.

### 5. Re-enable source automations

Services like Notion automatically pause webhooks after sustained 4xx responses. After fixing the backend, visit the source (Notion automation editor, Zapier dashboard, etc.) and re-enable it. Otherwise it stays paused silently.

## Quick decision tree

```javascript
Gateway receives request?
├─ No → Tunnel/firewall/DNS issue. Verify tunnel status.
├─ Yes, returns 401 Invalid signature
│  └─ Source doesn't send a recognized signature header.
│     Set INSECURE_NO_AUTH. Re-enable source automation.
├─ Yes, returns 404 Unknown route
│  └─ Route doesn't exist. Create or edit subscriptions JSON.
├─ Yes, returns 403 Route disabled
│  └─ Set enabled: true in subscription.
├─ Yes, returns 429 Rate limit
│  └─ Throttle the sender.
└─ Yes, returns 202 accepted
   └─ Delivery succeeded. Check agent output in logs/Home.
```