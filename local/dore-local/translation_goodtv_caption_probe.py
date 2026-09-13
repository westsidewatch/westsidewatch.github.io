#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from urllib.request import Request, urlopen

VIDEO_ID = "kMUngZq5jss"
WATCH_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"
CANONICAL_ID = "cinema:video:goodtv:waiting-on-god-no-minute-wasted"


def fetch_watch_page() -> str:
    req = Request(
        WATCH_URL,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/140 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        },
    )
    with urlopen(req, timeout=30) as response:
        body = response.read().decode("utf-8", errors="replace")
    if VIDEO_ID not in body:
        raise RuntimeError("YouTube watch page did not expose requested video identity")
    return body


def extract_caption_track_count(html: str) -> int:
    match = re.search(r'"captionTracks"\s*:\s*(\[[^\]]*\])', html)
    if not match:
        return 0
    try:
        tracks = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"captionTracks present but unparsable: {exc}") from exc
    return len(tracks)


def main() -> None:
    html = fetch_watch_page()
    count = extract_caption_track_count(html)
    print(f"GOODTV_CANONICAL_ID={CANONICAL_ID}")
    print(f"GOODTV_VIDEO_ID={VIDEO_ID}")
    print(f"GOODTV_CAPTION_TRACK_COUNT={count}")
    if count != 0:
        raise SystemExit(f"expected zero provider caption tracks, found {count}")
    print("DORE_TRANSLATOR_GOODTV_ZERO_CAPTION_GATE=PASS")
    print("DORE_TRANSLATOR_GOODTV_NEXT_GATE=ASR_TIMED_TRANSCRIPT")


if __name__ == "__main__":
    main()
