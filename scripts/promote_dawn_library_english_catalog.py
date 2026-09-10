#!/usr/bin/env python3
import json,re
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'static/dawn-library/biblical-world/english-resolver-results.json'
CAT=ROOT/'static/dawn-library/biblical-world/catalog.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-ENGLISH-PROMOTION.json'
now=datetime.now(timezone.utc).isoformat()
resolver=json.loads(RES.read_text())
catalog=json.loads(CAT.read_text())
existing_urls={s.get('url') for i in catalog.get('items',[]) for s in i.get('sources',[]) if s.get('url')}
existing_ids={i.get('id') for i in catalog.get('items',[])}
added=[]
for x in resolver.get('items',[]):
    if x.get('stage')!='verified' or x.get('rights',{}).get('status')!='public-domain': continue
    url=x.get('sourceUrl','')
    if not url or url in existing_urls: continue
    gid=str(x.get('edition',{}).get('gutenbergId') or x.get('sourceId') or '').strip()
    if not gid.isdigit(): continue
    ident=f'gutenberg-{gid}'
    if ident in existing_ids: continue
    title=x.get('edition',{}).get('canonicalTitle') or x.get('title') or f'Project Gutenberg {gid}'
    creators=x.get('edition',{}).get('creatorNames') or []
    author=x.get('author') or (creators[0] if creators else '')
    item={
      'id':ident,
      'work':{'title':title,'author':author,'language':'en'},
      'edition':{'label':f'Project Gutenberg #{gid}','publicDomain':True},
      'rights':{'status':'public-domain','jurisdiction':'USA','declaredBy':'Project Gutenberg','provenanceRequired':True,'evidenceUrl':x.get('edition',{}).get('metadataUrl')},
      'relations':x.get('suggestedRelations') or ['聖經世界'],
      'cover':{'mode':'one-fallback','title':title.upper(),'author':author.upper()},
      'sources':[{'provider':'Project Gutenberg','kind':'remote-public','url':url,'format':'html/epub/text','downloadOnCatalog':False}],
      'provenance':{'origin':'autonomous-discovery','discoveredAt':x.get('discoveredAt'),'verifiedAt':x.get('resolvedAt'),'catalogedAt':now}
    }
    catalog['items'].append(item);existing_urls.add(url);existing_ids.add(ident);added.append({'id':ident,'title':title})
CAT.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True)
report={'schema':'dawn.library.english-promotion.report.v1','generatedAt':now,'promoted':len(added),'items':added,'catalogTotal':len(catalog['items']),'origin':'autonomous-discovery','contentDownloaded':False}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
