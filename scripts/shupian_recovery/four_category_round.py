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
from source_discovery import search, variants, network_fetch

ROOT = Path(__file__).resolve().parent

BUCKETS = {
    "latest_us_uk_series": {
        "label": "最新美劇／英劇",
        "type_hints": ["欧美剧", "歐美劇", "美剧", "英剧", "欧美"],
        "seeds": ["美剧", "英剧", "欧美剧", "美国电视剧", "英国电视剧", "US TV", "British TV"],
        "year_terms": ["美剧", "英剧", "欧美剧"],
    },
    "japanese_anime": {
        "label": "日本動漫",
        "type_hints": ["日韩动漫", "日本动漫", "动漫", "動畫", "动漫片"],
        "seeds": ["日本动漫", "日漫", "日本动画", "番剧", "Anime", "新番"],
        "year_terms": ["日本动漫", "新番"],
    },
    "classic_films": {
        "label": "經典電影",
        "type_hints": ["电影", "電影", "剧情片", "劇情片"],
        "seeds": ["经典电影", "經典電影", "经典影片", "影史经典", "Classic film", "Cinema classics"],
        "year_terms": [],
    },
    "gospel_media": {
        "label": "福音影視",
        "type_hints": ["福音", "基督", "宗教", "圣经", "聖經"],
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

def classification_evidence(candidate, bucket, year):
    """Classify by record metadata, not by the search words used to find it.

    Insufficient metadata is explicitly UNKNOWN rather than a false positive.
    """
    title = str(candidate.get("title") or "").lower()
    typ = str(candidate.get("type_name") or "").lower()
    kind = str(candidate.get("class") or "").lower()
    area = str(candidate.get("area") or "").lower()
    blob = " ".join((title, typ, kind, area))
    try:
        release_year = int(str(candidate.get("year") or "")[:4])
    except (ValueError, TypeError):
        release_year = None
    def has(*words):
        return any(w in blob for w in words)
    if bucket == "latest_us_uk_series":
        category = has("欧美剧", "美剧", "英剧", "美国剧", "英国剧", "us tv", "british tv")
        recent = release_year is not None and year - 1 <= release_year <= year
        return "MATCH" if category and recent else "UNKNOWN" if category and release_year is None else "NO_MATCH"
    if bucket == "japanese_anime":
        anime = has("动漫", "动画", "anime", "番剧", "アニメ")
        japan = has("日本", "日韩", "japan", "jp")
        return "MATCH" if anime and japan else "UNKNOWN" if anime and not area else "NO_MATCH"
    if bucket == "classic_films":
        film = has("电影", "劇情片", "剧情片", "film", "movie", "动作片", "喜剧片", "战争片")
        return "MATCH" if film and release_year is not None and release_year <= 2000 else "UNKNOWN" if film and release_year is None else "NO_MATCH"
    if bucket == "gospel_media":
        gospel = has("基督", "福音", "聖經", "圣经", "耶稣", "耶穌", "christian", "gospel", "bible", "jesus")
        return "MATCH" if gospel else "UNKNOWN"
    raise KeyError(bucket)

def round_scan(providers, *, year=None, pages=2, limit=30, fetch=None, extras=None, query_budget=None):
    """Run ALL four category sweeps, regardless of failures in other buckets."""
    if not providers:
        raise ValueError("At least one provider is required")
    output = {"schema": 1, "purpose": "four-category-dynamic-fuzzy-source-discovery",
              "year": year or datetime.now(timezone.utc).year, "categories": {},
              "warning": "Candidates have not yet passed ad-filter, decode, browser playback, or website publication."}
    # Each category queries the same broad catalog pages. Avoid redundant requests.
    cache = {}
    host_failures = {}
    upstream = fetch if fetch is not None else network_fetch
    def memo_fetch(url):
        from urllib.parse import urlsplit
        hostname = urlsplit(url).hostname or ""
        if hostname in host_failures:
            raise OSError("HOST_UNREACHABLE: " + host_failures[hostname])
        if url not in cache:
            try:
                cache[url] = (True, upstream(url))
            except Exception as exc:
                message = str(exc)[:220]
                cache[url] = (False, message)
                # A DNS failure is infrastructural: do not issue 200 requests
                # against a hostname that cannot be resolved.
                if any(s in message.lower() for s in ("name resolution", "getaddrinfo", "gaierror", "temporary failure in name resolution")):
                    host_failures[hostname] = message
        success, result = cache[url]
        if not success:
            raise OSError(result)
        return result
    for key, cfg in BUCKETS.items():
        queries = bucket_queries(key, year=output["year"],
                                 extras=(extras or {}).get(key, ()))
        if query_budget is not None:
            queries = queries[:max(1, query_budget)]
        opts = dict(pages=pages, limit=limit, discover=True, type_hints=cfg["type_hints"])
        opts["fetch"] = memo_fetch
        result = search(providers, queries, **opts)
        for candidate in result["candidates"]:
            candidate["category_evidence"] = classification_evidence(candidate, key, output["year"])
        output["categories"][key] = {
            "label": cfg["label"], "queries": queries,
            "matched_count": sum(c["category_evidence"] == "MATCH" for c in result["candidates"]),
            "unclassified_count": sum(c["category_evidence"] == "UNKNOWN" for c in result["candidates"]),
            "provider_count": len(providers), "probe_count": len(result["probes"]),
            "error_count": len(result["errors"]),
            "candidate_count": len(result["candidates"]),
            "candidates": result["candidates"], "probes": result["probes"],
            "errors": result["errors"],
            "stage": "DISCOVERY_ONLY",
        }
    output["totals"] = {
        "categories": len(output["categories"]),
        "unique_candidates": len({(c["provider"], str(c["id"] or c["title"])) for b in output["categories"].values() for c in b["candidates"]}),
        "category_matches": sum(b["matched_count"] for b in output["categories"].values()),
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
    p.add_argument("--query-budget", type=int, help="Max fuzzy terms per bucket; broad scan still always runs")
    p.add_argument("--request-timeout", type=float, default=6)
    p.add_argument("--output", default="shupian-four-category-discovery.json")
    args = p.parse_args(argv)
    if not 1 <= args.pages <= 20 or not 1 <= args.limit <= 100:
        p.error("pages must be 1..20 and limit 1..100")
    providers = json.loads(Path(args.providers).read_text(encoding="utf-8"))
    def live_fetch(url):
        return network_fetch(url, timeout=args.request_timeout)
    result = round_scan(providers, year=args.year, pages=args.pages, limit=args.limit,
                        fetch=live_fetch, query_budget=args.query_budget)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": args.output, **result["totals"]}, ensure_ascii=False))
    return 2 if result["totals"]["errors"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
