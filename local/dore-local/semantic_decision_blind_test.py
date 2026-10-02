#!/usr/bin/env python3
"""Blind gate: Doré chooses the next capability using the resident local model."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from design_local_inference import MODEL, OLLAMA, ollama_json
from semantic_decision import decide_next

ARTIFACT = Path(__file__).resolve().parent / "artifacts" / "semantic-decision-blind-gate.json"


def infer(*, messages, schema):
    raw = ollama_json(messages, schema)
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("local_inference_not_object")
    return value


def write_artifact(payload):
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    started = datetime.now(timezone.utc).isoformat()
    decision = None
    try:
        decision = decide_next(
            goal="Find the repository file that defines Doré's canonical failure taxonomy, then inspect it before making any change.",
            state={
                "phase": "semantic-decision-blind-test",
                "last_action": None,
                "deterministic_route": None,
            },
            evidence=[
                {"id": "e1", "fact": "The target is known to be somewhere in the repository."},
                {"id": "e2", "fact": "No exact path has been supplied."},
            ],
            capabilities=[
                {"id": "knowledge.recall", "description": "Recall previously stored Doré knowledge and memory."},
                {"id": "design.intelligence", "description": "Evaluate or generate design decisions from visual evidence."},
                {"id": "engineering.repo-task", "description": "Inspect, read, write, verify, or commit within the allowed repository."},
                {"id": "source.dispatch", "description": "Dispatch discovery against external source adapters."},
            ],
            infer=infer,
        )
        passed = decision["action"] == "INVOKE" and decision["capability_id"] == "engineering.repo-task"
        payload = {
            "schema": "dore.semantic-decision-blind-gate.v0",
            "status": "PASS" if passed else "FAIL",
            "started_at": started,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "provider": "ollama-local",
            "model": MODEL,
            "endpoint": OLLAMA,
            "expected": {"action": "INVOKE", "capability_id": "engineering.repo-task"},
            "decision": decision,
        }
        write_artifact(payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if not passed:
            raise SystemExit(1)
        return
    except Exception as exc:
        payload = {
            "schema": "dore.semantic-decision-blind-gate.v0",
            "status": "ERROR",
            "started_at": started,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "provider": "ollama-local",
            "model": MODEL,
            "endpoint": OLLAMA,
            "decision": decision,
            "error": f"{type(exc).__name__}: {exc}",
        }
        write_artifact(payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        raise


if __name__ == "__main__":
    main()
