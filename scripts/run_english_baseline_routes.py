#!/usr/bin/env python3
"""Run Doré's complete English baseline witness gate.

Open/public-domain witnesses are validated from their persisted ingestion reports.
Copyrighted witnesses are never bulk-copied into the repository: they are tested
through licensed canonical-reference APIs when credentials are available.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

REPORT = Path("reports/DORÉ-ENGLISH-BASELINE.json")

LOCAL = {
    "webu": ("World English Bible Updated", "reports/DORÉ-WEBU-INGESTION.json"),
    "asv": ("American Standard Version", "reports/DORÉ-ASV-INGESTION.json"),
    "kjv": ("King James Version", "reports/DORÉ-KJV-INGESTION.json"),
}

LICENSED = {
    "rsv": "Revised Standard Version",
    "nrsvue": "New Revised Standard Version Updated Edition",
    "nasb": "New American Standard Bible",
    "esv": "English Standard Version",
    "niv": "New International Version",
    "nlt": "New Living Translation",
    "net": "NET Bible",
    "csb": "Christian Standard Bible",
}


def read_json(path: str) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {"status": "MISSING_REPORT"}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "INVALID_REPORT", "error": str(exc)}


def request_json(url: str, headers: dict[str, str], timeout: int = 20) -> tuple[int, Any]:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
            return response.status, json.loads(payload)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:1000]
        return exc.code, {"error": body}
    except Exception as exc:
        return 0, {"error": f"{type(exc).__name__}: {exc}"}


def api_bible_catalog(key: str) -> tuple[str, list[dict[str, Any]], Any]:
    if not key:
        return "CREDENTIAL_REQUIRED", [], None
    status, payload = request_json(
        "https://rest.api.bible/v1/bibles?language=eng",
        {"api-key": key, "Accept": "application/json"},
    )
    if status != 200 or not isinstance(payload, dict):
        return "ROUTE_FAIL", [], {"http_status": status, "response": payload}
    data = payload.get("data")
    if not isinstance(data, list):
        return "ROUTE_FAIL", [], {"http_status": status, "response_shape": type(data).__name__}
    return "PASS", data, {"http_status": status, "authorized_bibles": len(data)}


def match_api_bible(target_id: str, target_name: str, catalog: list[dict[str, Any]]) -> dict[str, Any] | None:
    aliases = {
        "rsv": ["revised standard version", "rsv"],
        "nrsvue": ["new revised standard version updated edition", "nrsvue", "nrsv updated edition"],
        "nasb": ["new american standard bible", "nasb"],
        "niv": ["new international version", "niv"],
        "nlt": ["new living translation", "nlt"],
        "net": ["net bible", "new english translation"],
        "csb": ["christian standard bible", "csb"],
    }
    needles = aliases.get(target_id, [target_name.lower()])
    for item in catalog:
        hay = " ".join(str(item.get(k, "")) for k in ("name", "nameLocal", "abbreviation", "abbreviationLocal")).lower()
        if any(n in hay for n in needles):
            return item
    return None


def test_api_bible_passage(key: str, bible_id: str) -> tuple[str, Any]:
    if not key:
        return "CREDENTIAL_REQUIRED", None
    ref = urllib.parse.quote("GEN.1.1", safe="")
    url = f"https://rest.api.bible/v1/bibles/{urllib.parse.quote(bible_id, safe='')}/search?query={ref}&limit=1"
    status, payload = request_json(url, {"api-key": key, "Accept": "application/json"})
    if status == 200:
        return "PASS", {"http_status": status, "canonical_probe": "GEN.1.1"}
    return "ROUTE_FAIL", {"http_status": status, "response": payload}


def test_esv(key: str) -> tuple[str, Any]:
    if not key:
        return "CREDENTIAL_REQUIRED", None
    query = urllib.parse.urlencode({
        "q": "Genesis 1:1",
        "include-headings": "false",
        "include-footnotes": "false",
        "include-verse-numbers": "true",
        "include-short-copyright": "true",
    })
    status, payload = request_json(
        f"https://api.esv.org/v3/passage/text/?{query}",
        {"Authorization": f"Token {key}", "Accept": "application/json"},
    )
    if status == 200 and isinstance(payload, dict) and payload.get("canonical"):
        return "PASS", {"http_status": status, "canonical": payload.get("canonical")}
    return "ROUTE_FAIL", {"http_status": status, "response": payload}


def main() -> None:
    result: dict[str, Any] = {
        "schema": "dore.english-baseline.v1",
        "policy": "local_corpus_for_open_witnesses; licensed_api_or_external_reader_for_copyrighted_witnesses; no_unlicensed_bulk_storage",
        "witnesses": {},
    }

    all_pass = True
    for witness_id, (name, path) in LOCAL.items():
        source = read_json(path)
        status = "PASS" if source.get("status") == "PASS" else "FAIL"
        result["witnesses"][witness_id] = {
            "name": name,
            "access": "local_corpus",
            "status": status,
            "source_report": path,
            "books": source.get("books"),
            "verses": source.get("verses"),
        }
        all_pass &= status == "PASS"

    api_bible_key = os.environ.get("DORE_API_BIBLE_KEY", "").strip()
    esv_key = os.environ.get("DORE_ESV_API_KEY", "").strip()
    catalog_status, catalog, catalog_diag = api_bible_catalog(api_bible_key)

    for witness_id, name in LICENSED.items():
        if witness_id == "esv":
            status, diag = test_esv(esv_key)
            result["witnesses"][witness_id] = {
                "name": name,
                "access": "licensed_api",
                "provider": "Crossway ESV API",
                "status": status,
                "credential": "DORE_ESV_API_KEY",
                "diagnostic": diag,
            }
        else:
            if catalog_status != "PASS":
                status, diag, match = catalog_status, catalog_diag, None
            else:
                match = match_api_bible(witness_id, name, catalog)
                if not match:
                    status, diag = "NOT_AUTHORIZED_OR_NOT_IN_CATALOG", {"catalog_entries": len(catalog)}
                else:
                    status, diag = test_api_bible_passage(api_bible_key, str(match.get("id", "")))
            result["witnesses"][witness_id] = {
                "name": name,
                "access": "licensed_api",
                "provider": "API.Bible",
                "status": status,
                "credential": "DORE_API_BIBLE_KEY",
                "bible_id": match.get("id") if match else None,
                "authorized_name": match.get("name") if match else None,
                "diagnostic": diag,
            }
        all_pass &= result["witnesses"][witness_id]["status"] == "PASS"

    counts: dict[str, int] = {}
    for entry in result["witnesses"].values():
        counts[entry["status"]] = counts.get(entry["status"], 0) + 1
    result["summary"] = {"total": len(result["witnesses"]), "status_counts": counts}
    result["status"] = "PASS" if all_pass else "PARTIAL"

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
