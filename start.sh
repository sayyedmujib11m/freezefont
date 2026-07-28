#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

if [[ -x ".venv/bin/uvicorn" ]]; then
    UVICORN=".venv/bin/uvicorn"
else
    UVICORN="uvicorn"
fi

exec "$UVICORN" backend.app:app --host "$HOST" --port "$PORT"
