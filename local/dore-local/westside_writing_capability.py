#!/usr/bin/env python3
"""Provider-neutral Westside Dimensional Journalism adapter for Doré Core."""
from __future__ import annotations

import json
from typing import Any, Callable

CAPABILITY = "writing.westside-dimensional-journalism"
SCHEMA = "dore.westside-writing-report.v0"
MAX_TEXT = 12000

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


def _input(args: dict[str, Any]) -> dict[str, Any]:
    text = _text(args.get("text"))[:MAX_TEXT]
    thesis = _text(args.get("authorThesis"))
    mode = _text(args.get("mode")) or "evaluate"
    if mode not in {"evaluate", "revise", "diagnose"}:
        mode = "evaluate"
    evidence = args.get("evidenceRoles") if isinstance(args.get("evidenceRoles"), list) else []
    return {
        "text": text,
        "authorThesis": thesis,
        "mode": mode,
        "context": _text(args.get("context"))[:3000],
        "evidenceRoles": evidence[:32],
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


def _messages(args: dict[str, Any]) -> list[dict[str, str]]:
    payload = _input(args)
    system = (
        "You are Doré Core's Westside Dimensional Journalism capability. "
        "Evaluate or revise Chinese long-form nonfiction while preserving the author's thesis and discovery authority. "
        "Do not normalize the prose into generic AI rhythm. Do not prefer fewer adjectives as an ideology. "
        "Do not create one-sentence-per-line punchline cadence. Connectors such as 然後/所以/但是 are used only when they add relational precision. "
        "Adjectives may be rich when they add dimension, evidence or semantic pressure. Repetition may remain when its second occurrence accumulates meaning. "
        "Poetic rhythm must remain embedded in prose and carry perception rather than merely sound impressive. "
        "Never invent weather, gestures, psychology, dialogue, sensory details or historical facts. "
        "If mode=revise, preserve substantive thesis and evidence claims; revise only expression/structure unless explicitly asked otherwise. "
        "Return exactly one JSON object and no markdown or prose outside it.\nFOUNDATION:\n- "
        + "\n- ".join(FOUNDATION)
    )
    user = (
        "Required response shape: " + json.dumps(_shape(), ensure_ascii=False)
        + "\nINPUT:\n" + json.dumps(payload, ensure_ascii=False)
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


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


def _safe_report(args: dict[str, Any], value: dict[str, Any], *, degraded: bool = False, reason: str = "") -> dict[str, Any]:
    payload = _input(args)
    signals = value.get("languageSignals") if isinstance(value.get("languageSignals"), dict) else {}
    revised = _text(value.get("revisedText")) if payload["mode"] == "revise" else ""
    return {
        "schema": SCHEMA,
        "capability": CAPABILITY,
        "mode": payload["mode"],
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
        "runtime": {"semantic": not degraded, "degraded": degraded, "reason": reason if degraded else ""},
    }


def execute(args: dict[str, Any] | None, infer: Callable[[list[dict[str, str]]], str] | None = None) -> dict[str, Any]:
    args = args or {}
    payload = _input(args)
    if not payload["text"]:
        return {"ok": False, "status": "failed", "capability": CAPABILITY, "error": {"code": "invalid_args", "message": "text is required"}}
    if infer is None:
        report = _safe_report(args, {}, degraded=True, reason="inference_unavailable")
        return {"ok": True, "status": "completed", "capability": CAPABILITY, "report": report}
    try:
        value = _parse(infer(_messages(args)))
        report = _safe_report(args, value)
    except Exception:
        report = _safe_report(args, {}, degraded=True, reason="semantic_inference_failed")
    return {"ok": True, "status": "completed", "capability": CAPABILITY, "report": report}
