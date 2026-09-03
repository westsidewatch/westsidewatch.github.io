#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from typing import Any

BASE_URL = "https://openlibrary.org/search.json"
USER_AGENT = os.environ.get(
    "DORE_OPEN_LIBRARY_USER_AGENT",
    "WestsideWatch-DawnLibrary/0.1 (+https://westsidewatch.github.io)",
)
MAX_RESULTS = 10
FIELDS = "key,title,author_name,author_key,first_publish_year,edition_count,isbn,language,cover_i"


@dataclass(frozen=True)
class BookResult:
    resource_type: str
    work_id: str | None
    title: str
    authors: list[str]
    author_ids: list[str]
    first_publish_year: int | None
    edition_count: int | None
    isbn: list[str]
    languages: list[str]
    cover_id: int | None
    provider: str
    provider_url: str | None
    provenance: dict[str, Any]


def normalize_doc(doc: dict[str, Any]) -> BookResult:
    raw_key = doc.get("key")
    work_id = raw_key.rsplit("/", 1)[-1] if isinstance(raw_key, str) and raw_key else None
    provider_url = f"https://openlibrary.org/works/{work_id}" if work_id else None
    return BookResult(
        resource_type="book-work",
        work_id=work_id,
        title=str(doc.get("title") or "").strip(),
        authors=[str(x) for x in (doc.get("author_name") or [])],
        author_ids=[str(x) for x in (doc.get("author_key") or [])],
        first_publish_year=doc.get("first_publish_year") if isinstance(doc.get("first_publish_year"), int) else None,
        edition_count=doc.get("edition_count") if isinstance(doc.get("edition_count"), int) else None,
        isbn=[str(x) for x in (doc.get("isbn") or [])[:12]],
        languages=[str(x) for x in (doc.get("language") or [])[:12]],
        cover_id=doc.get("cover_i") if isinstance(doc.get("cover_i"), int) else None,
        provider="open-library",
        provider_url=provider_url,
        provenance={
            "source": "Open Library Search API",
            "endpoint": BASE_URL,
            "record_key": raw_key,
            "network": True,
            "credentials_required": False,
            "paid_fallback": False,
        },
    )


def search_books(query: str, *, limit: int = 5, timeout: float = 8.0) -> dict[str, Any]:
    query = query.strip()
    if not query:
        raise ValueError("query must not be empty")
    if not 1 <= limit <= MAX_RESULTS:
        raise ValueError(f"limit must be between 1 and {MAX_RESULTS}")

    params = urllib.parse.urlencode({"q": query, "fields": FIELDS, "limit": limit})
    request = urllib.request.Request(
        f"{BASE_URL}?{params}",
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)

    docs = payload.get("docs") if isinstance(payload, dict) else None
    if not isinstance(docs, list):
        raise RuntimeError("Open Library response missing docs list")

    return {
        "schema": "dore.library.books.result.v1",
        "capability": "library.books",
        "provider": "open-library",
        "query": query,
        "count": len(docs),
        "results": [asdict(normalize_doc(doc)) for doc in docs if isinstance(doc, dict)],
        "evidence": {
            "endpoint": BASE_URL,
            "credentials_required": False,
            "cost": "free-only",
            "paid_fallback": False,
            "user_agent_identified": bool(USER_AGENT),
        },
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: dawn_library_books.py <query> [limit]", file=sys.stderr)
        return 2
    limit = int(argv[2]) if len(argv) > 2 else 5
    try:
        result = search_books(argv[1], limit=limit)
    except Exception as exc:
        print(json.dumps({"schema":"dore.library.books.error.v1","capability":"library.books","ok":False,"error":str(exc),"paid_fallback":False}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
