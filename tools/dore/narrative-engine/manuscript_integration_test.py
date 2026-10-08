#!/usr/bin/env python3
"""Offline Golden Gate regression test using actual manuscript, not a mock model."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from narrative import extract, audit
from revision_loop import prepare, critique
from training_runner import build_exercises

MANUSCRIPT = ROOT / "docs/projects/watch-city-vol00/manuscript/JERUSALEM-BUILD.md"

def main():
    source = MANUSCRIPT.read_text(encoding="utf-8")
    golden_gate = extract(source)
    assert len(golden_gate) > 1000, "Golden Gate chapter unexpectedly short"
    assert "1099" in golden_gate, "Crusade chronology missing"
    assert "金門" in golden_gate, "Golden Gate topic missing"
    task = prepare("final-assault", golden_gate)
    assert task["scene_id"] == "final-assault"
    assert len(build_exercises()) == 36
    inventory = audit(golden_gate)
    assert inventory["paragraphs"] > 10
    # Explicitly prohibit publication of an unreviewed candidate.
    candidate = {"scene_id": "final-assault", "draft": "七月十五日，攻城塔逼近城牆。守軍抵抗。",
                 "evidence": [{"category": "documented", "claim": "July 15 breach",
                               "source": "Gesta Francorum"}], "reviewed": False}
    assert critique(candidate)["gate"]["status"] == "BLOCK"
    print(json.dumps({"status": "PASS", "source": str(MANUSCRIPT.relative_to(ROOT)),
                      "section_characters": len(golden_gate),
                      "paragraphs": inventory["paragraphs"],
                      "exercise_count": 36, "unreviewed_candidate": "BLOCK"},
                     ensure_ascii=False))

if __name__ == "__main__":
    main()
