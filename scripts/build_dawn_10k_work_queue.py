#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from dawn_collection_scope import classify

ROOT = Path(__file__).resolve().parents[1]
GUTENBERG = ROOT / 'static/dawn-library/biblical-world/discovery-candidates.json'
OPENLIBRARY = ROOT / 'data/dawn-10k-openlibrary-works.json'
OUT = ROOT / 'data/dawn-10k-work-queue.json'


def norm(text: str) -> str:
    text = unicodedata.normalize('NFKC', text or '').casefold().strip()
    text = re.sub(r'[^\w\s-]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def signature(title: str, author: str) -> str:return f'{norm(title)}::{norm(author)}'
def add_unique(target: list, value) -> None:
    if value and value not in target:target.append(value)

def admitted(row:dict)->tuple[bool,str]:
    verdict=classify(row)
    return bool(verdict['admit']),str(verdict['scope'])


def main() -> int:
    gutenberg=json.loads(GUTENBERG.read_text()) if GUTENBERG.exists() else {'items':[]}
    openlibrary=json.loads(OPENLIBRARY.read_text()) if OPENLIBRARY.exists() else {'items':[]}
    previous={}
    if OUT.exists():
        previous_data=json.loads(OUT.read_text());previous={item['queueId']:item for item in previous_data.get('items',[])}
    grouped={};signature_to_key={};excluded=[]
    for work in openlibrary.get('items',[]):
        ok,scope=admitted(work)
        if not ok:
            excluded.append({'workId':work.get('workId'),'title':work.get('title'),'reason':'collection-scope'});continue
        work_id=str(work.get('workId') or '').strip();title=str(work.get('title') or '').strip();authors=[str(x).strip() for x in (work.get('authors') or []) if str(x).strip()]
        if not work_id or not title:continue
        primary_author=authors[0] if authors else '';key=f'openlibrary::{work_id}'
        entry={'queueId':f'work::{key}','workId':work_id,'title':title,'author':primary_author,'authors':authors,'languages':list(dict.fromkeys(work.get('languages') or [])),'providers':['Open Library'],'pointers':[p for p in (work.get('workPointer'),work.get('editionPointer')) if p],'relations':[],'authorityIds':dict(work.get('authorityIds') or {}),'preferredEdition':work.get('preferredEdition'),'coverId':work.get('coverId'),'firstPublishYear':work.get('firstPublishYear'),'status':'identity-established','checkpoint':1,'admission':'none','collectionScope':scope}
        grouped[key]=entry;sig=signature(title,primary_author)
        if sig!='::' and sig not in signature_to_key:signature_to_key[sig]=key
    for candidate in gutenberg.get('items',[]):
        ok,scope=admitted(candidate)
        if not ok:
            excluded.append({'workId':candidate.get('workId'),'title':candidate.get('title'),'reason':'collection-scope'});continue
        title=str(candidate.get('title') or '').strip();author=str(candidate.get('author') or '').strip();sig=signature(title,author)
        if not norm(title):continue
        key=signature_to_key.get(sig)
        if key is None:
            key=f'provisional::{sig}';grouped.setdefault(key,{'queueId':f'work::{key}','title':title,'author':author,'authors':[author] if author else [],'languages':[],'providers':[],'pointers':[],'relations':[],'authorityIds':{},'status':'pending-reconciliation','checkpoint':0,'admission':'none','collectionScope':scope})
        entry=grouped[key];add_unique(entry['providers'],candidate.get('provider'));add_unique(entry['pointers'],candidate.get('sourceUrl'))
        for relation in candidate.get('suggestedRelations',[]):add_unique(entry['relations'],relation)
    items=[]
    for key in sorted(grouped):
        item=grouped[key];old=previous.get(item['queueId'])
        if old:
            if item['checkpoint']==0:item['status']=old.get('status',item['status']);item['checkpoint']=old.get('checkpoint',item['checkpoint'])
            if 'notes' in old:item['notes']=old['notes']
        items.append(item)
    authority_backed=sum(1 for item in items if item.get('authorityIds',{}).get('openLibraryWork'));chinese=sum(1 for item in items if 'chi' in item.get('languages',[]) or item.get('matchedLanguage')=='chi');english=sum(1 for item in items if 'eng' in item.get('languages',[]) or item.get('matchedLanguage')=='eng')
    report={'schema':'dawn.library.10k-work-queue.v3','targetWorks':10000,'collectionPolicy':'Christian/Biblical public religious holdings; Jewish/Judaism materials admitted as research; other religions excluded at collection time.','sources':[str(GUTENBERG.relative_to(ROOT)),str(OPENLIBRARY.relative_to(ROOT))],'sourceCandidates':len(gutenberg.get('items',[]))+len(openlibrary.get('items',[])),'excludedByCollectionScope':len(excluded),'deduplicatedWorks':len(items),'authorityBackedWorks':authority_backed,'languageSignals':{'chi':chinese,'eng':english},'checkpointRule':'Authority-backed Work IDs are checkpoint 1; prior provisional progress survives rebuilds without downgrading established identities.','admission':'collection-scope gate precedes technical reconciliation','items':items}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'sourceCandidates':report['sourceCandidates'],'excludedByCollectionScope':len(excluded),'deduplicatedWorks':len(items),'authorityBackedWorks':authority_backed,'languageSignals':report['languageSignals']},ensure_ascii=False));return 0

if __name__=='__main__':raise SystemExit(main())
