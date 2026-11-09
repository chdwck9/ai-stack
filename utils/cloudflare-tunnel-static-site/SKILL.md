---


uuid: 40524dc8-ccd9-8110-a1c8-d3f1ed22faaa
name: cloudflare-tunnel-static-site
description: "Use when hosting a static site on a Cloudflare subdomain."
version: 1.0.0
author: Clarity
license: MIT
platforms: [macos]
metadata:
hermes:
tags: [cloudflare, tunnel, static-site, dns, oauth-branding, nginx]
category: devops


---


# Static site on a Cloudflare subdomain (no API token)

## When to Use

- A `*.dykes.digital` subdomain must serve a static/placeholder site (home page, privacy policy, landing page) and no Cloudflare API token is available.

- Google OAuth app branding is failing because the home-page URL is unresponsive or not verified.

## Preferred path FIRST: the Cloudflare MCP

The Nous-approved catalog MCP `cloudflare` fronts the whole Cloudflare API over OAuth (DNS, Pages, Workers, tunnels) — **no API token and no hand-wired tunnel/DNS/restart**. Install/authorise with `hermes mcp install cloudflare` then `hermes mcp login cloudflare`, and prefer it for any zone/DNS/Pages change. The tunnel method below is only the fallback when the MCP is not installed. The MCP's tools bind to the agent toolset only on a new session — but it can be driven immediately via raw JSON-RPC (see `mcp-server-onboarding`).

Stand up a placeholder/static site on a `*.dykes.digital` subdomain using the **existing** `edge-ai`
Cloudflare tunnel. Needs no Cloudflare API token — the tunnel's `cert.pem` already carries account/zone
access. Use for Google OAuth app branding pages (home + privacy policy) or any throwaway landing page.

## Environment facts

- Host: Mac Studio. Tunnel `edge-ai`, LaunchAgent `digital.dykes.cloudflared`, config `~/.cloudflared/config.yaml`.

- Account cert: `~/.cloudflared/cert.pem` (an ARGO TUNNEL TOKEN JWT). Export `TUNNEL_ORIGIN_CERT=~/.cloudflared/cert.pem` for CLI calls.

- No raw Cloudflare API token exists in env/keychain — but the OAuth `cloudflare` catalog MCP IS installed and carries `#dns_records:edit` + `#zone:read`, so DNS/TXT changes go through it (see the Preferred path above). `cloudflared tunnel route dns` only creates tunnel **CNAMEs** — it cannot create TXT records.

## Procedure

1. **Build the site** under `~/sites/<name>/` with `public/` (webroot) and `nginx.conf` OUTSIDE the webroot (so the config is never served). Use `try_files $uri $uri.html $uri/ =404;` so `/privacy` resolves to `privacy.html`.

1. **Serve** with a standalone container (bind-mounting NFS into the Docker VM is unreliable — keep files on local disk):
`docker run -d --name <name>-web --restart unless-stopped -p 127.0.0.1:<port>:80 -v ~/sites/<name>/public:/usr/share/nginx/html:ro -v ~/sites/<name>/nginx.conf:/etc/nginx/conf.d/default.conf:ro nginx:alpine`

1. **Back up** `cp ~/.cloudflared/config.yaml ~/.cloudflared/config.yaml.bak-$(date +%Y%m%d-%H%M%S)`.

1. **Add ingress** — insert the hostname entry ABOVE the `- service: http_status:404` catch-all, pointing at the local port.

1. **Create DNS**: `TUNNEL_ORIGIN_CERT=~/.cloudflared/cert.pem cloudflared tunnel route dns edge-ai <host>`.

1. **Reload**: `launchctl kickstart -k gui/$(id -u)/digital.dykes.cloudflared`. ~5s reconnect; wildcard `*.dykes.digital` SSL already covers the new subdomain.

1. **Verify**: curl local first, then `https://<host>/` and `https://<host>/privacy` (expect 200). Confirm existing routes still answer.

## Pitfalls

- **`dykes.digital`**** apex AND ****`www`**** are in an infinite 308 redirect loop** (location = itself). Do NOT use the apex as a Google OAuth home page — Google reports it "unresponsive". ALWAYS use a subdomain.

- **Google's "website is not registered to you" check is Search Console domain ownership, not DNS you control.** Fixing it needs a DNS **TXT** record (or the Search Console HTML/GA method) — impossible with the tunnel cert alone. Requires a Cloudflare API token (Zone:DNS:Edit) or a manual dashboard action, then a 24h wait before Google rechecks.

- **A ****`*.dykes.digital`**** host can be wired two ways; a 502 tells you which.** Tunnel-backed hosts are proxied **CNAMEs → ****`<tunnel-id>.cfargotunnel.com`** and are governed by `~/.cloudflared/config.yaml` ingress (confirm with the Cloudflare MCP `…/cfd_tunnel/{id}/configurations` — `config_src: local`). Legacy hosts are proxied **A records → the home IP (****`77.173.25.84`****)**, served by a local reverse proxy on :443. Editing tunnel ingress does NOTHING for an A-record host, and its 502 means that host's own backing service is down. Check the DNS record type before touching tunnel config or blaming the tunnel.

- `cloudflared` warns its version is outdated on every call — harmless.