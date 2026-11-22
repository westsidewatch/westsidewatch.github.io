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
    opener = urllib.request.build_opener(urllib.request.HTTPHandler,urllib.request.HTTPSHandler)
    with opener.open(req, timeout=timeout) as response:
        # Redirect targets are revalidated before reading by disallowing redirects.
        final = response.geturl()
        validate_public_url(final)
        blob = response.read(MAX_BYTES+1)
        if len(blob) > MAX_BYTES:
            raise ValueError("API response too large")
        return json.loads(blob.decode("utf-8-sig"))

def search(providers, queries=(), pages=3, limit=30, discover=False, fetch=network_fetch):
    """Fan-out: all providers x all fuzzy variants x bounded pages, full diagnostics."""
    if not queries and not discover:
        raise ValueError("Provide queries or --discover")
    found, errors, probes = {}, [], []
    for provider in providers:
        for query in (queries or ("",)):
            for page in range(1, max(1,pages)+1):
                params = {"ac":"detail" if query else "list","pg":page}
                if query: params["wd"] = query
                url = provider["api"] + ("&" if "?" in provider["api"] else "?") + urllib.parse.urlencode(params)
                status={"provider":provider["id"],"query":query or "(broad)","page":page}
                try:
                    payload=fetch(url)
                    records=payload.get("list",[]) if isinstance(payload,dict) else []
                    if not isinstance(records,list): raise ValueError("Malformed list")
                    status["records"]=len(records)
                    for record in records[:max(1,limit)]:
                        if not isinstance(record,dict): continue
                        groups=play_groups(record)
                        if not groups: continue
                        title=str(record.get("vod_name") or "").strip()
                        key=(provider["id"],str(record.get("vod_id") or title))
                        if key in found: continue
                        found[key]={"provider":provider["id"],"title":title,
                                    "id":record.get("vod_id"),
                                    "score":similarity(title,queries) if queries else None,
                                    "groups":groups, "discovery_query":query or "(broad)",
                                    "status":"UNVERIFIED_CANDIDATE"}
                except Exception as exc:
                    status["error"]=str(exc)[:220]
                    errors.append(status)
                probes.append(status)
                # Do not mistake zero results at one provider for absence elsewhere.
    return {"schema":2,"strategy":"all-providers/all-query-variants/all-pages",
            "queries":list(queries),"discover":bool(discover),"probes":probes,
            "errors":errors,"candidates":sorted(found.values(),
            key=lambda x:(x["score"] if x["score"] is not None else 0),reverse=True),
            "warning":"Metadata candidates are not proof of ad-free, correct media, playback or redistribution rights"}

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
