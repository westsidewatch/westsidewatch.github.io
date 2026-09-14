#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARSENAL = ROOT / "dore-design" / "motion-arsenal.v0.json"
CAPABILITY = ROOT / "dore-core" / "runtime" / "design-motion-capability.v0.json"
PROFILE = ROOT / "dore-design" / "living-water-motion-profile.v0.json"
ROUTER = ROOT / "static" / "dore-design" / "dore-motion.js"
ATLAS = ROOT / "static" / "dore-design" / "italian-editorial-grammars.v1.json"
COMPILER = ROOT / "dore-design" / "italian_editorial_motion_compiler.py"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

arsenal = load(ARSENAL)
cap = load(CAPABILITY)
profile = load(PROFILE)
atlas = load(ATLAS)
router = ROUTER.read_text(encoding="utf-8")

assert arsenal["schema"] == "dore.design-motion-arsenal.v0"
assert arsenal["enginePolicy"]["defaultTier"] == "native"
assert arsenal["enginePolicy"]["heavyEngineDefault"] is False
semantics = {item["id"] for item in arsenal["semantics"]}
required = {"stillness", "ceremonial-reveal", "threshold-opening", "architectural-assembly", "quiet-dissolve", "measured-drift", "editorial-cut", "weighted-convergence", "page-turn-continuity", "kinetic-typography"}
assert semantics == required
assert "motion-must-improve-composition-or-remain-still" == arsenal["admission"]["beautyGate"]

assert cap["id"] == "design.motion"
assert cap["status"] == "experimental-v0"
assert cap["defaultEngineTier"] == "native"
assert cap["heavyRuntimeDefault"] is False
assert cap["firstAcceptanceConsumer"] == "living-water"
assert cap["promotionPolicy"] == "promote-to-capability-registry-only-after-real-raster-beauty-acceptance"

assert profile["consumer"] == "living-water"
assert profile["requires"] == "design.motion"
assert profile["acceptance"]["beautyFirst"] is True
assert profile["acceptance"]["reducedMotionRequired"] is True
assert profile["acceptance"]["productionPromotion"] is False
profile_intents = {item["intent"] for item in profile["intentProfile"]}
assert profile_intents <= semantics
assert "threshold-opening" in profile_intents
assert "architectural-assembly" in profile_intents
assert "stillness" in profile_intents
assert "literal-door-animation-required" in profile["forbidden"]
assert "surface-owned-animation-engine" in profile["forbidden"]

assert "prefers-reduced-motion: reduce" in router
assert "IntersectionObserver" in router
assert ".animate(" in router
assert "native-first-v0" in router
for forbidden_runtime in ("gsap", "anime", "three", "theatre"):
    assert forbidden_runtime not in router.lower(), forbidden_runtime

assert atlas["schema"] == "dore.italian-editorial-grammars.v1"
assert "emergence" in atlas["modules"]
assert any(era.get("grammar", {}).get("emergence") for family in atlas["families"] for era in family["eras"])

spec = importlib.util.spec_from_file_location("italian_motion", COMPILER)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
compiled = module.compile_all()
era_count = sum(len(family["eras"]) for family in atlas["families"])
assert len(compiled) == era_count
assert all(item["intent"] in semantics for item in compiled)
assert all(item["engine"] is None for item in compiled)
assert all(item["enginePolicy"] == "router-selects-lowest-sufficient" for item in compiled)
assert all(item["sourceModule"] == "emergence" for item in compiled)

print(f"DORE_DESIGN_MOTION_ARSENAL=PASS semantics={len(semantics)} italian_eras={era_count} first_consumer=living-water default=native registry_promotion=deferred")
