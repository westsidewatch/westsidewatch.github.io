#!/usr/bin/env python3
"""Build the Dawn Library processing index and derived Chinese projection.

Catalogue is the holdings baseline. Queue/corpus metadata may enrich a holding
only after deterministic identity reconciliation. Discovery-only Chinese works
remain candidates and never silently become holdings.
"""
from __future__ import annotations
import json,re,unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOGUE=ROOT/'static/dawn-library/catalogue';QUEUE=ROOT/'data/dawn-10k-work-queue.json';DISCOVERY=ROOT/'data/dawn-10k-openlibrary-works.json'
OUT=ROOT/'data/dawn-library-build-index.json';ZH_OUT=ROOT/'data/dawn-library-chinese-projection.json';IDENTITY_OUT=ROOT/'data/dawn-library-identity-map.json'
HAN=re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def payload(o):
    if isinstance(o,dict) and isinstance(o.get('content'),str):
        try:return json.loads(o['content'])
        except json.JSONDecodeError:pass
    return o
def page_items(p):
    if isinstance(p,list):return p
    if isinstance(p,dict):
        for k in ('works','items','resources','entries'):
            if isinstance(p.get(k),list):return p[k]
    return []
def first(i,*ks):
    for k in ks:
        v=i.get(k)
        if v not in (None,'',[]):return v
    return None
def text_of(i):
    bits=[]
    for k in ('title','subtitle','creator','author','publisher','description'):
        v=i.get(k);bits.extend(v if isinstance(v,list) else [v] if isinstance(v,str) else [])
    for k in ('creators','authors'):
        if isinstance(i.get(k),list):bits.extend(str(x) for x in i[k])
    return ' '.join(str(x) for x in bits)
def norm(v):
    if isinstance(v,list):v=' '.join(str(x) for x in v)
    v=unicodedata.normalize('NFKC',str(v or '')).casefold().strip();v=re.sub(r'[^\w\s-]+',' ',v);return re.sub(r'\s+',' ',v).strip()
def title_key(i):return norm(first(i,'title'))
def author_key(i):return norm(first(i,'creator','author','creators','authors'))
def signature(i):return f'{title_key(i)}::{author_key(i)}'
def normalize_language(raw):
    vals=[raw] if isinstance(raw,str) else raw if isinstance(raw,list) else [];s=' '.join(str(x) for x in vals).lower()
    if any(x in s for x in ('chinese','zh','zho','chi','中文','漢','汉')):return 'zh'
    return s if s and s not in ('unknown','und') else 'unknown'
def language_state(i):
    l=normalize_language(i.get('language') or i.get('languages'))
    if l!='unknown':return l,'metadata'
    return ('zh','han-script') if HAN.search(text_of(i)) else ('unknown','unknown')
def queue_maps():
    if not QUEUE.exists():return {},{}, {}, {'chi':0,'eng':0}
    d=load(QUEUE);by_id={};by_sig={};by_title={}
    for i in d.get('items',[]):
        wid=str(i.get('workId') or '').strip()
        if wid:by_id[wid]=i
        s=signature(i)
        if s!='::':by_sig.setdefault(s,[]).append(i)
        t=title_key(i)
        if t:by_title.setdefault(t,[]).append(i)
    return by_id,by_sig,by_title,d.get('languageSignals') or {'chi':0,'eng':0}
def reconcile(item,by_id,by_sig,by_title):
    cid=str(first(item,'id','workId','work_id','key','canonicalId') or '')
    direct=by_id.get(cid)
    if direct:return direct,'authority-id'
    exact=by_sig.get(signature(item),[])
    if len(exact)==1:return exact[0],'title-author'
    title=by_title.get(title_key(item),[])
    if len(title)==1:return title[0],'unique-title'
    return None,'unmatched'
def discovery_chinese():
    if not DISCOVERY.exists():return [],0
    d=load(DISCOVERY);ids=[]
    for i in d.get('items',[]):
        if normalize_language(i.get('languages') or i.get('language'))=='zh' or i.get('matchedLanguage')=='chi':
            w=str(i.get('workId') or '').strip()
            if w:ids.append(w)
    return list(dict.fromkeys(ids)),int((d.get('metrics') or {}).get('chineseMatchedWorksAdded',0) or 0)
