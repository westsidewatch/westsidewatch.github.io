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
UA='Dore-Dawn-Library/1.1 (+https://westsidewatch.github.io; metadata-only)'
PAGES_PER_QUERY=2
now=datetime.now(timezone.utc).isoformat()
sources=json.loads(SOURCES.read_text())
queries=json.loads(QUERIES.read_text())
catalog=json.loads(CATALOG.read_text())
state=json.loads(STATE.read_text())
previous={'schema':'dawn.library.discovery-candidates.v1','items':[]}
if CANDIDATES.exists(): previous=json.loads(CANDIDATES.read_text())
source=next(s for s in sources['sources'] if s['id']=='project-gutenberg')
base=source['catalog']
existing_ids=set()
for b in catalog.get('items',[]):
    for s in b.get('sources',[]):
        m=re.search(r'/ebooks/(\d+)',s.get('url',''))
        if m: existing_ids.add(m.group(1))
# Promoted books leave the candidate queue; this prevents a dead queue from masking real growth.
candidate_by_id={str(x['sourceId']):x for x in previous.get('items',[]) if x.get('sourceId') and str(x['sourceId']) not in existing_ids}
cursor_state=state.setdefault('sourceCursors',{}).setdefault('project-gutenberg',{'mode':'opds'})
query_cursors=cursor_state.setdefault('queryCursors',{})
run_discovered=0;errors=[];pages_checked=0

def next_url(root,current):
    for link in root.findall('atom:link',NS):
        if link.attrib.get('rel')=='next' and link.attrib.get('href'):
            return urllib.parse.urljoin(current,link.attrib['href'])
    return None

def absorb(root,spec):
    global run_discovered
    q=spec['q']
    for entry in root.findall('atom:entry',NS):
        eid=(entry.findtext('atom:id',default='',namespaces=NS) or '').strip(); title=(entry.findtext('atom:title',default='',namespaces=NS) or '').strip(); author=''
        ae=entry.find('atom:author/atom:name',NS)
        if ae is not None and ae.text: author=ae.text.strip()
        m=re.search(r'(\d+)(?:/)?$',eid)
        if not m:
            for link in entry.findall('atom:link',NS):
                mm=re.search(r'/ebooks/(\d+)',link.attrib.get('href',''))
                if mm: m=mm;break
        if not m: continue
        gid=m.group(1)
        if gid in existing_ids or gid in candidate_by_id: continue
        candidate_by_id[gid]={'sourceId':gid,'provider':'Project Gutenberg','title':title,'author':author,'sourceUrl':f'https://www.gutenberg.org/ebooks/{gid}','matchedQuery':q,'suggestedRelations':spec.get('relations',[]),'stage':'discovered','discoveredAt':now,'rights':{'status':'unverified','jurisdiction':'USA','declaredBy':'Project Gutenberg'},'contentDownloaded':False}
        run_discovered+=1

for spec in queries.get('queries',[]):
    q=spec['q']; initial=base+'?'+urllib.parse.urlencode({'query':q}); url=query_cursors.get(q) or initial; last_next=None
    for _ in range(PAGES_PER_QUERY):
        req=urllib.request.Request(url,headers={'User-Agent':UA})
        try:
            with urllib.request.urlopen(req,timeout=25) as resp: root=ET.fromstring(resp.read())
            pages_checked+=1; absorb(root,spec); last_next=next_url(root,url)
            if not last_next: break
            url=last_next
        except Exception as exc:
            errors.append({'query':q,'url':url,'error':type(exc).__name__}); last_next=url; break
    # Continue where this run stopped. Exhausted queries restart only after the full result set has been walked.
    query_cursors[q]=last_next or initial

items=sorted(candidate_by_id.values(),key=lambda x:int(x['sourceId']))
CANDIDATES.write_text(json.dumps({'schema':'dawn.library.discovery-candidates.v1','generatedAt':now,'items':items},ensure_ascii=False,indent=2)+'\n')
cursor_state['lastChecked']=now;cursor_state['cursor']='per-query-opds-next'
state['metrics']['discovered']=len(catalog.get('items',[]))+len(items);state['metrics']['candidateQueue']=len(items);state['metrics']['newThisRun']=run_discovered;state['metrics']['pagesCheckedThisRun']=pages_checked
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True)
report={'schema':'dawn.library.discovery.report.v2','generatedAt':now,'collection':'biblical-world-books','source':'project-gutenberg','queries':len(queries.get('queries',[])),'pagesChecked':pages_checked,'newDiscovered':run_discovered,'candidateQueue':len(items),'catalogBooks':len(catalog.get('items',[])),'errors':errors,'invariant':'Discovery advances through OPDS result pages, persists per-query cursors, stores metadata only, and removes promoted source IDs from the candidate queue.'}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
