#!/usr/bin/env python3
"""Lightweight adapter for the open calligraphy-community index.

Mainline rule: indexed glyph libraries first; webpage preview scraping is fallback only.
No bulk asset download is required. Assets remain remote GitHub raw URLs.
"""
from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import PurePosixPath

INDEX_URL = "https://raw.githubusercontent.com/neil-zt/calligraphy-community/master/index.json"
RAW_BASE = "https://raw.githubusercontent.com/neil-zt/calligraphy-community/master/"
CORE = ("王羲之", "米芾", "趙孟頫", "赵孟頫", "赵孟俯", "文徵明", "文征明")
STYLE_WORDS = ("行書", "行书", "行草")


def load_index(url: str = INDEX_URL):
    req = urllib.request.Request(url, headers={"User-Agent": "WestsideWatch-Calligraphy/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def walk(node, prefix=""):
    if isinstance(node, dict):
        for key, value in node.items():
            p = f"{prefix}/{key}" if prefix else str(key)
            yield from walk(value, p)
    elif isinstance(node, list):
        for value in node:
            if isinstance(value, str):
                yield f"{prefix}/{value}" if prefix else value
            else:
                yield from walk(value, prefix)
    elif isinstance(node, str):
        yield f"{prefix}/{node}" if prefix else node


def score(path: str, char: str) -> int:
    parts = PurePosixPath(path).parts
    if char not in parts:
        return -1
    s = 100
    if any(name in path for name in CORE): s += 50
    if any(style in path for style in STYLE_WORDS): s += 30
    if "王羲之" in path: s += 10
    return s


def lookup(index, char: str):
    hits = []
    for path in walk(index):
        n = score(path, char)
        if n < 0: continue
        hits.append({
            "char": char,
            "score": n,
            "path": path,
            "assetUrl": RAW_BASE + urllib.parse.quote(path, safe="/!$&'()*+,;=:@")
        })
    hits.sort(key=lambda x: (-x["score"], x["path"]))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("text", nargs="?", default="敬畏耶和華是智慧的開端")
    ap.add_argument("--limit", type=int, default=8)
    args = ap.parse_args()
    index = load_index()
    result = {ch: lookup(index, ch)[:args.limit] for ch in dict.fromkeys(args.text) if not ch.isspace()}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
