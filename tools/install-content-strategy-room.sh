#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/codex-skills/content-strategy-room"
DEST="${CODEX_HOME:-$HOME/.codex}/skills/content-strategy-room"

if [ ! -d "$SRC" ]; then
  echo "Missing skill source: $SRC" >&2
  exit 1
fi

mkdir -p "$DEST"
cp -R "$SRC/." "$DEST/"

echo "Installed content-strategy-room to $DEST"
echo "Restart Codex or open a new thread if the skill is not detected immediately."
