#!/usr/bin/env bash
# Stop running `say` processes for the Fernanda voice on macOS.

if [ "$(uname)" != "Darwin" ]; then
  echo "This script is intended for macOS (Darwin)." >&2
  exit 1
fi

# Try to kill only processes that include the Fernanda voice flag.
pkill -f 'say -v "Fernanda"' && exit 0

# Fallback: kill all `say` processes if none matched specifically.
echo "No specific 'Fernanda' say process found; attempting to kill all 'say' processes." >&2
killall say 2>/dev/null || { echo "No running 'say' processes found." >&2; exit 1; }
