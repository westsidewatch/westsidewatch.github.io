#!/usr/bin/env python3
from resource_selection import book_allowed, book_decision, excluded
import hashlib,json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'dore-core/review/resource-selection/chinese-resolver-results.json'
CAT=ROOT/'static/dawn-library/biblical-world/catalog.json'

def stable_id(title,url):
    normalized=unicodedata.normalize('NFKC',title).strip().casefold()
    ascii_hint=re.sub(r'[^0-9a-z]+','-',normalized).strip('-')[:24]
    digest=hashlib.sha256((normalized+'\n'+url).encode('utf-8')).hexdigest()[:12]
    return 'zh-wikisource-'+((ascii_hint+'-') if ascii_hint else '')+digest

def valid(x):
    r=x.get('rights',{})
    return not excluded(x) and x.get('stage')=='verified' and '/' not in x.get('title','') and r.get('status')=='public-domain' and r.get('provenanceRequired') is True

resolver=json.loads(RES.read_text())
catalog=json.loads(CAT.read_text())
catalog['items']=[i for i in catalog.get('items',[]) if book_allowed(i)]
catalog['items']=[x for x in catalog['items'] if not excluded(x)]
# Repair IDs created by the first promoter version while preserving all existing non-Chinese IDs.
for item in catalog.get('items',[]):
    if item.get('work',{}).get('language')=='zh':
        src=(item.get('sources') or [{}])[0]
        if src.get('provider')=='中文維基文庫' and src.get('url'):
            item['id']=stable_id(item.get('work',{}).get('title',''),src['url'])
existing_urls={(i.get('sources') or [{}])[0].get('url') for i in catalog['items'] if i.get('sources')}
existing_ids={i.get('id') for i in catalog['items']}
added=[]
for x in resolver.get('items',[]):
    if not valid(x) or x.get('sourceUrl') in existing_urls: continue
    title=x['title']; url=x['sourceUrl']
    if any(k in title for k in ('路线图','路線圖','解决办法','解決辦法','冲突','衝突')) or title.endswith('序'): continue
    ident=stable_id(title,url)
    if ident in existing_ids: continue
    item={'id':ident,'work':{'title':title,'language':'zh'},'edition':{'label':x.get('edition',{}).get('canonicalTitle',title),'publicDomain':True},'rights':{'status':'public-domain','declaredBy':'中文維基文庫','provenanceRequired':True},'relations':['聖經世界','中文公版'],'cover':{'mode':'one-fallback','title':title,'author':''},'sources':[{'provider':'中文維基文庫','kind':'remote-public','url':url,'format':'html','downloadOnCatalog':False}]}

    if not book_allowed(item):continue
    item['admission']=book_decision(item)
    catalog['items'].append(item); existing_urls.add(url); existing_ids.add(ident); added.append(title)
ids=[i.get('id') for i in catalog['items']]
assert all(ids) and len(ids)==len(set(ids)), 'catalog IDs must be non-empty and unique'
CAT.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'verifiedInput':sum(1 for x in resolver.get('items',[]) if x.get('stage')=='verified'),'promoted':len(added),'titles':added,'catalogTotal':len(catalog['items']),'uniqueIds':len(set(ids)),'contentDownloaded':False},ensure_ascii=False,indent=2))
