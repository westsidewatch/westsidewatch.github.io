#!/usr/bin/env python3
"""Resolve all preview-first glyphs in corpus.json and write successes back.

No image download, crop, browser, or vectorization. A failed page stays unresolved
and never blocks successful glyphs. This script is the single batch entrypoint.
"""
from __future__ import annotations

import json
from pathlib import Path

from calligraphy_preview_resolver import resolve

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/calligraphy/corpus.json"


def main() -> int:
    data = json.loads(CORPUS.read_text(encoding="utf-8"))
    ok = 0
    failed = []
    for glyph in data.get("glyphs", []):
        if glyph.get("status") != "preview-resolve":
            continue
        page = glyph.get("sourceUrl")
        if not page:
            failed.append({"id": glyph.get("id"), "error": "missing sourceUrl"})
            continue
        try:
            result = resolve(page)
            preview = result.get("previewUrl")
            if preview:
                glyph["previewUrl"] = preview
                glyph["status"] = "preview-ready"
                glyph["previewResolvedFrom"] = result.get("finalPageUrl") or page
                ok += 1
            else:
                failed.append({"id": glyph.get("id"), "pageUrl": page, "error": "no preview candidate"})
        except Exception as exc:
            failed.append({"id": glyph.get("id"), "pageUrl": page, "error": str(exc)})
    tc = data.setdefault("tc001", {})
    tc["previewResolved"] = ok
    tc["previewFailed"] = [x["id"] for x in failed]
    tc["next"] = "render-resolved-previews-now"
    CORPUS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"resolved": ok, "failed": failed, "corpus": str(CORPUS)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
