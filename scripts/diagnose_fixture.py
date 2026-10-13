#!/usr/bin/env python3
"""Change for your project: nothing. Compares fixture labels against agents.router.route()."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agents.router import route


def main():
    if len(sys.argv) < 2:
        print("usage: diagnose_fixture.py <path-to-jsonl>")
        return 1
    path = Path(sys.argv[1])
    bad = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        got = route(row["text"])
        if got != row["label"]:
            bad.append((row["id"], row["label"], got))
    if bad:
        print("FAIL disagreements:", bad)
        return 1
    print("diagnose OK, all rows agree with router")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
