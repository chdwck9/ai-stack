---


uuid: 41324dc8-ccd9-81ae-b936-d79d89e6d104
name: vpn-isolated-downloads
version: 1
description: "Use when putting a download client behind a VPN."
thinking: "Medium"
temperature: 0.3
author: Clarity
license: proprietary
metadata:
hermes:
tags: [vpn, gluetun, qbittorrent, nordvpn, docker, synology, torrents]
related_skills: [media-volume-management, media-request-management, docker-management]


---


# Isolating a download client behind a VPN

A proxy setting is not a kill switch. The only shape that survives a provider drop is putting the
client in the VPN container's **network namespace**: it then has no interface to leak from.

## When to Use

- "Privatise the media box", "route the torrents through a VPN", "is my traffic anonymised?".

- A download client has proxy credentials stored but `Proxy\Type=None`, or a SOCKS5 proxy with no
kill switch.

## Procedure

1. **Find what is actually running** before writing anything: `docker ps` for the client, its
network (`downloaders_media_net` style), its published ports, and where its config lives. Check
whether the stack is Portainer-managed — if so the compose file it *runs* may be under
`/data/compose/<id>` and the real source of truth somewhere else on the share.

1. **Get the credential shape right for the provider.** For NordVPN the "service credentials" from the
dashboard's *Set up NordVPN manually* page are a username + password pair (24-char strings) and map
to `OPENVPN_USER` / `OPENVPN_PASSWORD`. The account API key/access token is a different thing and is
not what a tunnel needs.

1. **Prove the tunnel outside the estate first.** Run a throwaway gluetun on a machine you can iterate
on, watch for `Initialization Sequence Completed` and a `Public IP address is …` line naming the
expected country, then tear it down. Debugging a tunnel through a live media stack is much slower.

1. **Rewrite the stack so the tunnel owns the network.** gluetun publishes every port; the client has
`network_mode: "service:gluetun"` and no `ports:`/`networks:` of its own. Any helper that shares the
client's namespace (a loopback bridge, a socat proxy) must move to `service:gluetun` too.

1. **Preserve the client's DNS name** so nothing else needs reconfiguring: give gluetun the old
container name as a network alias (`networks: {media_net: {aliases: [qbittorrent]}}`). Then
sonarr/radarr/readarr keep pointing at `http://qbittorrent:8080` untouched.

1. **Harden the client's own settings** (see the API recipe below): DHT, PeX and LSD off, proxy type
None. In a netns those discovery protocols are pointless and only add leak surface.

