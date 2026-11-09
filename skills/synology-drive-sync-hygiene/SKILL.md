---


uuid: 40924dc8ccd9811d9408e3dc5f340a91
name: synology-drive-sync-hygiene
description: "Use when Synology Drive sync is stuck or churning."
version: 0.1.0
author: Clarity
license: MIT
metadata:
hermes:
tags: [synology, sync, nas, macos, fileprovider, storage]


---


# Synology Drive Sync Hygiene

## When to Use

A Synology Drive sync task is stuck, churning, or "processing N files" — or you are
deciding where machine-local runtime data should live.

## Core rule

Machine-local runtime artifacts must NOT live inside a Drive-synced share. Each of
these has caused a multi-week stall on its own: `.venv` (27k files), `node_modules`,
`__pycache__`, a second Hermes install (`config/hermes` = 142k files), Claude Code
state (`config/claude` = 22k files), Jellyfin/audiobook metadata, container caches.
Move them out; do not filter-and-hope.

## Topology (Richard)

- NAS `chdwck9NAS` / 192.168.2.6. Shares `/volume1/{Live,Love,Ship,temp}`.

- Studio holds **read-write NFS** mounts of every share at `/Volumes/<Share>`,
established by a root LaunchDaemon (`com.richard.nasmounts.plist`); other
machines run the Synology Drive Client into `~/Library/CloudStorage/SynologyDrive-*`.

- Workbox (herdr host, 192.168.2.20) runs the Client. Its local folder names are
arbitrary labels Richard chose and DO NOT equal the share or the remote path.

### The local folder name is not the remote path

Never infer which NAS folder a `SynologyDrive-*` folder mirrors from its name.
Resolve the mapping from the client's own session table:

sqlite3 -header -column 
"$HOME/Library/Application Support/SynologyDrive/data/db/sys.sqlite" 
"select id,share_name,remote_path,sync_folder from session_table;"

`sync_folder` is the local path, `share_name` + `remote_path` the NAS side. On this
estate `SynologyDrive-Ship/` mirrors `Ship:/@Mambu/` and `SynologyDrive-temp/`
mirrors `Ship:/---/` — the same share twice, one under a name that denotes a
different share. A destination guessed from the folder name writes to the wrong
place; always confirm against `session_table` before planning any path pair.

- Shared agent brain = `/Volumes/Live/@Edge/.ai` (skills, scripts, knowledge).
Per-machine Hermes homes are LOCAL: `~/.hermes` on Studio and on the workbox.

- `@Edge/.ai/skills` and `@Edge/.ai/config/claude/skills` are identical sets.

## macOS client internals

State dir: `~/Library/Application Support/SynologyDrive/data/`

- `db/filter.sqlite` — `filter_table(sess_id, sync_id, filter_type, filter_desc)`.
Codes are negative; confirmed `-15` = max_size, `-2` = black_ext.

- `db/sys.sqlite` — `session_table` (sessions, `share_name`, `is_daemon_enable`,
`is_mac_on_demand_sync_enable`).

- `session/<id>/conf/blacklist.filter` — rendered per-session filter snapshot
(INI-style `[Common]/[File]/[Directory]/[EA]`), written on GUI filter changes,
NOT regenerated at startup (so its mtime is not a liveness signal).

- `session/<id>/db/{event-db.sqlite,file.db}` — pending events / FileProvider index.

- `log/daemon.log`. Filters load at daemon start ("reload filter for session N");
there is no live reload.

- Restart: `kill` the `SynologyDrive.app/Contents/MacOS/cloud-drive*` PIDs, then
`open "/Applications/Synology Drive Client.app"`. `kill -9` trips approval gates.

- Always back up `data/db` + `data/config` before touching anything.

## Pitfalls (learned the hard way)

