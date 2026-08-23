"""Reader for STEPBible TIPNR proper-name records.

Only source-explicit identity/name/reference fields are admitted. Upstream @Brief,
@Short and @Article prose and file-format documentation are deliberately ignored.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib,re
from typing import Iterable
from .model import Alias,Attestation,WorldEntity

TIPNR_SOURCE='STEPBible/TIPNR'
BOOK_MAP={
'Gen':'GEN','Exo':'EXO','Lev':'LEV','Num':'NUM','Deu':'DEU','Jos':'JOS','Jdg':'JDG','Rut':'RUT','1Sa':'1SA','2Sa':'2SA','1Ki':'1KI','2Ki':'2KI','1Ch':'1CH','2Ch':'2CH','Ezr':'EZR','Neh':'NEH','Est':'EST','Job':'JOB','Psa':'PSA','Pro':'PRO','Ecc':'ECC','Sng':'SNG','Isa':'ISA','Jer':'JER','Lam':'LAM','Ezk':'EZK','Dan':'DAN','Hos':'HOS','Jol':'JOL','Amo':'AMO','Oba':'OBA','Jon':'JON','Mic':'MIC','Nah':'NAM','Hab':'HAB','Zep':'ZEP','Hag':'HAG','Zec':'ZEC','Mal':'MAL','Mat':'MAT','Mrk':'MRK','Luk':'LUK','Jhn':'JHN','Act':'ACT','Rom':'ROM','1Co':'1CO','2Co':'2CO','Gal':'GAL','Eph':'EPH','Php':'PHP','Col':'COL','1Th':'1TH','2Th':'2TH','1Ti':'1TI','2Ti':'2TI','Tit':'TIT','Phm':'PHM','Heb':'HEB','Jas':'JAS','1Pe':'1PE','2Pe':'2PE','1Jn':'1JN','2Jn':'2JN','3Jn':'3JN','Jud':'JUD','Rev':'REV'}
REF_RE=re.compile(r'\b([1-3]?[A-Z][a-z]{1,2})\.(\d+)\.(\d+)[a-z]?\b')

@dataclass(frozen=True)
class TIPNRRecord:
    category:str
    source_unique_name:str
    label:str
    source_strong:str|None
    aliases:tuple[Alias,...]
    canonical_refs:tuple[str,...]

def canonical_ref(raw:str)->str|None:
    m=REF_RE.search(raw)
    if not m or m.group(1) not in BOOK_MAP:return None
    return f'bible.ref.{BOOK_MAP[m.group(1)]}.{int(m.group(2))}.{int(m.group(3))}'
def refs_from_text(text:str)->tuple[str,...]:
    refs=[]
    for m in REF_RE.finditer(text):
        book=BOOK_MAP.get(m.group(1))
        if book:refs.append(f'bible.ref.{book}.{int(m.group(2))}.{int(m.group(3))}')
    return tuple(dict.fromkeys(refs))
def stable_id(category:str,source_unique_name:str)->str:
    digest=hashlib.sha1(f'{category}|{source_unique_name}'.encode()).hexdigest()[:12]
    prefix='person' if category=='PERSON' else 'place' if category=='PLACE' else 'entity'
    return f'bible.{prefix}.tipnr.{digest}'
def _label(unique:str)->str:return unique.split('@',1)[0].replace('_',' ').replace('|',' / ').strip()
def _alias_from_form(form_field:str,translated:str)->list[Alias]:
    out=[]
    for value in re.findall(r'=([^+;,]+)',form_field):
        value=value.strip()
        if value and len(value)<100:
            lang='he' if re.search(r'[\u0590-\u05ff]',value) else 'grc' if re.search(r'[\u0370-\u03ff\u1f00-\u1fff]',value) else 'und'
            out.append(Alias(value=value,language=lang,source_id=TIPNR_SOURCE,kind='source_form'))
    for part in (translated or '').split(';'):
        value=part.split('=',1)[0].replace('/',' ').strip().strip('()')
        value=re.sub(r'\s+',' ',value)
        if value and len(value)<100 and value.lower() not in {'his','her','their'}:
            out.append(Alias(value=value,language='en',source_id=TIPNR_SOURCE,kind='translation_form'))
    return out

def _is_format_metadata(first:str)->bool:
    """Reject TIPNR file documentation/examples that contain '@' like records."""
    s=first.strip()
    if not s:return True
    if s.startswith(('*','^','@','#','\\')):return True
    if any(x in s for x in ('UnifiedName═','UniqueName is ','Parents - the UniqueNames','@Briefest','@ShortDef','\\t','\\r\\n')):return True
    return False

def iter_tipnr_records(text:str)->Iterable[TIPNRRecord]:
    category=None;current=None;aliases=[];refs=[]
    def flush():
        nonlocal current,aliases,refs
        if current is None:return None
        unique,strong=current;label=_label(unique)
        if not label or _is_format_metadata(unique):
            current=None;aliases=[];refs=[]
            return None
        all_aliases=[Alias(label,'en',TIPNR_SOURCE,'preferred_source_label'),*aliases]
        dedup=[];seen=set()
        for a in all_aliases:
            if not a.value.strip():continue
            key=(a.value,a.language,a.kind)
            if key not in seen:seen.add(key);dedup.append(a)
        rec=TIPNRRecord(category,unique,label,strong,tuple(dedup),tuple(dict.fromkeys(refs)))
        current=None;aliases=[];refs=[]
        return rec
    for raw in text.splitlines():
        line=raw.rstrip('\r')
        if line.startswith('$=========='):
            old=flush()
            if old:yield old
            marker=line.upper();category='PERSON' if 'PERSON' in marker else 'PLACE' if 'PLACE' in marker else 'OTHER' if 'OTHER' in marker else None
            continue
        if not category or not line.strip():continue
        if line.startswith('@'):continue
        if line.startswith('–') or line.startswith('-'):
            if current is None:continue
            cols=line.split('\t')
            if len(cols)>=6:
                aliases.extend(_alias_from_form(cols[2].strip(),cols[3].strip()));refs.extend(refs_from_text(cols[5]))
            continue
        if line.startswith('‖') or line.startswith('=') or line.startswith('UnifiedName') or line.startswith('Header '):continue
        first=line.split('\t')[0].strip()
        if _is_format_metadata(first):continue
        if '@' in first and first.split('@',1)[0].strip():
            old=flush()
            if old:yield old
            if '=' in first:unique,strong=first.rsplit('=',1)
            else:unique,strong=first,None
            current=(unique.strip(),strong.strip() if strong else None)
            first_ref=canonical_ref(unique)
            if first_ref:refs.append(first_ref)
    old=flush()
    if old:yield old

def to_world_entity(record:TIPNRRecord,snapshot:str)->WorldEntity:
    entity_type='person' if record.category=='PERSON' else 'place' if record.category=='PLACE' else 'artifact_or_object'
    attestations=tuple(Attestation(TIPNR_SOURCE,ref,'SCRIPTURE_EXPLICIT',1.0,'TIPNR proper-name attestation') for ref in record.canonical_refs)
    if not attestations:attestations=(Attestation(TIPNR_SOURCE,record.source_unique_name,'EDITORIAL_NORMALIZATION',1.0,'TIPNR individualised identity record'),)
    return WorldEntity(stable_id(record.category,record.source_unique_name),entity_type,record.label,record.aliases,attestations)
