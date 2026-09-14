#!/usr/bin/env python3
from dawn_resource_exclusions import excluded
import json,re,unicodedata,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCES=ROOT/'static/dawn-library/sources.json'
SEEDS=ROOT/'static/dawn-library/biblical-world/chinese-seeds.json'
OUT=ROOT/'static/dawn-library/biblical-world/chinese-candidates.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-CHINESE-DISCOVERY.json'
NS={'atom':'http://www.w3.org/2005/Atom'}
UA='Dore-Dawn-Library/1.2 (+https://westsidewatch.github.io; Chinese metadata-only)'
FORBIDDEN_SOURCE=('wikisource','wikisource.org','維基文庫','维基文库')
DISPUTE_MARKERS=('政治','戰爭','战争','衝突','冲突','侵略','民族主義','民族主义')
CHINESE_CODES={'zh','zho','chi','chinese'}
PAGES_PER_QUERY=2
now=datetime.now(timezone.utc).isoformat()

def norm(value): return unicodedata.normalize('NFKC',str(value or '')).casefold().replace(' ','')

cfg=json.loads(SEEDS.read_text())
sources=json.loads(SOURCES.read_text())
source=next(s for s in sources['sources'] if s['id']=='project-gutenberg')
base=source['catalog']
if any(token in json.dumps(source,ensure_ascii=False).casefold() for token in FORBIDDEN_SOURCE):
    raise SystemExit('forbidden source configured for Chinese discovery')
if 'zh' not in {str(x).casefold() for x in source.get('languages',[])}:
    raise SystemExit('Project Gutenberg is not enabled for Chinese discovery')

items={}; errors=[]; pages_checked=0; run_discovered=0

def local(tag): return tag.rsplit('}',1)[-1].casefold()
def next_url(root,current):
    for link in root.findall('atom:link',NS):
        if link.attrib.get('rel')=='next' and link.attrib.get('href'):
            return urllib.parse.urljoin(current,link.attrib['href'])
    return None

def languages(entry):
    vals=[]
    for el in entry.iter():
        if local(el.tag) in ('language','rfc4646'):
            if el.text and el.text.strip(): vals.append(el.text.strip().casefold())
            for value in el.attrib.values():
                if value: vals.append(str(value).strip().casefold())
    return set(vals)

def is_chinese(entry):
    vals=languages(entry)
    return any(v in CHINESE_CODES or v.startswith('zh-') or 'chinese' in v for v in vals)

def forbidden_candidate(value):
    text=json.dumps(value,ensure_ascii=False).casefold()
    return excluded(value) or any(t in text for t in FORBIDDEN_SOURCE) or any(t in text for t in DISPUTE_MARKERS)

def candidate(gid,title,author='',matched_by='',relations=None,priority='discovered'):
    return {
        'sourceId':str(gid),'provider':'Project Gutenberg','language':'zh','title':title,'author':author,
        'canonicalTitle':title,'sourceUrl':f'https://www.gutenberg.org/ebooks/{gid}',
        'matchedBy':matched_by,'suggestedRelations':relations or [],'priority':priority,
        'stage':'discovered','discoveredAt':now,
        'rights':{'status':'unverified','jurisdiction':'USA','declaredBy':'Project Gutenberg','provenanceRequired':True},
        'contentDownloaded':False,
    }

def add(value):
    global run_discovered
    if forbidden_candidate(value): return False
    gid=str(value.get('sourceId') or '')
    if not gid.isdigit() or gid in items: return False
    items[gid]=value; run_discovered+=1; return True

def absorb(root,query,relations,priority):
    for entry in root.findall('atom:entry',NS):
        if not is_chinese(entry): continue
        eid=(entry.findtext('atom:id',default='',namespaces=NS) or '').strip()
        title=(entry.findtext('atom:title',default='',namespaces=NS) or '').strip()
        author=''
        ae=entry.find('atom:author/atom:name',NS)
        if ae is not None and ae.text: author=ae.text.strip()
        m=re.search(r'(\d+)(?:/)?$',eid)
        if not m:
            for link in entry.findall('atom:link',NS):
                mm=re.search(r'/ebooks/(\d+)',link.attrib.get('href',''))
                if mm: m=mm; break
        if not m or not title: continue
        effective_priority=priority if priority=='golden' and norm(title)==norm(query) else 'discovered'
        add(candidate(m.group(1),title,author,'gutenberg-search:'+query,relations,effective_priority))

# Known Gutenberg IDs establish source identity only. They do not establish rights:
# every candidate must still pass relevance and the independent RDF language/rights resolver.
for seed in cfg.get('seeds',[]):
    gid=str(seed.get('gutenbergId') or '').strip()
    if gid:
        add(candidate(gid,seed['title'],seed.get('author',''),'seed:gutenberg-id:'+gid,seed.get('relations',[]),seed.get('priority','golden')))

queries=[]
for seed in cfg.get('seeds',[]):
    queries.append((seed['title'],seed.get('relations',[]),seed.get('priority','golden')))
for q in cfg.get('searchQueries',[]):
    queries.append((q,[], 'discovered'))
seen=set()
for query,relations,priority in queries:
    if query in seen: continue
    seen.add(query)
    url=base+'?'+urllib.parse.urlencode({'query':query})
    for _ in range(PAGES_PER_QUERY):
        req=urllib.request.Request(url,headers={'User-Agent':UA})
        try:
            with urllib.request.urlopen(req,timeout=25) as resp: root=ET.fromstring(resp.read())
            pages_checked+=1; absorb(root,query,relations,priority)
            nxt=next_url(root,url)
            if not nxt: break
            url=nxt
        except Exception as exc:
            errors.append({'query':query,'url':url,'error':type(exc).__name__}); break

vals=sorted(items.values(),key=lambda x:int(x['sourceId']))
OUT.write_text(json.dumps({'schema':'dawn.library.chinese-candidates.v2','generatedAt':now,'items':vals},ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True)
report={
    'schema':'dawn.library.chinese-discovery.report.v2','generatedAt':now,'source':'project-gutenberg','language':'zh',
    'queries':len(seen),'pagesChecked':pages_checked,'newDiscovered':run_discovered,'candidateQueue':len(vals),'errors':errors,
    'sourcePolicy':{'wikisource':'forbidden','contentBoundary':'theology-bible-inner-life; no political/national/war dispute material'},
    'invariant':'Metadata only; known Gutenberg IDs establish identity only; explicit Chinese-language metadata and explicit rights are independently required before promotion; no bulk full-text ingestion.'
}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
