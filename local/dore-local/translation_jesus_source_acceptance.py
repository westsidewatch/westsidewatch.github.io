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
assert result["mediaRehost"] is False

# These imports execute the real timed JESUS WebVTT acceptance and the
# canonical Capability Bus dispatch acceptance. They remain separate modules
# so each contract is reusable outside this provider-source gate.
import translation_jesus_timed_acceptance  # noqa: E402,F401
import translation_bus_e2e  # noqa: E402,F401

print("DORE_TRANSLATOR_JESUS_SOURCE_ADMISSION=PASS")
print("DORE_TRANSLATOR_JESUS_TIMING_GATE=REAL_PROVIDER_WEBVTT_PASS")
