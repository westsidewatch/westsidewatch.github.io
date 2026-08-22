"""Adapter for Midvash-style per-book JSON Bible witnesses.

Chinese is segmented conservatively as Han-character / alphanumeric-run /
punctuation units. Word segmentation remains a later, separately sourced
linguistic-enrichment layer; the witness surface is never rewritten.
"""
from __future__ import annotations
import re
from typing import Any, Iterable
from dore_core.language.base import AdapterCapabilities, LanguageUnit, TextWitness

OSIS_TO_CANON = {
    "Gen":"GEN","Exod":"EXO","Lev":"LEV","Num":"NUM","Deut":"DEU","Josh":"JOS","Judg":"JDG","Ruth":"RUT",
    "1Sam":"1SA","2Sam":"2SA","1Kgs":"1KI","2Kgs":"2KI","1Chr":"1CH","2Chr":"2CH","Ezra":"EZR","Neh":"NEH",
    "Esth":"EST","Job":"JOB","Ps":"PSA","Prov":"PRO","Eccl":"ECC","Song":"SNG","Isa":"ISA","Jer":"JER","Lam":"LAM",
    "Ezek":"EZK","Dan":"DAN","Hos":"HOS","Joel":"JOL","Amos":"AMO","Obad":"OBA","Jonah":"JON","Mic":"MIC","Nah":"NAM",
    "Hab":"HAB","Zeph":"ZEP","Hag":"HAG","Zech":"ZEC","Mal":"MAL","Matt":"MAT","Mark":"MRK","Luke":"LUK","John":"JHN",
    "Acts":"ACT","Rom":"ROM","1Cor":"1CO","2Cor":"2CO","Gal":"GAL","Eph":"EPH","Phil":"PHP","Col":"COL","1Thess":"1TH",
    "2Thess":"2TH","1Tim":"1TI","2Tim":"2TI","Titus":"TIT","Phlm":"PHM","Heb":"HEB","Jas":"JAS","1Pet":"1PE","2Pet":"2PE",
    "1John":"1JN","2John":"2JN","3John":"3JN","Jude":"JUD","Rev":"REV",
}

ZH_UNIT_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]|[A-Za-z0-9]+|[^\s]", re.UNICODE)
DEFAULT_UNIT_RE = re.compile(r"\w+(?:['’\-]\w+)*|[^\w\s]", re.UNICODE)

class MidvashBookJSONAdapter:
    adapter_id = "adapter.biblical.midvash.book_json"
    capabilities = AdapterCapabilities(segmentation=True, normalization=True, canonical_alignment=True)

    def __init__(self, language: str):
        self.language = language

    def normalize(self, text: str) -> str:
        return " ".join(text.split())

    def _segments(self, text: str) -> list[str]:
        regex = ZH_UNIT_RE if self.language.startswith("zh") else DEFAULT_UNIT_RE
        return regex.findall(text)

    def ingest_book(self, source: Any, witness: TextWitness) -> Iterable[LanguageUnit]:
        if not isinstance(source, dict):
            raise ValueError("book source must be an object")
        osis = str(source.get("book", ""))
        code = OSIS_TO_CANON.get(osis)
        if not code:
            raise ValueError(f"unrecognized OSIS book id: {osis!r}")
        chapters = source.get("chapters")
        if not isinstance(chapters, list):
            raise ValueError(f"missing chapters for {osis}")
        for chapter_obj in chapters:
            if not isinstance(chapter_obj, dict):
                continue
            try:
                chapter = int(chapter_obj["chapter"])
            except (KeyError, TypeError, ValueError):
                continue
            verses = chapter_obj.get("verses")
            if not isinstance(verses, list):
                continue
            for verse_obj in verses:
                if not isinstance(verse_obj, dict):
                    continue
                try:
                    verse = int(verse_obj["number"])
                except (KeyError, TypeError, ValueError):
                    continue
                text = verse_obj.get("text")
                if not isinstance(text, str):
                    continue
                ref = f"bible.ref.{code}.{chapter}.{verse}"
                for order, surface in enumerate(self._segments(text), start=1):
                    yield LanguageUnit(
                        witness_id=witness.witness_id,
                        canonical_ref_id=ref,
                        order=order,
                        surface=surface,
                        normalized=self.normalize(surface),
                        language=witness.language,
                        analyses=(),
                        provenance=(f"textual_source:{witness.source_id}", f"snapshot:{witness.snapshot}"),
                    )
