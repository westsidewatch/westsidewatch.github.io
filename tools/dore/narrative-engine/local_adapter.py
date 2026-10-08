#!/usr/bin/env python3
"""Explicit local subprocess adapter for Doré narrative training.
Model command is supplied by the operator; no paid endpoint or implicit network access.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from narrative import extract
from revision_loop import prepare, critique

def invoke(command, task, timeout=120):
    if not command:
        raise ValueError("An explicit local command is required")
    proc = subprocess.run(command, input=json.dumps(task, ensure_ascii=False),
                          text=True, capture_output=True, timeout=timeout, check=False)
    if proc.returncode:
        raise RuntimeError("Model command failed: " + proc.stderr[-1000:])
    try:
        answer = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("Model must return one JSON submission on stdout") from exc
    if not isinstance(answer, dict) or answer.get("scene_id") != task["scene_id"]:
        raise ValueError("Response scene_id mismatch")
    return answer

def execute(source, scene_id, command):
    task = prepare(scene_id, extract(source))
    candidate = invoke(command, task)
    report = critique(candidate)
    return {"task": {"scene_id": scene_id}, "candidate": candidate, "assessment": report,
            "published": False}

def self_test():
    source = "## 金門\n\n六月十三日，士兵攻城。\n\n## 下一節\n\n不相關"
    mock = "import sys,json; t=json.load(sys.stdin); print(json.dumps({'scene_id':t['scene_id'],'draft':'六月十三日，士兵攻城。','evidence':[{'category':'documented','claim':'攻城','source':'Gesta Francorum'}],'reviewed':False},ensure_ascii=False))"
    result = execute(source, "failed-assault", [sys.executable, "-c", mock])
    assert result["candidate"]["scene_id"] == "failed-assault"
    assert result["assessment"]["gate"]["status"] == "BLOCK"
    assert result["published"] is False
    print("PASS: section extraction -> local process -> candidate JSON -> critique; unreviewed candidate blocked")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=("run", "test"))
    p.add_argument("--source")
    p.add_argument("--scene", default="failed-assault")
    p.add_argument("--output")
    p.add_argument("--model-command", nargs=argparse.REMAINDER,
                   help="Executable and args after --model-command; reads task JSON stdin, writes submission JSON stdout")
    a = p.parse_args()
    if a.command == "test":
        self_test()
        return
    if not a.source or not a.output or not a.model_command:
        p.error("run requires --source, --output and --model-command")
    source = Path(a.source).read_text(encoding="utf-8")
    result = execute(source, a.scene, a.model_command)
    output = Path(a.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Candidate and assessment written:", output)

if __name__ == "__main__":
    main()
