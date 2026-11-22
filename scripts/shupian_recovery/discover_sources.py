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
import unicodedata
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen, build_opener, HTTPRedirectHandler

from legacy_engine_core import VerificationError, validate_public_url, parse_hls
from source_lifecycle import (url_fingerprint, episode_key, equivalent_episode,
                              source_evidence, failure_class, sanitized_error)

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
    return quote(value, safe=":/?&=%#@!$\x27()*+,;~-._")

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

def probe_segment(url, timeout=10, max_bytes=4096, opener=SAFE_OPENER):
    """Small bounded bytes probe, no full-media download or public distribution."""
    validate_public_url(url)
    request = Request(url, headers={
        "Range": "bytes=0-" + str(max_bytes - 1),
        "User-Agent": "PARADISO-Research/2.0"
    })
    with opener(request, timeout=timeout) as response:
        data = response.read(max_bytes)
        status = response.status
        media_type = response.headers.get("Content-Type", "")
    ts = len(data) >= 189 and data[0] == 0x47 and data[188] == 0x47
    fmp4 = b"ftyp" in data[:32] or b"moof" in data[:32]
    html = b"<html" in data[:300].lower() or b"<!doctype" in data[:300].lower()
    return {"ok": bool((ts or fmp4) and not html), "http": status,
            "signature": "mpeg-ts" if ts else ("fmp4" if fmp4 else "unrecognized"),
            "sample_bytes": len(data), "content_type": media_type[:80]}

