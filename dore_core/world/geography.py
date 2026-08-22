"""OpenBible geocoding reader with ancient identity / modern candidate separation."""
from __future__ import annotations
from dataclasses import dataclass
import json,re
from typing import Iterable
from .tipnr import BOOK_MAP

OPENBIBLE_SOURCE='openbibleinfo/Bible-Geocoding-Data'
OSIS_BOOK_MAP={
'Gen':'GEN','Exod':'EXO','Lev':'LEV','Num':'NUM','Deut':'DEU','Josh':'JOS','Judg':'JDG','Ruth':'RUT','1Sam':'1SA','2Sam':'2SA','1Kgs':'1KI','2Kgs':'2KI','1Chr':'1CH','2Chr':'2CH','Ezra':'EZR','Neh':'NEH','Esth':'EST','Job':'JOB','Ps':'PSA','Prov':'PRO','Eccl':'ECC','Song':'SNG','Isa':'ISA','Jer':'JER','Lam':'LAM','Ezek':'EZK','Dan':'DAN','Hos':'HOS','Joel':'JOL','Amos':'AMO','Obad':'OBA','Jonah':'JON','Mic':'MIC','Nah':'NAM','Hab':'HAB','Zeph':'ZEP','Hag':'HAG','Zech':'ZEC','Mal':'MAL','Matt':'MAT','Mark':'MRK','Luke':'LUK','John':'JHN','Acts':'ACT','Rom':'ROM','1Cor':'1CO','2Cor':'2CO','Gal':'GAL','Eph':'EPH','Phil':'PHP','Col':'COL','1Thess':'1TH','2Thess':'2TH','1Tim':'1TI','2Tim':'2TI','Titus':'TIT','Phlm':'PHM','Heb':'HEB','Jas':'JAS','1Pet':'1PE','2Pet':'2PE','1John':'1JN','2John':'2JN','3John':'3JN','Jude':'JUD','Rev':'REV'}
OSIS_RE=re.compile(r'^([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)$')

@dataclass(frozen=True)
class ModernCandidate:
    modern_id:str
    description:str
    confidence:float
    lon:float|None
    lat:float|None
    geometry_type:str|None
    source_path_score:int|None

@dataclass(frozen=True)
class AncientPlace:
    source_id:str
    friendly_id:str
    url_slug:str
    types:tuple[str,...]
    canonical_refs:tuple[str,...]
    tipnr_source_id:str|None
    candidates:tuple[ModernCandidate,...]

def canonical_osis(osis:str)->str|None:
    m=OSIS_RE.match(osis)
    if not m:return None
    book=OSIS_BOOK_MAP.get(m.group(1))
    return f'bible.ref.{book}.{int(m.group(2))}.{int(m.group(3))}' if book else None

def _confidence(ident:dict,resolution:dict)->float:
    # OpenBible scores are 0..1000. Prefer the time-aware score where present,
    # otherwise the path/vote score. This remains source confidence, not truth.
    score=ident.get('score') or {}
    raw=score.get('time_total') if isinstance(score,dict) else None
    if raw is None:raw=resolution.get('best_path_score')
    try:return max(0.0,min(1.0,float(raw)/1000.0))
    except (TypeError,ValueError):return 0.0

def _candidate(ident:dict)->ModernCandidate|None:
    resolutions=ident.get('resolutions') or []
    if not resolutions:return None
    r=resolutions[0]
    lon=lat=None
    if r.get('lonlat'):
        try:lon,lat=(float(x) for x in str(r['lonlat']).split(',',1))
        except (TypeError,ValueError):lon=lat=None
    return ModernCandidate(
        modern_id=str(ident.get('id') or r.get('modern_basis_id') or ''),
        description=re.sub(r'<[^>]+>','',str(ident.get('description') or r.get('description') or '')).strip(),
        confidence=_confidence(ident,r),lon=lon,lat=lat,
        geometry_type=r.get('type'),source_path_score=r.get('best_path_score'))

def iter_ancient_places(text:str)->Iterable[AncientPlace]:
    for raw in text.splitlines():
        if not raw.strip():continue
        row=json.loads(raw)
        refs=tuple(dict.fromkeys(x for v in row.get('verses',[]) if (x:=canonical_osis(str(v.get('osis',''))))))
        linked=row.get('linked_data') or {}
        tipnr=None
        for value in linked.values():
            if isinstance(value,dict) and isinstance(value.get('id'),str) and '@' in value['id']:
                tipnr=value['id'];break
        candidates=tuple(c for ident in (row.get('identifications') or []) if (c:=_candidate(ident)))
        yield AncientPlace(str(row.get('id','')),str(row.get('friendly_id','')),str(row.get('url_slug','')),tuple(row.get('types') or ()),refs,tipnr,candidates)
