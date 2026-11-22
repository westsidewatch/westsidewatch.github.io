#!/usr/bin/env python3
"""Build a safe, public Changzhang experiment status from a private scan artifact.

Never publish raw third-party media links or call URL existence playback approval.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

KEYS=("latest_us_uk_series","japanese_anime","classic_films","gospel_media")
LABELS=("最新美劇／英劇","日本動漫","經典電影","福音影視")
def public_report(scan):
    buckets=scan.get("categories",{})
    candidates=scan.get("candidates", [])
    hls_checks=scan.get("media_samples", [])
    good_hls=sum(x.get("result",{}).get("status")=="segment-bytes-sampled" for x in hls_checks)
    ad_suspects=sum(bool(x.get("result",{}).get("ad_signals",{}).get("suspected")) for x in hls_checks)
    status=str(scan.get("status") or "NOT_RUN")
    catalog=scan.get("unique_catalog_ids",0)
    media=scan.get("unique_hls_urls",0)
    # A three-point segment probe does not certify ad-free playback or allow rehosting.
    progress = {"discovery":("PARTIAL" if media else "BLOCKED" if status in ("INFRASTRUCTURE_OR_API_FAILURE","PARTIAL_WITH_ERRORS") else "NO_MEDIA_FOUND"),
                "ad_quality":("AD_CUES_SUSPECTED" if ad_suspects else "SAMPLED_NOT_CERTIFIED" if hls_checks else "NOT_TESTED"),
                "playback":"NOT_TESTED",
                "website":"DIAGNOSTIC_ONLY"}
    summary={
        "schema":1, "source":"Changzhang", "origin":"https://changzhang.tv/help/app",
        "observed_at_utc":datetime.now(timezone.utc).isoformat(),
        "scan_status":status, "history":{"date":"2026-11-20","tested_titles":12,"segment_sample_pass":10},
        "today":{"catalog_candidates":(None if status=="INFRASTRUCTURE_OR_API_FAILURE" else catalog),"media_candidates":(None if status=="INFRASTRUCTURE_OR_API_FAILURE" else scan.get("media_candidate_titles",0)),
                 "unique_hls":(None if status=="INFRASTRUCTURE_OR_API_FAILURE" else media),"hls_sampled":len(hls_checks),"hls_sample_pass":good_hls,"manifest_ad_suspects":ad_suspects,
                 "failure_count":len(scan.get("errors",[]))},
        "stages":progress,"fully_verified_clean":0,"published_playable_sources":0,
        "categories":[{"key":k,"label":label,"catalog_ids":buckets.get(k,{}).get("candidate_ids",0),
                       "media_matches":buckets.get(k,{}).get("metadata_matches",0)}
                      for k,label in zip(KEYS,LABELS)],
        "errors":[{"stage":str(e.get("stage",""))[:80],
                   "reason":str(e.get("error",""))[:160]}
                  for e in scan.get("errors",[])[:10]],
        "warning":"A source is not certified ad-free or playable until actual playback, ad review and website acceptance."
    }
    return summary

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--scan",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(argv)
    if not a.scan.is_file():p.error("Real scan report file is required")
    data=json.loads(a.scan.read_text(encoding="utf-8"))
    result=public_report(data)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["today"],ensure_ascii=False))

if __name__=="__main__":
    main()
