#!/usr/bin/env python3
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCES=ROOT/'static/dawn-library/sources.json'
QUERIES=ROOT/'static/dawn-library/biblical-world/discovery-queries.json'
CATALOG=ROOT/'static/dawn-library/biblical-world/catalog.json'
STATE=ROOT/'static/dawn-library/biblical-world/discovery-state.json'
CANDIDATES=ROOT/'static/dawn-library/biblical-world/discovery-candidates.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-DISCOVERY.json'

NS={'atom':'http://www.w3.org/2005/Atom'}
now=datetime.now(timezone.utc).isoformat()
sources=json.loads(SOURCES.read_text())
queries=json.loads(QUERIES.read_text())
catalog=json.loads(CATALOG.read_text())
state=json.loads(STATE.read_text())
previous={'schema':'dawn.library.discovery-candidates.v1','items':[]}
if CANDIDATES.exists():
    previous=json.loads(CANDIDATES.read_text())

source=next(s for s in sources['sources'] if s['id']=='project-gutenberg')
base=source['catalog']
existing_ids=set()
for b in catalog.get('items',[]):
    for s in b.get('sources',[]):
        m=re.search(r'/ebooks/(\d+)',s.get('url',''))
        if m:
            existing_ids.add(m.group(1))

candidate_by_id={str(x['sourceId']):x for x in previous.get('items',[]) if x.get('sourceId')}
run_discovered=0
errors=[]
for spec in queries.get('queries',[]):
    q=spec['q']
    url=base+'?'+urllib.parse.urlencode({'query':q})
    req=urllib.request.Request(url,headers={'User-Agent':'Dore-Dawn-Library/1.0 (+https://westsidewatch.github.io)'})
    try:
        with urllib.request.urlopen(req,timeout=25) as resp:
            root=ET.fromstring(resp.read())
    except Exception as exc:
        errors.append({'query':q,'error':type(exc).__name__})
        continue
    for entry in root.findall('atom:entry',NS):
        eid=(entry.findtext('atom:id',default='',namespaces=NS) or '').strip()
        title=(entry.findtext('atom:title',default='',namespaces=NS) or '').strip()
        author=''
        author_el=entry.find('atom:author/atom:name',NS)
        if author_el is not None and author_el.text:
            author=author_el.text.strip()
        m=re.search(r'(\d+)(?:/)?$',eid)
        if not m:
            for link in entry.findall('atom:link',NS):
                href=link.attrib.get('href','')
                mm=re.search(r'/ebooks/(\d+)',href)
                if mm:
                    m=mm
                    break
        if not m:
            continue
        gid=m.group(1)
        if gid in existing_ids or gid in candidate_by_id:
            continue
        candidate_by_id[gid]={
          'sourceId':gid,
          'provider':'Project Gutenberg',
          'title':title,
          'author':author,
          'sourceUrl':f'https://www.gutenberg.org/ebooks/{gid}',
          'matchedQuery':q,
          'suggestedRelations':spec.get('relations',[]),
          'stage':'discovered',
          'discoveredAt':now,
          'rights':{'status':'unverified','jurisdiction':'USA','declaredBy':'Project Gutenberg'},
          'contentDownloaded':False
        }
        run_discovered+=1

items=sorted(candidate_by_id.values(),key=lambda x:int(x['sourceId']))
CANDIDATES.write_text(json.dumps({'schema':'dawn.library.discovery-candidates.v1','generatedAt':now,'items':items},ensure_ascii=False,indent=2)+'\n')
state['sourceCursors']['project-gutenberg']['lastChecked']=now
state['metrics']['discovered']=len(catalog.get('items',[]))+len(items)
state['metrics']['candidateQueue']=len(items)
state['metrics']['newThisRun']=run_discovered
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True)
report={
 'schema':'dawn.library.discovery.report.v1',
 'generatedAt':now,
 'collection':'biblical-world-books',
 'source':'project-gutenberg',
 'queries':len(queries.get('queries',[])),
 'newDiscovered':run_discovered,
 'candidateQueue':len(items),
 'catalogBooks':len(catalog.get('items',[])),
 'errors':errors,
 'invariant':'Discovery only creates metadata candidates. It does not download full text or auto-promote candidates into the public catalog.'
}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
