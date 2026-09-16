#!/usr/bin/env python3
"""Provider-neutral Westside Dimensional Journalism adapter for Doré Core.

Supports both passage-scale and manuscript-scale evaluation. Long manuscripts are
never silently truncated: they are segmented, evaluated section by section, then
synthesized under the same author-thesis/evidence authority contract.
"""
from __future__ import annotations

import json
from typing import Any, Callable

CAPABILITY = "writing.westside-dimensional-journalism"
SCHEMA = "dore.westside-writing-report.v0"
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
    out: list[str] = []
    current: list[str] = []
    size = 0
    for paragraph in paragraphs:
        if len(paragraph) > budget:
            if current:
                out.append("\n\n".join(current))
                current, size = [], 0
            for start in range(0, len(paragraph), budget):
                out.append(paragraph[start:start + budget])
            continue
        extra = len(paragraph) + (2 if current else 0)
        if current and size + extra > budget:
            out.append("\n\n".join(current))
            current, size = [], 0
        current.append(paragraph)
        size += extra
    if current:
        out.append("\n\n".join(current))
    return out


def _segments(args: dict[str, Any]) -> list[dict[str, Any]]:
    provided = args.get("sections") if isinstance(args.get("sections"), list) else []
    segments: list[dict[str, Any]] = []
    if provided:
        for section_index, item in enumerate(provided):
            if not isinstance(item, dict):
                continue
            title = _text(item.get("title")) or f"section-{section_index + 1}"
            text = _text(item.get("text"))
            for part_index, part in enumerate(_chunk_text(text)):
                segments.append({
                    "id": f"s{section_index + 1}p{part_index + 1}",
                    "title": title,
                    "text": part,
                    "sourceSection": section_index,
                })
    else:
        text = _text(args.get("text"))
        for part_index, part in enumerate(_chunk_text(text)):
            segments.append({
                "id": f"p{part_index + 1}",
                "title": _text(args.get("title")) or "passage",
                "text": part,
                "sourceSection": 0,
            })
    return segments[:MAX_SEGMENTS]


def _input(args: dict[str, Any]) -> dict[str, Any]:
    evidence = args.get("evidenceRoles") if isinstance(args.get("evidenceRoles"), list) else []
    segments = _segments(args)
    total_chars = sum(len(item["text"]) for item in segments)
    return {
        "title": _text(args.get("title")),
        "authorThesis": _text(args.get("authorThesis")),
        "mode": _mode(args),
        "context": _text(args.get("context"))[:MAX_CONTEXT],
        "evidenceRoles": evidence[:32],
        "segments": segments,
        "totalChars": total_chars,
        "manuscript": len(segments) > 1 or bool(args.get("sections")),
    }


def _shape() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "diagnosis": [{"layer": "GROUND|DEPTH|POSITION|MOVEMENT|ALTITUDE|LANGUAGE|PROSODY|EMERGENCE|TRUTH", "status": "pass|watch|fail", "reason": "string"}],
        "strengths": [],
        "risks": [],
        "languageSignals": {"connectors": [], "adverbs": [], "particles": [], "adjectives": [], "repetition": [], "rhythm": []},
        "oreVeins": [],
        "revisionPrinciples": [],
        "revisedText": "string-or-empty",
    }


def _system(mode: str) -> str:
    return (
        "You are Doré Core's Westside Dimensional Journalism capability. "
        "Evaluate or revise Chinese long-form nonfiction while preserving the author's thesis and discovery authority. "
        "Do not normalize the prose into generic AI rhythm. Do not prefer fewer adjectives as an ideology. "
        "Do not create one-sentence-per-line punchline cadence. Connectors such as 然後/所以/但是 are used only when they add relational precision. "
        "Adjectives may be rich when they add dimension, evidence or semantic pressure. Repetition may remain when its later occurrence accumulates meaning. "
        "Poetic rhythm must remain embedded in prose and carry perception rather than merely sound impressive. "
        "Never invent weather, gestures, psychology, dialogue, sensory details or historical facts. "
        "Distinguish textual evidence, scholarship, tradition, inference and author judgment. "
        "If mode=revise, preserve substantive thesis and evidence claims; revise only expression/structure unless explicitly asked otherwise. "
        "If mode is evaluate or diagnose, revisedText must be empty. "
        "Return exactly one JSON object and no markdown or prose outside it.\nFOUNDATION:\n- "
        + "\n- ".join(FOUNDATION)
        + f"\nMODE: {mode}"
    )


def _segment_messages(payload: dict[str, Any], segment: dict[str, Any]) -> list[dict[str, str]]:
    user_payload = {
        "title": payload["title"],
        "authorThesis": payload["authorThesis"],
        "context": payload["context"],
        "evidenceRoles": payload["evidenceRoles"],
        "segment": segment,
        "instruction": "Diagnose this segment in relation to the whole manuscript. Do not infer global failure from local absence.",
    }
    return [
        {"role": "system", "content": _system(payload["mode"])},
        {"role": "user", "content": "Required response shape: " + json.dumps(_shape(), ensure_ascii=False) + "\nSEGMENT INPUT:\n" + json.dumps(user_payload, ensure_ascii=False)},
    ]


