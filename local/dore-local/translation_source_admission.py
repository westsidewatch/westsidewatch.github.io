#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from urllib.request import Request, urlopen

SOURCE_SENTINEL = "Love your enemies, do good to those who hate you"


def fetch_text(url: str, timeout: int = 30) -> str:
    req = Request(url, headers={"User-Agent": "Doré-Translator/0.1 (+https://westsidewatch.ca)"})
    with urlopen(req, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", raw, flags=re.I | re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def admit_jesus_sermon_on_mount(source_page: str, reference_page: str) -> dict:
    source_text = fetch_text(source_page)
    reference_text = fetch_text(reference_page)

    required = ("Sermon on the Mount", "Transcript", SOURCE_SENTINEL)
    missing = [marker for marker in required if marker not in source_text]
    if missing:
        raise RuntimeError(f"official JESUS source admission failed; missing markers: {missing}")

    if "Sermon on the Mount" not in reference_text:
        raise RuntimeError("official Traditional Chinese reference surface is unavailable")

    return {
        "ok": True,
        "schema": "dore.translation-source-admission.v0",
        "canonicalId": "cinema:video:jesus-film:jesus",
        "sourcePointer": "https://www.jesusfilm.org/watch/jesus.html",
        "chapterPointer": source_page,
        "sourceLanguage": "en",
        "targetLanguage": "zh-Hant",
        "sourceAuthority": True,
        "sourceTranscriptObserved": True,
        "sourceSentinel": SOURCE_SENTINEL,
        "referenceTranslationPointer": reference_page,
        "referenceRole": "evaluation-only",
        "timingStatus": "not-admitted",
        "subtitleReady": False,
        "nextGate": "admit-real-provider-caption-timings-or-run-alignment",
        "mediaRehost": False,
    }
