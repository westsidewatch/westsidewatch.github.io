#!/usr/bin/env python3
"""Dawn Living Library v1.

Projects the canonical collection into a scientific knowledge map without
changing admission. Classification, facets and wall weight are derived
surfaces only: they can never create, delete or reject canonical Works.
"""
import json,re
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CANON=ROOT/'static/dawn-library/canonical-index.json'
OUT=ROOT/'static/dawn-library/living-library.json'

RULES={
 'bible': ('聖經', ('bible','biblical','old testament','new testament','hebrew bible','gospel','psalm','genesis','exodus','job','scripture')),
 'exegesis': ('釋經', ('commentary','exegesis','hermeneutic','concordance','bible dictionary','interpretation')),
 'theology': ('神學', ('theology','doctrine','christology','trinity','salvation','soteriology','eschatology','holy spirit','pneumatology')),
 'biblical-world': ('聖經世界', ('second temple','jewish','judaea','judea','galilee','jerusalem','hebrew','archaeology','ancient near east')),
 'church-history': ('教會歷史', ('church history','church fathers','early church','patristic','reformation','puritan','revival','augustine','eusebius','calvin','luther')),
 'christian-life': ('基督徒生命', ('prayer','devotion','spiritual','discipleship','holiness','suffering','christian life')),
 'ministry': ('教會與事奉', ('ministry','pastoral','preaching','sermon','worship','mission','missions','church leadership')),
}

def text(work):
    return ' '.join([str(work.get('title') or ''),*map(str,work.get('authors') or [])]).casefold()

def classify(work):
    t=text(work); hits=[]
    for key,(label,terms) in RULES.items():
        score=sum(1 for term in terms if term in t)
        if score:hits.append((score,key,label))
    hits.sort(reverse=True)
    return [{'id':key,'label':label,'confidence':'derived-keyword','score':score} for score,key,label in hits[:3]]

def language_values(work):
    vals=work.get('languages') or []
    if isinstance(vals,str):vals=[vals]
    return [str(x) for x in vals if x]

def period(year):
    if not isinstance(year,int):return 'unknown'
    if year < 500:return 'ancient'
    if year < 1500:return 'medieval'
    if year < 1800:return 'early-modern'
    if year < 1900:return 'nineteenth-century'
    if year < 2000:return 'twentieth-century'
    return 'contemporary'

def main():
    canonical=json.loads(CANON.read_text())
    works=canonical.get('works') or {}
    classes=Counter();languages=Counter();periods=Counter();authors=Counter();refs=[]
    for wid,work in works.items():
        cs=classify(work)
        for c in cs:classes[c['id']]+=1
        langs=language_values(work)
        for lang in langs:languages[lang]+=1
        p=period(work.get('firstPublishYear'));periods[p]+=1
        for author in work.get('authors') or []:
            if author:authors[str(author)]+=1
        refs.append({'workId':wid,'classification':[c['id'] for c in cs],'languages':langs,'period':p,'wall':{'span':2 if len(cs)>=2 else 1,'weight':max(1,len(cs))}})
    nodes=[]
    for key,(label,_) in RULES.items():nodes.append({'id':key,'label':label,'workCount':classes[key]})
    payload={
      'schema':'dawn.library.living-library.v1',
      'identityAuthority':'Dawn',
      'projectionOnly':True,
      'admissionAuthority':False,
      'canonicalWorkCount':canonical.get('workCount',len(works)),
      'classification':{'kind':'dawn-knowledge-map','nodes':nodes},
      'facets':{
        'languages':dict(languages.most_common()),
        'periods':dict(periods.most_common()),
        'authors':[{'value':k,'count':v} for k,v in authors.most_common(500)]
      },
      'livingWall':{'grammar':'weighted-multi-track-8:5','workRefs':refs},
      'editorialLayers':{'threeMorningStars':'independent','curatedCollections':'independent','spectrum':'independent'},
    }
    assert payload['canonicalWorkCount']==len(works)
    assert all(r['workId'] in works for r in refs)
    OUT.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n')
    print(json.dumps({'canonicalWorkCount':len(works),'classifiedWorks':sum(1 for r in refs if r['classification']),'classificationNodes':len(nodes),'livingWallRefs':len(refs)},ensure_ascii=False))

if __name__=='__main__':main()
