#!/usr/bin/env python3
"""Provider-neutral Westside Dimensional Journalism adapter for Doré Core.

Supports passage/manuscript evaluation and a governed writing-grammar preflight.
Project grammars may contribute transferable craft but never source identity, thesis,
voice, motifs, theology, or runtime Core authority.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

CAPABILITY = "writing.westside-dimensional-journalism"
SCHEMA = "dore.westside-writing-report.v0"
GRAMMAR_SCHEMA = "dore.writing-grammar-preflight.v1"
GRAMMAR_LIBRARY = Path(__file__).resolve().parents[2] / "dore-core" / "writing" / "grammar-library.v1.json"
SEGMENT_BUDGET = 7000
MAX_SEGMENTS = 24
MAX_CONTEXT = 3000

FOUNDATION = [
    "GROUND: enter through real scene/person/text/place/object/event, not abstract conclusion",
    "DEPTH: write the thing deep before analogy; larger meaning must emerge from defensible relation",
    "POSITION: author position is explicit; do not claim knowledge the evidence does not permit",
    "MOVEMENT: paragraph is a movement of thought; judgment may grow from narration",
    "ALTITUDE: move among detail, person, text, history, structure and theology without announcing every shift",
    "LANGUAGE: remove needless mediation; connectors/adverbs/的地得 are audited by function, not quota",
    "PROSODY: rhythm must carry perception; repetition must accumulate meaning; poetic rhythm stays inside prose",
    "EMERGENCE: deep writing may reveal ore veins that return to mother text or become separate/media work",
    "TRUTH: literary force cannot invent scene detail or collapse evidence roles",
]

UNIVERSAL_GRAMMAR = [
    "material carries thought before narrator explanation",
    "compression must be earned by accumulated material, never scheduled as an aphorism",
    "magnify scenes selectively where emotional or conceptual direction changes",
    "move scale through adjacent fact rather than performative signposting",
    "allow motifs and relations to recur before naming their meaning",
    "permit curiosity-led expansion when it remains inside the work's attractor",
    "re-enter the mother text instead of automatically closing every digression as a mini-essay",
    "treat narrator pressure as scarce and earned",
    "preserve human irregularity in paragraph and sentence pressure",
    "let readers discover relations without congratulatory or performative-discovery narration",
]

DIAGNOSTICS = [
    "performative-discovery",
    "dense-landing-sentences",
    "automatic-quotable-lines",
    "premature-echo-explanation",
    "fake-suspense",
    "mechanical-not-a-but-b-reversal",
    "scene-summary-where-magnification-is-required",
    "digression-mini-essay-closure",
]


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _mode(args: dict[str, Any]) -> str:
    mode = _text(args.get("mode")) or "evaluate"
    return mode if mode in {"evaluate", "revise", "diagnose"} else "evaluate"


def _chunk_text(text: str, budget: int = SEGMENT_BUDGET) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= budget:
        return [text]
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    out, current, size = [], [], 0
    for paragraph in paragraphs:
        if len(paragraph) > budget:
            if current:
                out.append("\n\n".join(current)); current, size = [], 0
            out.extend(paragraph[start:start + budget] for start in range(0, len(paragraph), budget))
            continue
        extra = len(paragraph) + (2 if current else 0)
        if current and size + extra > budget:
            out.append("\n\n".join(current)); current, size = [], 0
        current.append(paragraph); size += extra
    if current:
        out.append("\n\n".join(current))
    return out


def _segments(args: dict[str, Any]) -> list[dict[str, Any]]:
    provided = args.get("sections") if isinstance(args.get("sections"), list) else []
    segments: list[dict[str, Any]] = []
    if provided:
        for section_index, item in enumerate(provided):
            if not isinstance(item, dict): continue
            title, text = _text(item.get("title")) or f"section-{section_index + 1}", _text(item.get("text"))
            for part_index, part in enumerate(_chunk_text(text)):
                segments.append({"id": f"s{section_index + 1}p{part_index + 1}", "title": title, "text": part, "sourceSection": section_index})
    else:
        for part_index, part in enumerate(_chunk_text(_text(args.get("text")))):
            segments.append({"id": f"p{part_index + 1}", "title": _text(args.get("title")) or "passage", "text": part, "sourceSection": 0})
    return segments[:MAX_SEGMENTS]


def _input(args: dict[str, Any]) -> dict[str, Any]:
    evidence = args.get("evidenceRoles") if isinstance(args.get("evidenceRoles"), list) else []
    segments = _segments(args)
    return {
        "title": _text(args.get("title")), "projectId": _text(args.get("projectId")),
        "surface": _text(args.get("surface")) or "long-form", "authorThesis": _text(args.get("authorThesis")),
        "mode": _mode(args), "context": _text(args.get("context"))[:MAX_CONTEXT], "evidenceRoles": evidence[:32],
        "segments": segments, "totalChars": sum(len(item["text"]) for item in segments),
        "manuscript": len(segments) > 1 or bool(args.get("sections")),
    }


def _load_library() -> dict[str, Any]:
    try:
        value = json.loads(GRAMMAR_LIBRARY.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {"entries": []}
    except (OSError, json.JSONDecodeError):
        return {"entries": []}


def _grammar_preflight(payload: dict[str, Any]) -> dict[str, Any]:
    library = _load_library()
    candidates = []
    for item in library.get("entries", []):
        if not isinstance(item, dict) or item.get("status") != "proven": continue
        if payload["projectId"] and item.get("projectId") == payload["projectId"]:
            relation = "current-project"
        elif payload["surface"] in item.get("surfaceContexts", []) or "long-form-theological-nonfiction" in item.get("surfaceContexts", []):
            relation = "reference-candidate"
        else:
            relation = "not-selected"
        candidates.append({
            "grammarId": item.get("grammarId", ""), "projectId": item.get("projectId", ""), "relation": relation,
            "transferableCapabilities": item.get("transferableCapabilities", []) if relation != "not-selected" else [],
            "blockedIdentity": item.get("nonTransferableIdentity", []),
        })
    return {
        "schema": GRAMMAR_SCHEMA, "universal": UNIVERSAL_GRAMMAR, "diagnostics": DIAGNOSTICS,
        "referenceActionPerformed": True, "libraryAvailable": bool(library.get("entries")), "candidates": candidates,
        "authority": {"authorSourcePreserved": True, "mayRewriteThesis": False, "referenceGrammarAuthority": False},
        "isolation": {"runtimeCoreMutationAllowed": False, "projectIdentityTransferAllowed": False, "surfaceMayOverwriteProjectVoice": False},
    }


def _shape() -> dict[str, Any]:
    return {"schema": SCHEMA, "diagnosis": [{"layer": "GROUND|DEPTH|POSITION|MOVEMENT|ALTITUDE|LANGUAGE|PROSODY|EMERGENCE|TRUTH", "status": "pass|watch|fail", "reason": "string"}], "strengths": [], "risks": [], "languageSignals": {"connectors": [], "adverbs": [], "particles": [], "adjectives": [], "repetition": [], "rhythm": []}, "oreVeins": [], "revisionPrinciples": [], "revisedText": "string-or-empty"}


def _system(mode: str, grammar: dict[str, Any]) -> str:
    return (
        "You are Doré Core's Westside Dimensional Journalism capability. Preserve author/source/thesis authority. "
        "Project grammar references are craft experience only: borrow operations when relevant; never copy thesis, motifs, character voice, theology, signature phrases or cadence. "
        "Do not normalize prose into generic AI rhythm. Never invent evidence, weather, gestures, psychology, dialogue or sensory facts. "
        "If mode=revise, preserve substantive thesis/evidence claims. If evaluate/diagnose, revisedText must be empty. Return exactly one JSON object.\n"
        "FOUNDATION:\n- " + "\n- ".join(FOUNDATION) + "\nGRAMMAR PREFLIGHT:\n" + json.dumps(grammar, ensure_ascii=False) + f"\nMODE: {mode}"
    )


def _segment_messages(payload: dict[str, Any], segment: dict[str, Any], grammar: dict[str, Any]) -> list[dict[str, str]]:
    user_payload = {"title": payload["title"], "authorThesis": payload["authorThesis"], "context": payload["context"], "evidenceRoles": payload["evidenceRoles"], "segment": segment, "instruction": "Diagnose this segment in relation to the whole manuscript. Apply only relevant transferable grammar; do not infer global failure from local absence."}
    return [{"role": "system", "content": _system(payload["mode"], grammar)}, {"role": "user", "content": "Required response shape: " + json.dumps(_shape(), ensure_ascii=False) + "\nSEGMENT INPUT:\n" + json.dumps(user_payload, ensure_ascii=False)}]


def _synthesis_messages(payload: dict[str, Any], segment_reports: list[dict[str, Any]], grammar: dict[str, Any]) -> list[dict[str, str]]:
    compact = [{"segment": payload["segments"][i]["id"], "title": payload["segments"][i]["title"], "diagnosis": r.get("diagnosis", []), "strengths": r.get("strengths", []), "risks": r.get("risks", []), "languageSignals": r.get("languageSignals", {}), "oreVeins": r.get("oreVeins", []), "revisionPrinciples": r.get("revisionPrinciples", [])} for i, r in enumerate(segment_reports)]
    synthesis = {"title": payload["title"], "authorThesis": payload["authorThesis"], "mode": payload["mode"], "context": payload["context"], "totalChars": payload["totalChars"], "segmentCount": len(payload["segments"]), "segmentReports": compact, "instruction": "Synthesize manuscript-level findings without averaging away strong local prose or importing referenced project identity. revisedText stays empty unless mode=revise; never rewrite an entire manuscript from summaries."}
    return [{"role": "system", "content": _system(payload["mode"], grammar) + "\nWHOLE-MANUSCRIPT SYNTHESIS: yes"}, {"role": "user", "content": "Required response shape: " + json.dumps(_shape(), ensure_ascii=False) + "\nMANUSCRIPT SYNTHESIS INPUT:\n" + json.dumps(synthesis, ensure_ascii=False)}]


def _extract_json_object(text: str) -> str:
    start = text.find("{")
    if start < 0: raise ValueError("no_json_object")
    depth, in_string, escaped = 0, False, False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped: escaped = False
            elif char == "\\": escaped = True
            elif char == '"': in_string = False
            continue
        if char == '"': in_string = True
        elif char == "{": depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0: return text[start:index + 1]
    raise ValueError("unterminated_json")


def _parse(raw: str) -> dict[str, Any]:
    raw = _text(raw)
    try: value = json.loads(raw)
    except json.JSONDecodeError: value = json.loads(_extract_json_object(raw))
    if not isinstance(value, dict): raise ValueError("report_not_object")
    return value


def _list(value: Any, limit: int = 64) -> list[Any]: return value[:limit] if isinstance(value, list) else []


def _safe_report(payload: dict[str, Any], value: dict[str, Any], grammar: dict[str, Any], *, degraded: bool = False, reason: str = "", segment_reports: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    signals = value.get("languageSignals") if isinstance(value.get("languageSignals"), dict) else {}
    return {"schema": SCHEMA, "capability": CAPABILITY, "mode": payload["mode"], "title": payload["title"], "authorThesis": payload["authorThesis"], "authority": {"authorThesis": "author", "mayRewriteThesis": False}, "grammarPreflight": grammar, "diagnosis": _list(value.get("diagnosis")), "strengths": _list(value.get("strengths")), "risks": _list(value.get("risks")), "languageSignals": {"connectors": _list(signals.get("connectors")), "adverbs": _list(signals.get("adverbs")), "particles": _list(signals.get("particles")), "adjectives": _list(signals.get("adjectives")), "repetition": _list(signals.get("repetition")), "rhythm": _list(signals.get("rhythm"))}, "oreVeins": _list(value.get("oreVeins")), "revisionPrinciples": _list(value.get("revisionPrinciples")), "revisedText": _text(value.get("revisedText")) if payload["mode"] == "revise" else "", "manuscript": {"enabled": payload["manuscript"], "totalCharsEvaluated": payload["totalChars"], "segmentCount": len(payload["segments"]), "silentlyTruncated": False, "segmentReports": segment_reports or []}, "runtime": {"semantic": not degraded, "degraded": degraded, "reason": reason if degraded else ""}}


def execute(args: dict[str, Any] | None, infer: Callable[[list[dict[str, str]]], str] | None = None) -> dict[str, Any]:
    args = args or {}; payload = _input(args); grammar = _grammar_preflight(payload)
    if not payload["segments"]: return {"ok": False, "status": "failed", "capability": CAPABILITY, "error": {"code": "invalid_args", "message": "text or sections are required"}}
    if infer is None: return {"ok": True, "status": "completed", "capability": CAPABILITY, "report": _safe_report(payload, {}, grammar, degraded=True, reason="inference_unavailable")}
    try:
        segment_reports = [_parse(infer(_segment_messages(payload, segment, grammar))) for segment in payload["segments"]]
        value = segment_reports[0] if len(segment_reports) == 1 and not payload["manuscript"] else _parse(infer(_synthesis_messages(payload, segment_reports, grammar)))
        report = _safe_report(payload, value, grammar, segment_reports=segment_reports)
    except Exception:
        report = _safe_report(payload, {}, grammar, degraded=True, reason="semantic_inference_failed")
    return {"ok": True, "status": "completed", "capability": CAPABILITY, "report": report}
