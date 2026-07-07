#!/usr/bin/env bash

set -euo pipefail

VENV_DIR="$CLAUDE_PLUGIN_DATA/.venv"

if [ -x "$VENV_DIR/bin/python" ]; then
  exit 0
fi

python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --quiet --disable-pip-version-check -r "$CLAUDE_PLUGIN_ROOT/skills/bonk-a-dingus/scripts/requirements.txt"
