#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
events=json.loads((ROOT/'cinema/data/biblical-event.v1.json').read_text())
journey=json.loads((ROOT/'cinema/data/bible-journey.v0.json').read_text())
moments=json.loads((ROOT/'cinema/data/video-moment.v0.json').read_text())
overrides=json.loads((ROOT/'cinema/data/bible-journey-moment.v0.json').read_text())
graph=(ROOT/'cinema/resource-graph.js').read_text()
assert events['schema']=='dore.biblical-event.v1'
assert events['authority']=='biblical-event'
assert overrides['items']==[]
by_id={e['eventId']:e for e in events['items']}
assert set(by_id)=={'bible:event:incarnation','bible:event:baptism-of-jesus','bible:event:crucifixion','bible:event:resurrection'}
alias={a:e['eventId'] for e in events['items'] for a in [e['canonicalKey'],*e['aliases']]}
assert alias['baptism']=='bible:event:baptism-of-jesus'
assert alias['cross']=='bible:event:crucifixion'
expected={'incarnation':('bible:event:incarnation','cinema:moment:lumo-matthew:episode-01'),'baptism':('bible:event:baptism-of-jesus','cinema:moment:lumo-matthew:episode-02'),'cross':('bible:event:crucifixion','cinema:moment:lumo-matthew:episode-24'),'resurrection':('bible:event:resurrection','cinema:moment:lumo-matthew:episode-24')}
stations={s['stationId']:s for s in journey['journeys'][0]['stations']}
moment_by_event={}
for m in moments['items']:
    if m['kind']!='official-episode': continue
    for a in m.get('anchors',[]):
        if a['type']=='event' and a['value'] in alias:
            moment_by_event.setdefault(alias[a['value']],[]).append(m['momentId'])
for station_id,(event_id,moment_id) in expected.items():
    station_event=next((alias[w] for w in stations[station_id].get('world',[]) if w in alias),None)
    assert station_event==event_id
    assert moment_id in moment_by_event[event_id]
assert expected['cross'][1]==expected['resurrection'][1]
assert "EVENT_SCHEMA='dore.biblical-event.v1'" in graph
assert "events:'data/biblical-event.v1.json'" in graph
assert "exactSource=override.length?'editorial-override':(derived.length?'canonical-biblical-event':'none')" in graph
assert 'resolveEvent' in graph and 'biblicalEvent' in graph
assert "anchor.type==='event'" in graph
assert "MATCH_TYPES" not in graph
print('PARADISE_CINEMA_BIBLICAL_EVENT_IDENTITY=PASS events=4 core=4 overrides=0 shared_episode24=2')
