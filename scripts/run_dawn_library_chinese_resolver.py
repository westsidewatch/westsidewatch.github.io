#!/usr/bin/env python3
import json,re,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REL=ROOT/'static/dawn-library/biblical-world/chinese-relevance-results.json'
OUT=ROOT/'static/dawn-library/biblical-world/chinese-resolver-results.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-CHINESE-RESOLVER.json'
UA='Dore-Dawn-Library/1.1 (Chinese metadata and rights resolver; no bulk text)'
FORBIDDEN=('wikisource','wikisource.org','維基文庫','维基文库')
now=datetime.now(timezone.utc).isoformat()

def local(el): return el.tag.rsplit('}',1)[-1]
def text(el): return (el.text or '').strip() if el is not None else ''
def rdf_for(gid):
    url=f'https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.rdf'
    req=urllib.request.Request(url,headers={'User-Agent':UA})
    with urllib.request.urlopen(req,timeout=30) as r: root=ET.fromstring(r.read())
    vals={}; creators=[]; languages=[]
    for el in root.iter():
        name=local(el)
        val=text(el)
        if name in ('title','rights') and val and name not in vals: vals[name]=val
        if name in ('language','value') and val: languages.append(val.casefold())
        if name=='name' and val: creators.append(val)
    vals['creators']=creators; vals['languages']=languages; vals['rdfUrl']=url
    return vals

def is_chinese(meta):
    vals=meta.get('languages',[])
    return any(v in ('zh','zho','chi','chinese') or v.startswith('zh-') or 'chinese' in v for v in vals)

items=[]; counts={'verified':0,'needs-review':0,'blocked':0}
for x in json.loads(REL.read_text()).get('items',[]):
    if x.get('stage')!='qualified': continue
    serialized=json.dumps(x,ensure_ascii=False).casefold()
    result={'sourceId':x.get('sourceId'),'title':x.get('title',''),'author':x.get('author',''),'sourceUrl':x.get('sourceUrl'),'stage':'needs-review','contentDownloaded':False,'resolvedAt':now}
    m=re.search(r'/ebooks/(\d+)',x.get('sourceUrl',''))
    if any(t in serialized for t in FORBIDDEN) or x.get('provider')!='Project Gutenberg' or not m:
        result['stage']='blocked'; result['reason']='forbidden-or-unsupported-provider'; counts['blocked']+=1; items.append(result); continue
    gid=m.group(1)
    try:
        meta=rdf_for(gid); rights=meta.get('rights','')
        explicit_pd='public domain' in rights.casefold() and ('usa' in rights.casefold() or 'united states' in rights.casefold())
        chinese=is_chinese(meta)
        result['edition']={'gutenbergId':gid,'canonicalTitle':meta.get('title') or x.get('title',''),'language':'zh' if chinese else None,'creatorNames':meta.get('creators',[]),'metadataUrl':meta['rdfUrl']}
        result['rights']={'status':'public-domain' if explicit_pd else 'unverified','jurisdiction':'USA','declaredBy':'Project Gutenberg','evidence':rights,'provenanceRequired':True}
        if explicit_pd and chinese:
            result['stage']='verified'; result['reason']='gutenberg-rdf-explicit-public-domain-and-chinese-language'; counts['verified']+=1
        else:
            result['reason']='rights-or-language-needs-review'; counts['needs-review']+=1
    except Exception as e:
        result['reason']='resolver-error'; result['error']=f'{type(e).__name__}: {e}'; counts['needs-review']+=1
    items.append(result)

OUT.write_text(json.dumps({'schema':'dawn.library.chinese-resolver-results.v2','generatedAt':now,'items':items},ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True)
report={'schema':'dawn.library.chinese-resolver.report.v2','generatedAt':now,'qualifiedInput':len(items),'results':counts,'verifiedTitles':[x['title'] for x in items if x['stage']=='verified'],'sourcePolicy':{'wikisource':'forbidden'},'invariant':'Verification reads Project Gutenberg RDF metadata, explicit US public-domain rights, and explicit Chinese language metadata only; no book full text is stored.'}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
