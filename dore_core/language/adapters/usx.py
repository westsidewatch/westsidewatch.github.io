"""Reusable USX adapter for modern Bible witnesses."""
from __future__ import annotations
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable
from dore_core.language.base import AdapterCapabilities, LanguageUnit, TextWitness
from dore_core.language.adapters.verse_list_json import TOKEN_RE

class USXAdapter:
    adapter_id = "adapter.biblical.modern.usx"
    capabilities = AdapterCapabilities(segmentation=True, normalization=True, canonical_alignment=True)

    def __init__(self, language: str):
        self.language = language

    def normalize(self, text: str) -> str:
        return " ".join(text.split())

    def ingest(self, source, witness: TextWitness) -> Iterable[LanguageUnit]:
        paths = sorted(Path(source).glob("*.usx")) if Path(source).is_dir() else [Path(source)]
        for path in paths:
            root = ET.parse(path).getroot()
            book_node = root.find(".//book")
            if book_node is None:
                continue
            book = (book_node.attrib.get("code") or "").upper()
            chapter = None
            verse = None
            buffers: dict[tuple[int,int], list[str]] = {}
            for elem in root.iter():
                tag = elem.tag.rsplit("}", 1)[-1]
                if tag == "chapter" and elem.attrib.get("number"):
                    try: chapter = int(re.match(r"\d+", elem.attrib["number"]).group())
                    except Exception: chapter = None
                elif tag == "verse" and elem.attrib.get("number"):
                    try: verse = int(re.match(r"\d+", elem.attrib["number"]).group())
                    except Exception: verse = None
                if chapter is not None and verse is not None:
                    if elem.text and tag not in {"note"}:
                        buffers.setdefault((chapter, verse), []).append(elem.text)
                    if elem.tail:
                        buffers.setdefault((chapter, verse), []).append(elem.tail)
            for (ch, vs), pieces in sorted(buffers.items()):
                text = self.normalize(" ".join(pieces))
                if not text:
                    continue
                ref = f"bible.ref.{book}.{ch}.{vs}"
                for order, surface in enumerate(TOKEN_RE.findall(text), start=1):
                    yield LanguageUnit(witness_id=witness.witness_id, canonical_ref_id=ref, order=order,
                        surface=surface, normalized=self.normalize(surface), language=witness.language,
                        analyses=(), provenance=(f"textual_source:{witness.source_id}", f"snapshot:{witness.snapshot}"))
