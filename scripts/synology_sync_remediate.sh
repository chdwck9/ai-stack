#!/usr/bin/env bash
# synology_sync_remediate.sh
# Purpose: reduce Synology Drive sync churn on the NAS shares.
# Created by Clarity for Ship task "Unstuck synology drive" (2026-10-28).
#
# SAFETY: default mode is READ-ONLY (report). Nothing is deleted or moved
# unless you pass an explicit --flag. Every destructive phase prints the
# exact command it will run and waits for you to type YES.
#
# Usage:
#   synology_sync_remediate.sh                 # report only
#   synology_sync_remediate.sh --report        # same as above
#   synology_sync_remediate.sh --clean-junk    # (destructive) remove ._* / .DS_Store / @eaDir
#   synology_sync_remediate.sh --print-filters # print the Synology Drive Client filter list to apply
#   synology_sync_remediate.sh --all           # report + print-filters (still no deletes)

set -uo pipefail

SHARES=(/Volumes/Live /Volumes/Love /Volumes/Play /Volumes/Ship /Volumes/temp)
MODE="report"
case "${1:-}" in
  --clean-junk)    MODE="clean" ;;
  --print-filters) MODE="filters" ;;
  --all)           MODE="report_filters" ;;
  --report|"")     MODE="report" ;;
  *) echo "unknown flag: $1"; exit 2 ;;
esac

say() { printf '%s\n' "$*"; }
hdr() { printf '\n=== %s ===\n' "$*"; }

report() {
  hdr "macOS junk inside the synced shares"
  for s in "${SHARES[@]}"; do
    [ -d "$s" ] || continue
    local appledouble dsstore eadir smbdel
    appledouble=$(find "$s" -name '._*' -not -path '*/#recycle/*' 2>/dev/null | wc -l | tr -d ' ')
    dsstore=$(find "$s" -name '.DS_Store' -not -path '*/#recycle/*' 2>/dev/null | wc -l | tr -d ' ')
    eadir=$(find "$s" -type d -name '@eaDir' -not -path '*/#recycle/*' 2>/dev/null | wc -l | tr -d ' ')
    smbdel=$(find "$s" -name '.smbdelete*' 2>/dev/null | wc -l | tr -d ' ')
    printf '%-16s  ._*:%-7s .DS_Store:%-6s @eaDir:%-6s .smbdelete*:%s\n' "$s" "$appledouble" "$dsstore" "$eadir" "$smbdel"
  done

  hdr "container / tool runtime data living inside the synced Live share"
  for p in \
    /Volumes/Live/@Edge/.ai/data/openwebui/cache \
    /Volumes/Live/@Edge/.ai/data/openwebui/vector_db \
    /Volumes/Live/@Edge/.ai/data/anythingllm \
    /Volumes/Live/@Edge/.ai/data/searxng \
    /Volumes/Live/@Edge/.ai/config/hermes \
    /Volumes/Live/@Edge/.ai/config/claude \
    /Volumes/Live/@Edge/.ai/models \
    /Volumes/Live/@Edge/.ai/.git \
    /Volumes/Live/@Edge/.media/jellyfin-studio \
    /Volumes/Live/@Edge/.data ; do
    [ -e "$p" ] && printf '%-58s %s\n' "$p" "$(du -sh "$p" 2>/dev/null | cut -f1)"
  done
}

print_filters() {
  hdr "Synology Drive Client — apply per sync task (Edit task -> Filter / Selective Sync)"
  cat <<'EOF'
Do not sync files/folders with these NAMES (folder-name patterns work):
    .venv  venv  node_modules  __pycache__  .mypy_cache  .pytest_cache
    .git  .svn  .hg
    @eaDir  #recycle  .Trash  .SynologyWorkingDirectory
    .DS_Store  ._*  .smbdelete*  .fseventsd  .Spotlight-V100
    @Edge/.media   @Edge/.ai/data   @Edge/.ai/config   @Edge/.ai/models
    @Edge/.ai/state  @Edge/.ai/archive   @Edge/.data

Do not sync files with these EXTENSIONS:
    db  db-wal  db-shm  log  tmp  swp  part  lock  cache

Do not sync files larger than:  500 MB   (Play / Ship hold the media libraries)

Selective Sync (recommended for Play and Ship):
    sync only the subfolders that are actually needed on this machine.
EOF
  hdr "WORKBOX (NL-LPT-HKC9H7FT4J) — the small-file bomb lives here"
  cat <<'EOF'
Verified 2026-10-28: on the work laptop, inside its Synology Drive sync task:
    ~/Library/CloudStorage/SynologyDrive-Ship/Mambu Cost Margin Analysis/.venv
        -> 729 MB, 27,004 files   <-- worst case for the change queue
Also: system volume down to ~19 GiB free; a stale orphan sync folder
    ~/Library/CloudStorage/SynologyDrive-Live (02-03-2026 10:57)

Fix (highest value first):
  1. Pause the Ship sync task in Synology Drive Client on the workbox.
  2. Move the venv OUT of the synced tree and rebuild it locally:
        python -m venv ~/venvs/cost-margin && ~/venvs/cost-margin/bin/pip install -r ...
     (a venv is disposable and regenerable from pyproject.toml / requirements)
  3. Free disk on the workbox (~19 GiB free is marginal for sync retries).
  4. Resume sync.
EOF

  hdr "Structural fix (bigger win than filters)"
  cat <<'EOF'
Move these OFF the Synology-Drive-synced Live share:
  * /Volumes/Live/@Edge/.ai/data/openwebui/cache   (888 MB model cache)
  * /Volumes/Live/@Edge/.ai/data/openwebui/vector_db + webui.db  (live SQLite)
  * /Volumes/Live/@Edge/.ai/config/hermes          (568 MB — a second Hermes checkout)
  * /Volumes/Live/@Edge/.ai/config/claude          (188 MB)
  * /Volumes/Live/@Edge/.media/jellyfin-studio     (stale Jellyfin config, ~5k files)
Target: local disk (/var/lib/docker volumes or ~/docker/.data) or a NAS share
that is NOT attached to Synology Drive. Then update .ai/docker-compose.yaml binds.
EOF
}

clean_junk() {
  hdr "DESTRUCTIVE PHASE — removing macOS sidecar junk"
  say "These are metadata sidecars only (._* AppleDouble, .DS_Store, @eaDir, .smbdelete*)."
  say "Deleting them loses Finder/xattr metadata for the affected files, not file contents."
  say "The exact command that will run:"
  say
  for s in "${SHARES[@]}"; do
    [ -d "$s" ] || continue
    say "  find '$s' -not -path '*/#recycle/*' \\( -name '._*' -o -name '.DS_Store' -o -name '.smbdelete*' \\) -type f -delete"
    say "  find '$s' -type d -name '@eaDir' -not -path '*/#recycle/*' -prune -exec rm -rf {} +"
  done
  say
  printf 'Type YES to proceed: '
  read -r ans
  [ "$ans" = "YES" ] || { say "aborted."; exit 1; }
  for s in "${SHARES[@]}"; do
    [ -d "$s" ] || continue
    find "$s" -not -path '*/#recycle/*' \( -name '._*' -o -name '.DS_Store' -o -name '.smbdelete*' \) -type f -delete 2>/dev/null
    find "$s" -type d -name '@eaDir' -not -path '*/#recycle/*' -prune -exec rm -rf {} + 2>/dev/null
  done
  say "done."
}

case "$MODE" in
  report)         report ;;
  report_filters) report; print_filters ;;
  filters)        print_filters ;;
  clean)          report; clean_junk ;;
esac
