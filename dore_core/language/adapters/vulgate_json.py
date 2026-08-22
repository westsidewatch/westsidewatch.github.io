"""Latin Vulgate JSON adapter for Doré Language Core.

The adapter accepts several common Bible JSON shapes and emits verse-token
LanguageUnits without assuming lexical/morphological annotation that the
source does not provide.
"""
from __future__ import annotations
import re
from collections import defaultdict
from typing import Any, Iterable
from dore_core.language.base import AdapterCapabilities, LanguageUnit, TextWitness

BOOK_ALIASES = {
    "genesis":"GEN","exodus":"EXO","leviticus":"LEV","numbers":"NUM","deuteronomy":"DEU",
    "joshua":"JOS","judges":"JDG","ruth":"RUT","1 samuel":"1SA","2 samuel":"2SA",
    "1 kings":"1KI","2 kings":"2KI","1 chronicles":"1CH","2 chronicles":"2CH",
    "ezra":"EZR","nehemiah":"NEH","esther":"EST","job":"JOB","psalms":"PSA","psalm":"PSA",
    "proverbs":"PRO","ecclesiastes":"ECC","song of songs":"SNG","isaiah":"ISA","jeremiah":"JER",
    "lamentations":"LAM","ezekiel":"EZK","daniel":"DAN","hosea":"HOS","joel":"JOL","amos":"AMO",
    "obadiah":"OBA","jonah":"JON","micah":"MIC","nahum":"NAM","habakkuk":"HAB","zephaniah":"ZEP",
    "haggai":"HAG","zechariah":"ZEC","malachi":"MAL","matthew":"MAT","mark":"MRK","luke":"LUK",
    "john":"JHN","acts":"ACT","romans":"ROM","1 corinthians":"1CO","2 corinthians":"2CO",
    "galatians":"GAL","ephesians":"EPH","philippians":"PHP","colossians":"COL","1 thessalonians":"1TH",
    "2 thessalonians":"2TH","1 timothy":"1TI","2 timothy":"2TI","titus":"TIT","philemon":"PHM",
    "hebrews":"HEB","james":"JAS","1 peter":"1PE","2 peter":"2PE","1 john":"1JN","2 john":"2JN",
    "3 john":"3JN","jude":"JUD","revelation":"REV",
}

TOKEN_RE = re.compile(r"\w+(?:['’\-]\w+)*|[^\w\s]", re.UNICODE)

class VulgateJSONAdapter:
    adapter_id = "adapter.biblical.vulgate.json"
    language = "la"
    capabilities = AdapterCapabilities(
        segmentation=True, normalization=True, lemma=False, morphology=False,
        syntax=False, transliteration=False, speech=False, canonical_alignment=True,
    )

    def normalize(self, text: str) -> str:
        return " ".join(text.split())

    def _book_code(self, name: str) -> str | None:
        key = re.sub(r"\s+", " ", name.strip().lower())
        return BOOK_ALIASES.get(key)

    def _emit_verse(self, book: str, chapter: int, verse: int, text: str, witness: TextWitness) -> Iterable[LanguageUnit]:
        code = self._book_code(book)
        if not code:
            return ()
        ref = f"bible.ref.{code}.{int(chapter)}.{int(verse)}"
        result = []
        for order, surface in enumerate(TOKEN_RE.findall(text), start=1):
            result.append(LanguageUnit(
                witness_id=witness.witness_id,
                canonical_ref_id=ref,
                order=order,
                surface=surface,
                normalized=self.normalize(surface),
                language="la",
                analyses=(),
                provenance=(f"textual_source:{witness.source_id}", f"snapshot:{witness.snapshot}"),
            ))
        return tuple(result)

    def ingest(self, source: Any, witness: TextWitness) -> Iterable[LanguageUnit]:
        """Detect common nested Bible JSON shapes and emit all recognized verses."""
        yielded = 0

        # Shape A: {"Genesis": {"1": {"1": "..."}}}
        if isinstance(source, dict):
            for book, chapters in source.items():
                if self._book_code(str(book)) and isinstance(chapters, (dict, list)):
                    chapter_items = chapters.items() if isinstance(chapters, dict) else enumerate(chapters, start=1)
                    for chapter, verses in chapter_items:
                        try: ch = int(chapter)
                        except (TypeError, ValueError): continue
                        verse_items = verses.items() if isinstance(verses, dict) else enumerate(verses, start=1) if isinstance(verses, list) else ()
                        for verse, text in verse_items:
                            if not isinstance(text, str): continue
                            try: vs = int(verse)
                            except (TypeError, ValueError): continue
                            for unit in self._emit_verse(str(book), ch, vs, text, witness):
                                yielded += 1
                                yield unit

        # Shape B: [{"name"/"book":"Genesis", "chapters":[["verse", ...], ...]}]
        books = source if isinstance(source, list) else source.get("books") if isinstance(source, dict) else None
        if isinstance(books, list):
            for book_obj in books:
                if not isinstance(book_obj, dict): continue
                book = book_obj.get("name") or book_obj.get("book") or book_obj.get("title")
                chapters = book_obj.get("chapters")
                if not book or not self._book_code(str(book)) or not isinstance(chapters, list): continue
                for ch, verses in enumerate(chapters, start=1):
                    if isinstance(verses, list):
                        for vs, text in enumerate(verses, start=1):
                            if isinstance(text, str):
                                for unit in self._emit_verse(str(book), ch, vs, text, witness):
                                    yielded += 1
                                    yield unit
                    elif isinstance(verses, dict):
                        for vs, text in verses.items():
                            if isinstance(text, str):
                                try: vnum = int(vs)
                                except (TypeError, ValueError): continue
                                for unit in self._emit_verse(str(book), ch, vnum, text, witness):
                                    yielded += 1
                                    yield unit

        if yielded == 0:
            raise ValueError("unrecognized Vulgate JSON structure or no canonical verses found")
