#!/usr/bin/env python3
from copy import deepcopy
from translation_capability import execute


def verify(source_language, target_language, source_text, translated_text):
    request = {
        "canonicalId": "cinema:test:translation-v0",
        "sourcePointer": "urn:test:translation-v0",
        "sourceLanguage": source_language,
        "targetLanguage": target_language,
        "cues": [{
            "id": "c1",
            "startMs": 1000,
            "endMs": 3000,
            "sourceText": source_text,
            "translatedText": translated_text,
            "status": "verified",
            "evidence": [{"kind": "terminology"}, {"kind": "memory"}],
        }],
        "provenance": {"transcript": "source-authoritative"},
    }
    before = deepcopy(request)
    result = execute(request)
    artifact = result["artifact"]
    assert result["ok"] is True
    assert artifact["schema"] == "dore.bilingual-subtitle.v0"
    assert artifact["canonicalId"] == request["canonicalId"]
    assert artifact["sourcePointer"] == request["sourcePointer"]
    assert artifact["sourceAuthority"] is True
    assert artifact["translationAuthority"] is False
    assert artifact["timingPolicy"] == "source-authoritative-immutable"
    assert artifact["cues"][0]["startMs"] == 1000
    assert artifact["cues"][0]["endMs"] == 3000
    assert artifact["cues"][0]["sourceText"] == source_text
    assert artifact["cues"][0]["translatedText"] == translated_text
    assert request == before


verify("en", "zh-Hant", "Alpha.", "甲。")
verify("zh-Hant", "en", "甲。", "Alpha.")
print("DORE_TRANSLATION_PROJECT_ACCEPTANCE=PASS")
