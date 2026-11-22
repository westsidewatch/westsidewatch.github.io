#!/usr/bin/env python3
"""PARADISO source-discovery cycle: discovery -> ad/quality -> playback -> site evidence.

Discovery results are research candidates, never automatic catalog admission.
Only public HTTPS endpoints explicitly listed by the operator are queried.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen, build_opener, HTTPRedirectHandler

from legacy_engine_core import VerificationError, validate_public_url, parse_hls

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = Path(__file__).with_name("source_providers.json")
REPORT = ROOT / "static/shupian/recovery/engine-live-round.json"
MEDIA_RE = re.compile(r"\.(?:m3u8|mp4|mpd)(?:$|[?#])", re.I)
AD_RE = re.compile(r"(?:^|[/._-])(?:ads?|commercial|preroll|promo)(?:[/._-]|$)", re.I)
ALLOWED_MEDIA = {"m3u8", "mp4", "mpd"}

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise VerificationError("Redirect refused; do not fetch unapproved destination")

SAFE_OPENER = build_opener(NoRedirect()).open

def clean_url(value):
    value = str(value or "").strip()
    validate_public_url(value)
    if not MEDIA_RE.search(value):
        raise VerificationError("Not a recognized direct media URL")
    return value

def parse_groups(payload):
    """Restore original MacCMS $$$ groups / # episodes / $ URL grammar."""
    from_names = str(payload.get("vod_play_from") or "").split("$$$")
    groups = str(payload.get("vod_play_url") or "").split("$$$")
    output = []
    seen = set()
    for i, group in enumerate(groups):
        origin = from_names[i].strip() if i < len(from_names) else "unknown"
        episodes = []
        for item in group.split("#"):
            if "$" not in item:
                continue
            label, raw = item.split("$", 1)
            try:
                media_url = clean_url(raw)
            except (VerificationError, ValueError):
                continue
            key = (label.strip(), media_url)
            if key in seen:
                continue
            seen.add(key)
            episodes.append({"episode": label.strip() or "完整版", "url": media_url,
                             "format": urlparse(media_url).path.rsplit(".", 1)[-1].lower()})
        if episodes:
            output.append({"origin": origin, "episodes": episodes})
    return output

def fetch_json(url, timeout=12, max_bytes=1800000, opener=SAFE_OPENER):
    validate_public_url(url)
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "PARADISO-Research/2.0"})
    with opener(request, timeout=timeout) as response:
        if urlparse(response.geturl()).hostname != urlparse(url).hostname:
            raise VerificationError("Cross-host redirect blocked")
        data = response.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise VerificationError("Provider response too large")
    return json.loads(data.decode("utf-8-sig"))

def fetch_manifest(url, timeout=12, opener=SAFE_OPENER):
    validate_public_url(url)
    request = Request(url, headers={"Accept": "application/vnd.apple.mpegurl", "User-Agent": "PARADISO-Research/2.0"})
    with opener(request, timeout=timeout) as response:
        if urlparse(response.geturl()).hostname != urlparse(url).hostname:
            raise VerificationError("Cross-host redirect blocked")
        payload = response.read(600001)
        if len(payload) > 600000:
            raise VerificationError("Playlist too large")
    return parse_hls(payload.decode("utf-8-sig", errors="replace"), url)

def source_probe(candidate, fetcher=fetch_manifest):
    """HLS manifest inspection: *never* declares a film ad-free or playable."""
    url = candidate["url"]
    entry = {"format": candidate["format"], "manifest": "not-tested",
             "ad_cues": "unknown", "playback": "not-tested", "clean": "not-certified"}
    if candidate["format"] != "m3u8":
        entry["manifest"] = "other-format-requires-decoder"
        return entry
    try:
        parsed = fetcher(url)
        if parsed["master"] and parsed["children"]:
            parsed = fetcher(parsed["children"][0])
        entry["manifest"] = "parsed" if parsed["segments"] else "empty"
        entry["segment_count"] = len(parsed["segments"])
        entry["duration_sec"] = parsed["duration_sec"]
        entry["ad_cues"] = "suspected" if parsed["ad_markers"] or AD_RE.search(url) else "none-detected"
        entry["encrypted"] = bool(parsed["encryption"])
        entry["playback"] = "requires-in-site-browser-test"
    except Exception as exc:
        entry["manifest"] = "failed"
        entry["error"] = (type(exc).__name__ + ": " + str(exc))[:180]
    return entry

