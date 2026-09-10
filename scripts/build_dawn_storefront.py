#!/usr/bin/env python3
import json,re,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from html import unescape
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'static/dawn-library/storefront.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-STOREFRONT.json'
BIBLICAL_CATALOG=ROOT/'static/dawn-library/biblical-world/catalog.json'
IDENTITY_CACHE=ROOT/'static/dawn-library/identity-cache.json'
UA='Dore-Dawn-Library/1.3 (+https://westsidewatch.github.io)'
ATOM='http://www.w3.org/2005/Atom';NS={'atom':ATOM}
now=datetime.now(timezone.utc).isoformat()

def request(url,accept='*/*'):
    return urllib.request.Request(url,headers={'User-Agent':UA,'Accept':accept})
def fetch_bytes(url,accept='*/*',limit=None):
    with urllib.request.urlopen(request(url,accept),timeout=35) as r:return r.read() if limit is None else r.read(limit)
def fetch_xml(url,accept='application/atom+xml,application/xml;q=0.9,*/*;q=0.5'):
    return ET.fromstring(fetch_bytes(url,accept))
def fetch_json(url):
    return json.loads(fetch_bytes(url,'application/json').decode('utf-8','replace'))
def fetch_text(url):
    return fetch_bytes(url,'text/html,application/xhtml+xml;q=0.9,*/*;q=0.5',350000).decode('utf-8','replace')
def clean(s):return re.sub(r'\s+',' ',(s or '')).strip()
def http_url(url):return url if isinstance(url,str) and url.startswith(('https://','http://')) else ''
def slug(s,n=72):return re.sub(r'[^a-z0-9\u4e00-\u9fff]+','-',clean(s).lower()).strip('-')[:n]
def page_cover(url):
    try:
        html=fetch_text(url)
        for p in [r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']']:
            m=re.search(p,html,re.I)
            if m:return http_url(unescape(m.group(1)))
    except Exception:pass
    return ''

def atom_items(root,provider,kind='remote-public',limit=30,rights='public-domain-us',resolve_page_cover=False):
    items=[]
    for e in root.findall('atom:entry',NS):
        title=clean(e.findtext('atom:title',default='',namespaces=NS));names=[clean(a.text) for a in e.findall('atom:author/atom:name',NS) if clean(a.text)];author=', '.join(names)
        href='';cover='';download='';eid=clean(e.findtext('atom:id',default='',namespaces=NS))
        for ln in e.findall('atom:link',NS):
            rel=ln.attrib.get('rel','');typ=ln.attrib.get('type','');u=http_url(ln.attrib.get('href',''))
            if not u:continue
            if rel=='alternate' and not href:href=u
            if ('image' in rel or typ.startswith('image/')) and not cover:cover=u
            if ('acquisition' in rel or typ=='application/epub+zip') and not download:download=u
        if not href and eid.startswith('http'):href=eid
        if not title or not (href or download):continue
        if resolve_page_cover and href and not cover:cover=page_cover(href)
        sid=slug(title) or str(len(items)+1)
        items.append({'id':f'{provider.lower().replace(" ","-")}-{sid}','title':title,'author':author,'language':'zh' if provider=='Wikisource' else 'en','source':{'provider':provider,'url':href or download,'downloadUrl':download or None,'kind':kind},'cover':{'url':cover,'mode':'source'} if cover else {'mode':'one-fallback'},'rights':{'status':rights,'declaredBy':provider},'quality':'curated-edition' if kind.endswith('premium') else 'source-edition','contentDownloaded':False})
        if len(items)>=limit:break
    return items

def gutenberg_shelf(label,query,limit=36):
    root=fetch_xml('https://www.gutenberg.org/ebooks/search.opds/?'+urllib.parse.urlencode({'query':query}));items=[]
    for e in root.findall('atom:entry',NS):
        title=clean(e.findtext('atom:title',default='',namespaces=NS));a=e.find('atom:author/atom:name',NS);author=clean(a.text) if a is not None else ''
        eid=clean(e.findtext('atom:id',default='',namespaces=NS));gid='';m=re.search(r'(\d+)(?:/)?$',eid)
        if m:gid=m.group(1)
        links=e.findall('atom:link',NS)
        if not gid:
            for ln in links:
                mm=re.search(r'/ebooks/(\d+)',ln.attrib.get('href',''))
                if mm:gid=mm.group(1);break
        if not gid or not title:continue
        cover=''
        for ln in links:
            rel=ln.attrib.get('rel','');typ=ln.attrib.get('type','');href=http_url(ln.attrib.get('href',''))
            if href and ('image' in rel or typ.startswith('image/')):cover=href;break
        items.append({'id':f'gutenberg-{gid}','title':title,'author':author,'language':'en','source':{'provider':'Project Gutenberg','url':f'https://www.gutenberg.org/ebooks/{gid}','kind':'remote-public'},'cover':{'url':cover,'mode':'source'} if cover else {'mode':'one-fallback'},'rights':{'status':'public-domain-us','declaredBy':'Project Gutenberg'},'quality':'source-edition','contentDownloaded':False})
        if len(items)>=limit:break
    return {'id':'gutenberg-'+slug(query),'title':label,'kind':'source-shelf','source':'Project Gutenberg','items':items}

