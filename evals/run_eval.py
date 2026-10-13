#!/usr/bin/env python3
"""Prints a score against evals/golden.jsonl (starter pack). Adapted: lists every miss, and
--min makes it a CI gate (exit 1 below the threshold), the Week 8 eval-gate habit."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agents.router import route  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="evals/golden.jsonl")
    ap.add_argument("--min", type=float, default=0.0, help="fail (exit 1) below this score")
    args = ap.parse_args()
    rows = [json.loads(line) for line in Path(args.path).read_text().splitlines() if line.strip()]
    misses = [(r["id"], r["text"], r["expected_label"], route(r["text"])) for r in rows
              if route(r["text"]) != r["expected_label"]]
    correct = len(rows) - len(misses)
    score = correct / len(rows) if rows else 0.0
    for m in misses:
        print("  miss", m)
    print(f"golden-set score: {correct}/{len(rows)} = {score:.2f}")
    if score < args.min:
        print(f"EVAL GATE FAIL: {score:.2f} < {args.min:.2f}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