def normalize_results(raw, keyword, provider_id):
    normalized = []
    for item in raw.get("list", []) if isinstance(raw.get("list"), list) else []:
        if not isinstance(item, dict):
            continue
        groups = parse_groups(item)
        if not groups:
            continue
        normalized.append({
            "provider": provider_id, "query": keyword,
            "title": str(item.get("vod_name") or "")[:180],
            "id": str(item.get("vod_id") or "")[:80],
            "groups": groups,
        })
    return normalized

def scan(keywords, providers, fetcher=fetch_json, probe=source_probe,
         per_provider_limit=25, max_audits=12, workers=4):
    tasks = [(p, kw) for p in providers if p.get("enabled", True) for kw in keywords]
    records, errors = [], []
    def one(p, kw):
        api = validate_public_url(p["api"])
        separator = "&" if "?" in api else "?"
        data = fetcher(api + separator + "ac=detail&wd=" + quote(kw))
        if not isinstance(data, dict):
            raise VerificationError("Provider did not return a JSON object")
        return normalize_results({"list": data.get("list", [])[:per_provider_limit]}, kw, p["id"])
    with ThreadPoolExecutor(max_workers=max(1, min(workers, 8))) as executor:
        futures = {executor.submit(one, p, kw): (p["id"], kw) for p, kw in tasks}
        for future in as_completed(futures):
            provider, kw = futures[future]
            try:
                records.extend(future.result())
            except Exception as exc:
                errors.append({"provider": provider, "query": kw, "error": (type(exc).__name__ + ": " + str(exc))[:180]})
    records.sort(key=lambda x: (x["query"], x["title"], x["provider"]))
    candidates = []
    distinct = set()
    for row in records:
        for group in row["groups"]:
            for episode in group["episodes"]:
                if episode["url"] in distinct:
                    continue
                distinct.add(episode["url"])
                candidates.append({**episode, "provider": row["provider"], "title": row["title"]})
    audits = []
    for candidate in candidates[:max(0, max_audits)]:
        detail = probe(candidate)
        # Never write the discovered raw media URL to the public website report.
        audits.append({"title": candidate["title"], "episode": candidate["episode"],
                       "provider": candidate["provider"], **detail})
    return {
        "schema": 2, "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "queries": keywords, "providers_requested": len(providers),
        "provider_queries_attempted": len(tasks),
        "provider_queries_failed": len(errors),
        "works_found": len(records), "unique_media_candidates": len(candidates),
        "hls_candidates": sum(x["format"] == "m3u8" for x in candidates),
        "manifests_parsed": sum(a["manifest"] == "parsed" for a in audits),
        "suspected_ad_cues": sum(a["ad_cues"] == "suspected" for a in audits),
        "audited": len(audits), "errors": errors, "audits": audits,
        "stages": {"discovery": "attempted", "ad_quality": "manifest-only",
                   "playback": "not-tested-in-browser", "website": "report-only"},
        "completion": "NOT_COMPLETED",
        "limitations": "Manifest parsing cannot certify ads, playback, correct content or rights. No auto-import."
    }

def main(argv=None):
    parser = argparse.ArgumentParser(description="PARADISO fresh media-source discovery experiment")
    parser.add_argument("--keywords", nargs="+", required=True)
    parser.add_argument("--providers", type=Path, default=REGISTRY)
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--max-audits", type=int, default=12)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args(argv)
    providers = json.loads(args.providers.read_text(encoding="utf-8"))
    result = scan(args.keywords, providers, max_audits=args.max_audits, workers=args.workers)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("provider_queries_attempted", "provider_queries_failed", "works_found", "unique_media_candidates", "manifests_parsed", "completion")}, ensure_ascii=False))
    if result["provider_queries_failed"] == result["provider_queries_attempted"]:
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
