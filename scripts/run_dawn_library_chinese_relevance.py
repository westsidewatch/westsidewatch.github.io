#!/usr/bin/env python3
from resource_selection import excluded
import json,unicodedata
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAND=ROOT/'dore-core/review/resource-selection/chinese-candidates.json'
POL=ROOT/'static/dawn-library/biblical-world/chinese-relevance-policy.json'
OUT=ROOT/'dore-core/review/resource-selection/chinese-relevance-results.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-CHINESE-RELEVANCE.json'
now=datetime.now(timezone.utc).isoformat()
candidates=json.loads(CAND.read_text())['items']; policy=json.loads(POL.read_text())
def norm(s): return unicodedata.normalize('NFKC',s or '').casefold().replace(' ','')
def score(item):
    if excluded(item):return -10000,'rejected',['global-content-boundary']
    title=norm(item.get('title')); reasons=[]; value=0
    if str(item.get('matchedBy','')).startswith('seed:') or item.get('priority')=='golden': value+=policy['signals']['goldenSeed']; reasons.append('golden-seed')
    for term in policy['strongTerms']:
        if norm(term) in title: value+=policy['signals']['strongTerm']; reasons.append('strong:'+term)
    for term in policy['contextTerms']:
        if norm(term) in title: value+=policy['signals']['contextTerm']; reasons.append('context:'+term)
    if '/' in item.get('title',''): value+=policy['signals']['subpagePenalty']; reasons.append('subpage')
    for term in policy['knownNoise']:
        if norm(term) in title: value+=policy['signals']['knownNoise']; reasons.append('noise:'+term)
    if value>=policy['thresholds']['qualified']: stage='qualified'
    elif value>=policy['thresholds']['deferred']: stage='deferred'
    else: stage='rejected'
    return value,stage,reasons
results=[]; counts={'qualified':0,'deferred':0,'rejected':0}
for item in candidates:
    value,stage,reasons=score(item); counts[stage]+=1
    results.append({'sourceId':item['sourceId'],'provider':item['provider'],'language':item.get('language','zh'),'title':item['title'],'sourceUrl':item['sourceUrl'],'stage':stage,'relevance':{'score':value,'reasons':reasons,'evaluatedAt':now},'rights':item['rights'],'contentDownloaded':False})
OUT.write_text(json.dumps({'schema':'dawn.library.chinese-relevance-results.v1','generatedAt':now,'items':results},ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True)
report={'schema':'dawn.library.chinese-relevance.report.v1','generatedAt':now,'collection':'biblical-world-books','language':'zh','total':len(results),'results':counts,'next':'Only qualified Chinese candidates may enter Edition/Rights Resolver; none are auto-promoted.','invariant':'Search hit is not relevance. Relevance is not verification. Verification is not curation.'}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(report,ensure_ascii=False,indent=2))