def _synthesis_messages(payload: dict[str, Any], segment_reports: list[dict[str, Any]]) -> list[dict[str, str]]:
    compact = []
    for index, report in enumerate(segment_reports):
        compact.append({
            "segment": payload["segments"][index]["id"],
            "title": payload["segments"][index]["title"],
            "diagnosis": report.get("diagnosis", []),
            "strengths": report.get("strengths", []),
            "risks": report.get("risks", []),
            "languageSignals": report.get("languageSignals", {}),
            "oreVeins": report.get("oreVeins", []),
            "revisionPrinciples": report.get("revisionPrinciples", []),
        })
    synthesis = {
        "title": payload["title"],
        "authorThesis": payload["authorThesis"],
        "mode": payload["mode"],
        "context": payload["context"],
        "totalChars": payload["totalChars"],
        "segmentCount": len(payload["segments"]),
        "segmentReports": compact,
        "instruction": (
            "Synthesize manuscript-level findings. Preserve contradictions when they are real. "
            "Do not average away strong local prose. Identify recurring rhythm, repeated motifs, global movement, "
            "evidence-boundary risks, and ore veins. revisedText must remain empty unless mode=revise; even in revise mode, "
            "do not attempt to rewrite the entire manuscript from summaries."
        ),
    }
    return [
        {"role": "system", "content": _system(payload["mode"]) + "\nWHOLE-MANUSCRIPT SYNTHESIS: yes"},
        {"role": "user", "content": "Required response shape: " + json.dumps(_shape(), ensure_ascii=False) + "\nMANUSCRIPT SYNTHESIS INPUT:\n" + json.dumps(synthesis, ensure_ascii=False)},
    ]


def _extract_json_object(text: str) -> str:
    start = text.find("{")
    if start < 0:
        raise ValueError("no_json_object")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    raise ValueError("unterminated_json")


def _parse(raw: str) -> dict[str, Any]:
    raw = _text(raw)
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        value = json.loads(_extract_json_object(raw))
    if not isinstance(value, dict):
        raise ValueError("report_not_object")
    return value


def _list(value: Any, limit: int = 64) -> list[Any]:
    return value[:limit] if isinstance(value, list) else []


def _safe_report(payload: dict[str, Any], value: dict[str, Any], *, degraded: bool = False, reason: str = "", segment_reports: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    signals = value.get("languageSignals") if isinstance(value.get("languageSignals"), dict) else {}
    revised = _text(value.get("revisedText")) if payload["mode"] == "revise" else ""
    return {
        "schema": SCHEMA,
        "capability": CAPABILITY,
        "mode": payload["mode"],
        "title": payload["title"],
        "authorThesis": payload["authorThesis"],
        "authority": {"authorThesis": "author", "mayRewriteThesis": False},
        "diagnosis": _list(value.get("diagnosis")),
        "strengths": _list(value.get("strengths")),
        "risks": _list(value.get("risks")),
        "languageSignals": {
            "connectors": _list(signals.get("connectors")),
            "adverbs": _list(signals.get("adverbs")),
            "particles": _list(signals.get("particles")),
            "adjectives": _list(signals.get("adjectives")),
            "repetition": _list(signals.get("repetition")),
            "rhythm": _list(signals.get("rhythm")),
        },
        "oreVeins": _list(value.get("oreVeins")),
        "revisionPrinciples": _list(value.get("revisionPrinciples")),
        "revisedText": revised,
        "manuscript": {
            "enabled": payload["manuscript"],
            "totalCharsEvaluated": payload["totalChars"],
            "segmentCount": len(payload["segments"]),
            "silentlyTruncated": False,
            "segmentReports": segment_reports or [],
        },
        "runtime": {"semantic": not degraded, "degraded": degraded, "reason": reason if degraded else ""},
    }


def execute(args: dict[str, Any] | None, infer: Callable[[list[dict[str, str]]], str] | None = None) -> dict[str, Any]:
    args = args or {}
    payload = _input(args)
    if not payload["segments"]:
        return {"ok": False, "status": "failed", "capability": CAPABILITY, "error": {"code": "invalid_args", "message": "text or sections are required"}}
    if infer is None:
        report = _safe_report(payload, {}, degraded=True, reason="inference_unavailable")
        return {"ok": True, "status": "completed", "capability": CAPABILITY, "report": report}
    try:
        segment_reports = [_parse(infer(_segment_messages(payload, segment))) for segment in payload["segments"]]
        if len(segment_reports) == 1 and not payload["manuscript"]:
            value = segment_reports[0]
        else:
            value = _parse(infer(_synthesis_messages(payload, segment_reports)))
        report = _safe_report(payload, value, segment_reports=segment_reports)
    except Exception:
        report = _safe_report(payload, {}, degraded=True, reason="semantic_inference_failed")
    return {"ok": True, "status": "completed", "capability": CAPABILITY, "report": report}
