#!/usr/bin/env python3
from pathlib import Path
import json

from translation_source_admission import admit_jesus_sermon_on_mount

ROOT = Path(__file__).resolve().parents[2]
manifest = json.loads((ROOT / "cinema" / "data" / "translation-source.v0.json").read_text(encoding="utf-8"))
item = manifest["items"][0]

assert manifest["schema"] == "dore.translation-source.v0"
assert item["canonicalId"] == "cinema:video:jesus-film:jesus"
assert item["sourceAuthority"] is True
assert item["mediaRehost"] is False
assert item["transcript"]["timingStatus"] == "not-admitted"
assert item["transcript"]["subtitleReady"] is False
assert item["referenceTranslation"]["role"] == "evaluation-only"

result = admit_jesus_sermon_on_mount(
    item["transcript"]["page"],
    item["referenceTranslation"]["page"],
)
assert result["ok"] is True
assert result["canonicalId"] == item["canonicalId"]
assert result["sourcePointer"] == item["sourcePointer"]
assert result["sourceTranscriptObserved"] is True
assert result["sourceAuthority"] is True
assert result["referenceRole"] == "evaluation-only"
assert result["timingStatus"] == "not-admitted"
assert result["subtitleReady"] is False
assert result["mediaRehost"] is False

print("DORE_TRANSLATOR_JESUS_SOURCE_ADMISSION=PASS")
print("DORE_TRANSLATOR_JESUS_TIMING_GATE=PENDING_REAL_TIMINGS")
