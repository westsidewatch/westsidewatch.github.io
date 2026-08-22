"""Septuagint (LXX) adapter for Doré's universal language core.

Reference source: CenterBLC/LXX, Rahlfs 1935 Text-Fabric dataset.
The adapter keeps the source witness independent from the Hebrew Bible and NT.
"""
from __future__ import annotations
import re
from collections import defaultdict
from typing import Iterable, Any
from dore_core.language.base import AdapterCapabilities, LanguageUnit, TextWitness

BOOK_MAP = {
    "Genesis":"GEN","Exodus":"EXO","Leviticus":"LEV","Numbers":"NUM","Deuteronomy":"DEU",
    "Joshua":"JOS","Judges":"JDG","Ruth":"RUT","1 Samuel":"1SA","2 Samuel":"2SA",
    "1 Kings":"1KI","2 Kings":"2KI","1 Chronicles":"1CH","2 Chronicles":"2CH",
    "Ezra":"EZR","Nehemiah":"NEH","Esther":"EST","Job":"JOB","Psalms":"PSA","Psalm":"PSA",
    "Proverbs":"PRO","Ecclesiastes":"ECC","Song of Songs":"SNG","Isaiah":"ISA","Jeremiah":"JER",
    "Lamentations":"LAM","Ezekiel":"EZK","Daniel":"DAN","Hosea":"HOS","Joel":"JOL","Amos":"AMO",
    "Obadiah":"OBA","Jonah":"JON","Micah":"MIC","Nahum":"NAM","Habakkuk":"HAB","Zephaniah":"ZEP",
    "Haggai":"HAG","Zechariah":"ZEC","Malachi":"MAL",
}

class LXXTextFabricAdapter:
    adapter_id = "adapter.biblical.lxx.centerblc"
    language = "grc"
    capabilities = AdapterCapabilities(
        segmentation=True, normalization=True, lemma=True, morphology=True,
        syntax=False, transliteration=True, speech=False, canonical_alignment=True,
    )

    def normalize(self, text: str) -> str:
        return text.strip()

    @staticmethod
    def _feature(api: Any, name: str, node: int):
        try:
            return api.Fs(name).v(node)
        except Exception:
            return None

    @staticmethod
    def _ref(book: str, chapter: object, verse: object) -> str:
        mapped = BOOK_MAP.get(str(book))
        if mapped:
            return f"bible.ref.{mapped}.{chapter}.{verse}"
        slug = re.sub(r"[^A-Za-z0-9]+", "_", str(book)).strip("_").upper() or "UNKNOWN"
        return f"lxx.ref.{slug}.{chapter}.{verse}"

    def ingest(self, app: Any, witness: TextWitness) -> Iterable[LanguageUnit]:
        api = app.api
        F, T = api.F, api.T
        orders: dict[str, int] = defaultdict(int)
        for node in F.otype.s("word"):
            section = T.sectionFromNode(node)
            if not section or len(section) < 3:
                continue
            book, chapter, verse = section[:3]
            ref = self._ref(str(book), chapter, verse)
            orders[ref] += 1
            surface = self._feature(api, "word", node)
            if surface is None:
                surface = T.text(node).strip()
            analyses = []
            for kind, feature in (
                ("lemma", "lex_utf8"), ("morphology", "morphology"),
                ("part_of_speech", "sp"), ("strongs", "strongs"),
                ("transliteration", "translit_SBL"), ("subverse", "subverse"),
            ):
                value = self._feature(api, feature, node)
                if value not in (None, ""):
                    analyses.append((kind, str(value)))
            yield LanguageUnit(
                witness_id=witness.witness_id,
                canonical_ref_id=ref,
                order=orders[ref],
                surface=str(surface),
                normalized=self.normalize(str(surface)),
                language="grc",
                analyses=tuple(analyses),
                provenance=(
                    f"textual_source:{witness.source_id}",
                    f"snapshot:{witness.snapshot}",
                    f"tf_node:{node}",
                ),
            )
