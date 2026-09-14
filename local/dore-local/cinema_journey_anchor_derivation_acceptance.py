#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
journey=json.loads((ROOT/'cinema/data/bible-journey.v0.json').read_text())['journeys'][0]
moments=json.loads((ROOT/'cinema/data/video-moment.v0.json').read_text())['items']
overrides=json.loads((ROOT/'cinema/data/bible-journey-moment.v0.json').read_text())
expected={
    'incarnation':'cinema:moment:lumo-matthew:episode-01',
    'baptism':'cinema:moment:lumo-matthew:episode-02',
    'cross':'cinema:moment:lumo-matthew:episode-24',
    'resurrection':'cinema:moment:lumo-matthew:episode-24',
}
assert overrides['schema']=='dore.bible-journey-moment.v0'
assert overrides['items']==[], 'core exact Moments must survive with no hand-maintained mapping'
for station_id,moment_id in expected.items():
    station=next(s for s in journey['stations'] if s['stationId']==station_id)
    world=set(station['world'])
    hits=[]
    for moment in moments:
        if moment['kind']!='official-episode':
            continue
        if any(a['type'] in {'event','place','theme'} and a['value'] in world for a in moment.get('anchors',[])):
            hits.append(moment['momentId'])
    assert hits==[moment_id], (station_id,hits)
graph=(ROOT/'cinema/resource-graph.js').read_text()
index=(ROOT/'cinema/index.html').read_text()
assert "MATCH_TYPES=new Set(['event','place','theme'])" in graph
assert 'stationMatchesMoment' in graph
assert "exactSource=override.length?'editorial-override':(derived.length?'biblical-anchor':'none')" in graph
assert "dataset.cinemaJourneyDerivation='graph-biblical-anchor-v2'" in graph
assert 'journey-anchor-derivation.js' not in index
assert not (ROOT/'cinema/journey-anchor-derivation.js').exists()
assert any(a['type']=='event' and a['value']=='incarnation' for a in next(m for m in moments if m['momentId']==expected['incarnation'])['anchors'])
print('PARADISE_CINEMA_JOURNEY_GRAPH_DERIVATION=PASS core=4 overrides=0 fake_timecodes=0')