1. **You cannot rename/move a tree OUT of a FileProvider domain.** `mv` hangs and
then fails with `Stale NFS file handle`; `cp -a` works but materialises every
file (downloads the contents) and pegs `fileproviderd` at 90-124% CPU with
load >9. Prefer *unlink/delete* (cheap for dataless files) or let the client
remove the mirror.

1. Sessions ship with `is_mac_on_demand_sync_enable: 1`, so the handler logs
`use FileProvider, drop rescan event`: the daemon never scans locally and
locally-created test files never generate events. Do not conclude "the filter
works" from silence.

1. Server-side deletions can crawl (sync_id advancing without local change).
"Connected and polling" does not mean changes are landing.

1. The per-task **Filter is GUI-only**. Remote AppleEvent automation is blocked by
macOS TCC (times out), so it cannot be driven over SSH.

1. Adding a black filter makes Synology *remove matching files from the client*.
Never add a `.venv`/`node_modules` filter before securing a copy.

1. Direct `filter.sqlite` writes are read at daemon start, but the name-to-code
mapping is undocumented. Never guess a code for `black_name` — a wrong one can
exclude far more than intended.

1. **A non-root network mount is read-only.** macOS lets a normal user run
`mount_nfs` only with `-o ro`; drop `ro` and it fails `Operation not permitted`.
`mount_smbfs` needs root outright. So a host with no passwordless sudo cannot be
the *writer* of a share — do not burn time trying to mount read-write there.
Push from a machine that already holds root-mounted RW shares and read the
source over SSH. Writes land as the exporting uid (`1026` here), which matches
the existing NAS files.

1. **macOS ****`rsync`**** is ****`openrsync`****, and it does not quote the remote path.** Spaces
and `&` in a `host:/path` source get re-split by the remote shell
(`zsh: no such file or directory: CPQ/`). Quote the path yourself, or drive the
transfer with `tar` over `ssh` using `shlex.quote`. openrsync also aborts a run
on npm `.bin` symlinks ("empty link"), so it is a poor fit for trees
containing `node_modules`.

1. **Dataless FileProvider placeholders can be unreadable locally.** `stat`
reports the logical size, yet reading the file can fail with
`Stale NFS file handle` / `lseek(SEEK_HOLE)` — a file can be listed, sized and
still not copy. "The local mirror is the truth" has holes; enumerate what
failed instead of assuming the local side is complete.

1. `@eaDir` is Synology **server metadata**, NAS-side only. Filter it out of any
diff, push and delete list — otherwise it dominates as a bogus "NAS-only" set
and looks like a large divergence.

1. A literal backslash-escaped name on the client (e.g.
`Mambu\ Cost\ Margin\ Analysis`) is the fingerprint of an unquoted-space bug in
an earlier script or shell command, not a real folder. Report it as a symptom
of what broke; do not silently move or merge it.

1. **Diagnosing "blind", not "churning".** `Syncer event pool is now empty, no any<br>    event to process for session id N`, repeating while `Set session N's sync_id<br>    to …` creeps forward and files are still absent on the NAS, means the client
believes it has nothing to upload. No queued events ≠ the trees agree — diff
the two sides by manifest before concluding anything is synced.

## Procedure

1. Measure first: `find <dir> -type f | wc -l` per candidate prefix, on the NAS
(source of truth) and on the client.

1. Verify nothing live references the tree (`ps`, launchd plists, docker mounts)
and that a local equivalent exists.

1. Move to a recoverable place. `/volume1` root is NOT writable; use
`/volume1/<Share>/#recycle/<name>` — `#recycle` is system-filtered so it never
syncs, and it is recoverable.

1. Only then remove the client-side mirror — delete, never `mv`.

1. Verify with file counts, `df`, `uptime` and the daemon log.

## Recovery when the client is stuck

`synology_sync_remediate.sh` is the read-only report and filter/cleanup path. When
the client is not *churning* but *blind* — polling while the NAS sits behind the
local mirror — stop waiting for it and reconcile the two sides by hand, pushing
local truth up. Procedure, safety rules and command shapes:
`references/manual-reconcile.md`.

