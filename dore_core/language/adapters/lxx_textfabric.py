"""Septuagint (LXX) adapter for Doré's universal language core."""
from __future__ import annotations
import re
from collections import defaultdict
from typing import Iterable, Any
from dore_core.language.base import AdapterCapabilities, LanguageUnit, TextWitness

BOOK_MAP = {
    # CenterBLC/Rahlfs section labels are commonly abbreviated; keep full-name aliases too.
    "Gen":"GEN","Genesis":"GEN","Exod":"EXO","Exodus":"EXO","Lev":"LEV","Leviticus":"LEV",
    "Num":"NUM","Numbers":"NUM","Deut":"DEU","Deuteronomy":"DEU","Josh":"JOS","Joshua":"JOS",
    "Judg":"JDG","Judges":"JDG","Ruth":"RUT","1Sam":"1SA","1 Samuel":"1SA","2Sam":"2SA","2 Samuel":"2SA",
    "1Kgs":"1KI","1 Kings":"1KI","2Kgs":"2KI","2 Kings":"2KI","1Chr":"1CH","1 Chronicles":"1CH","2Chr":"2CH","2 Chronicles":"2CH",
    "Ezra":"EZR","Neh":"NEH","Nehemiah":"NEH","Esth":"EST","Esther":"EST","Job":"JOB",
    "Ps":"PSA","Pss":"PSA","Psalm":"PSA","Psalms":"PSA","Prov":"PRO","Proverbs":"PRO",
    "Eccl":"ECC","Ecclesiastes":"ECC","Song":"SNG","Song of Songs":"SNG","Isa":"ISA","Isaiah":"ISA",
    "Jer":"JER","Jeremiah":"JER","Lam":"LAM","Lamentations":"LAM","Ezek":"EZK","Ezekiel":"EZK",
    "Dan":"DAN","Daniel":"DAN","Hos":"HOS","Hosea":"HOS","Joel":"JOL","Amos":"AMO","Obad":"OBA","Obadiah":"OBA",
    "Jonah":"JON","Mic":"MIC","Micah":"MIC","Nah":"NAM","Nahum":"NAM","Hab":"HAB","Habakkuk":"HAB",
    "Zeph":"ZEP","Zephaniah":"ZEP","Hag":"HAG","Haggai":"HAG","Zech":"ZEC","Zechariah":"ZEC","Mal":"MAL","Malachi":"MAL",
}

class LXXTextFabricAdapter:
    adapter_id = "adapter.biblical.lxx.centerblc"
    language = "grc"
    capabilities = AdapterCapabilities(segmentation=True, normalization=True, lemma=True, morphology=True, syntax=False, transliteration=True, speech=False, canonical_alignment=True)
    def normalize(self, text: str) -> str: return text.strip()
    @staticmethod
    def _feature(api: Any, name: str, node: int):
        try: return api.Fs(name).v(node)
        except Exception: return None
    @staticmethod
    def _ref(book: str, chapter: object, verse: object) -> str:
        mapped = BOOK_MAP.get(str(book))
        if mapped: return f"bible.ref.{mapped}.{chapter}.{verse}"
        slug = re.sub(r"[^A-Za-z0-9]+", "_", str(book)).strip("_").upper() or "UNKNOWN"
        return f"lxx.ref.{slug}.{chapter}.{verse}"
    def ingest(self, app_or_api: Any, witness: TextWitness) -> Iterable[LanguageUnit]:
        api = getattr(app_or_api, "api", None) or app_or_api
        if api is None or not hasattr(api, "F") or not hasattr(api, "T"): raise ValueError("LXX Text-Fabric API is not loaded")
        F,T=api.F,api.T; orders:dict[str,int]=defaultdict(int)
        for node in F.otype.s("word"):
            section=T.sectionFromNode(node)
            if not section or len(section)<3: continue
            book,chapter,verse=section[:3]; ref=self._ref(str(book),chapter,verse); orders[ref]+=1; surface=self._feature(api,"word",node)
            if surface is None: surface=T.text(node).strip()
            analyses=[]
            for kind,feature in (("lemma","lex_utf8"),("morphology","morphology"),("part_of_speech","sp"),("strongs","strongs"),("transliteration","translit_SBL"),("subverse","subverse")):
                value=self._feature(api,feature,node)
                if value not in (None,""): analyses.append((kind,str(value)))
            yield LanguageUnit(witness.witness_id,ref,orders[ref],str(surface),self.normalize(str(surface)),"grc",tuple(analyses),(f"textual_source:{witness.source_id}",f"snapshot:{witness.snapshot}",f"tf_node:{node}"))
