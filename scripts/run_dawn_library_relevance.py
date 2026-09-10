#!/usr/bin/env python3
import json,re
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAND=ROOT/'static/dawn-library/biblical-world/discovery-candidates.json'
POLICY=ROOT/'static/dawn-library/biblical-world/relevance-policy.json'
OUT=ROOT/'static/dawn-library/biblical-world/relevance-results.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-RELEVANCE.json'
now=datetime.now(timezone.utc).isoformat()
data=json.loads(CAND.read_text()); p=json.loads(POLICY.read_text())

def has(text,term):
    return re.search(r'(?<![a-z0-9])'+re.escape(term.lower())+r'(?![a-z0-9])',text.lower()) is not None

def score(item):
    title=item.get('title',''); author=item.get('author',''); query=item.get('matchedQuery','')
    combined=f'{title} {author}'
    points=0; reasons=[]
    if query and has(title,query): points+=p['signals']['exactQueryInTitle']; reasons.append('query-in-title')
    if query and has(author,query): points+=p['signals']['exactQueryInAuthor']; reasons.append('query-in-author')
    for term in p['strongTerms']:
        if has(combined,term): points+=p['signals']['strongTerm']; reasons.append('strong:'+term)
    for term in p['contextTerms']:
        if has(combined,term): points+=p['signals']['contextTerm']; reasons.append('context:'+term)
    for term in p['knownNoise']:
        if has(combined,term): points+=p['signals']['knownNoise']; reasons.append('noise:'+term)
    if points>=p['thresholds']['qualified']: stage='qualified'
    elif points>=p['thresholds']['defer']: stage='deferred'
    else: stage='rejected'
    return points,stage,reasons

items=[]; counts={'qualified':0,'deferred':0,'rejected':0}
for raw in data.get('items',[]):
    item=dict(raw); points,stage,reasons=score(item)
    item['relevance']={'score':points,'stage':stage,'reasons':reasons,'evaluatedAt':now}
    item['stage']=stage; counts[stage]+=1; items.append(item)
OUT.write_text(json.dumps({'schema':'dawn.library.relevance-results.v1','generatedAt':now,'items':items},ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True)
report={'schema':'dawn.library.relevance.report.v1','generatedAt':now,'collection':'biblical-world-books','total':len(items),'results':counts,'next':'Only qualified candidates may enter Edition/Rights Resolver; none are auto-promoted.','invariant':'Search hit is not relevance. Relevance is not verification. Verification is not curation.'}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
