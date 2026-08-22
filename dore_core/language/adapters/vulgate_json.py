"""Latin Vulgate JSON adapter for Doré Language Core.

The adapter accepts several common Bible JSON shapes and emits verse-token
LanguageUnits without assuming lexical/morphological annotation that the
source does not provide.
"""
from __future__ import annotations
import re
from typing import Any, Iterable
from dore_core.language.base import AdapterCapabilities, LanguageUnit, TextWitness

BOOK_ALIASES = {
    # English/common names
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

    # Latin / traditional Vulgate titles used by common Vulgate datasets
    "numeri":"NUM","deuteronomium":"DEU","josue":"JOS","judicum":"JDG",
    "i regum":"1SA","ii regum":"2SA","iii regum":"1KI","iv regum":"2KI",
    "1 regum":"1SA","2 regum":"2SA","3 regum":"1KI","4 regum":"2KI",
    "i paralipomenon":"1CH","ii paralipomenon":"2CH","1 paralipomenon":"1CH","2 paralipomenon":"2CH",
    "i esdrae":"EZR","ii esdrae":"NEH","1 esdrae":"EZR","2 esdrae":"NEH",
    "psalmi":"PSA","proverbia":"PRO","canticum canticorum":"SNG","isaias":"ISA","jeremias":"JER",
    "lamentationes":"LAM","ezechiel":"EZK","osee":"HOS","abdias":"OBA","jonas":"JON","michaeas":"MIC",
    "habacuc":"HAB","sophonias":"ZEP","aggaeus":"HAG","zacharias":"ZEC","malachias":"MAL",
    "matthaeus":"MAT","marcus":"MRK","lucas":"LUK","joannes":"JHN","ioannes":"JHN",
    "actus apostolorum":"ACT","ad romanos":"ROM",
    "i ad corinthios":"1CO","ii ad corinthios":"2CO","1 ad corinthios":"1CO","2 ad corinthios":"2CO",
    "ad galatas":"GAL","ad ephesios":"EPH","ad philippenses":"PHP","ad colossenses":"COL",
    "i ad thessalonicenses":"1TH","ii ad thessalonicenses":"2TH","1 ad thessalonicenses":"1TH","2 ad thessalonicenses":"2TH",
    "i ad timotheum":"1TI","ii ad timotheum":"2TI","1 ad timotheum":"1TI","2 ad timotheum":"2TI",
    "ad titum":"TIT","ad philemonem":"PHM","ad hebraeos":"HEB","jacobi":"JAS","iacobi":"JAS",
    "i petri":"1PE","ii petri":"2PE","1 petri":"1PE","2 petri":"2PE",
    "i joannis":"1JN","ii joannis":"2JN","iii joannis":"3JN",
    "i ioannis":"1JN","ii ioannis":"2JN","iii ioannis":"3JN",
    "1 joannis":"1JN","2 joannis":"2JN","3 joannis":"3JN",
    "judae":"JUD","iudae":"JUD","apocalypsis":"REV","apocalypsis joannis":"REV","apocalypsis ioannis":"REV",

    # Deuterocanonical / Vulgate witnesses retained as distinct canonical-like ids.
    "tobias":"TOB","tobit":"TOB","judith":"JDT","iudith":"JDT","sapientia":"WIS",
    "ecclesiasticus":"SIR","baruch":"BAR","i machabaeorum":"1MA","ii machabaeorum":"2MA",
    "1 machabaeorum":"1MA","2 machabaeorum":"2MA","i maccabees":"1MA","ii maccabees":"2MA",

    # Exact titles in bible-api-io/bible-api-version-vulgate snapshot.
    "aggæus":"HAG","esdræ":"EZR","joannis i":"1JN","joannis ii":"2JN","joannis iii":"3JN",
    "joël":"JOL","judæ":"JUD","matthæus":"MAT","michæa":"MIC","nehemiæ":"NEH",
    "paralipomenon i":"1CH","paralipomenon ii":"2CH","petri i":"1PE","petri ii":"2PE",
    "regum i":"1SA","regum ii":"2SA","regum iii":"1KI","regum iv":"2KI",
    "ad corinthios i":"1CO","ad corinthios ii":"2CO","ad hebræos":"HEB",
    "ad thessalonicenses i":"1TH","ad thessalonicenses ii":"2TH",
    "ad timotheum i":"1TI","ad timotheum ii":"2TI",
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

    def recognized_book_names(self, source: Any) -> tuple[str, ...]:
        books_data = source.get("booksData") if isinstance(source, dict) else None
        if not isinstance(books_data, dict):
            return ()
        return tuple(sorted(
            str((obj.get("name") if isinstance(obj, dict) else None) or key)
            for key, obj in books_data.items()
            if self._book_code(str((obj.get("name") if isinstance(obj, dict) else None) or key))
        ))

    def unrecognized_book_names(self, source: Any) -> tuple[str, ...]:
        books_data = source.get("booksData") if isinstance(source, dict) else None
        if not isinstance(books_data, dict):
            return ()
        return tuple(sorted(
            str((obj.get("name") if isinstance(obj, dict) else None) or key)
            for key, obj in books_data.items()
            if not self._book_code(str((obj.get("name") if isinstance(obj, dict) else None) or key))
        ))

    def _emit_verse(self, book: str, chapter: int, verse: int, text: str, witness: TextWitness) -> Iterable[LanguageUnit]:
        code = self._book_code(book)
        if not code:
            return ()
        ref = f"bible.ref.{code}.{int(chapter)}.{int(verse)}"
        return tuple(LanguageUnit(
            witness_id=witness.witness_id,
            canonical_ref_id=ref,
            order=order,
            surface=surface,
            normalized=self.normalize(surface),
            language="la",
            analyses=(),
            provenance=(f"textual_source:{witness.source_id}", f"snapshot:{witness.snapshot}"),
        ) for order, surface in enumerate(TOKEN_RE.findall(text), start=1))

    def ingest(self, source: Any, witness: TextWitness) -> Iterable[LanguageUnit]:
        """Detect common nested Bible JSON shapes and emit all recognized verses."""
        yielded = 0

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

        books_data = source.get("booksData") if isinstance(source, dict) else None
        if isinstance(books_data, dict):
            for book_key, book_obj in books_data.items():
                if not isinstance(book_obj, dict):
                    continue
                book = book_obj.get("name") or book_key
                if not self._book_code(str(book)):
                    continue
                chapters = book_obj.get("chaptersData")
                if not isinstance(chapters, list):
                    continue
                for ch, verses in enumerate(chapters):
                    if ch == 0 or not isinstance(verses, list):
                        continue
                    for vs, text in enumerate(verses):
                        if vs == 0 or not isinstance(text, str):
                            continue
                        for unit in self._emit_verse(str(book), ch, vs, text, witness):
                            yielded += 1
                            yield unit

        if yielded == 0:
            raise ValueError("unrecognized Vulgate JSON structure or no canonical verses found")