1. **Verify with three probes**, not one: egress IP from inside the namespace
(`docker exec gluetun wget -qO- https://api.ipify.org`), the client's UI from the LAN
(`curl -o /dev/null -w '%{http_code}' http://<host>:<port>/`), and the *arr resolution
(`docker exec sonarr getent hosts qbittorrent` → gluetun's bridge IP).

## Running one specific endpoint from a downloaded `.ovpn`

Pinning the exit to a provider endpoint the user picked means gluetun must treat it as a **custom**
provider; leave `VPN_SERVICE_PROVIDER=nordvpn` and it silently chooses its own server and your `.ovpn`
is never used.

```yaml
  gluetun:
    image: qmcgaw/gluetun
    cap_add: [NET_ADMIN]
    devices: ["/dev/net/tun:/dev/net/tun"]
    env_file: [./nord.env]          # OPENVPN_USER / OPENVPN_PASSWORD, chmod 600
    environment:
      - VPN_SERVICE_PROVIDER=custom
      - VPN_TYPE=openvpn
      - OPENVPN_CUSTOM_CONFIG=/gluetun/custom.ovpn
      - FIREWALL_OUTBOUND_SUBNETS=192.168.2.0/24
    volumes: ["./gluetun:/gluetun"]  # the dir holding custom.ovpn
```

- The provider's `.ovpn` carries its own CA and tls-crypt, so no extra files are needed — but it does
contain `auth-user-pass` with no argument, i.e. it still needs the service username/password from
the env file.

- `FIREWALL_OUTBOUND_SUBNETS` is what keeps the *arr apps able to reach the client's UI on the LAN;
without it the tunnel's firewall drops their requests and the stack looks half-dead.

- **Prove it on the Mac first.** Docker Desktop's Linux VM does have `/dev/net/tun`, so a throwaway
`gluetun` with `--cap-add NET_ADMIN --device /dev/net/tun` connects in ~20 seconds and prints the
exit country — far faster than iterating against the live NAS stack.

## Synology: the tun device

DSM kernels ship the module but not the node, and a VPN container cannot start without it:

```bash
insmod /lib/modules/tun.ko
mkdir -p /dev/net && mknod /dev/net/tun c 10 200 && chmod 600 /dev/net/tun
```

Keep this as an idempotent script (`/volume1/docker/<stack>/ensure-tun.sh`, exits 0 when
`/dev/net/tun` already exists) and register it as a **boot-up** DSM task — the node does not survive a
reboot, and the stack fails closed, so the symptom is "nothing downloads" with a healthy-looking UI.
Check `/proc/modules` and `/lib/modules/tun.ko` existence rather than guessing which DSM versions have it.

## Hardening qBittorrent v5 through its API

The WebUI API is reachable passwordlessly from inside the namespace when
`WebUI\LocalHostAuth=false`, but it **rejects requests whose ****`Host`**** header is the forwarded port**:

```bash
curl -s -H 'Host: 127.0.0.1:9710' -H 'Referer: http://127.0.0.1:9710' \
  http://127.0.0.1:<bridge-port>/api/v2/app/preferences
curl -s -X POST -H 'Host: 127.0.0.1:9710' -H 'Referer: http://127.0.0.1:9710' \
  --data-urlencode 'json={"dht":false,"pex":false,"lsd":false}' \
  http://127.0.0.1:<bridge-port>/api/v2/app/setPreferences
```

Without the `Host` header you get `Unauthorized` and will waste time hunting credentials that are not
needed. Re-read preferences afterwards and quote the before/after values — the config file will **not**
show `dht`/`pex`/`lsd` keys at all, so editing `qBittorrent.conf` is not an option.

## Pitfalls

- **Stopping the client and rereading its config does not persist the bitfield toggles.** v5 only
writes changed settings; the three flags are absent from the file. Go through the API.

- **The proxy block keeps the old provider's credentials** (`Proxy\Password=`, `Proxy\Username=`) even
after `Proxy\Type=None`. Say they are inert rather than claiming they were removed.

- **Nord has no port forwarding.** The listen port is published and carried by the tunnel, but expect
fewer incoming peers on thin swarms. State this before someone buys a year of it; a forwarding
provider is the fix, and swapping one is just a new `.ovpn` plus credentials.

- **The UI usually stays LAN-reachable.** Isolating traffic is not the same as closing the WebUI; offer
to bind it to loopback if the user wants that too.

- **Never treat a proxy toggle as equivalent to the tunnel.** SOCKS5 has no drop protection: if the
proxy dies the client falls back to the bare route. That is the whole reason for the netns shape.

- **Secrets written over an SMB/NFS share come out 0777.** The share ACL wins over `umask`/chmod in the
write pipeline, so set `chmod 600` on the env file as a separate step and re-check the mode.

- **Probe ****`sudo -n`**** per binary, not per host.** A NAS allowlist that covers `docker` does not cover
`insmod`/`mknod`, so the tunnel device step is a handoff while the container work is not. Hand the
user one exact command and the expected `crw------- … /dev/net/tun` output.

- **The compose project name is not always the directory.** `docker compose ls` plus the network name
(`<project>_media_net`) tells you the real `-p` value; a Portainer stack may point at a
`/data/compose/<id>` file that no longer exists, in which case deploy from the share path with the
right project name or you will create a duplicate stack.

## Verification

- `docker ps` shows gluetun healthy and the client with **no ports** of its own.

- Egress IP from the namespace is the VPN exit, and it is stable across a client restart.

- The client's UI answers from the LAN; the *arr apps resolve the client by name.