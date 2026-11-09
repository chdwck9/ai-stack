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

Mount and troubleshoot media storage for Jellyfin / Plex on macOS.

## When to Use

- Media playback fails while the library looks populated; Jellyfin shows an empty library despite
files existing on the server.

- A NAS share needs remounting after a network reconnect or reboot.

- A media container cannot see mounted volumes.

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