#!/usr/bin/env bash
# setup-clarity-gateway.sh
# Add a Cloudflare Tunnel ingress route + DNS record for the Hermes gateway so
# Clarity is reachable from outside the home network.
#
# RUN ON THE MAC STUDIO (where cloudflared and ~/.cloudflared/config.yaml live).
#
#   ./setup-clarity-gateway.sh           # dry run - prints what it would change
#   ./setup-clarity-gateway.sh --apply   # applies, backs up config, restarts tunnel
#
# Additive and idempotent. The config is copied to config.yaml.bak.<timestamp>
# before any edit. Nothing is deleted. Written by Clarity 2026-10-19.
set -euo pipefail

HOSTNAME_GW="${HOSTNAME_GW:-clarity-gateway.dykes.digital}"
TUNNEL="${TUNNEL:-edge-ai}"
ORIGIN="${ORIGIN:-http://127.0.0.1:8642}"
CONFIG="${CONFIG:-$HOME/.cloudflared/config.yaml}"
APPLY=0
[ "${1:-}" = "--apply" ] && APPLY=1

command -v cloudflared >/dev/null 2>&1 || { echo "cloudflared not on PATH"; exit 1; }
[ -f "$CONFIG" ] || { echo "no cloudflared config at $CONFIG"; exit 1; }

echo "== tunnels"; cloudflared tunnel list || true
echo "== current ingress"; cat "$CONFIG"

if grep -q "hostname: $HOSTNAME_GW" "$CONFIG"; then
  echo "== $HOSTNAME_GW already present - no config change needed"
else
  echo "== will insert before the catch-all rule:"
  echo "  - hostname: $HOSTNAME_GW"
  echo "    service: $ORIGIN"
  if [ "$APPLY" = "1" ]; then
    cp "$CONFIG" "$CONFIG.bak.$(date +%Y%m%d%H%M%S)"
    awk -v h="$HOSTNAME_GW" -v o="$ORIGIN" '
      !done && /http_status:404/ {
        print "  - hostname: " h
        print "    service: " o
        print "    originRequest:"
        print "      connectTimeout: 30s"
        done=1
      }
      { print }
    ' "$CONFIG" > "$CONFIG.new"
    mv "$CONFIG.new" "$CONFIG"
    echo "== config updated; backup kept alongside"
  fi
fi

if [ "$APPLY" = "1" ]; then
  echo "== DNS route"
  cloudflared tunnel route dns "$TUNNEL" "$HOSTNAME_GW" || echo "(route probably already exists)"
  echo "== restart tunnel"
  if launchctl print system/com.cloudflare.cloudflared >/dev/null 2>&1; then
    sudo launchctl kickstart -k system/com.cloudflare.cloudflared
  else
    echo "restart cloudflared the way you run it (brew services restart cloudflared | docker compose restart cloudflared)"
  fi
fi

echo
echo "== verify from OUTSIDE the house:"
echo "   getent hosts $HOSTNAME_GW"
echo "   curl -sI https://$HOSTNAME_GW/ | head -1"
echo "   an unauthenticated 200 means the gate is NOT on - fix that before travelling"
