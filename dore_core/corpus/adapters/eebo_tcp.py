from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator
import csv
import xml.etree.ElementTree as ET

from dore_core.corpus.admission_pipeline import SourceRecord


@dataclass(frozen=True)
class EEBOTCPAdapterReport:
    scanned: int
    emitted: int
    malformed: int


def _first_text(root: ET.Element, names: tuple[str, ...]) -> str | None:
    for element in root.iter():
        local = element.tag.rsplit("}", 1)[-1]
        if local in names:
            text = " ".join("".join(element.itertext()).split())
            if text:
                return text
    return None


def _all_text(root: ET.Element, name: str) -> tuple[str, ...]:
    values: list[str] = []
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] == name:
            text = " ".join("".join(element.itertext()).split())
            if text and text not in values:
                values.append(text)
    return tuple(values)


def record_from_tei(path: Path) -> SourceRecord:
    root = ET.parse(path).getroot()
    source_id = path.stem
    title = _first_text(root, ("title",)) or source_id
    creator = _first_text(root, ("author",))
    date = _first_text(root, ("date",))
    publisher = _first_text(root, ("publisher",))
    availability = _first_text(root, ("availability",)) or ""
    notes = _all_text(root, "note")
    terms = _all_text(root, "term")
    languages = _all_text(root, "language")
    phase = next((n for n in notes if "phase" in n.casefold()), None)
    identifiers: dict[str, str] = {"tcp": source_id}
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] != "idno":
            continue
        value = " ".join("".join(element.itertext()).split())
        kind = (element.attrib.get("type") or "idno").casefold()
        if value:
            identifiers[kind] = value
    readable = any(element.tag.rsplit("}", 1)[-1] in ("body", "text") for element in root.iter())
    return SourceRecord(
        source="EEBO-TCP",
        source_id=source_id,
        title=title,
        creator=creator,
        date=date,
        language=languages[0] if languages else None,
        phase=phase,
        rights=availability,
        subjects=terms,
        text_types=(),
        readable=readable,
        identifiers=identifiers,
        publisher=publisher,
        metadata={"path": str(path), "notes": " | ".join(notes)},
    )


def iter_tei(root: str | Path, limit: int | None = None) -> Iterator[SourceRecord]:
    count = 0
    for path in sorted(Path(root).rglob("*.xml")):
        if path.name == "tcpchars.xml":
            continue
        try:
            yield record_from_tei(path)
            count += 1
        except (ET.ParseError, OSError, UnicodeError):
            continue
        if limit is not None and count >= limit:
            return


def iter_csv(path: str | Path, limit: int | None = None) -> Iterator[SourceRecord]:
    """Accept a TCP/derived catalogue CSV without coupling to one exact column spelling."""
    aliases = {
        "id": ("tcp", "tcp_id", "id", "identifier"),
        "title": ("title", "full_title"),
        "creator": ("author", "creator"),
        "date": ("date", "year", "publication_date"),
        "publisher": ("publisher",),
        "language": ("language", "lang"),
        "rights": ("rights", "availability", "license"),
        "phase": ("phase", "tcp_phase"),
        "subjects": ("subjects", "subject", "keywords"),
    }
    def value(row: dict[str, str], key: str) -> str | None:
        lowered = {k.casefold(): v for k, v in row.items() if k}
        for name in aliases[key]:
            if lowered.get(name):
                return lowered[name].strip()
        return None

    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for index, row in enumerate(csv.DictReader(handle), start=1):
            if limit is not None and index > limit:
                return
            source_id = value(row, "id") or f"csv-{index}"
            subjects = tuple(x.strip() for x in (value(row, "subjects") or "").split(";") if x.strip())
            yield SourceRecord(
                source="EEBO-TCP",
                source_id=source_id,
                title=value(row, "title") or source_id,
                creator=value(row, "creator"),
                date=value(row, "date"),
                language=value(row, "language"),
                phase=value(row, "phase"),
                rights=value(row, "rights"),
                subjects=subjects,
                readable=True,
                identifiers={"tcp": source_id},
                publisher=value(row, "publisher"),
                metadata={"row": str(index)},
            )
