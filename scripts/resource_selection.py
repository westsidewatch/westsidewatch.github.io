"""Shared product admission policy; upstream flags/scores never grant approval."""
import json,re,unicodedata
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
POLICY=json.loads((ROOT/'data/resource_selection_policy.json').read_text())
REVIEWS=json.loads((ROOT/'data/resource_book_reviews.json').read_text())['items']

def norm(value):return ' '.join(unicodedata.normalize('NFKC',str(value or '')).casefold().split())
def urlnorm(value):
    value=unquote(str(value or '')).replace('_',' ')
    return value.rstrip('/')

def identity(item):
    work=item.get('work') if isinstance(item.get('work'),dict) else {}
    title=work.get('title') or item.get('title') or item.get('name') or ''
    sources=item.get('sources') if isinstance(item.get('sources'),list) else []
    source=item.get('source') if isinstance(item.get('source'),dict) else {}
    urls=[s.get('url','') for s in sources if isinstance(s,dict)]+[source.get('url',''),item.get('sourceUrl',''),item.get('url','')]
    return title,{urlnorm(u) for u in urls if u}

def excluded(item):
    if not isinstance(item,dict):item={'title':str(item)}
    # Only resource metadata, not unrelated evidence/log prose or user writings.
    text=norm(unquote(json.dumps({k:item.get(k) for k in ('id','title','name','name_en','description','work','sourceUrl','url','topics','subject','categories','source','sources')},ensure_ascii=False)))
    if item.get('controversial') is True or item.get('contentReview') in ('rejected','controversial','excluded'):
        return True
    if any(v in text for v in POLICY['withdrawnIds']):return True
    topics=item.get('topics',[]) or []
    if isinstance(topics,str):topics=[topics]
    if any(t in POLICY['excludedTopics'] for t in topics):return True
    return any(re.search(pattern,text,re.I) for pattern in POLICY['excludedPatterns'])

def book_decision(item):
    if excluded(item):return {'status':'excluded','reason':'content-boundary'}
    if item.get('completeWork') is False:return {'status':'excluded','reason':'not-a-complete-book'}
    title,urls=identity(item)
    kind=item.get('resourceType') or (item.get('work') if isinstance(item.get('work'),dict) else {}).get('type') or item.get('kind')
    if kind in POLICY['nonBookKinds'] or any(re.search(p,norm(title),re.I) for p in POLICY['nonBookPatterns']):
        return {'status':'excluded','reason':'not-a-book'}
    review=next((r for r in REVIEWS if norm(title) in {norm(t) for t in r['titles']} and urls.intersection(urlnorm(u) for u in r['sourceUrls'])),None)
    if not review:return {'status':'hold','reason':'book-identity-and-content-review-required'}
    if not (review.get('status')=='approved' and review.get('contentReview')=='approved' and review.get('completeWork') is True and review.get('kind') in POLICY['acceptedBookKinds'] and review.get('creatorOrTranslation') and review.get('editionEvidence') and review.get('scope')):
        return {'status':'hold','reason':'incomplete-review'}
    return {'status':'approved','reason':'reviewed-complete-book','policyVersion':POLICY['version'],'kind':review['kind']}

def book_allowed(item):return book_decision(item)['status']=='approved'
