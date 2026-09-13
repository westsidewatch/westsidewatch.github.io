#!/usr/bin/env python3
from __future__ import annotations

from urllib.request import Request, urlopen

SOURCE_SENTINEL = "Love your enemies, do good to those who hate you"
PROVIDER_PROBE_URL = "https://api.arclight.org/videoPlayerUrl?refId=1_529-jf-0-0&playerStyle=default&player=bc.vanilla5"


def probe_provider(url: str, timeout: int = 30) -> dict:
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Doré-Translator/0.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    with urlopen(req, timeout=timeout) as response:
        status = int(getattr(response, "status", 200))
        content_type = str(response.headers.get("Content-Type") or "")
        sample = response.read(256)
    if status < 200 or status >= 400 or not sample:
        raise RuntimeError(f"official provider probe failed: status={status}")
    return {"status": status, "contentType": content_type, "bytesObserved": len(sample)}


def admit_jesus_source(item: dict) -> dict:
    transcript = item.get("transcript") or {}
    reference = item.get("referenceTranslation") or {}
    sentinel = str(transcript.get("evidenceSentinel") or "")
    if sentinel != SOURCE_SENTINEL:
        raise RuntimeError("JESUS transcript evidence sentinel drifted")
    if transcript.get("evidenceMode") != "official-page-verified-snapshot":
        raise RuntimeError("JESUS transcript evidence mode is not admitted")
    if reference.get("role") != "evaluation-only":
        raise RuntimeError("provider Chinese subtitle reference must remain evaluation-only")
    probe = probe_provider(str(item.get("providerProbeUrl") or PROVIDER_PROBE_URL))
    return {
        "ok": True,
        "schema": "dore.translation-source-admission.v0",
        "canonicalId": item["canonicalId"],
        "sourcePointer": item["sourcePointer"],
        "chapterPointer": transcript["page"],
        "sourceLanguage": item["sourceLanguage"],
        "targetLanguage": item["targetLanguage"],
        "sourceAuthority": True,
        "sourceTranscriptEvidence": transcript["evidenceMode"],
        "sourceTranscriptObserved": True,
        "sourceSentinel": sentinel,
        "referenceTranslationPointer": reference["page"],
        "referenceRole": reference["role"],
        "providerProbe": probe,
        "timingStatus": transcript["timingStatus"],
        "subtitleReady": bool(transcript["subtitleReady"]),
        "nextGate": "admit-real-provider-caption-timings-or-run-alignment",
        "mediaRehost": False,
    }


def admit_jesus_sermon_on_mount(source_page: str, reference_page: str) -> dict:
    item = {
        "canonicalId": "cinema:video:jesus-film:jesus",
        "sourcePointer": "https://www.jesusfilm.org/watch/jesus.html",
        "sourceLanguage": "en",
        "targetLanguage": "zh-Hant",
        "providerProbeUrl": PROVIDER_PROBE_URL,
        "transcript": {
            "page": source_page,
            "evidenceMode": "official-page-verified-snapshot",
            "evidenceSentinel": SOURCE_SENTINEL,
            "timingStatus": "not-admitted",
            "subtitleReady": False,
        },
        "referenceTranslation": {
            "page": reference_page,
            "role": "evaluation-only",
        },
    }
    return admit_jesus_source(item)
