from __future__ import annotations

from collections import Counter
from typing import Sequence
import re

from dore_core.corpus.admission_pipeline import SourceRecord, WorkCandidate


def _year(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", value)
    return int(match.group(1)) if match else None


def _century(year: int | None) -> str | None:
    if year is None:
        return None
    return f"{((year - 1) // 100) + 1}c"


def _record_pointer(record: SourceRecord) -> dict:
    return {
        "source": record.source,
        "sourceId": record.source_id,
        "readable": record.readable,
        "identifiers": dict(record.identifiers),
        "fetch": "on-demand",
    }


def _authority_ids(records: Sequence[SourceRecord]) -> dict[str, list[str]]:
    """Promote source provenance into deterministic catalogue authorities.

    Candidate ids remain stable internal ids. Source ids and provider identifiers
    are preserved separately so downstream indexing never has to infer identity
    from title/creator text.
    """
    authorities: dict[str, list[str]] = {}

    def add(key: str, value: object) -> None:
        text = str(value or "").strip()
        if not text:
            return
        values = authorities.setdefault(key, [])
        if text not in values:
            values.append(text)

    for record in records:
        source_key = re.sub(r"[^a-z0-9]+", "-", str(record.source).casefold()).strip("-") or "source"
        add(f"source:{source_key}", record.source_id)
        for key, value in dict(record.identifiers).items():
            if isinstance(value, (list, tuple, set)):
                for member in value:
                    add(str(key), member)
            else:
                add(str(key), value)
    return authorities


def work_entry(candidate: WorkCandidate) -> dict:
    records = candidate.source_records
    anchor = records[0]
    years = [year for year in (_year(record.date) for record in records) if year is not None]
    languages = sorted({record.language for record in records if record.language})
    subjects = sorted({subject for record in records for subject in record.subjects if subject})
    authorities = _authority_ids(records)
    return {
        "id": candidate.candidate_id,
        "internalId": candidate.candidate_id,
        "identity": {
            "kind": "source-authority",
            "authorityIds": authorities,
            "provenanceCount": len(records),
        },
        "authorityIds": authorities,
        "title": candidate.normalized_title,
        "creator": candidate.normalized_creator,
        "date": min(years) if years else anchor.date,
        "century": _century(min(years)) if years else None,
        "languages": languages,
        "subjects": subjects[:24],
        "matchState": candidate.match_state.value,
        "confidence": candidate.confidence,
        "witnessCount": len(records),
        "cover": {
            "mode": "remote-or-generated",
            "resolve": "on-demand",
        },
        "reading": {
            "source": True,
            "zhHant": "on-demand",
            "bilingual": "on-demand",
            "fullTextStoredLocally": False,
        },
        "sources": [_record_pointer(record) for record in records],
    }


def build_catalogue_manifest(candidates: Sequence[WorkCandidate]) -> dict:
    entries = [work_entry(candidate) for candidate in candidates]
    centuries = Counter(entry["century"] for entry in entries if entry["century"])
    languages = Counter(language for entry in entries for language in entry["languages"])
    creators = Counter(entry["creator"] for entry in entries if entry["creator"])
    authority_backed = sum(1 for entry in entries if entry["authorityIds"])
    return {
        "schema": "dawn-library-catalogue-manifest/v2",
        "holdingsModel": "remote-pointer-on-demand-reading",
        "identityModel": "stable-internal-id+source-authority",
        "count": len(entries),
        "authorityBackedCount": authority_backed,
        "facets": {
            "centuries": dict(sorted(centuries.items())),
            "languages": dict(languages.most_common()),
            "creators": dict(creators.most_common(250)),
        },
        "works": entries,
    }
