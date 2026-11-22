#!/usr/bin/env python3
"""One PARADISO round = four broad, dynamic fuzzy discovery buckets.

This performs source *discovery*, stage 1 of four. It does not claim ad-free
playback or automatically publish candidates onto the public website.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from source_discovery import search, variants

ROOT = Path(__file__).resolve().parent

BUCKETS = {
    "latest_us_uk_series": {
        "label": "最新美劇／英劇",
        "seeds": ["美剧", "英剧", "欧美剧", "美国电视剧", "英国电视剧", "US TV", "British TV"],
        "year_terms": ["美剧", "英剧", "欧美剧"],
    },
    "japanese_anime": {
        "label": "日本動漫",
        "seeds": ["日本动漫", "日漫", "日本动画", "番剧", "Anime", "新番"],
        "year_terms": ["日本动漫", "新番"],
    },
    "classic_films": {
        "label": "經典電影",
        "seeds": ["经典电影", "經典電影", "经典影片", "影史经典", "Classic film", "Cinema classics"],
        "year_terms": [],
    },
    "gospel_media": {
        "label": "福音影視",
        "seeds": ["福音电影", "基督教电影", "圣经电影", "福音影视", "耶稣电影", "Christian film", "Bible film"],
        "year_terms": [],
    },
}

def bucket_queries(key: str, year: int | None = None, extras=()):
    """Generate broad multilingual variants AND current/prior-year terms."""
    if key not in BUCKETS:
        raise KeyError(key)
    y = year if year is not None else datetime.now(timezone.utc).year
    cfg = BUCKETS[key]
    terms = list(cfg["seeds"])
    for base in cfg["year_terms"]:
        terms.extend([base + " " + str(y), base + " " + str(y - 1)])
    for value in extras:
        terms.extend(variants(value))
    return list(dict.fromkeys(terms))

def round_scan(providers, *, year=None, pages=2, limit=30, fetch=None, extras=None):
    """Run ALL four category sweeps, regardless of failures in other buckets."""
    if not providers:
        raise ValueError("At least one provider is required")
    output = {"schema": 1, "purpose": "four-category-dynamic-fuzzy-source-discovery",
              "year": year or datetime.now(timezone.utc).year, "categories": {},
              "warning": "Candidates have not yet passed ad-filter, decode, browser playback, or website publication."}
    for key, cfg in BUCKETS.items():
        queries = bucket_queries(key, year=output["year"],
                                 extras=(extras or {}).get(key, ()))
        opts = dict(pages=pages, limit=limit, discover=True)
        if fetch is not None:
            opts["fetch"] = fetch
        result = search(providers, queries, **opts)
        output["categories"][key] = {
            "label": cfg["label"], "queries": queries,
            "provider_count": len(providers), "probe_count": len(result["probes"]),
            "error_count": len(result["errors"]),
            "candidate_count": len(result["candidates"]),
            "candidates": result["candidates"], "probes": result["probes"],
            "errors": result["errors"],
            "stage": "DISCOVERY_ONLY",
        }
    output["totals"] = {
        "categories": len(output["categories"]),
        "probes": sum(v["probe_count"] for v in output["categories"].values()),
        "candidates": sum(v["candidate_count"] for v in output["categories"].values()),
        "errors": sum(v["error_count"] for v in output["categories"].values()),
    }
    return output

def main(argv=None):
    p = argparse.ArgumentParser(description="Run comprehensive four-category PARADISO discovery")
    p.add_argument("--providers", default=str(ROOT / "providers.json"))
    p.add_argument("--pages", type=int, default=2)
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--year", type=int)
    p.add_argument("--output", default="shupian-four-category-discovery.json")
    args = p.parse_args(argv)
    if not 1 <= args.pages <= 20 or not 1 <= args.limit <= 100:
        p.error("pages must be 1..20 and limit 1..100")
    providers = json.loads(Path(args.providers).read_text(encoding="utf-8"))
    result = round_scan(providers, year=args.year, pages=args.pages, limit=args.limit)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": args.output, **result["totals"]}, ensure_ascii=False))
    return 2 if result["totals"]["errors"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
