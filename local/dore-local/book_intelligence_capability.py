#!/usr/bin/env python3
"""Provider-neutral semantic Book Intelligence adapter for Doré Core."""
from __future__ import annotations

import json
from typing import Any, Callable

SCHEMA = "dore.book-intelligence-report.v2"
SECTION_BUDGET = 3200


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _semantic_window(value: Any, budget: int = SECTION_BUDGET) -> str:
    """Keep a real manuscript section within a stable local-model context budget.

    Preserve both the opening and closing argument of long sections rather than
    silently dropping later material. Short sections remain untouched.
    """
    text = str(value or "")
    if len(text) <= budget:
        return text
    marker = "\n\n[… middle omitted by Book Intelligence context budget …]\n\n"
    usable = max(2, budget - len(marker))
    head = usable * 3 // 5
    tail = usable - head
    return text[:head] + marker + text[-tail:]


def _sections(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    out = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            continue
        out.append({
            "index": index,
            "role": _text(item.get("role")) or "chapter",
            "title": _text(item.get("title")),
            "text": _semantic_window(item.get("text")),
        })
    return out


def _declared_intent(args: dict[str, Any]) -> dict[str, Any]:
    source = args.get("source") if isinstance(args.get("source"), dict) else {}
    intent = args.get("bookIntent") if isinstance(args.get("bookIntent"), dict) else source.get("bookIntent") or source.get("intent") or {}
    if not isinstance(intent, dict):
        intent = {}
    return {
        "category": _text(intent.get("category") or source.get("category")),
        "thesis": _text(intent.get("thesis") or source.get("thesis")),
        "audience": _text(intent.get("audience")),
        "readingMode": _text(intent.get("readingMode")) or "continuous",
    }


def _prompt_payload(args: dict[str, Any]) -> dict[str, Any]:
    source = args.get("source") if isinstance(args.get("source"), dict) else {}
    return {
        "title": _text(source.get("title")),
        "subtitle": _text(source.get("subtitle")),
        "declaredIntent": _declared_intent(args),
        "sections": _sections(args.get("sections")),
    }


def _messages(args: dict[str, Any]) -> list[dict[str, str]]:
    payload = _prompt_payload(args)
    system = (
        "You are Doré Core Book Intelligence. Analyze the supplied book as an editor, not as a replacement author. "
        "Return exactly one JSON object and nothing else: the first output character must be { and the final output character must be }. "
        "Do not use markdown fences, commentary, prefixes, suffixes, or prose outside the JSON object. "
        "Preserve any declared thesis as author authority. Do not rewrite doctrine or substantive authorial claims. "
        "Infer category, audience, reading mode, chapter roles, argument relations, structural gaps and visual tone hints. "
        "Use only the supplied manuscript evidence."
    )
    requested = {
        "schema": SCHEMA,
        "category": "string",
        "inferredThesis": "string",
        "thesisRelationship": "aligned|partial|tension|unknown",
        "confidence": "0..1",
        "audience": "string",
        "readingMode": "string",
        "chapterRoles": [],
        "argumentRelations": [],
        "structuralGaps": [],
        "visualToneHints": [],
        "evidence": [],
    }
    user = "Analyze this manuscript. Required response shape: " + json.dumps(requested, ensure_ascii=False) + "\nBOOK:\n" + json.dumps(payload, ensure_ascii=False)
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def _extract_json_object(text: str) -> str:
    """Return the first balanced top-level JSON object from a model response."""
    start = text.find("{")
    if start < 0:
        raise ValueError("semantic report did not contain a JSON object")
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
    raise ValueError("semantic report contained an unterminated JSON object")


def _parse(raw: str) -> dict[str, Any]:
    text = _text(raw)
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].lstrip()
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        value = json.loads(_extract_json_object(text))
    if not isinstance(value, dict):
        raise ValueError("semantic report must be a JSON object")
    return value


def _safe_report(args: dict[str, Any], value: dict[str, Any], *, degraded: bool = False, reason: str = "") -> dict[str, Any]:
    declared = _declared_intent(args)
    relationship = _text(value.get("thesisRelationship"))
    if relationship not in {"aligned", "partial", "tension", "unknown"}:
        relationship = "unknown"
    try:
        confidence = max(0.0, min(1.0, float(value.get("confidence", 0))))
    except (TypeError, ValueError):
        confidence = 0.0
    def array(name: str) -> list[Any]:
        current = value.get(name)
        return current[:64] if isinstance(current, list) else []
    return {
        "schema": SCHEMA,
        "category": _text(value.get("category")) or declared["category"] or "longform",
        "declaredThesis": declared["thesis"],
        "inferredThesis": _text(value.get("inferredThesis")),
        "thesisRelationship": relationship,
        "confidence": confidence,
        "audience": _text(value.get("audience")) or declared["audience"],
        "readingMode": _text(value.get("readingMode")) or declared["readingMode"],
        "chapterRoles": array("chapterRoles"),
        "argumentRelations": array("argumentRelations"),
        "structuralGaps": array("structuralGaps"),
        "visualToneHints": array("visualToneHints"),
        "evidence": array("evidence"),
        "authority": {"declaredThesis": "author", "mayRewriteThesis": False},
        "runtime": {"semantic": not degraded, "degraded": degraded, "reason": reason if degraded else ""},
    }


def execute(args: dict[str, Any] | None, infer: Callable[[list[dict[str, str]]], str] | None) -> dict[str, Any]:
    args = args or {}
    if not isinstance(args.get("source"), dict) or not _sections(args.get("sections")):
        return {"ok": False, "status": "failed", "capability": "publishing.book-intelligence", "error": {"code": "invalid_args", "message": "source and sections are required"}}
    if infer is None:
        return {"ok": True, "status": "completed", "capability": "publishing.book-intelligence", "report": _safe_report(args, {}, degraded=True, reason="inference_unavailable")}
    try:
        value = _parse(infer(_messages(args)))
        report = _safe_report(args, value)
    except Exception:
        report = _safe_report(args, {}, degraded=True, reason="semantic_inference_failed")
    return {"ok": True, "status": "completed", "capability": "publishing.book-intelligence", "report": report}
