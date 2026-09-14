from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

resources = json.loads((ROOT / "data/video-resource.v0.json").read_text())
coordinates = json.loads((ROOT / "data/bible-media-coordinate.v0.json").read_text())
module = (ROOT / "coordinate-layer.js").read_text().lower()

assert resources["schema"] == "holy-light.video-resource.v0"
assert coordinates["schema"] == "dore.bible-media-coordinate.v0"

resource_items = resources["items"]
coordinate_items = coordinates["items"]
resource_ids = {item["canonicalId"] for item in resource_items}
coordinate_ids = {item["canonicalId"] for item in coordinate_items}
collection_ids = {item["id"] for item in coordinates["collections"]}

assert resource_ids == coordinate_ids, (resource_ids - coordinate_ids, coordinate_ids - resource_ids)
assert len(coordinate_ids) == len(coordinate_items)

for item in coordinate_items:
    assert item["collection"] in collection_ids
    assert set(item["coordinates"]) == {"text", "world", "media"}
    assert isinstance(item["coordinates"]["text"], list)
    assert isinstance(item["coordinates"]["world"], list)
    assert item["coordinates"]["media"]["kind"] in {"work", "moment", "segment"}
    assert item["relations"]

for item in resource_items:
    assert item["rights"]["rehost"] is False

combined = json.dumps(resources, ensure_ascii=False).lower() + json.dumps(coordinates, ensure_ascii=False).lower()
assert "wikisource" not in combined
assert "goodtv" not in module
assert "provider" not in module
assert "dore.bible-media-coordinate.v0" in module
assert "paradisecinemacoordinates" in module

print("PARADISE_CINEMA_COORDINATE_COVERAGE=PASS")
print("PARADISE_CINEMA_COLLECTIONS=PASS")
print("PARADISE_CINEMA_PROVIDER_NEUTRAL=PASS")
print("PARADISE_CINEMA_REHOST_BOUNDARY=PASS")
print("PARADISE_CINEMA_WIKISOURCE_GATE=PASS")
