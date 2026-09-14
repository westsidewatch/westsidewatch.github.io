#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
journey_payload=json.loads((ROOT/'cinema/data/bible-journey.v0.json').read_text())
journey=journey_payload['journeys'][0]
moments=json.loads((ROOT/'cinema/data/video-moment.v0.json').read_text())['items']
event_payload=json.loads((ROOT/'data/bible-index/biblical-event.v1.json').read_text())
events=event_payload['items']
expected={'incarnation':('bible:event:incarnation','cinema:moment:lumo-matthew:episode-01'),'baptism':('bible:event:baptism-of-jesus','cinema:moment:lumo-matthew:episode-02'),'cross':('bible:event:crucifixion','cinema:moment:lumo-matthew:episode-24'),'resurrection':('bible:event:resurrection','cinema:moment:lumo-matthew:episode-24')}
alias={a:e['eventId'] for e in events for a in [e['canonicalKey'],*e['aliases']]}
assert event_payload['authority']=='bible-index'
assert journey_payload['exactMomentOverrides']==[]
assert not (ROOT/'cinema/data/bible-journey-moment.v0.json').exists()
for station_id,(event_id,moment_id) in expected.items():
    station=next(s for s in journey['stations'] if s['stationId']==station_id)
    assert station['eventId']==event_id
    hits=[]
    for moment in moments:
        if moment['kind']!='official-episode':continue
        moment_event_ids={alias[a['value']] for a in moment.get('anchors',[]) if a['type']=='event' and a['value'] in alias}
        if event_id in moment_event_ids:hits.append(moment['momentId'])
    assert hits==[moment_id],(station_id,hits)
graph=(ROOT/'cinema/resource-graph.js').read_text();index=(ROOT/'cinema/index.html').read_text()
assert "EVENT_SCHEMA='dore.biblical-event.v1'" in graph;assert "events:'../data/bible-index/biblical-event.v1.json'" in graph;assert 'stationMatchesMoment' in graph;assert 'resolveEvent' in graph
assert "stationEvent=station=>station.eventId?eventById.get(station.eventId)||null:null" in graph
assert "exactSource=override.length?'editorial-override':(derived.length?'canonical-biblical-event':'none')" in graph
assert "dataset.cinemaJourneyDerivation='canonical-event-id-v1'" in graph
assert 'journeyMoments' not in graph and 'JOURNEY_MOMENT_SCHEMA' not in graph
assert 'journey-anchor-derivation.js' not in index;assert not (ROOT/'cinema/journey-anchor-derivation.js').exists()
assert any(a['type']=='event' and a['value']=='incarnation' for a in next(m for m in moments if m['momentId']==expected['incarnation'][1])['anchors'])
print('PARADISE_CINEMA_JOURNEY_GRAPH_DERIVATION=PASS core=4 authority=bible-index overrides=0 identity=eventId compatibility=closed fake_timecodes=0')
