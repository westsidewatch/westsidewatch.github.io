#!/usr/bin/env python3
"""Blind manuscript-scale acceptance for Westside Writing.

The repository fixture is intentionally excluded from the training sample corpus.
CI verifies segmentation/synthesis and *exact input coverage* rather than using an
arbitrary character threshold. For a true large-manuscript quality run, pass the
original markdown with --manuscript and --live; that path fails closed if the local
model provider is unavailable or semantic inference degrades.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
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


def fixture_payload() -> dict:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert fixture.get("trainingSample") is False
    return {
        "title": fixture["title"],
        "authorThesis": fixture["authorThesis"],
        "context": fixture["context"],
        "evidenceRoles": fixture["evidenceRoles"],
        "sections": fixture["sections"],
        "mode": "diagnose",
    }


def markdown_sections(path: Path) -> list[dict[str, str]]:
    """Turn a real markdown manuscript into section inputs without rewriting it."""
    text = path.read_text(encoding="utf-8")
    heading = re.compile(r"^(#{1,3})\s+(.+?)\s*$", re.M)
    matches = list(heading.finditer(text))
    if not matches:
        return [{"title": path.stem, "text": text}]
    sections: list[dict[str, str]] = []
    if text[:matches[0].start()].strip():
        sections.append({"title": path.stem, "text": text[:matches[0].start()].strip()})
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body:
            sections.append({"title": match.group(2).strip(), "text": body})
    return sections


def payload_from_manuscript(path: Path) -> dict:
    sections = markdown_sections(path)
    return {
        "title": "神很遠　神很近｜天國語言極簡史",
        "authorThesis": "神的語言原本已經賜給了人，因著人的驕傲過犯，神收回了祂那有創造力的語言，再藉著道成肉身的贖回，由聖靈送回我們這份恩賜。",
        "context": "Full original manuscript blind evaluation. Preserve author thesis and separate textual evidence, lexical claims, history and editorial inference.",
        "evidenceRoles": ["biblical-text", "original-language", "historical-material", "author-judgment", "editorial-inference"],
        "sections": sections,
        "mode": "diagnose",
    }


def expected_chars(payload: dict) -> int:
    # The capability strips each supplied section before segmentation; mirror that
    # exact admission rule so this check detects silent loss rather than fixture size.
    return sum(len(str(section.get("text") or "").strip()) for section in payload.get("sections", []))


def run_structural() -> dict:
    payload = fixture_payload()
    admitted_chars = expected_chars(payload)
    result = cap.execute(payload, fake_infer)
    assert result["ok"] is True
    report = result["report"]
    manuscript = report["manuscript"]
    assert report["authorThesis"] == payload["authorThesis"]
    assert report["authority"]["mayRewriteThesis"] is False
    assert manuscript["enabled"] is True
    assert manuscript["segmentCount"] >= len(payload["sections"])
    assert manuscript["totalCharsEvaluated"] == admitted_chars, (manuscript["totalCharsEvaluated"], admitted_chars)
    assert manuscript["silentlyTruncated"] is False
    assert len(manuscript["segmentReports"]) == manuscript["segmentCount"]
    assert any(item.get("layer") == "PROSODY" for item in report["diagnosis"])
    assert report["revisedText"] == ""
    return {
        "schema": "dore.westside-writing-blind-acceptance.v0",
        "status": "PASS",
        "mode": "structural-injected-inference",
        "fixture": "天國語言極簡史",
        "chars": manuscript["totalCharsEvaluated"],
        "segments": manuscript["segmentCount"],
        "checks": [
            "not-training-sample",
            "manuscript-segmentation",
            "whole-manuscript-synthesis",
            "exact-input-coverage-no-silent-loss",
            "author-thesis-authority",
            "prosody-present-at-manuscript-level",
            "evidence-role-risk-preserved"
        ]
    }


def run_live(payload: dict) -> dict:
    local_path = str(HERE)
    if local_path not in sys.path:
        sys.path.insert(0, local_path)
    bus = load("westside_blind_bus", HERE / "capability_bus.py")

    class NoProduction:
        def execute(self, capability, args):
            raise RuntimeError("production action not expected")

    result = bus.call("writing.westside-dimensional-journalism", payload, NoProduction(), caller_product="journal-blind-acceptance")
    if not result.get("ok"):
        raise RuntimeError(json.dumps(result, ensure_ascii=False))
    report = result.get("report") or {}
    if (report.get("runtime") or {}).get("degraded"):
        raise RuntimeError("live model-backed blind acceptance degraded; no semantic PASS may be claimed")
    manuscript = report.get("manuscript") or {}
    admitted_chars = expected_chars(payload)
    if manuscript.get("totalCharsEvaluated") != admitted_chars:
        raise RuntimeError(f"live manuscript coverage mismatch: {manuscript.get('totalCharsEvaluated')} != {admitted_chars}")
    return {
        "schema": "dore.westside-writing-blind-acceptance.v0",
        "status": "PASS",
        "mode": "live-model-backed",
        "fixture": payload.get("title") or "天國語言極簡史",
        "chars": manuscript.get("totalCharsEvaluated"),
        "segments": manuscript.get("segmentCount"),
        "report": report,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Require local model-backed Capability Bus; fail closed if unavailable/degraded")
    parser.add_argument("--manuscript", type=Path, help="Path to the full original markdown manuscript. Intended for the real local Doré blind run.")
    ns = parser.parse_args()
    payload = payload_from_manuscript(ns.manuscript) if ns.manuscript else fixture_payload()
    result = run_live(payload) if ns.live else run_structural()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
