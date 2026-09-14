#!/usr/bin/env python3
from dawn_resource_exclusions import excluded
import hashlib,json,re,unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'static/dawn-library/biblical-world/chinese-resolver-results.json'
CAT=ROOT/'static/dawn-library/biblical-world/catalog.json'
FORBIDDEN=('wikisource','wikisource.org','維基文庫','维基文库')
DISPUTE_MARKERS=('政治','戰爭','战争','衝突','冲突','侵略','民族主義','民族主义')

def stable_id(title,url):
    normalized=unicodedata.normalize('NFKC',title).strip().casefold()
    ascii_hint=re.sub(r'[^0-9a-z]+','-',normalized).strip('-')[:24]
    digest=hashlib.sha256((normalized+'\n'+url).encode('utf-8')).hexdigest()[:12]
    return 'zh-gutenberg-'+((ascii_hint+'-') if ascii_hint else '')+digest

def valid(x):
    r=x.get('rights',{})
    serialized=json.dumps(x,ensure_ascii=False).casefold()
    return (
        not excluded(x)
        and not any(t in serialized for t in FORBIDDEN)
        and not any(t in serialized for t in DISPUTE_MARKERS)
        and x.get('stage')=='verified'
        and x.get('provider','Project Gutenberg') in ('Project Gutenberg','')
        and r.get('status')=='public-domain'
        and r.get('declaredBy')=='Project Gutenberg'
        and r.get('provenanceRequired') is True
        and bool((x.get('edition') or {}).get('gutenbergId'))
        and (x.get('edition') or {}).get('language')=='zh'
    )

resolver=json.loads(RES.read_text())
catalog=json.loads(CAT.read_text())
# Permanent source boundary: purge any historical Wikisource-derived catalog records before promotion.
catalog['items']=[x for x in catalog.get('items',[]) if not excluded(x)]
existing_urls={(i.get('sources') or [{}])[0].get('url') for i in catalog['items'] if i.get('sources')}
existing_ids={i.get('id') for i in catalog['items']}
added=[]
for x in resolver.get('items',[]):
    if not valid(x) or x.get('sourceUrl') in existing_urls: continue
    title=x['title']; url=x['sourceUrl']; ident=stable_id(title,url)
    if ident in existing_ids: continue
    edition=x.get('edition') or {}
    item={
        'id':ident,
        'work':{'title':title,'language':'zh','author':x.get('author','')},
        'edition':{'label':edition.get('canonicalTitle',title),'gutenbergId':edition.get('gutenbergId'),'publicDomain':True},
        'rights':{'status':'public-domain','jurisdiction':'USA','declaredBy':'Project Gutenberg','provenanceRequired':True},
        'relations':['聖經世界','中文公版'],
        'cover':{'mode':'one-fallback','title':title,'author':x.get('author','')},
        'sources':[{'provider':'Project Gutenberg','kind':'remote-public','url':url,'format':'html','downloadOnCatalog':False}],
        'provenance':{'origin':'autonomous-discovery','languageLane':'zh','source':'project-gutenberg'}
    }
    catalog['items'].append(item); existing_urls.add(url); existing_ids.add(ident); added.append(title)

ids=[i.get('id') for i in catalog['items']]
assert all(ids) and len(ids)==len(set(ids)), 'catalog IDs must be non-empty and unique'
assert not any(any(t in json.dumps(i,ensure_ascii=False).casefold() for t in FORBIDDEN) for i in catalog['items']), 'Wikisource residue in canonical catalog'
CAT.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'verifiedInput':sum(1 for x in resolver.get('items',[]) if x.get('stage')=='verified'),'promoted':len(added),'titles':added,'catalogTotal':len(catalog['items']),'uniqueIds':len(set(ids)),'contentDownloaded':False,'source':'project-gutenberg'},ensure_ascii=False,indent=2))
