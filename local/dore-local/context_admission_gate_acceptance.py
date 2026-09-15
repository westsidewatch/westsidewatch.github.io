#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("gate", ROOT / "local/dore-local/context_admission_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

for term in ["浮現", "Emergence", "Doré Emergence", "project.dore.emergence"]:
    result = gate.admit(term)
    assert result["state"] == "admitted", result
    assert result["entity"] == "project.dore.emergence", result
    assert result["atlasEntity"] == "capability:emergence", result
    assert result["status"] == "formally-established", result
    assert result["mayAnswerEngineeringFacts"] is True
    assert result["currentCheckpoint"] == "docs/CURRENT_MAINLINE.md"
    assert result["canonicalPath"] == "Context -> Bible Coordinate -> Canonical Relation -> Resource -> Emergence"
    assert "docs/CURRENT_MAINLINE.md" in result["authorityFiles"]
    assert result["authorityRank"] == "github-current-canon"

unknown = gate.admit("definitely-unregistered-project-xyz")
assert unknown["mayAnswerEngineeringFacts"] is False
assert unknown["reason"].startswith("UNKNOWN")

assert gate.AUTHORITY_RANK["github-current-canon"] > gate.AUTHORITY_RANK["accepted-recent-decision"] > gate.AUTHORITY_RANK["durable-event-decision-history"] > gate.AUTHORITY_RANK["memory-summary"] > gate.AUTHORITY_RANK["model-inference"]

print("DORE_CONTEXT_ADMISSION_GATE=PASS emergence_fresh_session=PASS fail_closed=PASS stale_authority=PASS")
