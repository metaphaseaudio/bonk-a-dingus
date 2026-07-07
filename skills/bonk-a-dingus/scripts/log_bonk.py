#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
import whatthepatch as wtp
from whatthepatch.patch import diffobj


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

        sys.stderr.write(args.correction)
        sys.stderr.write(f"\nApply correction to {out_path}? [y/N]: ")
        sys.stderr.flush()
        try:
            with open("/dev/tty", "r") as tty:
                answer = tty.readline().strip()
        except OSError:
            sys.exit("No TTY available. Correction denied.")
        if answer.lower() not in ("y", "yes"):
            sys.exit("Correction rejected.")

        patched = wtp.apply_diff(parsed, in_path.read_text())
        out_path.write_text("\n".join(patched) + "\n")

    entry = {
        "timestamp": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "rules": args.rules,
        "what": args.what,
        "why": args.why,
        "correction": args.correction
    }

    entries = []

    if LOG_PATH.exists():
        entries = json.loads(LOG_PATH.read_text())

    entries.append(entry)

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(entries, indent=4) + "\n", encoding="utf-8")
