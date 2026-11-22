#!/usr/bin/env python3
"""Changzhang comprehensive specialist experiment: four buckets, catalog->detail->HLS samples.

Source metadata and media candidates are not automatically placed on the public site.
The report explicitly separates catalog discovery, HLS probes, and playback certification.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from urllib.parse import urlencode

from source_discovery import network_fetch, play_groups
from four_category_round import BUCKETS, classification_evidence

API = "https://api.changzhang.tv/api.php/provide/vod/"
M3U8_API = "https://api.changzhang.tv/api.php/provide/vod/from/changzhangm3u8/"
ROOT = Path(__file__).resolve().parent
GOSPEL_WORDS = ("福音", "基督", "耶稣", "圣经", "耶穌", "聖經", "Jesus", "Christian", "Bible")
CATEGORY_NEEDLES = {
    "latest_us_uk_series": ("欧美剧", "歐美劇", "美国剧", "英国剧", "美剧", "英剧"),
    "japanese_anime": ("日韩动漫", "日本动漫", "日韩动画", "日本動畫"),
    "classic_films": ("电影", "電影", "剧情片", "劇情片", "喜剧片", "喜劇片"),
    "gospel_media": ("福音", "基督", "宗教", "圣经", "聖經"),
}

def endpoint(*, base=API, **params):
    return base + "?" + urlencode(params)

def category_tree(classes, category):
    """Return provider-native type IDs including descendants, never guessed IDs."""
    nodes = {}
    for x in classes:
        if isinstance(x, dict) and x.get("type_id") is not None:
            nodes[str(x["type_id"])] = x
    needles = CATEGORY_NEEDLES[category]
    direct = {ident for ident, item in nodes.items()
              if any(w.casefold() in str(item.get("type_name", "")).casefold() for w in needles)}
    selected = set(direct)
    while True:
        expanded = selected | {ident for ident, item in nodes.items()
                               if str(item.get("type_pid")) in selected}
        if expanded == selected:
            break
        selected = expanded
    return sorted(selected), sorted(direct)

def series_filter(item, category, year):
    """Strong genre/year checks only when provider supplied enough metadata."""
    info = {key:item.get(key) for key in ("vod_name","type_name","vod_class","vod_year","vod_area")}
    candidate={"title":info["vod_name"],"type_name":info["type_name"],
               "class":info["vod_class"],"year":info["vod_year"],"area":info["vod_area"]}
    return classification_evidence(candidate, category, year)

def scan(*, fetch=network_fetch, probe=None, max_pages=5, page_size=20,
         detail_batch=30, probe_count=6, current_year=None, sleep=0):
    year = current_year or datetime.now(timezone.utc).year
    report = {"schema": 1, "source": "changzhang", "url": API, "year": year,
              "method": "provider-class-tree/list-pagination/batch-detail/hls-byte-sample",
              "categories": {}, "errors": [], "media_samples": [],
              "status": "INCOMPLETE", "certified_ad_free": 0,
              "full_browser_playback": 0}
    def request(params, stage):
        try:
            value = fetch(endpoint(**params))
            if not isinstance(value, dict) or not isinstance(value.get("list"), list):
                raise ValueError("Malformed MacCMS response")
            return value
        except Exception as exc:
            report["errors"].append({"stage":stage,"params":params,"error":str(exc)[:220]})
            return None
    root = request({"ac":"list","pg":1,"pagesize":1}, "root")
    if root is None:
        report["status"] = "INFRASTRUCTURE_OR_API_FAILURE"
        return report
    classes = root.get("class", []) if isinstance(root.get("class", []), list) else []
    report["provider_class_count"] = len(classes)
    report["provider_total"] = root.get("total")
    found = {}
    per_bucket = defaultdict(set)
    for category, cfg in BUCKETS.items():
        ids, direct = category_tree(classes, category)
        stat = {"label":cfg["label"],"matched_type_ids":ids,
                "direct_type_ids":direct,"pages_requested":0,
                "records_listed":0,"candidate_ids":0,"metadata_matches":0}
        jobs = [("category", i) for i in ids]
        # Gospel themes often have no dedicated MacCMS type: search title/actors.
        if category == "gospel_media":
            jobs += [("keyword", word) for word in GOSPEL_WORDS]
        # If no provider-native match, record the issue rather than quietly calling
        # the global newest catalog a comprehensive category sweep.
        if not jobs:
            stat["warning"] = "Provider has no matching category IDs; category scan incomplete"
        for mode, term in jobs:
            for page in range(1, max_pages + 1):
                args = {"ac":"list" if mode=="category" else "detail",
                        "pg":page,"pagesize":page_size}
                if mode=="category": args["t"] = term
                else: args["wd"] = term
                payload = request(args, "%s:%s:%s" % (category,mode,term))
                stat["pages_requested"] += 1
                if payload is None: break
                rows = payload["list"]
                stat["records_listed"] += len(rows)
                for row in rows:
                    if not isinstance(row,dict):continue
                    item_id = row.get("vod_id")
                    if item_id is None:continue
                    ident = str(item_id)
                    found.setdefault(ident, row)
                    per_bucket[category].add(ident)
                if len(rows) < page_size or page >= int(payload.get("pagecount") or 1):
                    break
                if sleep: time.sleep(sleep)
        stat["candidate_ids"] = len(per_bucket[category])
        report["categories"][category] = stat
    # Fetch details in batches; the provider documents max 100 IDs per request.
    identifiers = list(found)
    report["unique_catalog_ids"] = len(identifiers)
    detail = {}
    for start in range(0, len(identifiers), detail_batch):
        batch = identifiers[start:start + detail_batch]
        payload = request({"ac":"detail","ids":",".join(batch)},
                          "batch-detail-%s" % start)
        if payload is None:continue
        for row in payload["list"]:
            if isinstance(row,dict) and row.get("vod_id") is not None:
                detail[str(row["vod_id"])] = row
        if sleep:time.sleep(sleep)
    report["details_received"] = len(detail)
    # The official provider offers a separate M3U8-only collection. If the
    # comprehensive endpoint returns web-player groups only, retry those IDs
    # against that canonical HLS collection without discarding original data.
    missing_media = [ident for ident,row in detail.items() if not play_groups(row)]
    report["hls_detail_fallback_requested"] = len(missing_media)
    report["hls_detail_fallback_recovered"] = 0
    for start in range(0,len(missing_media),detail_batch):
        ids = missing_media[start:start+detail_batch]
        try:
            payload = fetch(endpoint(base=M3U8_API,ac="detail",ids=",".join(ids)))
            rows = payload.get("list",[]) if isinstance(payload,dict) else []
            if not isinstance(rows,list):
                raise ValueError("Malformed M3U8-only API list")
            for row in rows:
                if not isinstance(row,dict) or row.get("vod_id") is None:
                    continue
                ident=str(row["vod_id"])
                if ident in detail and play_groups(row):
                    # Preserve the combined endpoint's editorial metadata.
                    old = detail[ident]
                    detail[ident] = {**old,
                                     "vod_play_from":row.get("vod_play_from"),
                                     "vod_play_url":row.get("vod_play_url")}
                    report["hls_detail_fallback_recovered"] += 1
        except Exception as exc:
            report["errors"].append({"stage":"m3u8-only-fallback",
                                     "batch":start, "error":str(exc)[:220]})
    candidates = []
    for ident, row in detail.items():
        groups = play_groups(row)
        if not groups:continue
        buckets = sorted(k for k, ids in per_bucket.items() if ident in ids)
        flags = {k:series_filter(row,k,year) for k in buckets}
        for k,v in flags.items():
            if v=="MATCH":report["categories"][k]["metadata_matches"] += 1
        candidates.append({
            "id":ident,"title":row.get("vod_name"),"year":row.get("vod_year"),
            "area":row.get("vod_area"),"type":row.get("type_name"),
            "category_buckets":buckets,"category_evidence":flags,
            "groups":groups,"status":"UNVERIFIED_CANDIDATE"
        })
    report["candidates"] = candidates
    report["media_candidate_titles"] = len(candidates)
    report["hls_urls"] = sum(1 for c in candidates for g in c["groups"]
                             for e in g["episodes"] if e["format"]=="m3u8")
    report["unique_hls_urls"] = len({e["url"] for c in candidates for g in c["groups"]
                                     for e in g["episodes"] if e["format"]=="m3u8"})
    seen = set()
    sampled_titles = set()
    if probe is not None:
        for c in candidates:
            for g in c["groups"]:
                for ep in g["episodes"]:
                    # Match the original 2026-11-20 benchmark: one first episode
                    # per distinct title, not 12 episodes from a single title.
                    if ep["format"]!="m3u8" or ep["url"] in seen or c["id"] in sampled_titles:
                        continue
                    seen.add(ep["url"])
                    sampled_titles.add(c["id"])
                    if len(report["media_samples"]) >= probe_count:
                        break
                    try:
                        finding = probe(ep["url"])
                        report["media_samples"].append({
                            "title":c["title"],"episode":ep["episode"],
                            "url":ep["url"],"result":finding})
                    except Exception as exc:
                        report["media_samples"].append({
                            "title":c["title"],"episode":ep["episode"],
                            "url":ep["url"],"result":{"status":"error","error":str(exc)[:220]}})
                if len(report["media_samples"])>=probe_count:break
            if len(report["media_samples"])>=probe_count:break
    report["status"] = ("PARTIAL_WITH_ERRORS" if report["errors"] else
                        "DISCOVERY_COMPLETE_UNVERIFIED")
    report["benchmark"] = {
        "2026-11-20_inspected":12,"2026-11-20_segment_probe_pass":10,
        "current_segment_probe_pass":sum(
            v["result"].get("status")=="segment-bytes-sampled"
            for v in report["media_samples"]),
        "comparable":len(sampled_titles)>=12,
        "note":"Historical 10/12 is only comparable after at least 12 equivalent first-episode 3-point probes."
    }
    return report

def main(argv=None):
    parser=argparse.ArgumentParser(description="Changzhang specialist four-bucket sweep")
    parser.add_argument("--max-pages",type=int,default=5)
    parser.add_argument("--page-size",type=int,default=20)
    parser.add_argument("--detail-batch",type=int,default=30)
    parser.add_argument("--probe-count",type=int,default=6)
    parser.add_argument("--sleep",type=float,default=.15)
    parser.add_argument("--output",default="shupian-changzhang-specialist.json")
    args=parser.parse_args(argv)
    if not 1<=args.max_pages<=200 or not 1<=args.page_size<=100 or not 1<=args.detail_batch<=100:
        parser.error("Invalid paging or batch limits")
    if not 0<=args.probe_count<=60:parser.error("probe-count must be 0..60")
    if args.sleep<0:parser.error("sleep must be nonnegative")
    from importlib.util import spec_from_file_location, module_from_spec
    src=ROOT.parent / "shupian_source_audit.py"
    spec=spec_from_file_location("shupian_source_audit",src)
    audit=module_from_spec(spec)
    spec.loader.exec_module(audit)
    report=scan(max_pages=args.max_pages,page_size=args.page_size,
                detail_batch=args.detail_batch,probe_count=args.probe_count,
                probe=(lambda url: audit.audit_one("Changzhang benchmark", url)) if args.probe_count else None,
                sleep=args.sleep)
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":report["status"],"unique_catalog_ids":report.get("unique_catalog_ids",0),
        "details_received":report.get("details_received",0),
        "candidate_titles":report.get("media_candidate_titles",0),
        "unique_hls_urls":report.get("unique_hls_urls",0),
        "media_samples":len(report["media_samples"]),
        "errors":len(report["errors"]),"output":args.output},ensure_ascii=False))
    return 0 if report["status"]=="DISCOVERY_COMPLETE_UNVERIFIED" else 2

if __name__=="__main__":
    raise SystemExit(main())
