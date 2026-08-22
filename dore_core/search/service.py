"""Product-independent Bible search service for Doré Core.

The service returns evidence-bearing candidates; consumers decide presentation.
It never invents missing Scripture text and never upgrades fuzzy matches to facts.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Iterable, Literal
import re

SearchMode = Literal["reference","text","lemma","morphology","fuzzy"]

@dataclass(frozen=True)
class SearchQuery:
    value: str
    mode: SearchMode = "text"
    language: str | None = None
    witness_id: str | None = None
    limit: int = 20

@dataclass(frozen=True)
class SearchHit:
    canonical_ref_id: str
    witness_id: str
    surface: str
    language: str
    score: float
    match_type: str
    provenance: tuple[str, ...] = ()
    analyses: tuple[tuple[str,str], ...] = ()

@dataclass
class BibleSearchIndex:
    units: list = field(default_factory=list)

    @classmethod
    def from_units(cls, units: Iterable) -> "BibleSearchIndex":
        return cls(list(units))

    def search(self, query: SearchQuery) -> list[SearchHit]:
        q=query.value.strip()
        if not q:return []
        candidates=[]
        for u in self.units:
            if query.language and getattr(u,"language",None)!=query.language:continue
            if query.witness_id and getattr(u,"witness_id",None)!=query.witness_id:continue
            score=self._score(u,q,query.mode)
            if score<=0:continue
            candidates.append(SearchHit(
                canonical_ref_id=getattr(u,"canonical_ref_id",""), witness_id=getattr(u,"witness_id",""),
                surface=getattr(u,"surface",""), language=getattr(u,"language",""), score=round(score,6),
                match_type=query.mode, provenance=tuple(getattr(u,"provenance",()) or ()), analyses=tuple(getattr(u,"analyses",()) or ())))
        candidates.sort(key=lambda h:(-h.score,h.canonical_ref_id,h.witness_id))
        return candidates[:max(1,min(query.limit,100))]

    def _score(self,u,q:str,mode:SearchMode)->float:
        surface=str(getattr(u,"surface","") or "")
        ref=str(getattr(u,"canonical_ref_id","") or "")
        analyses=dict(getattr(u,"analyses",()) or ())
        if mode=="reference":
            nq=self._normalize_ref(q); nr=self._normalize_ref(ref)
            return 1.0 if nq and (nq==nr or nr.endswith(nq)) else 0.0
        if mode=="lemma":return 1.0 if analyses.get("lemma","").casefold()==q.casefold() else 0.0
        if mode=="morphology":return 1.0 if q.casefold() in analyses.get("morphology","").casefold() else 0.0
        if mode=="text":
            a,b=self._norm(surface),self._norm(q)
            if not b:return 0.0
            if a==b:return 1.0
            if b in a:return 0.9
            return 0.0
        a,b=self._norm(surface),self._norm(q)
        if not a or not b:return 0.0
        ratio=SequenceMatcher(None,a,b).ratio()
        return ratio if ratio>=0.55 else 0.0

    @staticmethod
    def _norm(s:str)->str:return re.sub(r"\s+","",s).casefold()
    @staticmethod
    def _normalize_ref(s:str)->str:
        s=s.strip().upper().replace(":",".").replace(" ",".")
        s=re.sub(r"^BIBLE\.REF\.","",s)
        return re.sub(r"\.+",".",s).strip(".")
