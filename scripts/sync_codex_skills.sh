#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_SOURCE="$REPO_ROOT/skills"
DEFAULT_TARGET="$HOME/.codex/skills"

SOURCE_DIR="$DEFAULT_SOURCE"
TARGET_DIR="$DEFAULT_TARGET"
DRY_RUN=0
RELINK_BROKEN=1
SHARED_DIRS=("_shared")

usage() {
  cat <<USAGE
Usage: $(basename "$0") [options]

Create symlinks from each skill in SOURCE to TARGET without overwriting existing files.

Options:
  --source <dir>      Source directory containing skill folders (default: $DEFAULT_SOURCE)
  --target <dir>      Codex skills directory (default: $DEFAULT_TARGET)
  --shared-dir <name> Include a shared directory even without SKILL.md (repeatable)
  --dry-run           Show what would be done without changing anything
  --no-relink-broken  Do not relink broken symlinks in target
  -h, --help          Show this help
USAGE
}

log() {
  printf '%s\n' "$*"
}

run() {
  if (( DRY_RUN )); then
    printf '[dry-run] %s\n' "$*"
  else
    eval "$@"
  fi
}

action_label() {
  local live_label="$1"
  local dry_label="$2"
  if (( DRY_RUN )); then
    printf '%s' "$dry_label"
  else
    printf '%s' "$live_label"
  fi
}

is_shared_dir() {
  local name="$1"
  local shared
  for shared in "${SHARED_DIRS[@]}"; do
    if [[ "$name" == "$shared" ]]; then
      return 0
    fi
  done
  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      SOURCE_DIR="$2"
      shift 2
      ;;
    --target)
      TARGET_DIR="$2"
      shift 2
      ;;
    --shared-dir)
      SHARED_DIRS+=("$2")
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --no-relink-broken)
      RELINK_BROKEN=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      log "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
done

if [[ ! -d "$SOURCE_DIR" ]]; then
  log "Source directory not found: $SOURCE_DIR"
  exit 1
fi

run "mkdir -p \"$TARGET_DIR\""

linked=0
skipped=0
relinked=0

while IFS= read -r -d '' skill_dir; do
  skill_name="$(basename "$skill_dir")"

  if [[ ! -f "$skill_dir/SKILL.md" ]] && ! is_shared_dir "$skill_name"; then
    log "Skip (missing SKILL.md): $skill_name"
    ((skipped+=1))
    continue
  fi

  target_path="$TARGET_DIR/$skill_name"

  if [[ -L "$target_path" ]]; then
    current_target="$(readlink "$target_path")"
    if [[ "$current_target" == "$skill_dir" ]]; then
      log "Skip (already linked): $skill_name"
      ((skipped+=1))
      continue
    fi

    if [[ ! -e "$target_path" && $RELINK_BROKEN -eq 1 ]]; then
      run "ln -sfn \"$skill_dir\" \"$target_path\""
      log "$(action_label "Relinked broken symlink" "Would relink broken symlink"): $skill_name"
      ((relinked+=1))
      continue
    fi

    log "Skip (different symlink already exists): $skill_name -> $current_target"
    ((skipped+=1))
    continue
  fi

  if [[ -e "$target_path" ]]; then
    log "Skip (path already exists): $skill_name"
    ((skipped+=1))
    continue
  fi

  run "ln -s \"$skill_dir\" \"$target_path\""
  log "$(action_label "Linked" "Would link"): $skill_name"
  ((linked+=1))
done < <(find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

log ""
log "Done. linked=$linked relinked=$relinked skipped=$skipped"
