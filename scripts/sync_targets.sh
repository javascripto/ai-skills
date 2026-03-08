#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<USAGE
Usage: $(basename "$0") <target|all> [sync options]

Targets:
  codex         Sync to ~/.codex/skills
  agents        Sync to ~/.agents/skills
  claude        Sync to ~/.claude/skills
  antigravity   Sync to ~/.gemini/antigravity/skills
  all           Sync all targets above

Examples:
  $(basename "$0") codex
  $(basename "$0") agents --dry-run
  $(basename "$0") claude --dry-run
  $(basename "$0") all --dry-run
USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

TARGET_KEY="$1"
shift

sync_target() {
  local target_dir="$1"
  shift
  "$SCRIPT_DIR/sync_skills.sh" --target "$target_dir" "$@"
}

case "$TARGET_KEY" in
  codex)
    sync_target "$HOME/.codex/skills" "$@"
    ;;
  agents)
    sync_target "$HOME/.agents/skills" "$@"
    ;;
  claude)
    sync_target "$HOME/.claude/skills" "$@"
    ;;
  antigravity)
    sync_target "$HOME/.gemini/antigravity/skills" "$@"
    ;;
  all)
    sync_target "$HOME/.codex/skills" "$@"
    sync_target "$HOME/.agents/skills" "$@"
    sync_target "$HOME/.claude/skills" "$@"
    sync_target "$HOME/.gemini/antigravity/skills" "$@"
    ;;
  -h|--help)
    usage
    ;;
  *)
    printf 'Unknown target: %s\n\n' "$TARGET_KEY"
    usage
    exit 1
    ;;
esac
