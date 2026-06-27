#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PORT="${PORT:-8765}"
URL="http://127.0.0.1:${PORT}"

if command -v python3 >/dev/null 2>&1; then
  PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON="python"
else
  echo "Python is required to start the prompt dashboard." >&2
  exit 1
fi

if ! "$PYTHON" - <<PY >/dev/null 2>&1
import socket
s = socket.socket()
try:
    s.connect(("127.0.0.1", int("$PORT")))
    raise SystemExit(0)
except OSError:
    raise SystemExit(1)
finally:
    s.close()
PY
then
  nohup "$PYTHON" "$ROOT/prompt-dashboard/server.py" --port "$PORT" >/tmp/content-strategy-prompt-dashboard.log 2>&1 &
  sleep 1
fi

if command -v open >/dev/null 2>&1; then
  open "$URL"
else
  echo "$URL"
fi
