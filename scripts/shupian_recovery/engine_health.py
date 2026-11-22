#!/usr/bin/env python3
"""Diagnose search regression by distinguishing DNS, API, schema and detail failures.

Does not discover or publish media for consumption. All failed checks remain
visible, rather than being silently converted into zero search results.
"""
from __future__ import annotations
import argparse
import json
import socket
from pathlib import Path
from urllib.parse import urlsplit, urlencode
from source_discovery import network_fetch, play_groups

HERE = Path(__file__).resolve().parent

def probe_one(provider, resolve=socket.getaddrinfo, fetch=network_fetch):
    result = {"provider": provider["id"], "api": provider["api"],
              "dns": "UNTESTED", "api_list": "UNTESTED",
              "api_detail": "UNTESTED", "media_candidates": 0}
    host = urlsplit(provider["api"]).hostname
    try:
        resolve(host, 443)
        result["dns"] = "OK"
    except Exception as exc:
        result["dns"] = "FAILED"
        result["classification"] = "INFRASTRUCTURE_DNS"
        result["error"] = str(exc)[:240]
        return result
    endpoint = provider["api"]
    url = endpoint + ("&" if "?" in endpoint else "?") + urlencode({"ac":"list","pg":1})
    try:
        payload = fetch(url)
        if not isinstance(payload, dict) or not isinstance(payload.get("list"), list):
            raise ValueError("Expected MacCMS list array")
        result["api_list"] = "OK"
        result["items"] = len(payload["list"])
        result["classes"] = len(payload.get("class", []))
        samples = [x for x in payload["list"] if isinstance(x, dict) and x.get("vod_id")][:2]
        if not samples:
            result["classification"] = "EMPTY_CATALOG"
            return result
        detail_success = 0
        for item in samples:
            url = endpoint + ("&" if "?" in endpoint else "?") + urlencode(
                {"ac":"detail","ids":item["vod_id"]})
            try:
                detail = fetch(url)
                entries = detail.get("list", []) if isinstance(detail, dict) else []
                if not isinstance(entries, list):
                    raise ValueError("Malformed MacCMS detail")
                if any(play_groups(x) for x in entries if isinstance(x, dict)):
                    detail_success += 1
            except Exception as exc:
                result.setdefault("detail_errors", []).append(str(exc)[:200])
        result["media_candidates"] = detail_success
        result["api_detail"] = "OK" if detail_success else "NO_MEDIA"
        result["classification"] = "WORKING_DISCOVERY" if detail_success else "DETAIL_OR_MEDIA_FAILURE"
    except Exception as exc:
        result["classification"] = "API_OR_SCHEMA_FAILURE"
        result["api_list"] = "FAILED"
        result["error"] = str(exc)[:240]
    return result

def diagnose(providers, resolve=socket.getaddrinfo, fetch=network_fetch):
    results = [probe_one(p, resolve=resolve, fetch=fetch) for p in providers]
    statuses = {}
    for item in results:
        category = item["classification"]
        statuses[category] = statuses.get(category, 0) + 1
    return {"schema":1, "providers":results, "classes":statuses,
            "working":statuses.get("WORKING_DISCOVERY", 0),
            "warning":"API metadata health does not establish HLS decode, no ads, correct content or site playback."}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--providers",default=str(HERE/"providers.json"))
    parser.add_argument("--output",default="shupian-engine-health.json")
    a=parser.parse_args()
    sources=json.loads(Path(a.providers).read_text(encoding="utf-8"))
    report=diagnose(sources)
    Path(a.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"output":a.output,"counts":report["classes"]},ensure_ascii=False))
    return 0 if report["working"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