def source_probe(candidate, fetcher=fetch_manifest, segment_fetcher=probe_segment):
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
        if parsed["segments"] and not parsed["encryption"] and not parsed["ad_markers"]:
            segs = parsed["segments"]
            checks = []
            for i in sorted(set([0, len(segs) // 2, len(segs) - 1])):
                try:
                    checks.append({"position": i, **segment_fetcher(segs[i])})
                except Exception as subexc:
                    checks.append({"position": i, "ok": False,
                                   "error": sanitized_error(type(subexc).__name__ + ": " + str(subexc)),
                                   "failure_class": failure_class(subexc)})
            entry["segment_checks"] = checks
            entry["segment_sample"] = "pass" if all(x["ok"] for x in checks) else "failed"
    except Exception as exc:
        entry["manifest"] = "failed"
        entry["error"] = sanitized_error(type(exc).__name__ + ": " + str(exc))
        entry["failure_class"] = failure_class(exc)
    # A parsed manifest and a manifest HTTP failure are mutually exclusive.
    # Segment failure details belong to segment_checks, not top-level manifest.
    if entry["manifest"] == "parsed":
        entry.pop("error", None)
        entry.pop("failure_class", None)
    return entry

def title_matches(title, keyword):
    """Exact work match with season suffix, not loose provider keyword hits."""
    norm = lambda s: re.sub(r"[\W_]+", "", unicodedata.normalize("NFKC", str(s)).casefold())
    aliases = {
        "黑鏡": ("黑鏡", "黑镜", "Black Mirror"),
        "神探夏洛克": ("神探夏洛克", "Sherlock", "新福尔摩斯", "新福爾摩斯"),
    }
    alternatives = aliases.get(keyword, (keyword,))
    name = norm(title)
    for alias in alternatives:
        root = norm(alias)
        if name == root or re.fullmatch(re.escape(root) + r"(?:第[一二三四五六七八九十0-9]+季|s[0-9]+|season[0-9]+|[0-9]+)", name):
            return True
    return False

def normalize_results(raw, keyword, provider_id):
    normalized = []
    for item in raw.get("list", []) if isinstance(raw.get("list"), list) else []:
        if not isinstance(item, dict):
            continue
        if not title_matches(item.get("vod_name", ""), keyword):
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
         per_provider_limit=25, max_audits=12, workers=4, focus=None,
         previous_audits=None, previous_observed_at=None):
    previous_audits = previous_audits or {}
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
                errors.append({"provider": provider, "query": kw, "error": sanitized_error(type(exc).__name__ + ": " + str(exc)),
                               "failure_class": failure_class(exc)})
    records.sort(key=lambda x: (x["query"], x["title"], x["provider"]))
    candidates = []
    distinct = set()
    for row in records:
        for group in row["groups"]:
            for episode in group["episodes"]:
                if episode["url"] in distinct:
                    continue
                distinct.add(episode["url"])
                candidates.append({**episode, "query": row["query"], "provider": row["provider"], "title": row["title"]})
    # Spread audits over titles and providers, not just the first response.
    pools = {}
    for candidate in candidates:
        pools.setdefault((candidate["query"], candidate["provider"]), []).append(candidate)
    selected = []
    while len(selected) < max(0, max_audits) and any(pools.values()):
        for key in sorted(pools):
            if pools[key]:
                selected.append(pools[key].pop(0))
            if len(selected) >= max_audits:
                break
    # When repeating a scan, check the exact previous provider+episode first,
    # then alternate providers for that same title and episode. Do not lose URL
    # identity: matched title/episode alone is not proof of the same address.
    focus = focus or set()
    if focus:
        def priority(c):
            k = (c["provider"], c["title"], c["episode"])
            exact = k in focus
            alternate = any(equivalent_episode(c["title"], c["episode"], t, ep)
                            and c["provider"] != p for p, t, ep in focus)
            return (0 if exact else 1 if alternate else 2,
                    c["query"], c["provider"], c["episode"])
        selected = sorted(candidates, key=priority)[:max(0, max_audits)]
    audits = []
    for candidate in selected:
        key = episode_key(candidate["provider"], candidate["title"], candidate["episode"])
        prior = previous_audits.get(key)
        evidence = source_evidence(candidate, prior)
        if prior and previous_observed_at:
            evidence["previous_observed_at_utc"] = previous_observed_at
        detail = probe(candidate)
        if detail.get("manifest") == "parsed":
            detail = {k: v for k, v in detail.items() if k not in ("error", "failure_class")}
        previous_status = prior.get("manifest") if prior else None
        current_status = detail.get("manifest")
        if previous_status not in ("parsed", "failed"):
            transition = "new_observation"
        elif previous_status == "parsed" and current_status != "parsed":
            transition = "regressed"
        elif previous_status != "parsed" and current_status == "parsed":
            transition = "recovered"
        elif previous_status == "parsed":
            transition = "stable_healthy"
        else:
            transition = "stable_failure"
        old_health = prior.get("health_checks", 0) if prior else 0
        old_pass = prior.get("health_pass", 0) if prior else 0
        try:
            old_health = max(0, min(int(old_health), 10000))
            old_pass = max(0, min(int(old_pass), old_health))
        except (ValueError, TypeError):
            old_health, old_pass = 0, 0
        health_checks = old_health + 1
        health_pass = old_pass + int(current_status == "parsed" and detail.get("segment_sample") == "pass")
        # Bayesian-smoothed sampling score; not a guarantee of video playback.
        quality = round((health_pass + 1) / (health_checks + 2), 4)
        # Public report contains fingerprints, never raw media URLs.
        audits.append({"title": candidate["title"], "episode": candidate["episode"],
                       "provider": candidate["provider"], **evidence, **detail,
                       "status_transition": transition,
                       "health_checks": health_checks, "health_pass": health_pass,
                       "sample_reliability": quality})
    return {
        "schema": 2, "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "queries": keywords, "providers_requested": len(providers),
        "provider_queries_attempted": len(tasks),
        "provider_queries_failed": len(errors),
        "works_found": len(records), "unique_media_candidates": len(candidates),
        "hls_candidates": sum(x["format"] == "m3u8" for x in candidates),
        "manifests_parsed": sum(a["manifest"] == "parsed" for a in audits),
        "segment_sample_pass": sum(a.get("segment_sample") == "pass" for a in audits),
        "suspected_ad_cues": sum(a["ad_cues"] == "suspected" for a in audits),
        "audited": len(audits), "errors": errors, "audits": audits,
        "same_exact_url_count": sum(a["url_comparison"] == "same_exact_url" for a in audits),
        "changed_url_count": sum(a["url_comparison"] in ("same_path_changed_url","different_url") for a in audits),
        "missing_baseline_count": sum(a["url_comparison"] == "no_comparable_baseline" for a in audits),
        "http_404_count": sum(a.get("failure_class") == "http_404_missing_or_masked" for a in audits),
        "recovered_count": sum(a["status_transition"] == "recovered" for a in audits),
        "regressed_count": sum(a["status_transition"] == "regressed" for a in audits),
        "stable_healthy_count": sum(a["status_transition"] == "stable_healthy" for a in audits),
        "alternative_candidates_audited": sum(
            (a["provider"], a["title"], a["episode"]) not in focus
            and any(equivalent_episode(a["title"], a["episode"], t, ep)
                    and a["provider"] != p for p, t, ep in focus)
            for a in audits),
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
    parser.add_argument("--rescan-previous", action="store_true",
                        help="Reprobe previously parsed exact title/episode/provider candidates")
    args = parser.parse_args(argv)
    providers = json.loads(args.providers.read_text(encoding="utf-8"))
    focus = set()
    previous_audits = {}
    previous_time = None
    if args.rescan_previous and args.report.is_file():
        previous = json.loads(args.report.read_text(encoding="utf-8"))
        previous_time = previous.get("observed_at_utc")
        previous_audits = {episode_key(a["provider"], a["title"], a["episode"]): a
                           for a in previous.get("audits", [])}
        # Include prior failures: a 404 must not prevent a new alternative check.
        focus = {(a["provider"], a["title"], a["episode"]) for a in previous.get("audits", [])}
    result = scan(args.keywords, providers, max_audits=args.max_audits,
                  workers=args.workers, focus=focus, previous_audits=previous_audits,
                  previous_observed_at=previous_time)
    result["rescan_previous_count"] = len(focus)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("provider_queries_attempted", "provider_queries_failed", "works_found", "unique_media_candidates", "manifests_parsed", "completion")}, ensure_ascii=False))
    if result["provider_queries_failed"] == result["provider_queries_attempted"]:
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
