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

BOOK_ALIASES = {
    "MAT":"MAT","MATT":"MAT","MATTHEW":"MAT","馬太":"MAT","馬太福音":"MAT","马太":"MAT","马太福音":"MAT","太":"MAT",
    "MRK":"MRK","MARK":"MRK","馬可":"MRK","馬可福音":"MRK","马可":"MRK","马可福音":"MRK","可":"MRK",
    "LUK":"LUK","LUKE":"LUK","路加":"LUK","路加福音":"LUK","路":"LUK",
    "JHN":"JHN","JOHN":"JHN","約翰":"JHN","約翰福音":"JHN","约翰":"JHN","约翰福音":"JHN","約":"JHN","约":"JHN",
    "GEN":"GEN","GENESIS":"GEN","創世記":"GEN","创世记":"GEN","創":"GEN","创":"GEN",
    "PSA":"PSA","PSALM":"PSA","PSALMS":"PSA","詩篇":"PSA","诗篇":"PSA","詩":"PSA","诗":"PSA",
    "ISA":"ISA","ISAIAH":"ISA","以賽亞書":"ISA","以赛亚书":"ISA","賽":"ISA","赛":"ISA",
}
ZH_DIGITS={"零":0,"〇":0,"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"兩":2,"两":2}
ZH_VARIANTS=str.maketrans({
    '虚':'虛','来':'來','语':'語','书':'書','这':'這','马':'馬','约':'約','传':'傳','罗':'羅','后':'後','数':'數','创':'創','启':'啟','亚':'亞','结':'結','历':'歷','腊':'臘','国':'國','爱':'愛','灵':'靈','体':'體','万':'萬','与':'與','为':'為','义':'義','圣':'聖','经':'經','节':'節','处':'處','发':'發','从':'從','条':'條','树':'樹','见':'見','听':'聽','说':'說','问':'問','应':'應','难':'難','亲':'親','风':'風','声':'聲','头':'頭','会':'會','开':'開','长':'長','无':'無','时':'時','实':'實','进':'進','当':'當','归':'歸','众':'眾','还':'還','显':'顯','灭':'滅','将':'將','谁':'誰','让':'讓','觉':'覺','称':'稱','复':'復','获':'獲','读':'讀','写':'寫','译':'譯','词':'詞','证':'證','据':'據','类':'類','别':'別','简':'簡'
})

def _zh_number(s:str)->int|None:
    s=s.strip()
    if s.isdigit():return int(s)
    if not s:return None
    if "百" in s:
        a,b=s.split("百",1); left=ZH_DIGITS.get(a,1) if a else 1; right=_zh_number(b) if b else 0
        return left*100+(right or 0)
    if "十" in s:
        a,b=s.split("十",1); left=ZH_DIGITS.get(a,1) if a else 1; right=ZH_DIGITS.get(b,0) if b else 0
        return left*10+right
    return ZH_DIGITS.get(s)

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
    def from_units(cls, units: Iterable) -> "BibleSearchIndex":return cls(list(units))

    def search(self, query: SearchQuery) -> list[SearchHit]:
        q=query.value.strip()
        if not q:return []
        candidates=[]
        for u in self.units:
            if query.language and getattr(u,"language",None)!=query.language:continue
            if query.witness_id and getattr(u,"witness_id",None)!=query.witness_id:continue
            score=self._score(u,q,query.mode)
            if score<=0:continue
            candidates.append(SearchHit(getattr(u,"canonical_ref_id",""),getattr(u,"witness_id",""),getattr(u,"surface",""),getattr(u,"language",""),round(score,6),query.mode,tuple(getattr(u,"provenance",()) or ()),tuple(getattr(u,"analyses",()) or ())))
        candidates.sort(key=lambda h:(-h.score,h.canonical_ref_id,h.witness_id))
        return candidates[:max(1,min(query.limit,100))]

    def _score(self,u,q:str,mode:SearchMode)->float:
        surface=str(getattr(u,"surface","") or ""); ref=str(getattr(u,"canonical_ref_id","") or ""); analyses=dict(getattr(u,"analyses",()) or ())
        if mode=="reference":
            nq=self._normalize_ref(q); nr=self._normalize_ref(ref)
            if not nq:return 0.0
            return 1.0 if (nq==nr or nr.startswith(nq+".")) else 0.0
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
    def _norm(s:str)->str:
        folded=s.translate(ZH_VARIANTS)
        return re.sub(r"[\s.,;:!?，。；：！？「」『』()（）\-–—]+","",folded).casefold()

    @staticmethod
    def _normalize_ref(s:str)->str:
        raw=s.strip().upper().replace("：",":")
        raw=re.sub(r"^BIBLE\.REF\.","",raw)
        m=re.match(r"^(.+?)第?([零〇一二三四五六七八九十百兩两\d]+)章(?:第?([零〇一二三四五六七八九十百兩两\d]+)節?)?$",raw,re.I)
        if m:
            book=BOOK_ALIASES.get(m.group(1).replace(" ","")); chapter=_zh_number(m.group(2)); verse=_zh_number(m.group(3)) if m.group(3) else None
            if book and chapter:return f"{book}.{chapter}"+(f".{verse}" if verse else "")
        m=re.match(r"^(.+?)\s*(\d+)\s*[:.]\s*(\d+)$",raw)
        if m:
            book=BOOK_ALIASES.get(m.group(1).replace(" ",""));
            if book:return f"{book}.{int(m.group(2))}.{int(m.group(3))}"
        m=re.match(r"^(.+?)\s+(\d+)$",raw)
        if m:
            book=BOOK_ALIASES.get(m.group(1).replace(" ",""));
            if book:return f"{book}.{int(m.group(2))}"
        raw=raw.replace(":",".").replace(" ",".")
        parts=[p for p in re.sub(r"\.+",".",raw).strip(".").split(".") if p]
        if parts:parts[0]=BOOK_ALIASES.get(parts[0],parts[0])
        return ".".join(parts)