## Manual reconciliation: how to push content to the NAS

When the client is stuck and content must be forced server-side, use these rules.

### Resolve the local<->remote mapping from the client, never from folder names

The local folder name is a lie. `SynologyDrive-Ship` can be synced to
`/volume1/Ship/@Mambu/`, not the Ship root. The authoritative mapping is
`sys.sqlite` `session_table` -> `share_name` + `remote_path` + `sync_folder`:

sqlite3 "$HOME/Library/Application Support/SynologyDrive/data/db/sys.sqlite" 
"select id,share_name,remote_path,sync_folder from session_table;"

Confirm the mapping by diffing top-level entry counts either side before writing
anything. Getting this wrong writes a whole tree to the wrong path.

### The NAS writes its own files — use its SSH, not a mount

`ssh chdwck9NAS` (alias to 192.168.2.6, key `~/.ssh/id_ed25519_nas`, user
`chdwck9` = uid 1026, administrators) gives direct read-write `/volume1`. This is
the **only clean channel**: files are created by the NAS itself, so ownership is
correct, there are no stale NFS handles, and no AppleDouble junk. Prefer it.

- macOS allows a **non-root NFS mount read-only only**; read-write needs root.

- `mount_smbfs` needs root *and* a credential. A rejected SMB guest view plus a
keychain item whose account is `"No user account"` means there is no usable
SMB credential — do not go looking for a password to type.

### Never trust a macOS NFS read view for change detection

The NFS client serves a **stale directory cache**. A tree that holds 29,886 files
has been observed listing as ~258 entries, which makes a complete tree look
almost empty and produces wildly inflated "missing" counts. Any comparison that
reads the destination through `/Volumes/...` is suspect. Read ground truth
directly on the NAS:

ssh chdwck9NAS "cd '<dir>' && find . \( -type f -o -type l \) 
-printf '%y\t%s\t%T@\t%l\t%p\n'"

### `._` AppleDouble files: created by NFS writes and by bsdtar

Two independent sources — know which one you are hitting:

1. **Writing through a macOS NFS mount** creates a `._<name>` sidecar for every
file and directory (even a plain `open().write()`). No tar flag prevents it.
It is inherent to macOS+NFS. Synology Drive does **not** sync `._` files to
clients (verified: 0 in the client mirrors), so they are cosmetic on the NAS.

1. **macOS ****`bsdtar`**** silently embeds AppleDouble members in the archive.**
`tar tf` *hides* them, so the archive looks clean, but GNU tar on the NAS
extracts them as real files — doubling the file count. Fix with
`tar cf - --no-mac-metadata ...` on the creating side. (`--no-xattrs` alone is
not enough.) `--no-mac-metadata` is the verified flag; confirm by counting
files in the destination, not by listing the archive.

### Tooling gotchas that produced wrong answers

- **macOS ****`find`**** has no ****`-printf`****.** `find . -printf ...` on the Mac fails with
`-printf: unknown primary or operator` and yields *zero* rows, which looks like
"nothing changed" instead of an error. Scan the client side with `python3`
(`os.walk` + `os.lstat`), not with `find`. The NAS (GNU findutils) does support
`-printf`, so the two sides need different tooling.

- **`\t`**** survives SSH literally.** `stat -c '%s\t%Y\t%n'` over ssh emits the two
characters backslash-t, so splitting on a real tab parses nothing and every
file looks missing. Use a space and `split(' ', 2)` (size and mtime never
contain spaces, paths may) or a non-space-safe separator.

- Never conclude from a zero-row result without checking stderr.

### Deciding whether a difference is real

- **`.DS_Store`**** is filtered server-side.** Its presence on the client and absence
on the NAS is normal — do not report it as data loss.

