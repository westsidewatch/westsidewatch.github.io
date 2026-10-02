#!/usr/bin/env python3
"""Blind test: Doré must choose the next capability without an expected answer hint."""
from __future__ import annotations

import json

from design_local_inference import ollama_json
from semantic_decision import decide_next


def infer(*, messages, schema):
    raw = ollama_json(messages, schema=schema, temperature=0.0)
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("local_inference_not_object")
    return value


def main():
    # The expected capability is intentionally not stated in the prompt/context.
    # The model sees only the goal, evidence, state, and available capabilities.
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
            {
                "id": "knowledge.recall",
                "description": "Recall previously stored Doré knowledge and memory.",
            },
            {
                "id": "design.intelligence",
                "description": "Evaluate or generate design decisions from visual evidence.",
            },
            {
                "id": "engineering.repo-task",
                "description": "Inspect, read, write, verify, or commit within the allowed repository.",
            },
            {
                "id": "source.dispatch",
                "description": "Dispatch discovery against external source adapters.",
            },
        ],
        infer=infer,
    )
    print(json.dumps(decision, ensure_ascii=False, indent=2))

    # This assertion is test code, not information shown to the model.
    if decision["action"] != "INVOKE":
        raise SystemExit("BLIND_TEST_FAIL: expected an executable capability choice")
    if decision["capability_id"] != "engineering.repo-task":
        raise SystemExit("BLIND_TEST_FAIL: wrong capability selected")
    print("BLIND_TEST_PASS")


if __name__ == "__main__":
    main()
