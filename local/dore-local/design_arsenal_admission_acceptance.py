#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "dore-design" / "design_arsenal_admission.py"
spec = importlib.util.spec_from_file_location("design_arsenal_admission", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)

report = mod.validate()
assert report["ok"], report
assert report["findings"] >= 20, report
assert report["modes"]["assimilate"] > 0
assert report["modes"]["learn"] > 0
assert report["modes"]["mount"] > 0
assert report["modes"]["defer"] > 0
assert report["first_real_consumer"] == "living-water"

for target in [
    "design.primitive",
    "design.typography",
    "design.composition",
    "design.image-art-direction",
    "design.tokens",
    "design.accessibility-gate",
    "design.performance-gate",
    "design.visual-regression",
    "design.visual-artifact",
]:
    plan = mod.plan_for(target)
    assert plan["findings"], target
    assert "westside-canon" in plan["authority"]

raw = json.loads((ROOT / "dore-design" / "design_arsenal_assimilation.v0.json").read_text(encoding="utf-8"))
for finding in raw["findings"]:
    assert finding["mode"] != "chat-only"
    assert finding.get("why")
    if finding["mode"] == "defer":
        assert finding.get("reconsider_when")
    else:
        assert finding.get("target")

print("DESIGN_ARSENAL_ADMISSION=PASS")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
