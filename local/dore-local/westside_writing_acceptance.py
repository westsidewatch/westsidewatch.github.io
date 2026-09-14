#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE = HERE / "westside_writing_capability.py"
spec = importlib.util.spec_from_file_location("westside_writing_capability", MODULE)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot_load_westside_writing_capability")
cap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cap)

THESIS = "三個朋友的共同問題不是完全無知，而是不知道自己不知道。"
TEXT = "七天，沒有一個人開口。靜默和約伯的痛苦哪個更大似乎都不能被明辨。七天又過了一天，約伯發出了聲音。"


def fake_infer(messages):
    assert messages and messages[0]["role"] == "system"
    system = messages[0]["content"]
    assert "Do not prefer fewer adjectives as an ideology" in system
    assert "Poetic rhythm must remain embedded in prose" in system
    return json.dumps({
        "schema": "dore.westside-writing-report.v0",
        "diagnosis": [
            {"layer": "PROSODY", "status": "pass", "reason": "rhythm carries perception through silence-to-sound pressure"},
            {"layer": "TRUTH", "status": "pass", "reason": "no added scene fact"}
        ],
        "strengths": ["experiential-time", "semantic-pressure"],
        "risks": [],
        "languageSignals": {
            "connectors": [], "adverbs": [], "particles": [], "adjectives": [],
            "repetition": ["七天 returns with added time"],
            "rhythm": ["silence-to-sound"]
        },
        "oreVeins": ["silence and voice in Job"],
        "revisionPrinciples": ["preserve perception between facts"],
        "revisedText": "SHOULD_NOT_APPEAR_IN_EVALUATE_MODE"
    }, ensure_ascii=False)


def main():
    evaluated = cap.execute({"text": TEXT, "authorThesis": THESIS, "mode": "evaluate"}, fake_infer)
    assert evaluated["ok"] is True
    report = evaluated["report"]
    assert report["schema"] == "dore.westside-writing-report.v0"
    assert report["capability"] == "writing.westside-dimensional-journalism"
    assert report["authorThesis"] == THESIS
    assert report["authority"] == {"authorThesis": "author", "mayRewriteThesis": False}
    assert report["revisedText"] == ""
    assert report["runtime"]["degraded"] is False
    assert any(item.get("layer") == "PROSODY" for item in report["diagnosis"])

    revised = cap.execute({"text": TEXT, "authorThesis": THESIS, "mode": "revise"}, lambda _: json.dumps({
        "diagnosis": [], "strengths": [], "risks": [], "languageSignals": {}, "oreVeins": [],
        "revisionPrinciples": [], "revisedText": TEXT
    }, ensure_ascii=False))
    assert revised["report"]["authorThesis"] == THESIS
    assert revised["report"]["revisedText"] == TEXT

    degraded = cap.execute({"text": TEXT, "authorThesis": THESIS}, lambda _: "not json")
    assert degraded["ok"] is True
    assert degraded["report"]["runtime"]["degraded"] is True
    assert degraded["report"]["authorThesis"] == THESIS

    invalid = cap.execute({"text": ""}, fake_infer)
    assert invalid["ok"] is False
    assert invalid["error"]["code"] == "invalid_args"

    print(json.dumps({
        "schema": "dore.westside-writing-acceptance.v0",
        "status": "PASS",
        "checks": [
            "provider-neutral-adapter",
            "author-thesis-authority",
            "evaluate-does-not-rewrite",
            "revise-mode-explicit",
            "degraded-fail-safe",
            "prosody-perception-contract",
            "no-adjective-minimization-ideology"
        ]
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
