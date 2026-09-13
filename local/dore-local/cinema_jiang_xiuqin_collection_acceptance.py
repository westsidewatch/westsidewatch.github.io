#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]
RESOURCE_FILE = ROOT / "cinema" / "data" / "video-resource.v0.json"
EXPECTED_CREATOR = "江秀琴"
EXPECTED_MINIMUM = 4
OFFICIAL_CHANNELS = {"GOOD TV 特會精選", "GOOD TV 好消息電視台"}


def youtube_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc.endswith("youtube.com"):
        return (parse_qs(parsed.query).get("v") or [""])[0]
    return ""


def main() -> None:
    payload = json.loads(RESOURCE_FILE.read_text(encoding="utf-8"))
    assert payload.get("schema") == "holy-light.video-resource.v0"
    items = payload.get("items") or []
    jiang = [item for item in items if item.get("creator") == EXPECTED_CREATOR]
    assert len(jiang) >= EXPECTED_MINIMUM, f"expected >= {EXPECTED_MINIMUM} Jiang Xiuqin resources, found {len(jiang)}"

    canonical_ids = [item.get("canonicalId") for item in jiang]
    assert all(canonical_ids)
    assert len(set(canonical_ids)) == len(canonical_ids), "duplicate Jiang canonical IDs"

    source_urls = []
    video_ids = []
    for item in jiang:
        assert item.get("language") == ["zh-Hant"]
        assert item.get("rights", {}).get("rehost") is False
        sources = item.get("providerSources") or []
        assert sources, f"missing provider source: {item['canonicalId']}"
        source = sources[0]
        assert source.get("provider") == "youtube"
        assert source.get("official") is True
        assert source.get("channel") in OFFICIAL_CHANNELS
        assert source.get("embed") is True
        assert source.get("access") == "embedded-playback"
        url = source.get("url") or ""
        vid = youtube_id(url)
        assert vid, f"invalid YouTube URL: {url}"
        source_urls.append(url)
        video_ids.append(vid)
        assert item.get("sourcePointer") == url
        assert source.get("embedUrl") == f"https://www.youtube.com/embed/{vid}"

    assert len(set(source_urls)) == len(source_urls), "duplicate Jiang provider URLs"
    assert len(set(video_ids)) == len(video_ids), "duplicate Jiang YouTube IDs"

    print(f"CINEMA_JIANG_XIUQIN_RESOURCE_COUNT={len(jiang)}")
    print("CINEMA_JIANG_XIUQIN_CANONICAL_DEDUP=PASS")
    print("CINEMA_JIANG_XIUQIN_OFFICIAL_PROVIDER_POLICY=PASS")
    print("CINEMA_JIANG_XIUQIN_COLLECTION=PASS")


if __name__ == "__main__":
    main()
