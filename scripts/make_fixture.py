#!/usr/bin/env python3
"""Change for your project: nothing. Generates a generic labelled-record fixture.
Usage: python scripts/make_fixture.py --rows 300 --out fixtures/triage_messages_sample.jsonl
"""
import argparse
import json
import random
from pathlib import Path

random.seed(11)
TEMPLATES = {
    "triage": ["symptom check", "general question", "follow-up needed"],
    "logistics_lookup": ["track delivery", "shipment delay", "where is my order"],
    "catalog_mismatch": ["listing photo mismatch", "wrong sku listed", "catalog title wrong"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=300)
    ap.add_argument("--out", default="fixtures/triage_messages_sample.jsonl")
    args = ap.parse_args()

    labels = list(TEMPLATES.keys())
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        # keep gold ids T-001..T-003 stable for tests
        gold = [
            {"id": "T-001", "text": "fever", "label": "triage"},
            {"id": "T-002", "text": "track delivery", "label": "logistics_lookup"},
            {"id": "T-003", "text": "listing photo mismatch", "label": "catalog_mismatch"},
        ]
        for row in gold:
            f.write(json.dumps(row) + "\n")
        for i in range(4, args.rows + 1):
            label = random.choice(labels)
            text = random.choice(TEMPLATES[label])
            f.write(json.dumps({"id": f"T-{i:03d}", "text": text, "label": label}) + "\n")
    print(f"wrote {args.rows} rows to {out_path}")


if __name__ == "__main__":
    main()