- **`du -sh`**** = 0B means the tree is dataless placeholders only.** No content is
on disk, so deleting is cheap and loses nothing.

- **A client-local tree the NAS does not have may be stale, not newer.** Do not
assume the client is the truth. Check mtimes on both sides and look for conflict
copies (`<name>_<HOSTNAME>_<date>_Conflict.md`) — their presence means the mirror
is a divergent mess, not pending work. Where another machine writes the share
directly (the Studio writes `@Edge/.ai` over NFS), the client mirror is the
stale side and pushing it destroys good server content.

- **A client-local tree the NAS does not have is a restore payload**, not a
syncing question. Before restarting a stopped client, check both sides: any
local-only tree gets uploaded on reconnect. Removing the junk (e.g. a second
`config/hermes`, `config/claude`, `config/pi` inside the share) from the
**client** is what prevents the restore; the NAS being already clean is not
enough.

- An item that appears both "missing on the NAS" and "NAS-only" is usually the
same file under a different unicode normalisation (see below).

### Compare name-wise carefully

macOS names are **NFD**, the NAS is **NFC**: `Artūras` differs by bytes only.
Normalise with `unicodedata.normalize('NFC', ...)` before concluding a file is
missing. A name that looks "missing" on the NAS is often the same file, and may
also show up as an unexplained destination-only entry.

### Diagnostics that identify the real fault

- `rescan-handler.cpp: session 'N' use FileProvider, drop rescan event` in
`log/daemon.log` is the root cause of "local changes never upload": the daemon
deliberately drops local rescans and relies on the FileProvider extension. If
that extension is broken the daemon believes it has nothing to send, while the
log otherwise shows only `Syncer event pool is now empty` and a slowly
advancing `sync_id`. This is **not** a queue backlog.

- Port 6690 closed/refused at daemon start (`proto-ui.cpp: failed to connect`)
is usually a startup transient — re-check before concluding the NAS is down.

- A source file marked `compressed,dataless` that fails to read (`Stale NFS file<br>  handle`, `lseek(SEEK_HOLE) failed`) is a **broken FileProvider placeholder on
the client**. "The client is the source of truth" has holes where the client
cannot read its own files; report these explicitly.

### Removing vs recreating a sync task

Removing a sync task in the client does **not** delete the local folder — it
**renames it aside** as `SynologyDrive-<Share> (DD-MM-YYYY HH:MM)`. Those renamed
siblings accumulate (more than one dated copy has been seen) and look alarming
when you list `~/Library/CloudStorage`. They are leftovers, not data loss.

Recreating a task also issues a **new session id** in `session_table` (a recreated
Live/Ship pair went from ids 3/7 to 9/10). So "session 3's `db/file.db` is
missing" is usually *replaced*, not corrupted — check the current `session_table`
and the folder dates before concluding anything was lost.

A stopped client also makes its FileProvider domains look **empty** (only
`.SynologyWorkingDirectory` / `.Trash` remain). Do not read that as deletion, and
check the NAS directly before raising an alarm.

### Writing safely

Adds and updates only — never `--delete`. Verify every file against a source
manifest (size + mtime, or link target) after the write, and keep an ops log.
Back up anything about to be overwritten first. Do not clobber a NAS entry with a
broken local one: an empty local symlink target must not replace a good link.

## References

- `~/.hermes/scripts/synology_sync_remediate.sh` — read-only report,
`--print-filters` (the exclusion list to enter in the GUI), `--clean-junk`.

- `~/.hermes/scripts/wb_sync_nas.py` — parameterised push to the NAS over its own
SSH: manifest diff, overwrite backup, batched tar transfer, per-file verify.

- `references/manual-reconcile.md` — enumerate the local↔NAS delta by manifest and
push local truth up safely (adds/updates only; overwrites backed up first).

- `scripts/synology_manifest.py` — emit a JSONL manifest (type, relpath, size,
mtime, link target) for any tree; the compare primitive for that recipe.