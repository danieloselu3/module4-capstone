"""Starter-pack gate. Checks artefact roles and path existence only, not domain words."""
import json
import sys
from pathlib import Path

REQUIRED_ARTEFACTS = {"api", "tool", "pins", "smoke"}


def main() -> int:
    rows = json.loads(Path('integration_map.json').read_text())
    artefacts = {r['artefact'] for r in rows}
    if not REQUIRED_ARTEFACTS.issubset(artefacts):
        print('FAIL missing artefacts', REQUIRED_ARTEFACTS - artefacts)
        return 1
    for r in rows:
        p = Path(r.get('path') or '')
        if not p.exists():
            print('FAIL missing path', r)
            return 1
    print('integration map OK', len(rows))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
