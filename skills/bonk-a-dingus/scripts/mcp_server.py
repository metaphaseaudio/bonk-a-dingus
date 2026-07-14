#!/usr/bin/env python3
from datetime import datetime
import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP
import whatthepatch as wtp

LOG_PATH = Path.home() / ".claude" / "dingus_log.json"

mcp = FastMCP("bonk-a-dingus")


@mcp.tool()
def log_bonk(rules: str, what: str, why: str, correction: str | None = None) -> str:
    if correction is not None:
        parsed = list(wtp.parse_patch(correction))[0]
        old_path = parsed.header.old_path
        new_path = parsed.header.new_path
        if not (old_path.startswith("/") and new_path.startswith("/")):
            raise ValueError(
                f"correction header paths must be plain absolute paths, no a/ or b/ prefix "
                f"(e.g. '--- /full/path/to/CLAUDE.md'); got old_path={old_path!r} new_path={new_path!r}"
            )
        in_path = Path(old_path)
        out_path = Path(new_path)
        patched = wtp.apply_diff(parsed, in_path.read_text())
        out_path.write_text("\n".join(patched) + "\n")

    entry = {
        "timestamp": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "rules": rules,
        "what": what,
        "why": why,
        "correction": correction,
    }

    entries = []
    if LOG_PATH.exists():
        entries = json.loads(LOG_PATH.read_text())
    entries.append(entry)

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(entries, indent=4) + "\n", encoding="utf-8")
    return "Violation logged, ya dingus."


if __name__ == "__main__":
    mcp.run()