def main():
    root=payload(load(CATALOGUE/'index.json'));by_id,by_sig,by_title,signals=queue_maps();candidate_ids,new_zh=discovery_chinese()
    rows=[];chinese=[];seen=set();identity=[];methods={};enriched_lang=enriched_class=0
    for page_name in root.get('pages',[]):
        page=payload(load(CATALOGUE/page_name))
        for item in page_items(page):
            if not isinstance(item,dict):continue
            cid=str(first(item,'id','workId','work_id','key','canonicalId') or f'anon:{len(rows)+1}')
            if cid in seen:continue
            seen.add(cid);q,method=reconcile(item,by_id,by_sig,by_title);methods[method]=methods.get(method,0)+1
            if q:identity.append({'catalogueId':cid,'queueWorkId':q.get('workId'),'queueId':q.get('queueId'),'method':method})
            lang,evidence=language_state(item)
            if lang=='unknown' and q:
                qlang=normalize_language(q.get('languages') or q.get('language'))
                if qlang!='unknown':lang,evidence=qlang,'reconciled-work-queue';enriched_lang+=1
            cover=first(item,'cover','coverId','cover_id','coverUrl','cover_url')
            classification=first(item,'classification','subjects','subject','categories');ce='catalogue' if classification else 'missing'
            if not classification and q and q.get('collectionScope'):
                classification=q['collectionScope'];ce='reconciled-collection-scope';enriched_class+=1
            row={'id':cid,'page':page_name,'title':first(item,'title') or '','author':first(item,'creator','author','creators','authors'),'period':first(item,'period','century','date','year'),'language':lang,'languageEvidence':evidence,'chineseCollection':lang=='zh','coverStatus':'known' if cover else 'missing','classificationStatus':'known' if classification else 'missing','classificationEvidence':ce,'identityStatus':'reconciled' if q else 'unmatched','identityMethod':method,'catalogueStatus':'present'}
            rows.append(row)
            if row['chineseCollection']:chinese.append(cid)
    missing_cover=sum(r['coverStatus']=='missing' for r in rows);missing_class=sum(r['classificationStatus']=='missing' for r in rows)
    out={'schema':'dawn-library-build-index/v3','source':'current-catalogue+reconciled-work-queue','count':len(rows),'expectedCatalogueCount':root.get('count'),'identityReconciledCount':len(identity),'identityUnmatchedCount':len(rows)-len(identity),'identityMethods':methods,'chineseCollectionCount':len(chinese),'queueLanguageSignals':signals,'newlyDiscoveredChineseWorks':new_zh,'languageEnrichedFromQueueCount':enriched_lang,'classificationEnrichedFromQueueCount':enriched_class,'missingCoverCount':missing_cover,'missingClassificationCount':missing_class,'items':rows}
    zh={'schema':'dawn-library-projection/v3','id':'chinese-collection','label':{'zh-Hant':'中文館藏','en':'Chinese Collection'},'projectionOnly':True,'count':len(chinese),'workIds':chinese,'discoveryCandidateCount':len(candidate_ids),'newlyDiscoveredCandidateCount':new_zh,'discoveryCandidateWorkIds':candidate_ids,'candidatePolicy':'Discovery candidates remain pre-canonical until admission and promotion gates pass.'}
    im={'schema':'dawn-library-identity-map/v1','catalogueCount':len(rows),'reconciledCount':len(identity),'unmatchedCount':len(rows)-len(identity),'methods':methods,'links':identity}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8');ZH_OUT.write_text(json.dumps(zh,ensure_ascii=False,separators=(',',':')),encoding='utf-8');IDENTITY_OUT.write_text(json.dumps(im,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(json.dumps({'indexed':len(rows),'expected':root.get('count'),'identityReconciled':len(identity),'identityUnmatched':len(rows)-len(identity),'identityMethods':methods,'chinese':len(chinese),'queueLanguageSignals':signals,'newlyDiscoveredChinese':new_zh,'languageEnrichedFromQueue':enriched_lang,'classificationEnrichedFromQueue':enriched_class,'missingCover':missing_cover,'missingClassification':missing_class},ensure_ascii=False))
    if root.get('count') is not None and len(rows)!=root['count']:raise SystemExit(f"catalogue count mismatch: indexed={len(rows)} expected={root['count']}")
if __name__=='__main__':main()
