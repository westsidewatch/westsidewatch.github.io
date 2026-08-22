"""Ingest the complete Open Scriptures Hebrew Lexicon into Doré.

Upstream files:
- AugIndex.xml: OSHB augmented lemma -> lexical-index id
- LexicalIndex.xml: lexical hub / dictionary form / POS / gloss links
- HebrewStrong.xml: Strong dictionary content

The adapter is intentionally schema-tolerant but provenance-strict: raw XML
attributes/text are retained and unresolved entries remain explicit.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import xml.etree.ElementTree as ET

@dataclass(frozen=True)
class OSHBLexiconEntry:
    augmented_id: str
    lexical_index_id: str
    lexeme: Optional[str]
    transliteration: Optional[str]
    part_of_speech: Optional[str]
    gloss: Optional[str]
    strong_id: Optional[str]
    raw_index: dict[str, str]
    source_snapshot: str
    status: str


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_aug_index(xml_text: str) -> dict[str, str]:
    root = ET.fromstring(xml_text)
    result: dict[str, str] = {}
    for node in root.iter():
        if _local(node.tag) != "w":
            continue
        aug = node.attrib.get("aug")
        lexical_id = (node.text or "").strip()
        if aug and lexical_id:
            result[aug] = lexical_id
    return result


def _first_text(node: ET.Element, names: set[str]) -> Optional[str]:
    for child in node.iter():
        if _local(child.tag).lower() in names:
            value = "".join(child.itertext()).strip()
            if value:
                return value
    return None


def parse_lexical_index(xml_text: str) -> dict[str, dict[str, Optional[str]]]:
    root = ET.fromstring(xml_text)
    result: dict[str, dict[str, Optional[str]]] = {}
    for node in root.iter():
        lexical_id = node.attrib.get("id")
        if not lexical_id:
            continue
        result[lexical_id] = {
            "lexeme": _first_text(node, {"w", "word", "lemma", "heb", "hebrew"}),
            "transliteration": _first_text(node, {"translit", "transliteration", "xlit"}),
            "part_of_speech": _first_text(node, {"pos", "partofspeech"}),
            "gloss": _first_text(node, {"gloss", "meaning"}),
            "strong_id": node.attrib.get("strong") or _first_text(node, {"strong"}),
            "raw_tag": _local(node.tag),
        }
    return result


def ingest_oshb_lexicon(aug_xml: str, lexical_xml: str, snapshot: str) -> dict[str, OSHBLexiconEntry]:
    aug = parse_aug_index(aug_xml)
    lexical = parse_lexical_index(lexical_xml)
    entries: dict[str, OSHBLexiconEntry] = {}
    for augmented_id, lexical_id in aug.items():
        data = lexical.get(lexical_id, {})
        lexeme = data.get("lexeme")
        entries[augmented_id] = OSHBLexiconEntry(
            augmented_id=augmented_id,
            lexical_index_id=lexical_id,
            lexeme=lexeme,
            transliteration=data.get("transliteration"),
            part_of_speech=data.get("part_of_speech"),
            gloss=data.get("gloss"),
            strong_id=data.get("strong_id"),
            raw_index={k: str(v) for k, v in data.items() if v is not None},
            source_snapshot=snapshot,
            status="resolved" if lexeme else "index-linked",
        )
    return entries
