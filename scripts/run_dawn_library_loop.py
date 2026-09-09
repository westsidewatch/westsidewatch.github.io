#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'static/dawn-library/biblical-world/catalog.json'
COLLECTIONS=ROOT/'static/dawn-library/collections.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-LOOP.json'
HISTORY=ROOT/'reports/DAWN-LIBRARY-GROWTH.json'

catalog=json.loads(CATALOG.read_text())
registry=json.loads(COLLECTIONS.read_text())
items=catalog.get('items',[])
verified=[b for b in items if b.get('edition',{}).get('publicDomain') is True and b.get('sources')]
pending=[b for b in items if b not in verified]
relations=sorted({r for b in items for r in b.get('relations',[])})
providers=sorted({s.get('provider') for b in items for s in b.get('sources',[]) if s.get('provider')})
book_state=next(c for c in registry['collections'] if c['id']=='biblical-world-books')
book_state.update(published=len(items),verified=len(verified),pending=len(pending))
now=datetime.now(timezone.utc).isoformat()
today=now[:10]
registry['generatedAt']=now

history={'schema':'dawn.library.growth.v1','days':[]}
if HISTORY.exists():
    history=json.loads(HISTORY.read_text())
previous=history.get('days',[])[-1] if history.get('days') else None
snapshot={'date':today,'books':len(items),'verifiedBooks':len(verified),'relations':len(relations)}
if previous:
    snapshot['growth']={
      'books':len(items)-previous.get('books',0),
      'verifiedBooks':len(verified)-previous.get('verifiedBooks',0),
      'relations':len(relations)-previous.get('relations',0)
    }
else:
    snapshot['growth']={'books':len(items),'verifiedBooks':len(verified),'relations':len(relations)}
# One canonical snapshot per UTC day; reruns update rather than inflate history.
days=[d for d in history.get('days',[]) if d.get('date')!=today]
days.append(snapshot)
history['days']=days[-90:]
recent=history['days'][-7:]
avg_growth=sum(d.get('growth',{}).get('verifiedBooks',0) for d in recent)/max(len(recent),1)
# Cadence is a signal consumed by scheduling policy; GitHub cron remains daily during bootstrap.
if len(verified)<100 or avg_growth>=1:
    cadence='daily'
elif len(verified)<500 or avg_growth>=0.25:
    cadence='3x-week'
else:
    cadence='weekly'
book_state['cadence']={'recommended':cadence,'recentVerifiedGrowthPerRun':round(avg_growth,3),'density':len(verified)}

COLLECTIONS.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
HISTORY.parent.mkdir(parents=True,exist_ok=True)
HISTORY.write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n')
report={
 'schema':'dawn.library.loop.report.v1','generatedAt':now,
 'results':{
   'books':{'published':len(items),'verified':len(verified),'pending':len(pending),'relations':len(relations),'providers':providers},
   'growthToday':snapshot['growth'],
   'cadence':book_state['cadence'],
   'collections':[{'id':c['id'],'kind':c['kind'],'status':c['status'],'output':c.get('output')} for c in registry['collections']]
 },
 'pendingBooks':[{'id':b.get('id'),'title':b.get('work',{}).get('title'),'reason':'missing verified public source'} for b in pending],
 'invariant':'A Dawn Library loop is successful only when it leaves inspectable persisted output and a comparable growth snapshot.'
}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report['results'],ensure_ascii=False,indent=2))