def standard_new_releases():
    root=fetch_xml('https://standardebooks.org/feeds/atom/new-releases')
    return {'id':'standard-ebooks-new','title':'精品書架 · Standard Ebooks','kind':'premium-shelf','source':'Standard Ebooks','items':atom_items(root,'Standard Ebooks','remote-public-premium',15,'public-domain-us',True)}

def wikisource_export_shelf():
    catalog=json.loads(BIBLICAL_CATALOG.read_text());items=[]
    for book in catalog.get('items',[]):
        work=book.get('work') or {};title=clean(work.get('title',''));lang=(work.get('language') or '').lower();sources=book.get('sources') or []
        src=next((s for s in sources if s.get('provider')=='中文維基文庫' and s.get('url')),None);rights=book.get('rights') or {}
        if not title or not src or not lang.startswith('zh') or rights.get('status')!='public-domain':continue
        page=urllib.parse.unquote(src['url'].split('/wiki/',1)[-1]).replace('_',' ')
        export='https://ws-export.wmcloud.org/?'+urllib.parse.urlencode({'format':'epub','lang':'zh','page':page})
        items.append({'id':'wikisource-export-'+book['id'],'title':title,'author':clean(work.get('author','')),'language':'zh','source':{'provider':'Wikisource','url':src['url'],'downloadUrl':export,'kind':'remote-public-export','catalogId':book['id']},'cover':book.get('cover') or {'mode':'one-fallback'},'rights':{'status':'public-domain','declaredBy':'中文維基文庫','provenanceRequired':True},'quality':'verified-export-ready','contentDownloaded':False})
    return {'id':'wikisource-zh-verified-export','title':'中文典籍 · 維基文庫 EPUB','kind':'source-shelf','source':'Wikisource','items':items[:30]}

def metadata_map(raw):
    out={};rows=raw or []
    if isinstance(rows,dict):
        for k,v in rows.items():
            vals=v if isinstance(v,list) else [v];out[k]=[clean(x.get('value','') if isinstance(x,dict) else str(x)) for x in vals if clean(x.get('value','') if isinstance(x,dict) else str(x))]
        return out
    for row in rows if isinstance(rows,list) else []:
        if not isinstance(row,dict):continue
        key=row.get('key') or row.get('metadataField') or row.get('field');val=row.get('value')
        if isinstance(key,dict):key=key.get('key') or key.get('name')
        if key and val is not None:out.setdefault(str(key),[]).append(clean(str(val)))
    return out

def first(meta,*keys):
    for k in keys:
        vals=meta.get(k) or []
        if vals:return vals[0]
    return ''

def doab_records(data):
    if isinstance(data,list):return data
    if not isinstance(data,dict):return []
    for k in ('items','results'):
        if isinstance(data.get(k),list):return data[k]
    emb=data.get('_embedded') or {}
    if isinstance(emb,dict):
        for k in ('items','objects'):
            if isinstance(emb.get(k),list):return emb[k]
        sr=emb.get('searchResult') or {};se=sr.get('_embedded') if isinstance(sr,dict) else {}
        if isinstance(se,dict) and isinstance(se.get('objects'),list):return se['objects']
    return []

