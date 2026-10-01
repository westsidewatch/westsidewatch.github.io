#!/usr/bin/env python3
"""Resolve a visible glyph preview URL from a calligraphy reference page.

Intentionally small: no browser, no download/crop/vectorization pipeline.
It fetches HTML and ranks image candidates from og:image, img src/srcset,
data-src/data-original/data-lazy-src. Output is JSON for direct corpus use.
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; WestsideWatch-Calligraphy/1.0)"
IMAGE_EXT = re.compile(r"\.(?:jpe?g|png|webp|gif|avif)(?:[?#].*)?$", re.I)
ATTR = re.compile(r'''(?:src|data-src|data-original|data-lazy-src)\s*=\s*["']([^"']+)["']''', re.I)
SRCSET = re.compile(r'''srcset\s*=\s*["']([^"']+)["']''', re.I)
OG = re.compile(r'''<meta[^>]+(?:property|name)=["'](?:og:image|twitter:image)["'][^>]+content=["']([^"']+)["']''', re.I)
OG_REV = re.compile(r'''<meta[^>]+content=["']([^"']+)["'][^>]+(?:property|name)=["'](?:og:image|twitter:image)["']''', re.I)
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)

BAD = ("logo", "icon", "avatar", "banner", "qrcode", "qr-code", "loading", "placeholder", "spacer", "advert", "ads/")


def absolute(base: str, value: str) -> str:
    value = html_lib.unescape(value.strip())
    if value.startswith("data:"):
        return ""
    return urllib.parse.urljoin(base, value)


def score(url: str, tag: str = "", bonus: int = 0) -> int:
    low = (url + " " + tag).lower()
    if any(x in low for x in BAD):
        return -100
    s = bonus
    if IMAGE_EXT.search(url): s += 12
    if any(x in low for x in ("shufa", "calligraphy", "glyph", "zi-", "upload", "image", "img")): s += 5
    if any(x in low for x in ("thumb", "small")): s -= 2
    if any(x in low for x in ("large", "original", "zoom")): s += 3
    return s


def resolve(page_url: str) -> dict:
    req = urllib.request.Request(page_url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=15) as r:
        final_url = r.geturl()
        body = r.read().decode(r.headers.get_content_charset() or "utf-8", errors="replace")

    candidates: dict[str, dict] = {}
    def add(raw: str, kind: str, tag: str = "", bonus: int = 0):
        url = absolute(final_url, raw)
        if not url or not url.startswith(("http://", "https://")): return
        item = {"url": url, "kind": kind, "score": score(url, tag, bonus)}
        old = candidates.get(url)
        if not old or item["score"] > old["score"]: candidates[url] = item

    for rx in (OG, OG_REV):
        for m in rx.finditer(body): add(m.group(1), "meta-preview", bonus=8)

    for tagm in IMG_TAG.finditer(body):
        tag = tagm.group(0)
        for m in ATTR.finditer(tag): add(m.group(1), "img", tag, 4)
        for m in SRCSET.finditer(tag):
            for part in m.group(1).split(','):
                raw = part.strip().split()[0] if part.strip() else ""
                if raw: add(raw, "srcset", tag, 6)

    ranked = sorted((x for x in candidates.values() if x["score"] >= 0), key=lambda x: x["score"], reverse=True)
    return {"pageUrl": page_url, "finalPageUrl": final_url, "previewUrl": ranked[0]["url"] if ranked else None, "candidates": ranked[:12]}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("urls", nargs="+")
    args = p.parse_args()
    results = []
    for url in args.urls:
        try: results.append(resolve(url))
        except Exception as e: results.append({"pageUrl": url, "previewUrl": None, "error": str(e)})
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
