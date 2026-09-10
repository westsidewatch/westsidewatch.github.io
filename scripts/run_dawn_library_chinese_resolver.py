#!/usr/bin/env python3
import json,re,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REL=ROOT/'static/dawn-library/biblical-world/chinese-relevance-results.json'
OUT=ROOT/'static/dawn-library/biblical-world/chinese-resolver-results.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-CHINESE-RESOLVER.json'
API='https://zh.wikisource.org/w/api.php'
UA='Dore-Dawn-Library/1.0 (metadata and rights resolver; no bulk text)'
now=datetime.now(timezone.utc).isoformat()
def api(params):
    q=urllib.parse.urlencode({'format':'json','formatversion':2,**params})
    req=urllib.request.Request(API+'?'+q,headers={'User-Agent':UA})
    with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
def page_meta(title):
    data=api({'action':'query','prop':'info|pageprops','inprop':'url','titles':title})
    p=data.get('query',{}).get('pages',[{}])[0]
    return {'pageid':p.get('pageid'),'title':p.get('title',title),'canonicalUrl':p.get('canonicalurl'),'missing':p.get('missing',False)}
def rights_evidence(title):
    # Parse only the root page HTML to inspect its rights/license templates; do not fetch transcluded book text.
    data=api({'action':'parse','page':title,'prop':'text|categories|templates','disablelimitreport':1,'disableeditsection':1})
    parse=data.get('parse',{}); html=parse.get('text','')
    templates=[x.get('*','') for x in parse.get('templates',[])]
    cats=[x.get('*','') for x in parse.get('categories',[])]
    hay=' '.join(templates+cats)+' '+re.sub('<[^>]+>',' ',html[-12000:])
    positive=any(k in hay for k in ('公有領域','公版','Public domain','PD-old','PD-','作者逝世','版權到期'))
    return {'explicitPublicDomain':positive,'templates':templates[-20:],'categories':cats[-20:]}
items=[]; counts={'verified':0,'needs-review':0,'blocked':0}
for x in json.loads(REL.read_text())['items']:
    if x.get('stage')!='qualified': continue
    title=x['title']; root='/' not in title
    result={'sourceId':x['sourceId'],'title':title,'sourceUrl':x['sourceUrl'],'stage':'needs-review','contentDownloaded':False,'resolvedAt':now}
    if not root:
        result['stage']='blocked'; result['reason']='not-work-root'; counts['blocked']+=1; items.append(result); continue
    try:
        meta=page_meta(title); ev=rights_evidence(title)
        result['edition']={'canonicalTitle':meta['title'],'pageid':meta['pageid'],'canonicalUrl':meta['canonicalUrl']}
        result['rights']={'status':'public-domain' if ev['explicitPublicDomain'] else 'unverified','declaredBy':'中文維基文庫','evidence':ev,'provenanceRequired':True}
        if not meta['missing'] and ev['explicitPublicDomain']:
            result['stage']='verified'; result['reason']='root-page-with-explicit-public-domain-evidence'; counts['verified']+=1
        else:
            result['reason']='rights-or-edition-needs-review'; counts['needs-review']+=1
    except Exception as e:
        result['reason']='resolver-error'; result['error']=str(e); counts['needs-review']+=1
    items.append(result)
OUT.write_text(json.dumps({'schema':'dawn.library.chinese-resolver-results.v1','generatedAt':now,'items':items},ensure_ascii=False,indent=2)+'\n')
REPORT.parent.mkdir(parents=True,exist_ok=True)
report={'schema':'dawn.library.chinese-resolver.report.v1','generatedAt':now,'qualifiedInput':len(items),'results':counts,'verifiedTitles':[x['title'] for x in items if x['stage']=='verified'],'invariant':'Verification reads metadata and root-page rights evidence only; no book full text is stored.'}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(report,ensure_ascii=False,indent=2))
