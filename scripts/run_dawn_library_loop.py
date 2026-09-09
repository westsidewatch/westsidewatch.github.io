#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'static/dawn-library/biblical-world/catalog.json'
COLLECTIONS=ROOT/'static/dawn-library/collections.json'
REPORT=ROOT/'reports/DAWN-LIBRARY-LOOP.json'

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
registry['generatedAt']=now
COLLECTIONS.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
report={
 'schema':'dawn.library.loop.report.v1','generatedAt':now,
 'results':{
   'books':{'published':len(items),'verified':len(verified),'pending':len(pending),'relations':len(relations),'providers':providers},
   'collections':[{'id':c['id'],'kind':c['kind'],'status':c['status'],'output':c.get('output')} for c in registry['collections']]
 },
 'pendingBooks':[{'id':b.get('id'),'title':b.get('work',{}).get('title'),'reason':'missing verified public source'} for b in pending],
 'invariant':'A Dawn Library loop is successful only when it leaves inspectable persisted output.'
}
REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report['results'],ensure_ascii=False,indent=2))
