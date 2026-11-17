---


uuid: 41a24dc8ccd9817f82e7f4f6ea34adfa
name: smb-share-diagnosis
description: Use when an SMB share drops, reconnects, or won't mount.
version: 1.1.0
author: Clarity
license: MIT
platforms: [macos, linux]
metadata:
hermes:
tags: [smb, samba, macos, shares, networking, bonjour, diagnosis]
category: devops
requires_toolsets: [terminal]


---


# SMB share diagnosis

Work out *why* a share drops, loops, hides folders, or refuses a login — and answer
"what is the path to my shared folder" with verified output rather than a guess.
Covers a macOS host serving SMB (Apple's `smbd`, not [samba.org](http://samba.org/)) and any client
reaching it.

## When to Use

- "The share connects and disconnects too fast to open anything" — flapping, looping,
Finder remounting.

- "What's the path to my shared folders?"

- A client sees no shares, or auth is refused on a share that claims guest access.

- Deciding whether to reach the NAS directly or through a host that already mounts it.

For a plain "connection refused / wrong server answered", `service-port-diagnosis`
is the better skill. This one is for sessions that establish and then die.

## Core principle

Three independent layers produce the same user complaint:

1. **Listener** — is `smbd` up and bound?

1. **Share and auth** — does a sharepoint exist, and is the credential the *client*
uses actually accepted?

1. **Network identity** — does the client's traffic stay pinned to one interface?

**A flapping session is almost never a timer and almost never a crashed daemon.**
Check identity (layer 3) first; it is the cheapest to prove and the most commonly
missed.

## Procedure

### 1. Confirm the listener — with a command that can see root processes

macOS `smbd` runs as root and is **socket-activated by launchd**: it is absent
between connections and exits after an idle period. Absence is normal, so do not
read it as a fault.

```bash
ps -Ao pid,user,command | grep '/usr/sbin/smbd' | grep -v grep
netstat -anv -p tcp | grep '\.445 ' | grep LISTEN   # carries the owner PID, no root needed
```

Never conclude "not running" from an empty unprivileged `lsof -iTCP:445`. The
launchd log is the liveness record: `log show --last 30m --predicate 'process ==<br>"launchd" AND eventMessage CONTAINS[c] "smbd"'` shows spawn / `service inactive`.

### 2. Inventory shares without root

```bash
sharing -l                                  # macOS: name, path, smb shared/guest/read-only
dscl . -list /SharePoints
dscl . -read "/SharePoints/<name>" directory_path smb_name smb_guestaccess
```

`sharing -l` answers the user's question directly. Both of these work unprivileged —
do not stall on "needs sudo" before trying them.

Answer "what's the path" concretely: `smb://<ip>/<Share Name>` plus the on-disk
path. **Say plainly when there is exactly one share** and that everything else is
not exported — a client that connects and sees an unexpected (short) list is
usually this, not a fault. Offer the `sharing -a` commands to add more, but adding
sharepoints is an admin action the user runs.

NAS volumes a host has mounted (NFS at `/Volumes/*`) are **not** re-exported over
SMB. If the user wants those, point them at the NAS directly (`smb://<nas-ip>/`)
rather than routing through the intermediate host.

### 3. Test auth the way the client will

```bash
smbutil view -N //<host>        # anonymous / guest
smbutil view //<user>@<host>    # authenticated (prompts)
```

`server rejected the authentication` on a share flagged `guest access: 1` means
guest is not actually granted — `smbd` logs `smbd_detect_sg_mode: NOT enabling<br>super guest mode, errno: 2`. Tell the user to connect as a real account. **A client
looping on refused guest auth looks exactly like a network flap**, so rule this out
before hunting the network.

### 4. Read the host's network identity

```bash
for i in en0 en1; do echo "--- $i"; ifconfig $i | grep -E 'inet |status'; done
networksetup -getinfo "Ethernet"; networksetup -getinfo "Wi-Fi"
route -n get default | grep -E 'gateway|interface'
netstat -rn -f inet | grep -E '^192\.168|^default'
```

Two distinct defects, both fatal to an SMB session:

- **The same address on two interfaces.** An ARP conflict: two MACs claim one IP, the
switch's CAM entry flips, and every TCP session is reset. Also check the mask — a
`/32` (`netmask 0xffffffff`) on a LAN interface means that interface has no route
to its own subnet at all, which is how the duplicate goes unnoticed.

- **Two interfaces on the same subnet with different addresses.** Still a defect. It
leaves two routes to one network and duplicates the host's own Bonjour records.

### 5. Count the host's Bonjour records — the decisive test

```bash
scutil --get LocalHostName                      # the real name; never guess it
dscacheutil -q host -a name <LocalHostName>.local
```

A healthy single-homed host resolves to **exactly one address per interface, plus
loopback** — so a macOS host with one active LAN interface measures **2 IPv4 A
records** (`127.0.0.1` and the LAN address), not 1. Do not read 2 as still broken;
the defect is a *duplicate LAN address* or a second interface's address, and
loopback is always present. Likewise `_smb._tcp` shows one registration per
interface index including loopback (healthy single-homed = 2 lines for the host,
indices 1 and the LAN index), so count *distinct LAN indices*, not total lines. A
measured broken host returned five A records for one
host — the same address twice per interface plus loopback — and three
`_smb._tcp` registrations across three interface indices. A client resolving by
name gets a rotating answer and dies on the address change.

Corroborating signal: macOS de-duplicates the NetBIOS name on collision, so a host
that was `MAC-STUDIO` comes back as `mac-studio-1` in the `com.apple.smb.server`
plist. The host is colliding with its own second advertisement.

`dns-sd -B _smb._tcp local` browses forever — bound it:

```python
import subprocess
p = subprocess.Popen("dns-sd -B _smb._tcp local", shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
try:
    out, _ = p.communicate(timeout=7)
except subprocess.TimeoutExpired:
    p.kill(); out, _ = p.communicate()
```

### 6b. When the network is clean, hunt the keepalive job

"It's like it's on a timer" is usually literal. A watchdog that keeps shares
mounted is the classic culprit and it hides in plain sight because it is *doing
its job* by remounting:

```bash
ls -1 /Library/LaunchDaemons /Library/LaunchAgents ~/Library/LaunchAgents
launchctl print system/<label> | grep -E 'state|runs|last exit'
tail -40 /var/log/<watchdog>.log
```

Measured case: `com.richard.nasmounts` ran `/usr/local/bin/nas-mount-watchdog.sh`
every 60s and force-unmounted + remounted **all five** NAS shares every single
run, for a month. Any client with a file open (VLC playing from `/Volumes/Play`,
a sync job, an editor) saw a drop/reconnect cycle.

**The bug to look for: treating any non-zero probe exit as "hung".** The probe
ran as root; root's `ls` on the NFS export exited non-zero immediately, so every
share was declared dead every minute.

Prove it is not a real hang before believing the log:

- **Timing.** A genuine timeout costs `PROBE_TIMEOUT` per share. Five shares
"hanging" inside ~1 second means they returned an error immediately, not a
timeout — the script is misclassifying an exit code.

- **Compare contexts.** Run the same probe as the logged-in user. `rc=0` in
0.00s while the daemon logs HUNG means the daemon's *identity*, not the mount,
is the difference.

Rules for the fixed watchdog: only a timeout (rc 124) counts as a hang; probe
with `stat -f` on the mount point rather than `ls` (no huge directory walk, and
it does not need read permission); require N consecutive strikes before acting;
bound the log.

Stopping a root LaunchDaemon and editing a root-owned script is an admin action —
prepare the corrected script and hand the user the exact `launchctl bootout` /
`bootstrap` sequence. Do not attempt it yourself.

### 7. Fix, then confirm with the same test

One interface per LAN. **The re-count is the confirmation, not "the client seems
fine now":** the `.local` name must collapse to one LAN address (plus loopback) and
`_smb._tcp` to one registration per real interface. If the LAN address is *already*
singular and sessions still flap, the identity layer is clean — go back to layers 1
and 2 rather than repeating the network theory. After the fix, also re-test the
credential layer (§3): a guest refusal that was masked by the flap is still there
and will keep looping an anonymous client.

## Pitfalls

- **Unprivileged ****`lsof`**** cannot see a root-owned listener.** macOS `smbd` runs as
root, so an empty `lsof -iTCP:445` reports a healthy server as dead. Use
`netstat -anv -p tcp` or `ps -Ao`.

- **Never guess the ****`.local`**** name.** The Bonjour name (`scutil --get LocalHostName`),
the ComputerName and the NetBIOS name are three different strings. Guessing
`<hostname>.local` yields an empty resolve, which reads as "mDNS is broken" when
the name was simply wrong.

- **A flapping session is a network-identity symptom.** Reach for timers, keepalive
settings or a reinstall only after the A-record count is 1.

- **Two interfaces on one subnet is a defect even with different addresses.** The
duplicate-address case is louder, but the different-address case still duplicates
Bonjour and leaves two routes — it does not self-resolve.

- **A guest-flagged share is not a guest-granted share.** `smb_guestaccess: 1` in
`dscl` coexists with an authentication refusal.

- **Do not treat a host's NFS mounts as exports.** `/Volumes/<Share>` on the Studio is
an NFS client mount; sharing it over SMB is a separate, unconfigured thing.

- **Report the first confirmed finding before continuing to dig.** A multi-round
diagnosis with no interim message reads as a stall and the user will interrupt to
ask whether you are stuck. Send the one verified fact (listener state, share
inventory and path, or the A-record count) and keep going.

- **macOS has no ****`timeout(1)`****.** Bound long-running probes (`dns-sd`, `nc`) with
`-w`/`-G` flags or a python `communicate(timeout=)`.

## Verification

Before reporting, be able to state: the listener and its owner, the share inventory
with on-disk paths, whether the credential the client uses is accepted, the address
and mask per interface, and the count of `.local` A records and `_smb._tcp`
registrations. Those five together name the layer that is actually broken.