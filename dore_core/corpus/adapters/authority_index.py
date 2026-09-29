from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence
import csv
import gzip
import json
import re
import unicodedata

from dore_core.corpus.authority_reconciliation import AuthorityWork


def _norm(value: str | None) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    value = re.sub(r"[^\w\s]", " ", value)
    return " ".join(value.split())


def _keys(work: AuthorityWork) -> tuple[str, ...]:
    creator = _norm(work.creator)
    titles = {_norm(work.title), *(_norm(t) for t in work.alternate_titles)}
    keys = {f"c:{creator}"} if creator else set()
    for title in titles:
        if not title:
            continue
        keys.add(f"t:{title}")
        if creator:
            keys.add(f"ct:{creator}::{title}")
    return tuple(keys)


def build_index(works: Iterable[AuthorityWork]) -> dict[str, tuple[AuthorityWork, ...]]:
    index: dict[str, list[AuthorityWork]] = defaultdict(list)
    seen: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for work in works:
        identity = (work.authority, work.authority_id)
        for key in _keys(work):
            if identity not in seen[key]:
                seen[key].add(identity)
                index[key].append(work)
    return {key: tuple(values) for key, values in index.items()}


def iter_openlibrary_works(path: str | Path, limit: int | None = None) -> Iterator[AuthorityWork]:
    """Read Open Library works dump (.txt or .gz): type, key, revision, last_modified, JSON."""
    opener = gzip.open if str(path).endswith(".gz") else open
    emitted = 0
    with opener(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t", 4)
            if len(parts) != 5:
                continue
            _, key, _, _, payload = parts
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                continue
            title = data.get("title")
            if not title:
                continue
            author_keys = [a.get("author", {}).get("key") for a in data.get("authors", []) if isinstance(a, dict)]
            # Work dumps do not carry author display names. Keep stable author IDs as identifiers;
            # a separate author dump can enrich creator names without changing Work identity.
            identifiers = {"openlibrary_work": key}
            if author_keys:
                identifiers["openlibrary_author"] = ";".join(k for k in author_keys if k)
            yield AuthorityWork(
                authority="OpenLibrary",
                authority_id=key,
                title=title,
                creator=None,
                alternate_titles=tuple(data.get("subtitle") and [data["subtitle"]] or ()),
                identifiers=identifiers,
            )
            emitted += 1
            if limit is not None and emitted >= limit:
                return


def iter_prdl_csv(path: str | Path, limit: int | None = None) -> Iterator[AuthorityWork]:
    """Read a normalized/derived PRDL bibliography CSV while tolerating common column names."""
    aliases = {
        "id": ("prdl_id", "id", "record_id", "identifier"),
        "title": ("title", "work_title", "short_title"),
        "creator": ("author", "creator", "author_name"),
        "alternate": ("alternate_title", "alt_title", "other_title"),
    }
    def pick(row: Mapping[str, str], key: str) -> str | None:
        lowered = {str(k).casefold(): v for k, v in row.items() if k}
        for name in aliases[key]:
            value = lowered.get(name)
            if value:
                return value.strip()
        return None

    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for index, row in enumerate(csv.DictReader(handle), start=1):
            title = pick(row, "title")
            if not title:
                continue
            authority_id = pick(row, "id") or f"prdl-row-{index}"
            alt = pick(row, "alternate")
            yield AuthorityWork(
                authority="PRDL",
                authority_id=authority_id,
                title=title,
                creator=pick(row, "creator"),
                alternate_titles=(alt,) if alt else (),
                identifiers={"prdl": authority_id},
            )
            if limit is not None and index >= limit:
                return


def merge_indexes(*indexes: Mapping[str, Sequence[AuthorityWork]]) -> dict[str, tuple[AuthorityWork, ...]]:
    merged: dict[str, list[AuthorityWork]] = defaultdict(list)
    seen: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for index in indexes:
        for key, works in index.items():
            for work in works:
                identity = (work.authority, work.authority_id)
                if identity not in seen[key]:
                    seen[key].add(identity)
                    merged[key].append(work)
    return {key: tuple(values) for key, values in merged.items()}
