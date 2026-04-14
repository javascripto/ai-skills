#!/usr/bin/env bash
# Simple wrapper to make the `say` usage consistent for this skill.

VOICE="Fernanda"
RATE=300

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 \"Texto que será lido\"" >&2
  exit 1
fi

TEXT="$*"

say -v "${VOICE}" -r "${RATE}" "${TEXT}"
