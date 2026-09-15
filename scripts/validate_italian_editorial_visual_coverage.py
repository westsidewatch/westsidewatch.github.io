#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "static" / "dore-design"
grammars = json.loads((ROOT / "italian-editorial-grammars.v1.json").read_text())
evidence = json.loads((ROOT / "italian-editorial-evidence.v1.json").read_text())

items = evidence.get("items", [])
missing = []
covered = 0
for family in grammars.get("families", []):
    for era in family.get("eras", []):
        for module, tokens in era.get("grammar", {}).items():
            for token in tokens:
                matches = [x for x in items if x.get("family") == family["id"] and x.get("era") == era["id"] and token in x.get("tokens", []) and x.get("image")]
                if matches:
                    covered += 1
                else:
                    missing.append(f"{family['id']} / {era['id']} / {module} / {token}")

if missing:
    print("FAIL: selectable grammar tokens without visual evidence:")
    for row in missing:
        print(" -", row)
    raise SystemExit(1)

print(f"PASS: {covered} selectable canonical grammar tokens resolve to at least one historical visual evidence image.")