def doab_shelf(label,query,limit=24):
    url='https://directory.doabooks.org/rest/search?'+urllib.parse.urlencode({'query':query,'expand':'metadata,bitstreams','limit':limit});rows=doab_records(fetch_json(url));items=[]
    for row in rows:
        if not isinstance(row,dict):continue
        if 'indexableObject' in row and isinstance(row['indexableObject'],dict):row=row['indexableObject']
        meta=metadata_map(row.get('metadata'));title=first(meta,'dc.title','dc.title.main') or clean(row.get('name',''));author=first(meta,'dc.contributor.author','dc.creator','dc.contributor');language=first(meta,'dc.language','dc.language.iso') or 'en'
        handle=clean(row.get('handle','')) or first(meta,'dc.identifier.uri');page=http_url(handle) if handle.startswith('http') else (f'https://directory.doabooks.org/handle/{handle}' if handle else '')
        doi=first(meta,'dc.identifier.doi','dc.identifier');isbn=first(meta,'dc.identifier.isbn','dc.identifier.isbn13');license_url=first(meta,'dc.rights.uri','dc.rights.license');rights_text=first(meta,'dc.rights','dc.rights.accessRights');download='';cover=''
        for b in row.get('bitstreams') or []:
            if not isinstance(b,dict):continue
            mime=(b.get('mimeType') or b.get('format') or '').lower();name=(b.get('name') or '').lower();link=b.get('retrieveLink') or b.get('link') or ''
            if isinstance(link,str) and link.startswith('/'):link='https://directory.doabooks.org'+link
            link=http_url(link)
            if not download and (mime=='application/pdf' or name.endswith('.pdf')):download=link
            if not cover and (mime.startswith('image/') or re.search(r'cover.*\.(jpe?g|png|webp)$',name)):cover=link
        if not title or not page:continue
        stable=handle or doi or isbn or title;sid=slug(stable) or str(len(items)+1)
        items.append({'id':'doab-'+sid,'title':title,'author':author,'language':language,'identifiers':{'doi':doi or None,'isbn':isbn or None,'handle':handle or None},'source':{'provider':'DOAB','url':page,'downloadUrl':download or None,'kind':'remote-open-access'},'cover':{'url':cover,'mode':'source'} if cover else {'mode':'one-fallback'},'rights':{'status':'open-access','license':license_url or rights_text or None,'declaredBy':'DOAB','provenanceRequired':True},'quality':'open-access-scholarly','contentDownloaded':False})
        if len(items)>=limit:break
    return {'id':'doab-'+slug(query),'title':label,'kind':'academic-shelf','source':'DOAB','items':items}

def ia_shelf(label,query,limit=20):
    params=[('q',f'({query}) AND mediatype:texts'),('fl[]','identifier'),('fl[]','title'),('fl[]','creator'),('fl[]','language'),('fl[]','year'),('rows',str(limit)),('page','1'),('output','json')]
    data=fetch_json('https://archive.org/advancedsearch.php?'+urllib.parse.urlencode(params));items=[]
    for row in (data.get('response') or {}).get('docs',[]):
        ident=clean(row.get('identifier',''));title=clean(row.get('title',''))
        if not ident or not title:continue
        creator=row.get('creator','');author=clean(', '.join(creator) if isinstance(creator,list) else str(creator or ''))
        lang=row.get('language','en');language=clean(lang[0] if isinstance(lang,list) and lang else str(lang or 'en'))
        items.append({'id':'internet-archive-'+ident,'title':title,'author':author,'language':language,'source':{'provider':'Internet Archive','url':f'https://archive.org/details/{urllib.parse.quote(ident)}','kind':'remote-scan','reader':'Internet Archive BookReader'},'cover':{'url':f'https://archive.org/services/img/{urllib.parse.quote(ident)}','mode':'source'},'rights':{'status':'source-rights-check','declaredBy':'Internet Archive','provenanceRequired':True},'quality':'original-scan','contentDownloaded':False})
    return {'id':'internet-archive-'+slug(label),'title':label,'kind':'scan-shelf','source':'Internet Archive','items':items}

def load_identity_cache():
    try:return json.loads(IDENTITY_CACHE.read_text())
    except Exception:return {'schema':'dawn.library.identity-cache.v1','items':{}}
def openlibrary_lookup(item):
    title=clean(item.get('title',''));author=clean(item.get('author',''))
    if not title:return None
    q={'title':title,'limit':1,'fields':'key,edition_key,cover_i,isbn,ia,title,author_name'}
    if author:q['author']=author
    docs=fetch_json('https://openlibrary.org/search.json?'+urllib.parse.urlencode(q)).get('docs') or []
    if not docs:return None
    d=docs[0];work=d.get('key');edition=(d.get('edition_key') or [None])[0];isbn=(d.get('isbn') or [None])[0];ia=(d.get('ia') or [None])[0];cover=d.get('cover_i')
    return {'provider':'Open Library','workId':work,'editionId':edition,'isbn':isbn,'coverId':cover,'internetArchiveId':ia,'resolvedAt':now}
