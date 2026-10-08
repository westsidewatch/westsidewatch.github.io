#!/usr/bin/env python3
"""Run evidence-aware editorial training tasks without external APIs."""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQUIRED = ("scene_id", "draft", "evidence", "reviewed")
CATEGORIES = {"documented", "contextual", "unsupported"}

def load_curriculum():
    return json.loads((HERE / "training-curriculum.json").read_text(encoding="utf-8"))

def load_scenes():
    return json.loads((HERE / "golden-gate-scene-ledger.json").read_text(encoding="utf-8"))["scenes"]

def build_exercises():
    modules = load_curriculum()["modules"]
    scenes = load_scenes()
    return [{"exercise_id": m["id"] + ":" + s["id"],
             "module": m["id"], "scene_id": s["id"],
             "task": m["exercise"], "criteria": m["rubric"],
             "scene": s} for m in modules for s in scenes]

def assess(submission):
    missing = [key for key in REQUIRED if key not in submission]
    if missing:
        return {"status": "INVALID", "errors": ["missing:" + k for k in missing]}
    scene_ids = {s["id"] for s in load_scenes()}
    errors = []
    if submission["scene_id"] not in scene_ids:
        errors.append("unknown_scene")
    if not isinstance(submission["draft"], str) or not submission["draft"].strip():
        errors.append("empty_draft")
    evidence = submission["evidence"]
    if not isinstance(evidence, list) or not evidence:
        errors.append("missing_evidence_ledger")
    else:
        for i, item in enumerate(evidence):
            if not isinstance(item, dict) or item.get("category") not in CATEGORIES or not item.get("claim"):
                errors.append("invalid_evidence_entry:" + str(i))
            elif item["category"] == "documented" and not item.get("source"):
                errors.append("documented_claim_without_source:" + str(i))
            elif item["category"] == "unsupported":
                errors.append("unsupported_claim:" + str(i))
    if submission["reviewed"] is not True:
        errors.append("human_review_required")
    draft = submission["draft"] if isinstance(submission["draft"], str) else ""
    warnings = []
    if re.search(r"[「『][^」』]{2,}[」』]", draft):
        warnings.append("verify_all_quoted_material_against_source")
    if len(draft) < 160:
        warnings.append("short_scene_check_specificity")
    return {"status": "BLOCK" if errors else "REVIEW_READY", "errors": errors,
            "warnings": warnings, "characters": len(draft),
            "note": "REVIEW_READY is not a factual certification or literary quality score."}

def tests():
    exercises = build_exercises()
    assert len(exercises) == 36, len(exercises)
    sample = {"scene_id": "failed-assault", "draft": "戈弗雷在城下看着梯子。", "evidence": [
        {"category": "documented", "claim": "攻城梯不足", "source": "Gesta Francorum"}], "reviewed": True}
    assert assess(sample)["status"] == "REVIEW_READY"
    assert assess({**sample, "reviewed": False})["status"] == "BLOCK"
    assert assess({**sample, "evidence": [{"category": "unsupported", "claim": "invented"}]})["status"] == "BLOCK"
    assert assess({**sample, "scene_id": "not-real"})["status"] == "BLOCK"
    assert assess({**sample, "evidence": [{"category": "documented", "claim": "no source"}]})["status"] == "BLOCK"
    print("PASS: 36 exercises; valid submission; missing review; unsupported claim; invalid scene; missing source")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=("exercises", "assess", "test"))
    p.add_argument("file", nargs="?")
    a = p.parse_args()
    if a.command == "test":
        tests()
    elif a.command == "exercises":
        print(json.dumps(build_exercises(), ensure_ascii=False, indent=2))
    else:
        if not a.file:
            p.error("submission JSON path required")
        print(json.dumps(assess(json.loads(Path(a.file).read_text(encoding="utf-8"))), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
