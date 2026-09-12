#!/usr/bin/env python3
import json,re,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REL=ROOT/'static/dawn-library/biblical-world/relevance-results.json'
OUT=ROOT/'static/dawn-library/biblical-world/english-resolver-results.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-ENGLISH-RESOLVER.json'
UA='Dore-Dawn-Library/1.0 (metadata and rights resolver; no bulk text)'
now=datetime.now(timezone.utc).isoformat()

def local(el): return el.tag.rsplit('}',1)[-1]
def text(el): return (el.text or '').strip() if el is not None else ''
def rdf_for(gid):
    url=f'https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.rdf'
    req=urllib.request.Request(url,headers={'User-Agent':UA})
    with urllib.request.urlopen(req,timeout=30) as r: root=ET.fromstring(r.read())
    vals={}
    creators=[]
    for el in root.iter():
        name=local(el)
        if name in ('title','language','rights') and text(el) and name not in vals: vals[name]=text(el)
        if name=='name' and text(el): creators.append(text(el))
    vals['creators']=creators
    vals['rdfUrl']=url
    return vals

items=[]; counts={'verified':0,'needs-review':0,'blocked':0}
for x in json.loads(REL.read_text()).get('items',[]):
    if x.get('stage')!='qualified': continue
    m=re.search(r'/ebooks/(\d+)',x.get('sourceUrl',''))
    result={'sourceId':x.get('sourceId'),'title':x.get('title',''),'author':x.get('author',''),'sourceUrl':x.get('sourceUrl'),'suggestedRelations':x.get('suggestedRelations',[]),'discoveredAt':x.get('discoveredAt'),'stage':'needs-review','contentDownloaded':False,'resolvedAt':now}
    if x.get('provider')!='Project Gutenberg' or not m:
        result['stage']='blocked';result['reason']='unsupported-provider-or-source';counts['blocked']+=1;items.append(result);continue
    gid=m.group(1)
    try:
        meta=rdf_for(gid); rights=meta.get('rights','')
        is_pd='public domain' in rights.lower() and ('usa' in rights.lower() or 'united states' in rights.lower())
        result['edition']={'gutenbergId':gid,'canonicalTitle':meta.get('title') or x.get('title',''),'language':meta.get('language',''),'creatorNames':meta.get('creators',[]),'metadataUrl':meta['rdfUrl']}
        result['rights']={'status':'public-domain' if is_pd else 'unverified','jurisdiction':'USA','declaredBy':'Project Gutenberg','evidence':rights,'provenanceRequired':True}
        if is_pd:
            result['stage']='verified';result['reason']='gutenberg-rdf-explicit-public-domain';counts['verified']+=1
        else:
            result['reason']='rdf-rights-not-explicit-public-domain';counts['needs-review']+=1
    except Exception as e:
        result['reason']='resolver-error';result['error']=f'{type(e).__name__}: {e}';counts['needs-review']+=1
    items.append(result)
OUT.write_text(json.dumps({'schema':'dawn.library.english-resolver-results.v1','generatedAt':now,'items':items},ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True)
report={'schema':'dawn.library.english-resolver.report.v1','generatedAt':now,'qualifiedInput':len(items),'results':counts,'verifiedTitles':[x['title'] for x in items if x['stage']=='verified'],'invariant':'Verification reads Gutenberg RDF metadata and explicit rights only; no book full text is stored.'}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
