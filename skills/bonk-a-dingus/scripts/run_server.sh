#!/usr/bin/env bash
set -euo pipefail

exec "${CLAUDE_PLUGIN_DATA}/.venv/bin/python" "${CLAUDE_PLUGIN_ROOT}/skills/bonk-a-dingus/scripts/mcp_server.py"
