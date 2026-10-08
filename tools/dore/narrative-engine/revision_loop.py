#!/usr/bin/env python3
"""Portable revision loop: prepare prompt, ingest candidate, audit, and request revision.
No API keys, network calls or automatic manuscript writes.
"""
import argparse
import json
import re
from pathlib import Path
from training_runner import assess, load_scenes, load_curriculum

def prepare(scene_id, source):
    scenes = {s["id"]: s for s in load_scenes()}
    if scene_id not in scenes:
        raise ValueError("Unknown scene: " + scene_id)
    scene = scenes[scene_id]
    return {
        "scene_id": scene_id,
        "instruction": "Write historically grounded narrative nonfiction in Traditional Chinese. Build scene through observable action, physical obstacles, character decisions and consequences. Do not invent quotations, private thoughts or unsupported precision. Return draft and claim-level evidence ledger.",
        "scene": scene,
        "source_excerpt": source,
        "methods": [{"id": m["id"], "skill": m["skill"], "rubric": m["rubric"]} for m in load_curriculum()["modules"]],
        "output_schema": {"scene_id": scene_id, "draft": "string", "evidence": [{"category": "documented|contextual|unsupported", "claim": "string", "source": "required for documented"}], "reviewed": False}
    }

def critique(submission):
    result = assess(submission)
    draft = submission.get("draft", "")
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", draft) if p.strip()]
    metrics = {"paragraphs": len(paragraphs), "dialogue_markers": len(re.findall(r"[「『]", draft)),
               "chronology_markers": len(re.findall(r"10[0-9]{2}年|六月|七月", draft)),
               "physical_action_markers": sum(draft.count(v) for v in ("搬", "推", "爬", "攻", "射", "填", "退", "渡", "走")),
               "characters": len(draft)}
    suggestions = []
    if metrics["physical_action_markers"] == 0:
        suggestions.append("Replace static exposition with a source-supported observable action.")
    if metrics["chronology_markers"] == 0:
        suggestions.append("Anchor the scene in a sourced time or sequence.")
    if len(paragraphs) < 2:
        suggestions.append("Check scene progression: situation, obstacle, action, consequence.")
    if result["errors"]:
        suggestions.append("Resolve evidence and review gate errors before publication.")
    return {"gate": result, "metrics": metrics, "revision_tasks": suggestions,
            "warning": "Heuristics cannot certify literary merit, source truth, or model training."}

def tests():
    task = prepare("failed-assault", "June 13 attack failed for lack of ladders.")
    assert task["scene_id"] == "failed-assault"
    sample = {"scene_id": "failed-assault", "draft": "六月十三日，士兵爬上梯子。\n\n守軍射箭，攻勢退下。", "evidence": [{"category": "documented", "claim": "Ladder shortage", "source": "Gesta Francorum"}], "reviewed": False}
    result = critique(sample)
    assert result["gate"]["status"] == "BLOCK"
    assert result["metrics"]["paragraphs"] == 2
    assert critique({**sample, "reviewed": True})["gate"]["status"] == "REVIEW_READY"
    print("PASS: prepare, critique, chronology/action metrics, review gate")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=("prepare", "critique", "test"))
    p.add_argument("--scene", default="failed-assault")
    p.add_argument("--source-file")
    p.add_argument("--submission")
    a = p.parse_args()
    if a.command == "test":
        tests()
        return
    if a.command == "prepare":
        if not a.source_file:
            p.error("--source-file required")
        source = Path(a.source_file).read_text(encoding="utf-8")
        result = prepare(a.scene, source)
    else:
        if not a.submission:
            p.error("--submission required")
        result = critique(json.loads(Path(a.submission).read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
