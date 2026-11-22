#!/usr/bin/env python3
"""PARADISO multi-provider, fuzzy and broad discovery. No auto-publication.

Every search fans out to every configured provider, every query variant and
bounded result pages. Broad scan (--discover) does not require a named show.
A candidate is NOT verified, ad-free or authorized for public rebroadcast.
"""
from __future__ import annotations
import argparse
import difflib
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAX_BYTES = 2_000_000
UA = "PARADISO-Discovery/2.0 (source research)"

def normalized(s):
    s = unicodedata.normalize("NFKC", str(s or "")).casefold()
    return re.sub(r"[^\w\u3400-\u9fff]+", "", s)

def variants(query, aliases=()):
    """Generate broad AND specific forms, preserving order and no duplicates."""
    terms = []
    for raw in (query, *aliases):
        v = str(raw or "").strip()
        if not v:
            continue
        terms.append(v)
        simplified = re.sub(r"\b(?:season|series|s)\s*\d+\b|第[一二三四五六七八九十\d]+季|\b(?:19|20)\d{2}\b", "", v, flags=re.I).strip(" -—:")
        if simplified and simplified != v:
            terms.append(simplified)
        for part in re.split(r"\s*[/／|]\s*", v):
            if part and part != v:
                terms.append(part)
    return list(dict.fromkeys(t for t in terms if t))

def similarity(title, terms):
    title_n = normalized(title)
    if not title_n:
        return 0.0
    scores = []
    for term in terms:
        n = normalized(term)
        if not n:
            continue
        if n == title_n:
            scores.append(1.0)
        elif n in title_n or title_n in n:
            scores.append(0.85)
        else:
            scores.append(round(difflib.SequenceMatcher(None, n, title_n).ratio(), 4))
    return max(scores, default=0.0)

def play_groups(record):
    """Retain ALL playable episode links, rather than the first source only."""
    origins = str(record.get("vod_play_from") or "").split("$$$")
    groups = str(record.get("vod_play_url") or "").split("$$$")
    result = []
    for i, raw in enumerate(groups):
        episodes = []
        for item in raw.split("#"):
            if "$" not in item:
                continue
            label, link = item.split("$", 1)
            link = link.strip()
            parts = urllib.parse.urlsplit(link)
            if parts.scheme != "https" or not parts.hostname:
                continue
            if not re.search(r"\.(?:m3u8|mp4|mpd)(?:$|[?#])", link, re.I):
                continue
            episodes.append({"episode":label.strip() or "完整版", "url":link,
                             "format":re.search(r"\.(m3u8|mp4|mpd)(?:$|[?#])",link,re.I).group(1).lower()})
        if episodes:
            result.append({"origin":origins[i].strip() if i < len(origins) else "unknown", "episodes":episodes})
    return result

def network_fetch(url, timeout=15):
    from legacy_engine_core import validate_public_url
    validate_public_url(url)
    req = urllib.request.Request(url, headers={"User-Agent":UA,"Accept":"application/json"})
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            raise ValueError("Unexpected source API redirect: " + str(code))
    opener = urllib.request.build_opener(NoRedirect)
    with opener.open(req, timeout=timeout) as response:
        validate_public_url(response.geturl())
        blob = response.read(MAX_BYTES+1)
        if len(blob) > MAX_BYTES:
            raise ValueError("API response too large")
        return json.loads(blob.decode("utf-8-sig"))

