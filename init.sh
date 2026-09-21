#!/usr/bin/env bash
# @Edge/.ai/init.sh — symlinks local AI config dirs to Synology
# Run: bash ~/.ai-init.sh

set -euo pipefail

SELF_DIR="$(cd "$(dirname "$0")" && pwd)"

symlink() {
  local target="$1" link="$2"
  if readlink "$link" 2>/dev/null | grep -qF "$SELF_DIR"; then
    echo "  ✓ $link already points to Synology"
  elif [ -e "$link" ]; then
    echo "  ⚠ $link exists ($(stat -f '%Y' "$link" 2>/dev/null || echo "file")) — skipping"
  else
    ln -sfn "$target" "$link"
    echo "  ✓ $link → $(realpath "$target")"
  fi
}

echo "=== AI Config Symlinks ==="

symlink "$SELF_DIR/config/claude"  ~/.claude
symlink "$SELF_DIR/config/hermes"  ~/.hermes
symlink "$SELF_DIR/config/goose"   ~/.config/goose
symlink "$SELF_DIR/config/continue" ~/.continue
symlink "$SELF_DIR/resources/resources.md" ~/.resources.md
symlink "$SELF_DIR/skills"                ~/.Agents/skills/user-skills

echo "=== Done ==="
