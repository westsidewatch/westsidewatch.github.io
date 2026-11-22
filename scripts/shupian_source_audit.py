#!/usr/bin/env python3
"""Shupian non-DRM public HLS source audit. No media rehosting or catalog promotion.

This is a technical source check, NOT proof of complete browser playback,
full-episode integrity, absence of advertising, or content licensing.
"""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "Shupian-Source-Audit/1.0 (+ non-commercial validation)"
MAX_PLAYLIST_BYTES = 600_000
MAX_SEGMENT_BYTES = 1_200_000

def fetch(url, max_bytes, timeout=18, use_range=False):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https":
        raise ValueError("Only HTTPS sources are accepted")
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    if use_range:
        headers["Range"] = f"bytes=0-{max_bytes - 1}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read(max_bytes + 1)
        if len(payload) > max_bytes:
            raise ValueError("Response exceeded audit byte cap")
        return payload, response.status, response.headers.get("Content-Type", "")

def lines_from_playlist(url):
    payload, code, mime = fetch(url, MAX_PLAYLIST_BYTES)
    text = payload.decode("utf-8-sig", errors="replace")
    if "#EXTM3U" not in text[:500]:
        raise ValueError("Not a recognized M3U8 playlist")
    return [line.strip() for line in text.splitlines() if line.strip()], code, mime

def audit_one(name, url):
    result = {"title": name, "url": url, "status": "error", "sampled_segments": [], "limitations": "Not complete video decode, full-episode verification, rights approval or browser playback"}
    try:
        lines, code, mime = lines_from_playlist(url)
        result["manifest_http"] = code
        result["manifest_content_type"] = mime
        result["playlist_is_master"] = any("#EXT-X-STREAM-INF" in line for line in lines)
        if any(line.startswith("#EXT-X-KEY:") and "METHOD=NONE" not in line for line in lines):
            result["status"] = "encrypted-or-keyed"
            return result
        if result["playlist_is_master"]:
            for idx, line in enumerate(lines[:-1]):
                if line.startswith("#EXT-X-STREAM-INF"):
                    child = next((value for value in lines[idx + 1:] if not value.startswith("#")), None)
                    if child:
                        url = urllib.parse.urljoin(url, child)
                        result["variant_url"] = url
                        lines, code, mime = lines_from_playlist(url)
                        break
        if any(line.startswith("#EXT-X-KEY:") and "METHOD=NONE" not in line for line in lines):
            result["status"] = "encrypted-or-keyed"
            return result
        segments = [urllib.parse.urljoin(url, value) for value in lines if not value.startswith("#")]
        result["segments_in_manifest"] = len(segments)
        if not segments:
            result["status"] = "no-segments"
            return result
        indices = sorted(set([0, len(segments) // 2, len(segments) - 1]))
        all_success = True
        for index in indices:
            seg_url = segments[index]
            record = {"index": index, "url": seg_url, "http": None, "bytes": 0, "ffprobe": "not-run"}
            try:
                payload, code, content_type = fetch(seg_url, MAX_SEGMENT_BYTES, timeout=20, use_range=True)
                record.update(http=code, bytes=len(payload), content_type=content_type)
                if len(payload) < 188:
                    raise ValueError("Segment sample too short")
                if payload[:5].lower() in (b"<html", b"<?xml") or b"<!doctype" in payload[:100].lower():
                    raise ValueError("Received HTML/XML, not media data")
                with tempfile.NamedTemporaryFile(suffix=".ts") as tmp:
                    tmp.write(payload)
                    tmp.flush()
                    if shutil.which("ffprobe"):
                        check = subprocess.run(
                            ["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,codec_type",
                             "-of", "json", tmp.name], capture_output=True, text=True, timeout=12
                        )
                        record["ffprobe"] = (json.loads(check.stdout).get("streams", [])
                                              if check.returncode == 0 else "unable-to-decode-partial-range")
                record["byte_sample_ok"] = True
            except Exception as exc:
                record["error"] = str(exc)[:250]
                all_success = False
            result["sampled_segments"].append(record)
        result["status"] = "segment-bytes-sampled" if all_success else "segment-check-failed"
    except Exception as exc:
        result["error"] = str(exc)[:250]
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", default="static/shupian/recovery/hls-candidates-16.json")
    parser.add_argument("--catalog", default="static/shupian/catalog.json")
    parser.add_argument("--output", default="shupian-audit-report.json")
    parser.add_argument("--limit", type=int, default=17)
    args = parser.parse_args()
    candidates = json.loads(Path(args.candidates).read_text())
    works = json.loads(Path(args.catalog).read_text())["titles"]
    jobs = [(x["title"], x["hls_master_url"]) for x in candidates["candidates"]]
    for work in works:
        for episode in work.get("episodes", []):
            for source in episode.get("sources", []):
                if source.get("format") == "m3u8" and source.get("url"):
                    jobs.append((work["title"] + " / " + episode.get("label", ""), source["url"]))
    jobs = jobs[:max(0, min(args.limit, 100))]
    records = []
    for i, (name, url) in enumerate(jobs, 1):
        print(f"[{i}/{len(jobs)}] auditing {name}", flush=True)
        record = audit_one(name, url)
        print("   " + record["status"], flush=True)
        records.append(record)
        time.sleep(0.25)
    summary = {"total": len(records), "sample_pass": sum(x["status"] == "segment-bytes-sampled" for x in records),
               "warning": "Passing does not authorize or certify full playback."}
    Path(args.output).write_text(json.dumps({"schema": 1, "summary": summary, "results": records}, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary))
if __name__ == "__main__":
    main()