def search(providers, queries=(), pages=3, limit=30, discover=False, fetch=network_fetch, type_hints=()):
    """Search every provider/page and hydrate list-only records via ac=detail.

    Native MacCMS ac=list normally omits vod_play_url. Search is a two-stage
    process: discover catalog IDs, then retrieve each matching detail record.
    Providers may return full details from search; those avoid extra requests.
    """
    if not queries and not discover:
        raise ValueError("Provide queries or --discover")
    found, errors, probes = {}, [], []
    details_seen = set()
    for provider in providers:
        base = provider["api"]
        categories = [None]
        # Ask each provider for its OWN categories: type_id values vary by site.
        # Search category listings first; free-text keywords remain complementary.
        if discover and type_hints:
            class_url = base + ("&" if "?" in base else "?") + urllib.parse.urlencode({"ac": "list", "pg": 1})
            try:
                class_payload = fetch(class_url)
                entries = class_payload.get("class", []) if isinstance(class_payload, dict) else []
                selected = []
                for entry in entries if isinstance(entries, list) else []:
                    if not isinstance(entry, dict):
                        continue
                    name = str(entry.get("type_name") or "")
                    if any(hint.casefold() in name.casefold() for hint in type_hints):
                        type_id = entry.get("type_id")
                        if type_id is not None:
                            selected.append(str(type_id))
                categories = list(dict.fromkeys(selected)) or [None]
            except Exception as exc:
                errors.append({"provider": provider["id"], "stage": "category-index",
                               "error": str(exc)[:220]})
        requests = [(query, None) for query in queries]
        if discover:
            requests.extend([("", category_id) for category_id in categories])
        for query, category_id in requests:
            for page in range(1, max(1, pages) + 1):
                params = {"ac": "detail" if query else "list", "pg": page}
                if query:
                    params["wd"] = query
                if category_id is not None:
                    params["t"] = category_id
                url = base + ("&" if "?" in base else "?") + urllib.parse.urlencode(params)
                status = {"provider": provider["id"], "query": query or "(broad)", "page": page,
                          "category_id": category_id}
                try:
                    payload = fetch(url)
                    records = payload.get("list", []) if isinstance(payload, dict) else []
                    if not isinstance(records, list):
                        raise ValueError("Malformed list")
                    status["records"] = len(records)
                    hydrated = 0
                    for record in records[:max(1, limit)]:
                        if not isinstance(record, dict):
                            continue
                        record_id = str(record.get("vod_id") or "").strip()
                        title = str(record.get("vod_name") or "").strip()
                        key = (provider["id"], record_id or title)
                        if key in found:
                            continue
                        groups = play_groups(record)
                        if not groups and record_id and key not in details_seen:
                            details_seen.add(key)
                            detail_url = base + ("&" if "?" in base else "?") + urllib.parse.urlencode(
                                {"ac": "detail", "ids": record_id})
                            try:
                                detail_payload = fetch(detail_url)
                                detailed = detail_payload.get("list", []) if isinstance(detail_payload, dict) else []
                                if not isinstance(detailed, list):
                                    raise ValueError("Malformed detail list")
                                for candidate in detailed:
                                    if str(candidate.get("vod_id") or "") == record_id:
                                        groups = play_groups(candidate)
                                        if groups:
                                            record = {**record, **{k: v for k, v in candidate.items() if v is not None}}
                                            hydrated += 1
                                        break
                            except Exception as exc:
                                errors.append({"provider": provider["id"], "query": query or "(broad)",
                                               "page": page, "id": record_id, "stage": "detail",
                                               "error": str(exc)[:220]})
                        if not groups:
                            continue
                        found[key] = {
                            "provider": provider["id"], "title": str(record.get("vod_name") or title),
                            "id": record.get("vod_id"),
                            "type_name": record.get("type_name"),
                            "year": record.get("vod_year"),
                            "area": record.get("vod_area"),
                            "class": record.get("vod_class"),
                            "score": similarity(str(record.get("vod_name") or title), queries) if queries else None,
                            "groups": groups, "discovery_query": query or "(broad)",
                            "discovery_type_id": category_id,
                            "status": "UNVERIFIED_CANDIDATE",
                        }
                    status["detail_hydrated"] = hydrated
                except Exception as exc:
                    status["error"] = str(exc)[:220]
                    status["stage"] = "list-or-search"
                    errors.append(status)
                probes.append(status)
                # Never treat one provider's empty response as global absence.
    return {
        "schema": 4, "strategy": "all-providers/provider-specific-type-IDs/fuzzy-queries/pagination/detail-hydration",
        "queries": list(queries), "discover": bool(discover), "probes": probes,
        "errors": errors, "candidates": sorted(
            found.values(), key=lambda x: (x["score"] if x["score"] is not None else 0),
            reverse=True),
        "warning": "Metadata candidates do not certify correct content, ad-free playback or rights",
    }

def main(argv=None):
    p=argparse.ArgumentParser(description="Batch broad and fuzzy source research")
    p.add_argument("--query",action="append",default=[],help="Repeat for multiple film/series names")
    p.add_argument("--alias",action="append",default=[],help="Known alternate/localized title")
    p.add_argument("--discover",action="store_true",help="Scan provider recent catalog without a named title")
    p.add_argument("--pages",type=int,default=3)
    p.add_argument("--limit",type=int,default=30)
    p.add_argument("--providers",default=str(ROOT/"providers.json"))
    p.add_argument("--output",default="shupian-discovery-report.json")
    a=p.parse_args(argv)
    if not 1<=a.pages<=20 or not 1<=a.limit<=100: p.error("pages 1..20, limit 1..100")
    providers=json.loads(Path(a.providers).read_text(encoding="utf-8"))
    terms=[]
    for q in a.query: terms.extend(variants(q,a.alias))
    terms=list(dict.fromkeys(terms))
    result=search(providers,terms,pages=a.pages,limit=a.limit,discover=a.discover)
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"providers":len(providers),"queries":len(terms),
                      "pages":a.pages,"probes":len(result["probes"]),
                      "candidates":len(result["candidates"]),"errors":len(result["errors"]),
                      "output":a.output},ensure_ascii=False))
    return 0 if not result["errors"] else 2

if __name__=="__main__":
    sys.exit(main())
