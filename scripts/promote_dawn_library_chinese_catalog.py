#!/usr/bin/env python3
import json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'static/dawn-library/biblical-world/chinese-resolver-results.json'
CAT=ROOT/'static/dawn-library/biblical-world/catalog.json'

def slug(s):
    s=unicodedata.normalize('NFKC',s).strip().lower()
    return 'zh-wikisource-'+re.sub(r'[^0-9a-z]+','-',s).strip('-')[:48]

def valid(x):
    r=x.get('rights',{})
    return x.get('stage')=='verified' and '/' not in x.get('title','') and r.get('status')=='public-domain' and r.get('provenanceRequired') is True

resolver=json.loads(RES.read_text())
catalog=json.loads(CAT.read_text())
existing={(i.get('sources') or [{}])[0].get('url') for i in catalog['items'] if i.get('sources')}
added=[]
for x in resolver.get('items',[]):
    if not valid(x) or x.get('sourceUrl') in existing: continue
    title=x['title']
    # Conservative curation guard: automated catalog is for durable works/editions, not modern policy documents or incidental prefaces.
    if any(k in title for k in ('路线图','路線圖','解决办法','解決辦法','冲突','衝突')) or title.endswith('序'):
        continue
    item={
      'id':slug(title),
      'work':{'title':title,'language':'zh'},
      'edition':{'label':x.get('edition',{}).get('canonicalTitle',title),'publicDomain':True},
      'rights':{'status':'public-domain','declaredBy':'中文維基文庫','provenanceRequired':True},
      'relations':['聖經世界','中文公版'],
      'cover':{'mode':'one-fallback','title':title,'author':''},
      'sources':[{'provider':'中文維基文庫','kind':'remote-public','url':x['sourceUrl'],'format':'html','downloadOnCatalog':False}]
    }
    catalog['items'].append(item); existing.add(x['sourceUrl']); added.append(title)
CAT.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'verifiedInput':sum(1 for x in resolver.get('items',[]) if x.get('stage')=='verified'),'promoted':len(added),'titles':added,'catalogTotal':len(catalog['items']),'contentDownloaded':False},ensure_ascii=False,indent=2))
