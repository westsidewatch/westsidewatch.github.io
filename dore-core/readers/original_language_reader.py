"""Doré original-language corpus reader v0.1.

Foundation implementation for pinned OSHB and MorphGNT/SBLGNT corpora.
The reader emits provenance-preserving token records; it does not perform
interpretation or promote analytical metadata to textual fact.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional, Iterable
import re
import xml.etree.ElementTree as ET


OSHB_SNAPSHOT = "3d15126fb1ef74867fc1434be1942e837932691f"
MORPHGNT_SNAPSHOT = "aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d"
OSIS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"


@dataclass
class Analysis:
    type: str
    value: str
    source_id: str


@dataclass
class TokenRecord:
    token_id: str
    canonical_ref_id: str
    source_native_ref: str
    witness_id: str
    language: str
    order: int
    surface: str
    normalized: Optional[str]
    analyses: list[Analysis]
    textual_source_id: str
    corpus_snapshot: str
    validation_status: str = "pass"

    def to_dict(self) -> dict:
        value = asdict(self)
        return value


def canonical_id(book: str, chapter: str, verse: str) -> str:
    return f"bible.ref.{book.upper()}.{int(chapter)}.{int(verse)}"


def parse_morphgnt_line(line: str, order: int) -> TokenRecord:
    """Parse one standard MorphGNT line.

    Expected columns include source reference, POS, morphology, surface,
    normalized form, and lemma. Extra columns are tolerated.
    """
    cols = line.rstrip("\n").split()
    if len(cols) < 6:
        raise ValueError("MorphGNT record has insufficient columns")

    ref, pos, morph, surface, normalized, lemma = cols[:6]
    if not re.fullmatch(r"\d{6}", ref):
        raise ValueError(f"Unexpected MorphGNT reference: {ref}")

    book_num, chapter, verse = ref[:2], ref[2:4], ref[4:6]
    # Foundation mapping begins with Matthew (61 in MorphGNT source scheme).
    book_map = {"61": "MAT"}
    if book_num not in book_map:
        raise ValueError(f"Book mapping not yet registered: {book_num}")

    cref = canonical_id(book_map[book_num], chapter, verse)
    return TokenRecord(
        token_id=f"morphgnt.{ref}.{order}",
        canonical_ref_id=cref,
        source_native_ref=ref,
        witness_id="witness.sblgnt",
        language="grc",
        order=order,
        surface=surface,
        normalized=normalized,
        analyses=[
            Analysis("part_of_speech", pos, "source.morphgnt"),
            Analysis("morphology", morph, "source.morphgnt"),
            Analysis("lemma", lemma, "source.morphgnt"),
        ],
        textual_source_id="source.sblgnt",
        corpus_snapshot=MORPHGNT_SNAPSHOT,
    )


def iter_oshb_words(xml_text: str, book_code: str) -> Iterable[TokenRecord]:
    """Yield OSHB word records while preserving source surface and analysis.

    Language resolution is deliberately conservative. File-level Hebrew is
    not sufficient to assert token-level Hebrew in mixed-language books.
    Mixed-language boundary resolution is a separate required component.
    """
    root = ET.fromstring(xml_text)
    order_by_verse: dict[str, int] = {}

    for verse in root.iter(f"{OSIS}verse"):
        osis_id = verse.attrib.get("osisID")
        if not osis_id or "." not in osis_id:
            continue
        parts = osis_id.split(".")
        if len(parts) != 3:
            continue
        _, chapter, verse_no = parts
        cref = canonical_id(book_code, chapter, verse_no)
        order_by_verse.setdefault(cref, 0)

        for word in verse.iter(f"{OSIS}w"):
            surface = "".join(word.itertext())
            if not surface:
                continue
            order_by_verse[cref] += 1
            order = order_by_verse[cref]

            lemma = word.attrib.get("lemma")
            morph = word.attrib.get("morph")
            analyses: list[Analysis] = []
            if lemma:
                analyses.append(Analysis("lemma", lemma, "source.oshb"))
            if morph:
                analyses.append(Analysis("morphology", morph, "source.oshb"))

            # Do not fabricate language certainty in Daniel/Ezra.
            language = "und" if book_code.upper() in {"DAN", "EZR"} else "he"
            status = "warn" if language == "und" else "pass"

            yield TokenRecord(
                token_id=f"oshb.{osis_id}.{order}",
                canonical_ref_id=cref,
                source_native_ref=osis_id,
                witness_id="witness.oshb.wlc",
                language=language,
                order=order,
                surface=surface,
                normalized=None,
                analyses=analyses,
                textual_source_id="source.oshb",
                corpus_snapshot=OSHB_SNAPSHOT,
                validation_status=status,
            )


def validate_token(token: TokenRecord) -> list[str]:
    errors: list[str] = []
    if not token.surface:
        errors.append("missing_surface")
    if not token.source_native_ref:
        errors.append("missing_source_native_ref")
    if not token.canonical_ref_id.startswith("bible.ref."):
        errors.append("invalid_canonical_ref")
    if not token.textual_source_id or not token.corpus_snapshot:
        errors.append("missing_textual_provenance")
    for analysis in token.analyses:
        if not analysis.source_id:
            errors.append(f"missing_analysis_provenance:{analysis.type}")
    return errors
