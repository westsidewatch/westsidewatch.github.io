#!/usr/bin/env python3
import json,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SEEDS=ROOT/'static/dawn-library/biblical-world/chinese-seeds.json'
OUT=ROOT/'static/dawn-library/biblical-world/chinese-candidates.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-CHINESE-DISCOVERY.json'
API='https://zh.wikisource.org/w/api.php'
now=datetime.now(timezone.utc).isoformat(); cfg=json.loads(SEEDS.read_text())
items={}
def api(params):
    params.update({'format':'json','formatversion':'2','utf8':'1'})
    req=urllib.request.Request(API+'?'+urllib.parse.urlencode(params),headers={'User-Agent':'Dore-Dawn-Library/1.0 (+https://westsidewatch.github.io)'})
    with urllib.request.urlopen(req,timeout=25) as r:return json.loads(r.read())
def add(title,pageid,origin,relations=None,priority='discovered'):
    if not pageid:return
    items[str(pageid)]={'sourceId':str(pageid),'provider':'中文維基文庫','language':'zh','title':title,'canonicalTitle':title,'sourceUrl':'https://zh.wikisource.org/wiki/'+urllib.parse.quote(title.replace(' ','_')),'matchedBy':origin,'suggestedRelations':relations or [],'priority':priority,'stage':'discovered','discoveredAt':now,'rights':{'status':'unverified','declaredBy':'中文維基文庫','provenanceRequired':True},'contentDownloaded':False}
errors=[]
for seed in cfg['seeds']:
    try:
        d=api({'action':'query','titles':seed['title'],'prop':'info'})
        for p in d.get('query',{}).get('pages',[]):
            if not p.get('missing'):add(p.get('title',seed['title']),p.get('pageid'),'seed:'+seed['title'],seed.get('relations'),seed.get('priority','golden'))
    except Exception as e:errors.append({'seed':seed['title'],'error':type(e).__name__})
for q in cfg['searchQueries']:
    try:
        d=api({'action':'query','list':'search','srsearch':q,'srnamespace':'0','srlimit':'20'})
        for p in d.get('query',{}).get('search',[]):add(p.get('title',''),p.get('pageid'),'search:'+q)
    except Exception as e:errors.append({'query':q,'error':type(e).__name__})
vals=sorted(items.values(),key=lambda x:int(x['sourceId']))
OUT.write_text(json.dumps({'schema':'dawn.library.chinese-candidates.v1','generatedAt':now,'items':vals},ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True)
report={'schema':'dawn.library.chinese-discovery.report.v1','generatedAt':now,'source':'zh-wikisource','language':'zh','goldenSeeds':len(cfg['seeds']),'candidateQueue':len(vals),'errors':errors,'invariant':'Metadata only; no bulk full-text ingestion.'}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
