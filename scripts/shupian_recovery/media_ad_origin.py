#!/usr/bin/env python3
"""PARADISO evidence-based ad-origin classifier.

Inspects saved page HTML/scripts, browser HAR and HLS playlist text, WITHOUT
loading or distributing copyrighted media. Page-layer redirect ads are NOT
the same as HLS advertising or baked-in video frames. Unobserved != absent.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

SITE_REDIRECT_PATTERNS = {
    "click_trigger": re.compile(r"addEventListener\s*\(\s*['\"](?:mousedown|click|pointerdown)['\"]", re.I),
    "timed_state": re.compile(r"localStorage|sessionStorage|shown_at", re.I),
    "popup_api": re.compile(r"window\.open\s*\(", re.I),
    "iframe_creation": re.compile(r"createElement\s*\(\s*['\"]iframe['\"]", re.I),
    "navigation": re.compile(r"location\.(?:assign|replace)\s*\(|location\.href\s*=", re.I),
}
HLS_AD = re.compile(r"(?im)^#EXT-X-(?:CUE-OUT|CUE-IN|DATERANGE|SCTE35|OATCLS-SCTE35|ASSET)\b")
MEDIA_SUFFIX = re.compile(r"\.(?:m3u8|mpd|mp4|ts|m4s)(?:$|[?#])", re.I)
KNOWN_AD_TERMS = re.compile(r"(?:casino|gambl|betting|lottery|彩票|賭場|赌场|博彩|/ads?/|popunder|popads)", re.I)

def inspect_html(html: str):
    hits = [name for name, pattern in SITE_REDIRECT_PATTERNS.items() if pattern.search(html)]
    # A page can mention these names without actually installing a malicious handler;
    # classify as suspects until correlated with observed network/navigation events.
    return {"page_signals": hits, "page_script_suspected": bool(hits),
            "confidence": "SIGNALS_ONLY" if hits else "NO_SCRIPT_SIGNAL_OBSERVED"}

def inspect_hls(text: str):
    if not text.lstrip("\ufeff\n ").startswith("#EXTM3U"):
        return {"status": "NOT_HLS", "ad_markers": []}
    markers = [line.strip()[:300] for line in text.splitlines() if HLS_AD.search(line)]
    return {"status": "HLS_PARSED", "ad_markers": markers,
            "ad_marker_suspected": bool(markers),
            "warning": "No markers cannot exclude baked-in frame advertising"}

def inspect_har(har: dict, page_host="www.mvffm.net"):
    entries = har.get("log", {}).get("entries", [])
    media, cross_origin, suspect, script = [], [], [], []
    for row in entries if isinstance(entries, list) else []:
        req = row.get("request", {}) if isinstance(row, dict) else {}
        res = row.get("response", {}) if isinstance(row, dict) else {}
        url = req.get("url", "")
        if not isinstance(url, str) or not url.startswith(("https://","http://")):
            continue
        host = (urlsplit(url).hostname or "").lower()
        info = {"host": host, "status": res.get("status"), "resource": urlsplit(url).path}
        if MEDIA_SUFFIX.search(url):
            media.append(info)
        if host != page_host.lower() and not host.endswith("." + page_host.lower().removeprefix("www.")):
            cross_origin.append(info)
        if KNOWN_AD_TERMS.search(url):
            suspect.append(info)
        if re.search(r"\.js(?:$|[?])", url, re.I):
            script.append(info)
    return {"requests_total": len(entries),
            "media_requests": media, "third_party_requests": cross_origin,
            "ad_suspect_requests": suspect, "script_requests": script,
            "note": "A third-party request alone is not proof it carries advertising"}

def classify(page=None, hls=None, har=None):
    result = {"schema":1, "site":"mvffm.net", "page":inspect_html(page) if page is not None else None,
              "hls":inspect_hls(hls) if hls is not None else None,
              "har":inspect_har(har) if har is not None else None,
              "site_layer": "NOT_OBSERVED", "manifest_layer": "NOT_OBSERVED",
              "baked_in_video": "UNDETERMINED"}
    if result["page"]:
        result["site_layer"] = ("SUSPECTED" if result["page"]["page_script_suspected"] else "NO_SIGNAL_IN_SUPPLIED_HTML")
    if result["har"] and result["har"]["ad_suspect_requests"]:
        result["site_layer"] = "SUSPECTED_BY_NETWORK"
    if result["hls"]:
        result["manifest_layer"] = ("AD_MARKERS_PRESENT" if result["hls"].get("ad_marker_suspected")
                                    else "NO_MARKERS_OBSERVED" if result["hls"]["status"]=="HLS_PARSED"
                                    else "NOT_HLS")
    return result

def main(argv=None):
    p=argparse.ArgumentParser(description="Classify page vs manifest vs in-video ad origin")
    p.add_argument("--html",type=Path)
    p.add_argument("--hls",type=Path)
    p.add_argument("--har",type=Path)
    p.add_argument("--output",type=Path,default=Path("shupian-ad-origin-evidence.json"))
    a=p.parse_args(argv)
    if not any((a.html,a.hls,a.har)):
        p.error("Provide at least one saved HTML, HLS, or HAR evidence file")
    data=classify(page=a.html.read_text(encoding="utf-8") if a.html else None,
                  hls=a.hls.read_text(encoding="utf-8") if a.hls else None,
                  har=json.loads(a.har.read_text(encoding="utf-8")) if a.har else None)
    a.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"site_layer":data["site_layer"],"manifest_layer":data["manifest_layer"],
                      "baked_in_video":data["baked_in_video"],"output":str(a.output)},ensure_ascii=False))

if __name__=="__main__":
    main()
