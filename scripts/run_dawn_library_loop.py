#!/usr/bin/env python3
from resource_selection import book_allowed
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'static/dawn-library/biblical-world/catalog.json'
COLLECTIONS=ROOT/'static/dawn-library/collections.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-LOOP.json'
HISTORY=ROOT/'reports/DAWN-LIBRARY-GROWTH.json'
ENG_DISC=ROOT/'reports/DAWN-LIBRARY-DISCOVERY.json'
ZH_DISC=ROOT/'reports/DAWN-LIBRARY-CHINESE-DISCOVERY.json'
ENG_PROMO=ROOT/'reports/DAWN-LIBRARY-ENGLISH-PROMOTION.json'

def load(path,default=None):
    try:return json.loads(path.read_text())
    except Exception:return {} if default is None else default

catalog=json.loads(CATALOG.read_text());registry=json.loads(COLLECTIONS.read_text());items=[i for i in catalog.get('items',[]) if book_allowed(i)]
verified=[b for b in items if b.get('edition',{}).get('publicDomain') is True and b.get('sources')]
pending=[b for b in items if b not in verified]
relations=sorted({r for b in items for r in b.get('relations',[])})
providers=sorted({s.get('provider') for b in items for s in b.get('sources',[]) if s.get('provider')})
book_state=next(c for c in registry['collections'] if c['id']=='biblical-world-books');book_state.update(published=len(items),verified=len(verified),pending=len(pending))
now=datetime.now(timezone.utc).isoformat();today=now[:10];registry['generatedAt']=now
history=load(HISTORY,{'schema':'dawn.library.growth.v2','days':[]}); history['schema']='dawn.library.growth.v2'
prior_days=[d for d in history.get('days',[]) if d.get('date')!=today]
previous=prior_days[-1] if prior_days else None
snapshot={'date':today,'books':len(items),'verifiedBooks':len(verified),'relations':len(relations)}
if previous:
    snapshot['growth']={'books':len(items)-previous.get('books',0),'verifiedBooks':len(verified)-previous.get('verifiedBooks',0),'relations':len(relations)-previous.get('relations',0)}
else:snapshot['growth']={'books':0,'verifiedBooks':0,'relations':0}
# Autonomous growth is deliberately stricter than catalog delta: only works discovered by the loop itself count.
auto_today=[b for b in items if b.get('provenance',{}).get('origin')=='autonomous-discovery' and str(b.get('provenance',{}).get('catalogedAt','')).startswith(today)]
snapshot['autonomousGrowth']={'books':len(auto_today),'titles':[b.get('work',{}).get('title') for b in auto_today]}
days=prior_days+[snapshot];history['days']=days[-90:]
recent=history['days'][-7:];avg_growth=sum(d.get('autonomousGrowth',{}).get('books',0) for d in recent)/max(len(recent),1)
if len(verified)<100 or avg_growth>=1:cadence='daily'
elif len(verified)<500 or avg_growth>=0.25:cadence='3x-week'
else:cadence='weekly'
book_state['cadence']={'recommended':cadence,'recentAutonomousGrowthPerDay':round(avg_growth,3),'density':len(verified)}
eng_disc=load(ENG_DISC);zh_disc=load(ZH_DISC);eng_promo=load(ENG_PROMO)
pipeline={'englishDiscoveredThisRun':eng_disc.get('newDiscovered',0),'chineseDiscoveredThisRun':zh_disc.get('newDiscovered',0),'englishPromotedThisRun':eng_promo.get('promoted',0),'englishPromotedTitles':[x.get('title') for x in eng_promo.get('items',[])]}
COLLECTIONS.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n');HISTORY.parent.mkdir(parents=True,exist_ok=True);HISTORY.write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n')
report={'schema':'dawn.library.loop.report.v2','generatedAt':now,'results':{'books':{'published':len(items),'verified':len(verified),'pending':len(pending),'relations':len(relations),'providers':providers},'catalogDeltaToday':snapshot['growth'],'autonomousGrowthToday':snapshot['autonomousGrowth'],'pipelineThisRun':pipeline,'cadence':book_state['cadence'],'collections':[{'id':c['id'],'kind':c['kind'],'status':c['status'],'output':c.get('output')} for c in registry['collections']]},'pendingBooks':[{'id':b.get('id'),'title':b.get('work',{}).get('title'),'reason':'missing verified public source'} for b in pending],'invariant':'Seed promotion is not autonomous growth. Autonomous growth requires loop discovery provenance plus verified rights and catalog promotion.'}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report['results'],ensure_ascii=False,indent=2))
