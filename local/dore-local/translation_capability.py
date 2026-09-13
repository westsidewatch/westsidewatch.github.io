#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from translation_contracts import validate_artifact


def execute(args: dict) -> dict:
    canonical_id = str(args.get("canonicalId") or "").strip()
    source_pointer = str(args.get("sourcePointer") or "").strip()
    source_language = str(args.get("sourceLanguage") or "").strip()
    target_language = str(args.get("targetLanguage") or "").strip()
    cues = deepcopy(args.get("cues") or [])
    provenance = deepcopy(args.get("provenance") or {})

    artifact = {
        "schema": "dore.bilingual-subtitle.v0",
        "canonicalId": canonical_id,
        "sourcePointer": source_pointer,
        "sourceLanguage": source_language,
        "targetLanguage": target_language,
        "sourceAuthority": True,
        "translationAuthority": False,
        "timingPolicy": "source-authoritative-immutable",
        "cues": cues,
        "provenance": provenance,
    }
    validate_artifact(artifact)
    return {
        "ok": True,
        "status": "completed",
        "capability": "translation.project",
        "artifact": artifact,
        "providerNeutral": True,
        "persistence": "artifact-only-no-media",
    }
