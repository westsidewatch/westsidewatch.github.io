#!/usr/bin/env python3
"""Repeatable local revision rounds with evidence gate and immutable history."""
import argparse
import hashlib
import json
from pathlib import Path
from revision_loop import critique, prepare

def run_round(scene_id, source, submission, history):
    if not isinstance(history, list):
        raise ValueError("History must be a JSON list")
    if submission.get("scene_id") != scene_id:
        raise ValueError("Candidate scene mismatch")
    report = critique(submission)
    digest = hashlib.sha256(submission.get("draft", "").encode("utf-8")).hexdigest()
    previous = {x["draft_sha256"] for x in history}
    if digest in previous:
        raise ValueError("Identical draft already evaluated; revise before another round")
    entry = {"round": len(history) + 1, "scene_id": scene_id, "draft_sha256": digest,
             "candidate": submission, "assessment": report,
             "ready_for_human_review": report["gate"]["status"] == "REVIEW_READY"}
    return history + [entry]

def next_task(scene_id, source, history):
    task = prepare(scene_id, source)
    if history:
        last = history[-1]
        task["revision_feedback"] = {"round": last["round"], "errors": last["assessment"]["gate"]["errors"],
                                     "warnings": last["assessment"]["gate"]["warnings"],
                                     "revision_tasks": last["assessment"]["revision_tasks"],
                                     "previous_draft": last["candidate"]["draft"]}
    return task

def test():
    src = "## 金門\n\n六月十三日，攻城失敗。"
    a = {"scene_id": "failed-assault", "draft": "六月十三日，士兵攻城。", "evidence": [
         {"category": "documented", "claim": "Assault", "source": "Gesta Francorum"}], "reviewed": False}
    h = run_round("failed-assault", src, a, [])
    assert len(h) == 1 and h[0]["ready_for_human_review"] is False
    assert next_task("failed-assault", src, h)["revision_feedback"]["round"] == 1
    try:
        run_round("failed-assault", src, a, h)
        raise AssertionError("duplicate must fail")
    except ValueError:
        pass
    b = {**a, "draft": "六月十三日，士兵沿梯子攻城，守軍抵抗。", "reviewed": True}
    h = run_round("failed-assault", src, b, h)
    assert len(h) == 2 and h[-1]["ready_for_human_review"]
    print("PASS: two rounds, revision feedback, duplicate prevention, evidence review gate")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=("round", "next", "test"))
    p.add_argument("--scene", default="failed-assault")
    p.add_argument("--source")
    p.add_argument("--submission")
    p.add_argument("--history")
    a = p.parse_args()
    if a.command == "test":
        test()
        return
    if not a.source or not a.history:
        p.error("--source and --history required")
    source = Path(a.source).read_text(encoding="utf-8")
    path = Path(a.history)
    history = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    if a.command == "next":
        print(json.dumps(next_task(a.scene, source, history), ensure_ascii=False, indent=2))
        return
    if not a.submission:
        p.error("--submission required for round")
    submission = json.loads(Path(a.submission).read_text(encoding="utf-8"))
    updated = run_round(a.scene, source, submission, history)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"round": len(updated), "status": updated[-1]["assessment"]["gate"]["status"]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
