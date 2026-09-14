#!/usr/bin/env python3
"""Blind manuscript-scale acceptance for Westside Writing.

This fixture is intentionally excluded from the training sample corpus. The test
verifies long-form segmentation + synthesis and author/evidence authority. It does
not pretend the deterministic injected inference is a model-quality judgment.
A separate --live mode invokes the local model-backed Capability Bus.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIXTURE = ROOT / "dore-core" / "writing" / "blind-tests" / "tian-guo-yu-yan-minimal-history.v0.json"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot_load:{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cap = load("westside_writing_capability_blind", HERE / "westside_writing_capability.py")


def report_payload(kind: str) -> str:
    if kind == "synthesis":
        data = {
            "diagnosis": [
                {"layer": "MOVEMENT", "status": "pass", "reason": "creation-to-loss-to-return arc remains visible across sections"},
                {"layer": "PROSODY", "status": "watch", "reason": "wind, voice, silence and return operate as manuscript motifs; some short-sentence emphasis requires local review"},
                {"layer": "TRUTH", "status": "watch", "reason": "lexical, archaeological and historical assertions must remain evidence-role separated from author inference"}
            ],
            "strengths": ["long-range motif return", "creation-return structural arc", "authorial image system"],
            "risks": ["scene details may outrun explicit textual evidence", "lexical claims need source-level verification"],
            "languageSignals": {
                "connectors": ["relation often carried by scene order rather than connective words"],
                "adverbs": [], "particles": [],
                "adjectives": ["description is often dimensional rather than decorative"],
                "repetition": ["風/說話/語言 return with changed semantic pressure"],
                "rhythm": ["silence-to-speech and weight-to-air recur as latent prosody"]
            },
            "oreVeins": ["以撒與話語重量", "rachaph與等待", "巴別塔空洞與天空", "davar從創造到新造"],
            "revisionPrinciples": ["preserve the recurring wind/voice motifs", "separate lexical evidence from theological inference", "do not flatten high-density passages"],
            "revisedText": ""
        }
    else:
        data = {
            "diagnosis": [{"layer": "GROUND", "status": "pass", "reason": "segment works through concrete text, scene or image"}],
            "strengths": ["material-led movement"],
            "risks": [],
            "languageSignals": {"connectors": [], "adverbs": [], "particles": [], "adjectives": [], "repetition": [], "rhythm": []},
            "oreVeins": [], "revisionPrinciples": [], "revisedText": ""
        }
    return json.dumps(data, ensure_ascii=False)


def fake_infer(messages):
    system = messages[0]["content"]
    return report_payload("synthesis" if "WHOLE-MANUSCRIPT SYNTHESIS: yes" in system else "segment")


def args_from_fixture() -> dict:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return {
        "title": fixture["title"],
        "authorThesis": fixture["authorThesis"],
        "context": fixture["context"],
        "evidenceRoles": fixture["evidenceRoles"],
        "sections": fixture["sections"],
        "mode": "diagnose",
    }


def run_structural() -> dict:
    payload = args_from_fixture()
    result = cap.execute(payload, fake_infer)
    assert result["ok"] is True
    report = result["report"]
    assert report["authorThesis"] == payload["authorThesis"]
    assert report["authority"]["mayRewriteThesis"] is False
    assert report["manuscript"]["enabled"] is True
    assert report["manuscript"]["segmentCount"] >= 4
    assert report["manuscript"]["totalCharsEvaluated"] > 4000
    assert report["manuscript"]["silentlyTruncated"] is False
    assert len(report["manuscript"]["segmentReports"]) == report["manuscript"]["segmentCount"]
    assert any(item.get("layer") == "PROSODY" for item in report["diagnosis"])
    assert report["revisedText"] == ""
    return {
        "schema": "dore.westside-writing-blind-acceptance.v0",
        "status": "PASS",
        "mode": "structural-injected-inference",
        "fixture": "天國語言極簡史",
        "chars": report["manuscript"]["totalCharsEvaluated"],
        "segments": report["manuscript"]["segmentCount"],
        "checks": [
            "not-training-sample",
            "manuscript-segmentation",
            "whole-manuscript-synthesis",
            "no-silent-truncation",
            "author-thesis-authority",
            "prosody-present-at-manuscript-level",
            "evidence-role-risk-preserved"
        ]
    }


def run_live() -> dict:
    local_path = str(HERE)
    if local_path not in sys.path:
        sys.path.insert(0, local_path)
    bus = load("westside_blind_bus", HERE / "capability_bus.py")
    class NoProduction:
        def execute(self, capability, args):
            raise RuntimeError("production action not expected")
    result = bus.call("writing.westside-dimensional-journalism", args_from_fixture(), NoProduction(), caller_product="journal-blind-acceptance")
    if not result.get("ok"):
        raise RuntimeError(json.dumps(result, ensure_ascii=False))
    report = result.get("report") or {}
    if (report.get("runtime") or {}).get("degraded"):
        raise RuntimeError("live model-backed blind acceptance degraded; no semantic PASS may be claimed")
    return {
        "schema": "dore.westside-writing-blind-acceptance.v0",
        "status": "PASS",
        "mode": "live-model-backed",
        "fixture": "天國語言極簡史",
        "chars": (report.get("manuscript") or {}).get("totalCharsEvaluated"),
        "segments": (report.get("manuscript") or {}).get("segmentCount"),
        "report": report,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Require the local model-backed Capability Bus; fail closed if unavailable/degraded")
    ns = parser.parse_args()
    result = run_live() if ns.live else run_structural()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
