#!/usr/bin/env python3
from __future__ import annotations

VALID_STATUSES = {"candidate", "verified", "revised"}


def validate_artifact(data: dict) -> dict:
    if data.get("schema") != "dore.bilingual-subtitle.v0":
        raise ValueError("unsupported bilingual subtitle schema")
    if not data.get("canonicalId") or not data.get("sourcePointer"):
        raise ValueError("canonicalId and sourcePointer are required")
    source_language = str(data.get("sourceLanguage") or "").strip()
    target_language = str(data.get("targetLanguage") or "").strip()
    if not source_language or not target_language or source_language == target_language:
        raise ValueError("distinct sourceLanguage and targetLanguage are required")
    cues = data.get("cues")
    if not isinstance(cues, list) or not cues:
        raise ValueError("cues must be a non-empty list")
    last_end = -1
    for cue in cues:
        if not isinstance(cue, dict) or not cue.get("id"):
            raise ValueError("every cue requires id")
        start = int(cue.get("startMs", -1))
        end = int(cue.get("endMs", -1))
        if start < 0 or end <= start or start < last_end:
            raise ValueError("cue timing must be ordered and non-overlapping")
        last_end = end
        if not str(cue.get("sourceText") or ""):
            raise ValueError("sourceText is required")
        if not str(cue.get("translatedText") or ""):
            raise ValueError("translatedText is required")
        if cue.get("status", "candidate") not in VALID_STATUSES:
            raise ValueError("invalid translation status")
    return data
