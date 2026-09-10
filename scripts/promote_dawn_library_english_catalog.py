#!/usr/bin/env python3
import json,re
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'static/dawn-library/biblical-world/english-resolver-results.json'
CAT=ROOT/'static/dawn-library/biblical-world/catalog.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-ENGLISH-PROMOTION.json'
now=datetime.now(timezone.utc).isoformat()
resolver=json.loads(RES.read_text());catalog=json.loads(CAT.read_text())

def quality_ok(title):
    t=' '.join((title or '').lower().split())
    if not t:return False
    if 'project gutenberg works' in t and 'index' in t:return False
    if 'augustine' in t and 'florida' in t:return False
    if re.search(r'\b(index|catalogue|catalog)\b$',t):return False
    return True

# Autonomous entries remain subject to the same quality gate on every run; bad loop output is self-correcting.
kept=[];removed=[]
for item in catalog.get('items',[]):
    if item.get('provenance',{}).get('origin')=='autonomous-discovery' and not quality_ok(item.get('work',{}).get('title','')):
        removed.append({'id':item.get('id'),'title':item.get('work',{}).get('title')});continue
    kept.append(item)
catalog['items']=kept
existing_urls={s.get('url') for i in catalog.get('items',[]) for s in i.get('sources',[]) if s.get('url')};existing_ids={i.get('id') for i in catalog.get('items',[])}
added=[];rejected=[]
for x in resolver.get('items',[]):
    if x.get('stage')!='verified' or x.get('rights',{}).get('status')!='public-domain':continue
    url=x.get('sourceUrl','');gid=str(x.get('edition',{}).get('gutenbergId') or x.get('sourceId') or '').strip();title=x.get('edition',{}).get('canonicalTitle') or x.get('title') or f'Project Gutenberg {gid}'
    if not quality_ok(title):rejected.append({'sourceId':gid,'title':title,'reason':'quality-gate'});continue
    if not url or url in existing_urls or not gid.isdigit():continue
    ident=f'gutenberg-{gid}'
    if ident in existing_ids:continue
    creators=x.get('edition',{}).get('creatorNames') or [];author=x.get('author') or (creators[0] if creators else '')
    item={'id':ident,'work':{'title':title,'author':author,'language':'en'},'edition':{'label':f'Project Gutenberg #{gid}','publicDomain':True},'rights':{'status':'public-domain','jurisdiction':'USA','declaredBy':'Project Gutenberg','provenanceRequired':True,'evidenceUrl':x.get('edition',{}).get('metadataUrl')},'relations':x.get('suggestedRelations') or ['聖經世界'],'cover':{'mode':'one-fallback','title':title.upper(),'author':author.upper()},'sources':[{'provider':'Project Gutenberg','kind':'remote-public','url':url,'format':'html/epub/text','downloadOnCatalog':False}],'provenance':{'origin':'autonomous-discovery','discoveredAt':x.get('discoveredAt'),'verifiedAt':x.get('resolvedAt'),'catalogedAt':now}}
    catalog['items'].append(item);existing_urls.add(url);existing_ids.add(ident);added.append({'id':ident,'title':title})
CAT.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n');REPORT.parent.mkdir(parents=True,exist_ok=True)
report={'schema':'dawn.library.english-promotion.report.v2','generatedAt':now,'promoted':len(added),'items':added,'removedFalsePositives':removed,'rejectedByQualityGate':rejected,'catalogTotal':len(catalog['items']),'origin':'autonomous-discovery','contentDownloaded':False}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
