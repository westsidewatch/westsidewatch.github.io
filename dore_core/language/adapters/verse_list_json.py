"""Reusable verse-list JSON adapter for modern Bible witnesses."""
from __future__ import annotations
import re
from typing import Any, Iterable
from dore_core.language.base import AdapterCapabilities, LanguageUnit, TextWitness

BOOK_ALIASES = {
    "genesis":"GEN","exodus":"EXO","leviticus":"LEV","numbers":"NUM","deuteronomy":"DEU","joshua":"JOS","judges":"JDG","ruth":"RUT","1 samuel":"1SA","2 samuel":"2SA","1 kings":"1KI","2 kings":"2KI","1 chronicles":"1CH","2 chronicles":"2CH","ezra":"EZR","nehemiah":"NEH","esther":"EST","job":"JOB","psalms":"PSA","psalm":"PSA","proverbs":"PRO","ecclesiastes":"ECC","song of songs":"SNG","isaiah":"ISA","jeremiah":"JER","lamentations":"LAM","ezekiel":"EZK","daniel":"DAN","hosea":"HOS","joel":"JOL","amos":"AMO","obadiah":"OBA","jonah":"JON","micah":"MIC","nahum":"NAM","habakkuk":"HAB","zephaniah":"ZEP","haggai":"HAG","zechariah":"ZEC","malachi":"MAL","matthew":"MAT","mark":"MRK","luke":"LUK","john":"JHN","acts":"ACT","romans":"ROM","1 corinthians":"1CO","2 corinthians":"2CO","galatians":"GAL","ephesians":"EPH","philippians":"PHP","colossians":"COL","1 thessalonians":"1TH","2 thessalonians":"2TH","1 timothy":"1TI","2 timothy":"2TI","titus":"TIT","philemon":"PHM","hebrews":"HEB","james":"JAS","1 peter":"1PE","2 peter":"2PE","1 john":"1JN","2 john":"2JN","3 john":"3JN","jude":"JUD","revelation":"REV"
}
TOKEN_RE = re.compile(r"\w+(?:['’\-]\w+)*|[^\w\s]", re.UNICODE)

class VerseListJSONAdapter:
    adapter_id = "adapter.biblical.modern.verse_list_json"
    capabilities = AdapterCapabilities(segmentation=True, normalization=True, canonical_alignment=True)

    def __init__(self, language: str):
        self.language = language

    def normalize(self, text: str) -> str:
        return " ".join(text.split())

    def ingest(self, source: Any, witness: TextWitness) -> Iterable[LanguageUnit]:
        if not isinstance(source, list):
            raise ValueError("verse-list source must be a list")
        for row in source:
            if not isinstance(row, dict):
                continue
            book = BOOK_ALIASES.get(str(row.get("book", "")).strip().lower())
            text = row.get("text")
            if not book or not isinstance(text, str):
                continue
            try:
                chapter, verse = int(row["chapter"]), int(row["verse"])
            except (KeyError, TypeError, ValueError):
                continue
            ref = f"bible.ref.{book}.{chapter}.{verse}"
            for order, surface in enumerate(TOKEN_RE.findall(text), start=1):
                yield LanguageUnit(
                    witness_id=witness.witness_id, canonical_ref_id=ref, order=order,
                    surface=surface, normalized=self.normalize(surface), language=witness.language,
                    analyses=(), provenance=(f"textual_source:{witness.source_id}", f"snapshot:{witness.snapshot}"),
                )
