#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("source_probe_capability", HERE / "source_probe_capability.py")
assert SPEC and SPEC.loader
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)

FIXTURE = '''<!doctype html><html><head>
<meta property="og:title" content="Unknown Church Teaching">
<meta property="og:image" content="/poster.jpg">
<link rel="alternate" type="application/json+oembed" href="/oembed?url=x">
<script type="application/ld+json">{
  "@context":"https://schema.org","@type":"VideoObject",
  "name":"Unknown Church Teaching","thumbnailUrl":"/jsonld.jpg",
  "embedUrl":"https://player.example.invalid/embed/42","contentUrl":"https://cdn.example.invalid/master.m3u8"
}</script></head><body>
<video poster="/video-poster.jpg"><track kind="subtitles" srclang="zh-Hant" src="/captions.vtt"></video>
</body></html>'''

result = PROBE.execute({"url": "https://unknown-church.example/teaching/42", "html": FIXTURE})
assert result["ok"] is True
assert result["schema"] == "dore.source-probe.v0"
assert result["sourceAuthority"] is True and result["probeAuthority"] is False
assert result["reflexPersistent"] is False
assert len(result["capabilities"]["poster"]) >= 3
assert result["capabilities"]["oembed"]
assert result["capabilities"]["embed"]
assert result["capabilities"]["caption"][0]["language"] == "zh-Hant"
assert result["capabilities"]["manifest"][0]["manifest"] == "hls"
assert result["rights"]["rehost"] is False

blocked = PROBE.execute({"url": "https://zh.wikisource.org/wiki/Test", "html": "<html></html>"})
assert blocked["status"] == "blocked"

print("DORE_SOURCE_PROBE_STANDARD_FIRST=PASS")
print("DORE_SOURCE_PROBE_PROVIDER_NEUTRAL=PASS")
print("DORE_SOURCE_PROBE_WIKISOURCE_GATE=PASS")

if os.environ.get("DORE_SOURCE_PROBE_LIVE") == "1":
    goodtv = PROBE.execute({
        "url": "https://www.goodtv.tv/watch?episode=81076&series=196524&type=2",
        "allowNetwork": True,
        "timeoutSeconds": 25,
    })
    assert goodtv.get("ok") is True, goodtv
    assert goodtv.get("sourceAuthority") is True
    assert goodtv.get("rights", {}).get("rehost") is False
    if goodtv.get("status") == "completed":
        posters = goodtv.get("capabilities", {}).get("poster", [])
        assert posters, f"GOOD TV static fetch succeeded but exposed no poster: {goodtv}"
        print(f"DORE_SOURCE_PROBE_GOODTV_POSTER_COUNT={len(posters)}")
        print(f"DORE_SOURCE_PROBE_GOODTV_POSTER_SOURCE={posters[0].get('source')}")
        print("DORE_SOURCE_PROBE_GOODTV_STANDARD_LAYER=PASS")
    else:
        assert goodtv.get("status") == "partial", goodtv
        assert "runtime-browser-probe" in goodtv.get("needs", []), goodtv
        boundary = goodtv.get("provenance", {}).get("fetchBoundary", {})
        print(f"DORE_SOURCE_PROBE_GOODTV_FETCH_BOUNDARY={boundary.get('httpStatus')}")
        print("DORE_SOURCE_PROBE_GOODTV_RUNTIME_FALLBACK=PASS")
    print("DORE_SOURCE_PROBE_GOODTV_LIVE=PASS")
