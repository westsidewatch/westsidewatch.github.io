#!/usr/bin/env python3
"""Run one exact Italian Editorial Atlas evidence image through DORÉ local vision."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from editorial_visual_provider import observe, provenance
from italian_editorial_evidence_bridge import observe_atlas_evidence

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "static" / "dore-design" / "italian-editorial-evidence.v1.json"


def load_item(evidence_id: str) -> dict:
    data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    matches = [x for x in data.get("items", []) if x.get("id") == evidence_id]
    if len(matches) != 1:
        raise SystemExit(f"exact evidence id required; found {len(matches)} for {evidence_id!r}")
    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_id")
    parser.add_argument("--output")
    args = parser.parse_args()
    item = load_item(args.evidence_id)
    p = provenance()
    result = observe_atlas_evidence(
        item,
        observe,
        provider_id=p["providerId"],
        provider_kind=p["providerKind"],
    )
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
