"""Final Scripture-reading capability contracts for Doré.

This layer does not pretend to pre-interpret every passage. It tests whether Doré
can independently move from a canonical passage to original-language evidence,
context scope, intertext evidence and calibrated conclusions.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ReadingCase:
    case_id: str
    canonical_ref: str
    testament: str
    genre: str
    required: tuple[str, ...]

REQUIRED_READING_CAPABILITIES = (
    "canonical_location",
    "original_language_surface",
    "lemma",
    "morphology",
    "context_hierarchy",
    "cross_witness_alignment",
    "intertext_classification",
    "provenance",
    "uncertainty_boundary",
)

INTERTEXT_CLASSES = (
    "explicit_quotation",
    "strong_allusion",
    "possible_echo",
    "thematic_parallel",
)

def context_hierarchy(ref: str) -> dict[str, str]:
    parts = ref.split(".")
    if len(parts) != 6 or parts[:2] != ["bible", "ref"]:
        raise ValueError(f"invalid canonical reference: {ref}")
    _, _, book, chapter, verse = parts[0], parts[1], parts[2], parts[3], parts[4]
    # Canonical IDs are bible.ref.BOOK.CHAPTER.VERSE => five components.
    raise AssertionError("unreachable")

def parse_context(ref: str) -> dict[str, str]:
    parts=ref.split(".")
    if len(parts)!=5 or parts[0]!="bible" or parts[1]!="ref":
        raise ValueError(f"invalid canonical reference: {ref}")
    book,chapter,verse=parts[2:]
    return {"verse":ref,"chapter":f"bible.chapter.{book}.{chapter}","book":f"bible.book.{book}","canon":"bible.canon.protestant66","verse_number":verse}

def classify_intertext(*, explicit_formula: bool=False, source_wording_overlap: float=0.0, thematic_only: bool=False) -> tuple[str,str]:
    if explicit_formula:
        return "explicit_quotation","high"
    if source_wording_overlap >= 0.65:
        return "strong_allusion","medium_high"
    if source_wording_overlap >= 0.35:
        return "possible_echo","medium"
    if thematic_only:
        return "thematic_parallel","medium_low"
    return "possible_echo","low"

def original_language_capability(tokens: list[dict]) -> dict:
    if not tokens:
        return {"status":"FAIL","reason":"no_original_language_tokens"}
    analyses=[a for t in tokens for a in t.get("analyses",[])]
    types={a.get("type") for a in analyses}
    return {"status":"PASS" if {"lemma","morphology"} <= types else "FAIL","token_count":len(tokens),"has_lemma":"lemma" in types,"has_morphology":"morphology" in types,"languages":sorted({t.get("language") for t in tokens if t.get("language")}),"provenance_complete":all(t.get("textual_source_id") and t.get("corpus_snapshot") for t in tokens)}
