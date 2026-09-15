#!/usr/bin/env python3
"""Dawn collection-domain gate.

Bulk collection policy is deny-list first: candidates continue unless they hit an
explicit hard exclusion. Editorial relevance, recommendation quality, curation
value and display prominence are NOT admission gates.
"""
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

# These are collection hard boundaries, not recommendation signals.
FORBIDDEN_SOURCE=('wikisource','wikisource.org','zh-wikisource','維基文庫','维基文库')
DISPUTE_MARKERS=('politics','political','war','warfare','conflict','nationalism','ethnic conflict','民族','政治','戰爭','战争','衝突','冲突','侵略','民族主義','民族主义')

def payload(item):
    return json.dumps(item,ensure_ascii=False).casefold()

def hard_exclusion(item):
    text=payload(item)
    if any(term in text for term in FORBIDDEN_SOURCE):
        return 'forbidden-source:wikisource'
    searchable=' '.join(str(item.get(k,'')) for k in ('title','author','matchedQuery')).casefold()
    if any(term in searchable for term in DISPUTE_MARKERS):
        return 'brand-boundary:political-ethnic-war-content'
    return None

items=[]; counts={'qualified':0,'deferred':0,'rejected':0}
for raw in data.get('items',[]):
    item=dict(raw)
    blocked=hard_exclusion(item)
    if blocked:
        item['relevance']={'stage':'rejected','reason':blocked,'evaluatedAt':now,'policy':'hard-exclusion-only'}
        item['stage']='rejected'; counts['rejected']+=1
    else:
        # During bulk growth, absence of a hard exclusion is sufficient to continue
        # to identity/edition/rights/provenance verification.
        item['relevance']={'stage':'qualified','reason':'no-hard-exclusion','evaluatedAt':now,'policy':'hard-exclusion-only'}
        item['stage']='qualified'; counts['qualified']+=1
    items.append(item)
OUT.write_text(json.dumps({'schema':'dawn.library.relevance-results.v2','generatedAt':now,'items':items},ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True)
report={'schema':'dawn.library.relevance.report.v2','generatedAt':now,'collection':'biblical-world-books','total':len(items),'results':counts,'next':'All candidates without an explicit hard exclusion proceed to Edition/Rights Resolver.','invariant':'Collection growth is deny-list first. Recommendation, curation and display quality never gate canonical admission.'}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
