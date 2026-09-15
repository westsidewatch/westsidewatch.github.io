#!/usr/bin/env python3
"""Dawn Living Library v2 — canonical -> hierarchy/facets -> Living Wall.
Derived navigation only. It has no admission or recommendation authority.
"""
import json,re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CANON=ROOT/'static/dawn-library/canonical-index.json'
CLASS=ROOT/'static/dawn-library/classification.json'
OUT=ROOT/'static/dawn-library/living-library.json'

TERMS={
'bible.text':('hebrew text','greek text','masoretic','septuagint','manuscript','textual criticism'),
'bible.translation':('translation','version','king james','revised version'),
'bible.old-testament':('old testament','genesis','exodus','leviticus','numbers','deuteronomy','psalm','proverbs','job','isaiah','jeremiah','ezekiel'),
'bible.new-testament':('new testament','gospel','matthew','mark','luke','john','acts','romans','corinthians','revelation'),
'bible.book-study':('bible study','scripture study'),
'exegesis.commentary':('commentary','comments on','exposition'),
'exegesis.hermeneutics':('hermeneutic','interpretation','exegesis'),
'exegesis.reference':('concordance','dictionary','lexicon','reference'),
'exegesis.biblical-theology':('biblical theology',),
'theology.systematic':('systematic theology','dogmatic'),
'theology.trinity':('trinity','trinitarian'),
'theology.christology':('christology','person of christ','jesus christ'),
'theology.salvation':('salvation','soteriology','atonement','justification'),
'theology.spirit':('holy spirit','pneumatology'),
'theology.church':('ecclesiology','doctrine of the church'),
'theology.eschatology':('eschatology','last things','second coming'),
'biblical-world.jewish':('jewish','jews','judaism','hebrew'),
'biblical-world.second-temple':('second temple','josephus','maccabee'),
'biblical-world.archaeology':('archaeology','archaeological'),
'biblical-world.geography':('geography','jerusalem','judea','galilee'),
'biblical-world.languages':('hebrew language','greek language','aramaic'),
'biblical-world.ane':('ancient near east','assyrian','babylonian','mesopotamia'),
'church-history.early':('early church','primitive church','apostolic age'),
'church-history.fathers':('church fathers','patristic','augustine','eusebius','chrysostom','athanasius','irenaeus','tertullian','origen'),
'church-history.medieval':('medieval church','middle ages','scholastic'),
'church-history.reformation':('reformation','calvin','luther','melanchthon','knox'),
'church-history.puritan':('puritan','john owen','richard baxter'),
'church-history.revival':('revival','whitefield','wesley','moody'),
'church-history.missions':('mission history','missionary','hudson taylor','amy carmichael'),
'christian-life.prayer':('prayer','praying'),
'christian-life.devotion':('devotion','devotional','spiritual life'),
'christian-life.discipleship':('disciple','discipleship'),
'christian-life.holiness':('holiness','holy life','sanctification'),
'christian-life.suffering':('suffering','affliction','trial'),
'christian-life.family':('christian family','marriage','home life'),
'christian-life.pastoral-care':('pastoral care','soul care'),
'ministry.preaching':('preaching','sermon','sermons','homiletic'),
'ministry.teaching':('christian teaching','sunday school','catechism'),
'ministry.worship':('worship','hymn','liturgy'),
'ministry.mission':('mission','missions','evangelism'),
'ministry.pastoral':('pastoral','pastor','ministry'),
'ministry.governance':('church government','church order','governance'),
}

def work_text(w):
    parts=[w.get('title',''),w.get('subtitle','')]
    a=w.get('authors') or []
    if isinstance(a,str):a=[a]
    parts+=a
    return ' '.join(map(str,parts)).casefold()

def langs(w):
    x=w.get('languages') or w.get('language') or []
    if isinstance(x,str):x=[x]
    return [str(v) for v in x if v]

def era(y):
    try:y=int(y)
    except:return 'unknown'
    return 'ancient' if y<500 else 'medieval' if y<1500 else 'early-modern' if y<1800 else 'nineteenth-century' if y<1900 else 'twentieth-century' if y<2000 else 'contemporary'

def main():
    canonical=json.loads(CANON.read_text()); taxonomy=json.loads(CLASS.read_text())
    works=canonical.get('works') or {}; counts=Counter(); language_counts=Counter(); era_counts=Counter(); author_counts=Counter(); refs=[]
    valid={c['id'] for r in taxonomy['roots'] for c in r.get('children',[])}
    parent={c['id']:r['id'] for r in taxonomy['roots'] for c in r.get('children',[])}
    for wid,w in works.items():
        t=work_text(w); scored=[]
        for cid,terms in TERMS.items():
            score=sum(1 for term in terms if term in t)
            if score:scored.append((score,cid))
        scored.sort(key=lambda x:(-x[0],x[1])); leaf=[cid for _,cid in scored[:4] if cid in valid]; roots=[]
        for cid in leaf:
            counts[cid]+=1
            if parent[cid] not in roots:roots.append(parent[cid])
        for r in roots:counts[r]+=1
        ls=langs(w)
        for x in ls:language_counts[x]+=1
        e=era(w.get('firstPublishYear') or w.get('year'));era_counts[e]+=1
        aa=w.get('authors') or []
        if isinstance(aa,str):aa=[aa]
        for a in aa:
            if a:author_counts[str(a)]+=1
        density=len(leaf)
        refs.append({'workId':wid,'classification':{'roots':roots,'leaves':leaf},'facets':{'languages':ls,'period':e},'wall':{'span':2 if density>=3 else 1,'weight':min(4,max(1,density)),'trackSeed':sum(map(ord,wid))%7}})
    roots=[]
    for r in taxonomy['roots']:
        roots.append({'id':r['id'],'label':r['label'],'workCount':counts[r['id']], 'children':[{'id':c['id'],'label':c['label'],'workCount':counts[c['id']]} for c in r.get('children',[])]})
    payload={'schema':'dawn.library.living-library.v2','identityAuthority':'Dawn','projectionOnly':True,'admissionAuthority':False,'canonicalWorkCount':len(works),'classification':{'kind':'dawn-knowledge-map','roots':roots},'facets':{'languages':dict(language_counts.most_common()),'periods':dict(era_counts.most_common()),'authors':[{'value':k,'count':v} for k,v in author_counts.most_common(1000)]},'livingWall':{'grammar':'weighted-multi-track-8:5','trackCount':7,'motionContract':{'flow':'continuous','focus':'decelerate-neighbours','resume':'rejoin-flow','reducedMotion':'static-weighted-grid'},'workRefs':refs},'editorialLayers':{'threeMorningStars':'independent','curatedCollections':'independent','spectrum':'independent'}}
    assert payload['canonicalWorkCount']==len(refs)==len(works)
    assert all(x['workId'] in works for x in refs)
    assert all(cid in valid for x in refs for cid in x['classification']['leaves'])
    OUT.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n')
    print(json.dumps({'canonicalWorkCount':len(works),'classifiedWorks':sum(bool(x['classification']['leaves']) for x in refs),'leafNodes':len(valid),'livingWallRefs':len(refs)},ensure_ascii=False))
if __name__=='__main__':main()
