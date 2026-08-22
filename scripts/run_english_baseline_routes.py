#!/usr/bin/env python3
"""Run Doré's complete English baseline witness gate.

Open/public-domain witnesses are validated from persisted ingestion reports.
Copyrighted witnesses are never bulk-copied into the repository. When licensed
API credentials are available, API routes are preferred; otherwise Doré verifies
public, licensed external-reader canonical-reference routes without extracting or
persisting protected text.
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
    "nasb": "New American Standard Bible 2020",
    "esv": "English Standard Version",
    "niv": "New International Version",
    "nlt": "New Living Translation",
    "net": "NET Bible",
    "csb": "Christian Standard Bible",
}

# Public reader routes are licensed reading surfaces, not corpus sources. Doré
# validates navigation only and deliberately does not parse or retain verse text.
EXTERNAL_READERS = {
    "rsv": {
        "provider": "Bible Gateway",
        "url": "https://www.biblegateway.com/passage/?search=Genesis%201%3A1&version=RSV",
        "probe": "GEN.1.1",
    },
    "nrsvue": {
        "provider": "YouVersion",
        "url": "https://www.bible.com/bible/3523/GEN.1.1.NRSVUE",
        "probe": "GEN.1.1",
        "version_id": "3523",
    },
    "nasb": {
        "provider": "YouVersion",
        "url": "https://www.bible.com/bible/2692/GEN.1.1.NASB2020",
        "probe": "GEN.1.1",
        "version_id": "2692",
    },
    "esv": {
        "provider": "YouVersion",
        "url": "https://www.bible.com/bible/59/GEN.1.1.ESV",
        "probe": "GEN.1.1",
        "version_id": "59",
    },
    "niv": {
        "provider": "YouVersion",
        "url": "https://www.bible.com/bible/111/GEN.1.1.NIV",
        "probe": "GEN.1.1",
        "version_id": "111",
    },
    "nlt": {
        "provider": "YouVersion",
        "url": "https://www.bible.com/bible/116/GEN.1.1.NLT",
        "probe": "GEN.1.1",
        "version_id": "116",
    },
    "net": {
        "provider": "YouVersion",
        "url": "https://www.bible.com/bible/107/GEN.1.1.NET",
        "probe": "GEN.1.1",
        "version_id": "107",
    },
    "csb": {
        "provider": "YouVersion",
        "url": "https://www.bible.com/bible/1713/GEN.1.1.CSB",
        "probe": "GEN.1.1",
        "version_id": "1713",
    },
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


def probe_external_reader(route: dict[str, str], timeout: int = 20) -> tuple[str, Any]:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; DoreResearchRouteValidator/1.0; +https://westsidewatch.github.io/)",
        "Accept": "text/html,application/xhtml+xml",
    }
    req = urllib.request.Request(route["url"], headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            # Do not read the body: this is route validation, not text ingestion.
            status = int(getattr(response, "status", 0) or 0)
            final_url = response.geturl()
            if 200 <= status < 400:
                return "PASS", {
                    "http_status": status,
                    "canonical_probe": route["probe"],
                    "reader_url": route["url"],
                    "final_url": final_url,
                    "text_retained": False,
                }
            return "ROUTE_FAIL", {"http_status": status, "reader_url": route["url"]}
    except urllib.error.HTTPError as exc:
        return "ROUTE_FAIL", {"http_status": exc.code, "reader_url": route["url"]}
    except Exception as exc:
        return "ROUTE_FAIL", {"error": f"{type(exc).__name__}: {exc}", "reader_url": route["url"]}


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
        return "PASS", {"http_status": status, "canonical_probe": "GEN.1.1", "text_retained": False}
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
        return "PASS", {"http_status": status, "canonical": payload.get("canonical"), "text_retained": False}
    return "ROUTE_FAIL", {"http_status": status, "response": payload}


def main() -> None:
    result: dict[str, Any] = {
        "schema": "dore.english-baseline.v2",
        "policy": "local_corpus_for_open_witnesses; licensed_api_preferred; licensed_external_reader_fallback; no_unlicensed_bulk_storage",
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
        status = "CREDENTIAL_REQUIRED"
        diag: Any = None
        provider = ""
        access = "licensed_api"
        match: dict[str, Any] | None = None

        if witness_id == "esv" and esv_key:
            status, diag = test_esv(esv_key)
            provider = "Crossway ESV API"
        elif witness_id != "esv" and catalog_status == "PASS":
            match = match_api_bible(witness_id, name, catalog)
            if match:
                status, diag = test_api_bible_passage(api_bible_key, str(match.get("id", "")))
                provider = "API.Bible"
            else:
                status = "NOT_AUTHORIZED_OR_NOT_IN_CATALOG"
                diag = {"catalog_entries": len(catalog)}

        # Credentials are optional for Foundation completion because the registry
        # explicitly permits an external_reader route. Also fall back if the
        # licensed API account does not authorize a specific edition.
        if status != "PASS":
            route = EXTERNAL_READERS[witness_id]
            fallback_status, fallback_diag = probe_external_reader(route)
            if fallback_status == "PASS":
                status, diag = fallback_status, fallback_diag
                provider = route["provider"]
                access = "external_reader"
            else:
                diag = {
                    "api_diagnostic": diag if diag is not None else catalog_diag,
                    "external_reader_diagnostic": fallback_diag,
                }

        entry: dict[str, Any] = {
            "name": name,
            "access": access,
            "provider": provider or "unresolved",
            "status": status,
            "diagnostic": diag,
        }
        if access == "licensed_api":
            entry["credential"] = "DORE_ESV_API_KEY" if witness_id == "esv" else "DORE_API_BIBLE_KEY"
            if match:
                entry["bible_id"] = match.get("id")
                entry["authorized_name"] = match.get("name")
        else:
            route = EXTERNAL_READERS[witness_id]
            entry["reader_url"] = route["url"]
            entry["version_id"] = route.get("version_id")
            entry["copyright_text_stored"] = False

        result["witnesses"][witness_id] = entry
        all_pass &= status == "PASS"

    counts: dict[str, int] = {}
    for entry in result["witnesses"].values():
        counts[entry["status"]] = counts.get(entry["status"], 0) + 1
    result["summary"] = {"total": len(result["witnesses"]), "status_counts": counts}
    result["status"] = "PASS" if all_pass else "PARTIAL"
    if all_pass:
        result["milestone"] = "ENGLISH_BIBLICAL_WITNESS_BASELINE_COMPLETE"

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
