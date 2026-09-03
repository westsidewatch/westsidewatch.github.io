#!/usr/bin/env python3
"""Storybook → Doré Design promotion pipeline v1.

Graduates verified Storybook compositions into read-only Doré Design candidates.
The locked #262 homepage is an immutable comparison baseline, never a target.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMOTION = ROOT / "dore-design" / "promotion"
CANDIDATES = ROOT / "dore-design" / "candidates"
REGISTRY = CANDIDATES / "registry.json"
BASELINE = ROOT / "dore-design" / "new-westside" / "homepage-v3-threshold-promoted.html"
FEEDBACK = Path(os.environ.get("DORE_DESIGN_DATA", Path.home() / ".dore" / "design")) / "candidate-feedback.jsonl"
REQUIRED_GATES = ("BUILD_PASS", "RENDER_PASS", "FUNCTION_PASS", "A11Y_PASS", "VISUAL_STABLE", "RESPONSIVE_PASS", "DESIGN_DISTINCT", "WESTSIDE_FIT")


def now():
    return datetime.now(timezone.utc).isoformat()


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def registry():
    return read_json(REGISTRY, {"schema": "dore.design-candidate-registry.v1", "candidates": []})


def evaluate(spec):
    gates = dict(spec.get("gates") or {})
    checks = {name: gates.get(name) is True for name in REQUIRED_GATES}
    checks.update({
        "PROVENANCE_COMPLETE": len(spec.get("references") or []) >= 3 and len(set(spec.get("source_families") or [])) >= 2,
        "EDITABLE_BINDINGS": len(spec.get("editable_bindings") or []) >= 5,
        "BASELINE_262_IMMUTABLE": spec.get("baseline_262_sha256") == sha256(BASELINE),
        "NOT_BASELINE_REPLACEMENT": spec.get("target_page_id") != "homepage",
        "RENDERER_AVAILABLE": (ROOT / str(spec.get("template_entrypoint") or "")).is_file(),
        "STORY_AVAILABLE": (ROOT / str(spec.get("source_story_file") or "")).is_file(),
        "MATERIALLY_DISTINCT": bool(spec.get("composition_signature")) and spec.get("composition_signature") != spec.get("baseline_composition_signature"),
    })
    failed = [name for name, passed in checks.items() if not passed]
    return {"ok": not failed, "schema": "dore.promotion-gate.v1", "candidate_id": spec.get("candidate_id"), "checks": checks, "failed": failed}


def promote_spec(spec):
    result = evaluate(spec)
    if not result["ok"]:
        return {**result, "promoted": False}
    candidate_id = spec["candidate_id"]
    manifest = {
        "schema": "dore.design-candidate.v1",
        "id": candidate_id,
        "name": spec["name"],
        "status": "candidate",
        "source": {"kind": "storybook", "story_id": spec["source_story_id"], "story_file": spec["source_story_file"], "evidence": spec["evidence"]},
        "provenance": {"references": spec["references"], "source_families": spec["source_families"]},
        "template": {"entrypoint": spec["template_entrypoint"], "renderer": spec["renderer"], "page_id": spec["target_page_id"], "editable_bindings": spec["editable_bindings"], "assets": spec.get("assets") or []},
        "promotion_gate": result,
        "baseline_262": {"immutable": True, "sha256": spec["baseline_262_sha256"], "targeted": False},
    }
    folder = CANDIDATES / candidate_id
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    data = registry()
    summary = {"id": candidate_id, "name": spec["name"], "status": "candidate", "manifest": f"dore-design/candidates/{candidate_id}/manifest.json", "page_id": spec["target_page_id"], "source_story_id": spec["source_story_id"]}
    data["candidates"] = [x for x in data.get("candidates", []) if x.get("id") != candidate_id] + [summary]
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**result, "promoted": True, "candidate": summary, "manifest": str(folder / "manifest.json")}


def promote(spec_path):
    spec = read_json(spec_path)
    if not isinstance(spec, dict):
        raise ValueError("invalid_specimen")
    return promote_spec(spec)


def promote_storybook_evidence(spec_path, evidence_path):
    """Derive candidate gates from one real Storybook story, then promote it."""
    spec = read_json(spec_path)
    evidence = read_json(evidence_path)
    if not isinstance(spec, dict) or not isinstance(evidence, dict):
        raise ValueError("invalid_storybook_evidence")
    story = next((x for x in evidence.get("candidates", []) if x.get("id") == spec.get("source_story_id")), None)
    if not story:
        raise ValueError("source_story_missing_from_evidence")
    views = list((story.get("viewports") or {}).values())
    global_gates = evidence.get("gates") or {}
    spec["gates"] = {
        "BUILD_PASS": global_gates.get("BUILD_PASS") is True,
        "RENDER_PASS": bool(views) and all(x.get("render_pass") is True for x in views),
        "FUNCTION_PASS": global_gates.get("FUNCTION_PASS") in {True, "authoritative_in_vitest"},
        "A11Y_PASS": global_gates.get("A11Y_PASS") in {True, "authoritative_in_storybook_vitest_addon"},
        "VISUAL_STABLE": bool(views) and all(x.get("visual_stable") is True for x in views),
        "RESPONSIVE_PASS": bool(views) and all(x.get("responsive_pass") is True for x in views),
        "DESIGN_DISTINCT": global_gates.get("DESIGN_DISTINCT") is True,
        "WESTSIDE_FIT": bool(views) and all(x.get("metrics", {}).get("westside_text_signal") and (x.get("metrics", {}).get("brand_color_signal") or x.get("metrics", {}).get("editorial_system_signal")) for x in views),
    }
    evidence_file = Path(evidence_path).resolve()
    try: spec["evidence"] = str(evidence_file.relative_to(ROOT).as_posix())
    except ValueError: spec["evidence"] = str(evidence_file)
    return promote_spec(spec)


def list_candidates():
    data = registry()
    decisions = {}
    if FEEDBACK.exists():
        for line in FEEDBACK.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
                decisions[row["candidate_id"]] = row
            except (ValueError, KeyError):
                pass
    rows = []
    for item in data.get("candidates", []):
        row = dict(item)
        decision = decisions.get(item.get("id"))
        row["runtime_status"] = decision.get("decision") if decision else item.get("status", "candidate")
        row["last_judgment"] = decision
        rows.append(row)
    return {"ok": True, "schema": data.get("schema"), "candidates": rows, "locked_baseline_262_sha256": sha256(BASELINE)}


def record_judgment(candidate_id, decision, reason="", signals=None):
    if decision not in {"accepted", "rejected", "needs_revision"}:
        raise ValueError("invalid_candidate_decision")
    if not any(x.get("id") == candidate_id for x in registry().get("candidates", [])):
        raise ValueError("candidate_not_found")
    row = {"schema": "dore.design-feedback.v1", "candidate_id": candidate_id, "decision": decision, "reason": str(reason).strip(), "signals": list(signals or []), "created_at": now(), "returns_to": ["storybook", "knowledge-lab"]}
    FEEDBACK.parent.mkdir(parents=True, exist_ok=True)
    with FEEDBACK.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return {"ok": True, "feedback": row, "candidate_status": decision, "baseline_262_modified": False}


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("evaluate"); p.add_argument("specimen")
    p = sub.add_parser("promote"); p.add_argument("specimen")
    p = sub.add_parser("promote-storybook"); p.add_argument("specimen"); p.add_argument("evidence")
    sub.add_parser("list")
    p = sub.add_parser("judge"); p.add_argument("candidate_id"); p.add_argument("decision", choices=("accepted", "rejected", "needs_revision")); p.add_argument("--reason", default="")
    args = parser.parse_args()
    if args.command == "evaluate": result = evaluate(read_json(args.specimen, {}))
    elif args.command == "promote": result = promote(args.specimen)
    elif args.command == "promote-storybook": result = promote_storybook_evidence(args.specimen, args.evidence)
    elif args.command == "list": result = list_candidates()
    else: result = record_judgment(args.candidate_id, args.decision, args.reason)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
