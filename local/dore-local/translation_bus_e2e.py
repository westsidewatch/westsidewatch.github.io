#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCAL = Path(__file__).resolve().parent
for path in (str(ROOT), str(LOCAL)):
    if path not in sys.path:
        sys.path.insert(0, path)

import capability_bus


class ProductionStub:
    CAPABILITIES = set()

    @staticmethod
    def execute(capability, args):
        raise AssertionError(f"unexpected production dispatch: {capability}")


production = ProductionStub()
descriptor = capability_bus.resolve("translation.project", production)
assert descriptor is not None
assert descriptor["callable"] is True
assert descriptor["owner"] == "dore-core"

result = capability_bus.call(
    "translation.project",
    {
        "canonicalId": "cinema:test:translation-bus",
        "sourcePointer": "urn:test:translation-bus",
        "sourceLanguage": "en",
        "targetLanguage": "zh-Hant",
        "cues": [{
            "id": "c1",
            "startMs": 1000,
            "endMs": 2000,
            "sourceText": "Alpha.",
            "translatedText": "甲。",
            "status": "candidate",
        }],
        "provenance": {"test": True},
    },
    production,
    caller_product="cinema",
)
assert result["ok"] is True
assert result["capability"] == "translation.project"
assert result["artifact"]["sourceAuthority"] is True
assert result["artifact"]["translationAuthority"] is False
assert result["core_route"]["capability"] == "translation.project"
assert result["core_route"]["caller_product"] == "cinema"
assert result["core_route"]["provider"] == "dore-core"
assert result["core_route"]["transport"] == "core-adapter"
print("DORE_TRANSLATION_CAPABILITY_BUS_E2E=PASS")
