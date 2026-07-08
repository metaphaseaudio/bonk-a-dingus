#!/usr/bin/env python3
import argparse
from datetime import datetime
import json
import logging
from pathlib import Path
import subprocess
import sys

import whatthepatch as wtp
from whatthepatch.patch import diffobj

logging.basicConfig(level=logging.INFO)


LOG_PATH = Path.home() / ".claude" / "dingus_log.json"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log the bonking of an agent")
    parser.add_argument("--rules", required=True, help="the text of the rule(s) violated")
    parser.add_argument("--what", required=True, help="the output which violated the rules")
    parser.add_argument("--why", required=True, help="why the violated output was produced")
    parser.add_argument("--correction", required=False, default=None, help="rule changes as a patch diff")

    args = parser.parse_args()

    if args.correction:
        parsed: diffobj = list(wtp.parse_patch(args.correction))[0]
        in_path = Path(parsed.header.old_path).expanduser()
        out_path = Path(parsed.header.new_path).expanduser()

        prompt = (
            f'display dialog "Apply this bonk-a-dingus rule correction to {out_path}?" '
            'buttons {"Deny", "Apply"} default button "Deny" '
            'with title "bonk-a-dingus"'
        )
        result = subprocess.run(["osascript", "-e", prompt], capture_output=True, text=True, check=True)

        if "button returned:Apply" not in result.stdout:
            sys.exit("Correction rejected.")

        patched = wtp.apply_diff(parsed, in_path.read_text())
        out_path.write_text("\n".join(patched) + "\n")

    entry = {
        "timestamp": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "rules": args.rules,
        "what": args.what,
        "why": args.why,
        "correction": args.correction,
    }

    entries = []

    if LOG_PATH.exists():
        entries = json.loads(LOG_PATH.read_text())

    entries.append(entry)

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(entries, indent=4) + "\n", encoding="utf-8")
    logging.info("Violation log complete, ya dingus.")