def enrich_identities(shelves,limit=60):
    cache=load_identity_cache();items_cache=cache.setdefault('items',{});queried=0;resolved=0;covers=0;ia_links=0
    for shelf in shelves:
        for item in shelf.get('items',[]):
            if item.get('source',{}).get('provider')=='Internet Archive':continue
            key=item['id'];ident=items_cache.get(key)
            if ident is None and queried<limit:
                queried+=1
                try:ident=openlibrary_lookup(item) or {'miss':True,'resolvedAt':now}
                except Exception as e:ident={'miss':True,'error':type(e).__name__,'resolvedAt':now}
                items_cache[key]=ident
            if not ident or ident.get('miss'):continue
            resolved+=1;item['identity']=ident
            ids=item.setdefault('identifiers',{})
            if ident.get('workId'):ids['openLibraryWork']=ident['workId']
            if ident.get('editionId'):ids['openLibraryEdition']=ident['editionId']
            if ident.get('isbn') and not ids.get('isbn'):ids['isbn']=ident['isbn']
            if not item.get('cover',{}).get('url') and ident.get('coverId'):
                item['cover']={'url':f'https://covers.openlibrary.org/b/id/{ident["coverId"]}-L.jpg?default=false','mode':'edition-identity','provider':'Open Library'};covers+=1
            if ident.get('internetArchiveId'):
                item.setdefault('alternateSources',[]).append({'provider':'Internet Archive','url':f'https://archive.org/details/{urllib.parse.quote(ident["internetArchiveId"])}','kind':'remote-scan','reader':'Internet Archive BookReader','rightsStatus':'source-rights-check'});ia_links+=1
    cache['updatedAt']=now;IDENTITY_CACHE.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
    return {'queriedThisRun':queried,'resolved':resolved,'coversAdded':covers,'internetArchiveLinks':ia_links,'cacheEntries':len(items_cache)}

shelf_specs=[('聖經與基督教','bible christianity',40),('早期教會與教父','early church fathers',36),('猶太與第二聖殿世界','jewish history josephus',36),('古代世界與考古','ancient history archaeology',36),('哲學與思想','philosophy classics',36),('傳記與回憶','biography memoir',36)]
shelves=[];errors=[]
for source_name,fn in [('Standard Ebooks',standard_new_releases),('Wikisource',wikisource_export_shelf),('DOAB theology',lambda:doab_shelf('開放學術 · 神學與宗教','theology OR biblical',24)),('DOAB archaeology',lambda:doab_shelf('開放學術 · 聖經世界與考古','archaeology AND religion',24)),('Internet Archive Bible history',lambda:ia_shelf('原版古籍 · 聖經歷史與地理','title:(bible OR biblical) AND (subject:(history) OR subject:(geography))',20)),('Internet Archive church history',lambda:ia_shelf('原版古籍 · 教會歷史','title:(church history OR early church)',20))]:
    try:
        shelf=fn()
        if shelf.get('items'):shelves.append(shelf)
        else:errors.append({'source':source_name,'error':'empty-shelf'})
    except Exception as e:errors.append({'source':source_name,'error':type(e).__name__+': '+str(e)[:180]})
for label,q,limit in shelf_specs:
    try:shelves.append(gutenberg_shelf(label,q,limit))
    except Exception as e:errors.append({'source':'Project Gutenberg','query':q,'error':type(e).__name__+': '+str(e)[:180]})
seen=set();deduped=[]
for shelf in shelves:
    items=[]
    for item in shelf['items']:
        if item['id'] in seen:continue
        seen.add(item['id']);items.append(item)
    shelf['items']=items
    if items:deduped.append(shelf)
shelves=deduped
identity_metrics=enrich_identities(shelves,60)
total=sum(len(s['items']) for s in shelves);cover_count=sum(1 for s in shelves for i in s['items'] if i.get('cover',{}).get('url'));download_count=sum(1 for s in shelves for i in s['items'] if i.get('source',{}).get('downloadUrl'));provider_counts={}
for s in shelves:
    for i in s['items']:
        p=i.get('source',{}).get('provider','unknown');provider_counts[p]=provider_counts.get(p,0)+1
store={'schema':'dawn.library.storefront.v3','generatedAt':now,'title':'黎明書局','storagePolicy':'index-only','principle':'映射 ≠ 導入。閱讀 ≠ 收藏。收藏 ≠ 下載。','shelves':shelves,'metrics':{'shelves':len(shelves),'mappedBooks':total,'sourceCovers':cover_count,'directPublications':download_count,'providers':provider_counts,'identity':identity_metrics},'errors':errors}
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(store,ensure_ascii=False,indent=2)+'\n')
report={'schema':'dawn.library.storefront.report.v4','generatedAt':now,'shelves':[{'id':s['id'],'title':s['title'],'books':len(s['items']),'source':s['source']} for s in shelves],'mappedBooks':total,'sourceCovers':cover_count,'directPublications':download_count,'providers':provider_counts,'identity':identity_metrics,'errors':errors,'contentDownloaded':False}
REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
