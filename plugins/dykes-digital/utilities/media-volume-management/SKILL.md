---


name: media-volume-management
uuid: 3f524dc8-ccd9-8103-bfbe-e4cded706ae2
version: 2
description: "Media Volume Management"
last-used: "2026-10-27"
thinking: "Medium"
temperature: 0.3
author: Hermes Agent
license: MIT
metadata:
hermes:
tags: [media, jellyfin, plex, smb, nfs, docker, macos, nas, volumes, mounts]


---


# Media volume management

Mount and troubleshoot media storage for Jellyfin / Plex on macOS, and keep the download side of the
media stack off the home IP.

## When to Use

- Media playback fails while the library looks populated; Jellyfin shows an empty library despite
files existing on the server.

- A NAS share needs remounting after a network reconnect or reboot.

- A media container cannot see mounted volumes.

- The torrent client needs to be routed through a VPN with a real kill switch.

## Core principle

**Docker Desktop on macOS cannot let a container negotiate SMB to a NAS on its own network.** Mount
the SMB share **on the host** (`/Volumes/*` with sudo, or a user-writable path like
`/tmp/play_mount`), then bind-mount that host path into the container with `-v`.

Three strategies, in reliability order:

1. **Host-path bridge (most reliable, verified)** — `mount_smbfs` to a host path, then
`-v <hostpath>:/media`. Works even when the share is mounted under `/tmp/`.

1. **Host-side ****`/Volumes/*`**** mount** — needs root; not available to a passwordless agent.

1. **Container-internal ****`mount.cifs`** — a custom image (FROM the app image, `cifs-utils`, wrap
ENTRYPOINT) that mounts then execs the real binary. Verified working run `--privileged` with
bridge networking + `-p`, guest mount of `//192.168.2.6/Play`, `vers=2.1`. The **only**
self-contained option with no host-side mount and no sudo. Retry the mount in the entrypoint
(sleep 4, up to ~30 attempts) to survive a rebooting NAS.

To verify a container truly has an internal mount (vs a host bind):
`docker exec <c> mount | grep ' /media '` — `type cifs` means mounted inside the container.

**Port-mapping rule:** `--network host` **ignores ****`-p HOST:CONTAINER`**. To keep a reverse-proxy
port, use **bridge networking + ****`-p`**; only use host networking if you launch the app with an
explicit in-process `--port=<hostport>`.

## Procedure

### Diagnose

```bash
ls /Volumes/Play/                  # host sees the share?
docker exec <container> ls /media  # container sees it?
```

Host shows files but the container shows nothing → the virtiofs barrier; use the bridge.

### Strategy A — host-path bridge (preferred, verified)

```bash
mkdir -p /tmp/play_mount
mount_smbfs //guest@192.168.2.6/Play /tmp/play_mount

docker run -d --name chdwck9studio-jellyfin-1 \
  --network edge-net -p 13377:8096 \
  -v /Users/chdwck9studio/config/media/jellyfin/config:/config \
  -v /tmp/play_mount:/media \
  jellyfin/jellyfin:latest
```

```bash
docker exec chdwck9studio-jellyfin-1 ls /media
curl -s -o /dev/null -w '%{http_code}' http://localhost:13377   # expect 200/302
```

### Strategy B — host-side `/Volumes/*` (needs sudo)

`sudo mount_smbfs //guest@chdwck9NAS/Play /Volumes/Play`

### Strategy C — container-internal mount.cifs (last resort)

Only when the host cannot mount SMB at all. Expect apt-get latency and possible SMB negotiation
failure; keep Strategy A as the fallback.

## Routing the download client through a VPN

A SOCKS5 proxy set in the client is **not** anonymisation: if the proxy drops, the client falls back to
the home IP. A real kill switch is a network namespace — put the client inside the VPN container's
namespace so a dead tunnel leaves it with no interface at all.

```yaml
  vpn:
    image: qmcgaw/gluetun
    cap_add: [NET_ADMIN]
    devices: ["/dev/net/tun:/dev/net/tun"]
    env_file: [/volume1/docker/gluetun/nord.env]      # credentials out of the compose file
    environment:
      - VPN_SERVICE_PROVIDER=custom                    # a downloaded .ovpn, not a built-in provider
      - VPN_TYPE=openvpn
      - OPENVPN_CUSTOM_CONFIG=/gluetun/custom.ovpn
      - FIREWALL_OUTBOUND_SUBNETS=192.168.2.0/24       # LAN peers can still reach the UI
    ports: ["9710:9710", "9711:9711", "9711:9711/udp"]
    networks:
      media_net:
        aliases: [qbittorrent]                         # keep the old DNS name

  qbittorrent:
    image: linuxserver/qbittorrent
    network_mode: "service:vpn"                        # no ports:, no networks:
    depends_on: [vpn]
```

- **Every published port moves to the VPN container.** The client keeps none.

- **Give the VPN container the client's old network alias**, so sonarr/radarr/readarr keep resolving
the same hostname and no download-client setting changes.

- **A loopback bridge (****`socat`****) must move too** — `network_mode: "service:vpn"` — or its upstream
`127.0.0.1:<port>` lands in a different namespace.

- **Prove it before touching the live stack:** run the VPN image standalone with the real config,
wait for `Initialization Sequence Completed` in the logs, and read the public IP gluetun reports.
With NordVPN, the OpenVPN service credentials are the `NORDVPN_USER_ID` / `NORDVPN_API_KEY` pair and
the `.ovpn` already carries its CA and tls-crypt.

- **After the tunnel is up, harden the client itself:** clear any configured proxy, and turn **off**
DHT, PeX and LSD — they leak peer discovery past the tunnel's reach.

- Expect **fewer incoming peers** with providers that do not offer port forwarding (NordVPN, for one).

**Synology has no TUN device by default.** `/dev/net` does not exist and `tun` is not loaded, so any
VPN container fails until the host provides it — but `/lib/modules/tun.ko` is usually present:

```bash
sudo sh -c 'insmod /lib/modules/tun.ko; mkdir -p /dev/net; mknod /dev/net/tun c 10 200; chmod 600 /dev/net/tun'
ls -l /dev/net/tun     # crw------- 1 root root 10, 200
```

This does **not** survive a NAS reboot — add a DSM triggered/boot-up task, or the client silently comes
back without its tunnel.

## Pitfalls

- `--network host` with `-p` shows `{}` in `docker port` — not a failure; bind the port in-process
instead, or switch to bridge.

- `mkdir: Permission denied /Volumes/Play` — `/Volumes` is root-owned; create a user-writable mount
point (`/tmp/play_mount`) and bridge that.

- Container sees empty `/media` — the host mount is not up yet, or the path changed; check
`ls /tmp/play_mount` on the host first.

- DNS resolves but the mount times out — the NAS name resolved to the Tailscale overlay while you
are not on VPN; pin the LAN IP (`192.168.2.6`).

- ICMP ping times out but SMB/web work — the NAS blocks ICMP; test TCP (`nc -z -w5 <ip> 445`) instead
of ping.

The full pitfall table, network diagnostics, permanent self-healing mounts (NFS + a launchd
watchdog) and the reconnect script: `references/media-mounts-detail.md`.