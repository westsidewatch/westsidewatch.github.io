#!/usr/bin/env python3
from __future__ import annotations

import re
from urllib.request import Request, urlopen

from translation_capability import execute

PLAYER_URL = "https://api.arclight.org/videoPlayerUrl?refId=1_529-jf-0-0&playerStyle=default&player=bc.vanilla5"
TIMES = [(2061110, 2062860), (2064210, 2067010)]
TRANSLATIONS = ["愛你們的仇敵。", "善待恨你們的人。"]


def fetch(url: str, accept: str, referer: str | None = None) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        "Accept": accept,
    }
    if referer:
        headers["Referer"] = referer
        headers["Origin"] = "https://api.arclight.org"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def to_ms(value: str) -> int:
    parts = value.split(":")
    if len(parts) == 2:
        minutes = int(parts[0])
        seconds = float(parts[1])
        return round((minutes * 60 + seconds) * 1000)
    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return round((hours * 3600 + minutes * 60 + seconds) * 1000)
    raise ValueError(value)


def parse_vtt(text: str) -> list[dict]:
    cues = []
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if "-->" not in line:
            i += 1
            continue
        start_raw, end_raw = [part.strip().split()[0] for part in line.split("-->", 1)]
        i += 1
        body = []
        while i < len(lines) and lines[i].strip():
            body.append(re.sub(r"<[^>]+>", "", lines[i]).strip())
            i += 1
        cues.append({"startMs": to_ms(start_raw), "endMs": to_ms(end_raw), "text": " ".join(x for x in body if x)})
    return cues


player = fetch(PLAYER_URL, "text/html,*/*")
tracks = dict(re.findall(r'<track[^>]+src="([^"]+)"[^>]+srcLang="([^"]+)"', player))
# regex yields URL->lang; invert without persisting provider text
by_lang = {lang.lower(): url for url, lang in tracks.items()}
assert "en" in by_lang and "zh-hant" in by_lang
english_vtt = fetch(by_lang["en"], "text/vtt,text/plain,*/*", "https://api.arclight.org/")
reference_vtt = fetch(by_lang["zh-hant"], "text/vtt,text/plain,*/*", "https://api.arclight.org/")
assert english_vtt.startswith("WEBVTT")
assert reference_vtt.startswith("WEBVTT")
english = parse_vtt(english_vtt)
selected = []
for index, (start_ms, end_ms) in enumerate(TIMES):
    cue = next((c for c in english if c["startMs"] == start_ms and c["endMs"] == end_ms), None)
    assert cue and cue["text"]
    selected.append({
        "id": f"jesus-real-{index+1}",
        "startMs": start_ms,
        "endMs": end_ms,
        "sourceText": cue["text"],
        "translatedText": TRANSLATIONS[index],
        "status": "candidate",
        "evidence": [
            {"kind": "scripture", "reference": "Luke 6:27"},
            {"kind": "provider-caption-timing", "language": "en"},
        ],
    })

result = execute({
    "canonicalId": "cinema:video:jesus-film:jesus",
    "sourcePointer": "https://www.jesusfilm.org/watch/jesus.html",
    "sourceLanguage": "en",
    "targetLanguage": "zh-Hant",
    "cues": selected,
    "provenance": {
        "provider": "Jesus Film Project",
        "sourceTranscript": "official English WebVTT",
        "referenceTranslationRole": "evaluation-only",
        "mediaRehost": False,
    },
})
artifact = result["artifact"]
assert result["ok"] is True
assert artifact["canonicalId"] == "cinema:video:jesus-film:jesus"
assert artifact["sourceAuthority"] is True
assert artifact["translationAuthority"] is False
assert [(c["startMs"], c["endMs"]) for c in artifact["cues"]] == TIMES
assert all(c["sourceText"] for c in artifact["cues"])
assert all(c["translatedText"] for c in artifact["cues"])
assert artifact["provenance"]["referenceTranslationRole"] == "evaluation-only"
assert artifact["provenance"]["mediaRehost"] is False
print("DORE_TRANSLATOR_JESUS_REAL_TIMED_ARTIFACT=PASS")
print("DORE_TRANSLATOR_JESUS_REAL_CUES=2")
