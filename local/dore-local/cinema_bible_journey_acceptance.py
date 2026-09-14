#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
journey=json.loads((ROOT/'cinema/data/bible-journey.v0.json').read_text())
projection=json.loads((ROOT/'cinema/data/bible-journey-moment.v0.json').read_text())
moments=json.loads((ROOT/'cinema/data/video-moment.v0.json').read_text())
assert journey['schema']=='dore.bible-journey.v0'
assert projection['schema']=='dore.bible-journey-moment.v0'
assert projection['items']==[]
assert journey['reflexPersistent'] is False
assert len(journey['journeys'])==1
item=journey['journeys'][0]
assert item['journeyId']=='cinema:journey:creation-to-new-creation'
stations=item['stations']
assert len(stations)>=11
assert stations[0]['stationId']=='creation'
assert stations[-1]['stationId']=='new-creation'
assert stations[-1]['terminal'] is True
assert 'Rev 21:1-22:5' in stations[-1]['scripture']
assert 'new-heavens-new-earth' in stations[-1]['world']
assert [s['order'] for s in stations]==sorted(s['order'] for s in stations)
assert len({s['stationId'] for s in stations})==len(stations)
expected={
    'incarnation':'cinema:moment:lumo-matthew:episode-01',
    'baptism':'cinema:moment:lumo-matthew:episode-02',
    'cross':'cinema:moment:lumo-matthew:episode-24',
    'resurrection':'cinema:moment:lumo-matthew:episode-24',
}
for station_id,moment_id in expected.items():
    station=next(s for s in stations if s['stationId']==station_id)
    hits=[]
    for moment in moments['items']:
        if moment['kind']!='official-episode':
            continue
        if any(a['type'] in {'event','place','theme'} and a['value'] in station['world'] for a in moment.get('anchors',[])):
            hits.append(moment['momentId'])
    assert hits==[moment_id], (station_id,hits)
graph=(ROOT/'cinema/resource-graph.js').read_text()
index=(ROOT/'cinema/index.html').read_text()
layer=(ROOT/'cinema/journey-layer.js').read_text()
style=(ROOT/'cinema/journey-layer.css').read_text()
assert "journeys:'data/bible-journey.v0.json'" in graph
assert "journeyMoments:'data/bible-journey-moment.v0.json'" in graph
assert "JOURNEY_MOMENT_SCHEMA='dore.bible-journey-moment.v0'" in graph
assert 'stationMatchesMoment' in graph
assert 'overrideByStation' in graph
assert 'exactSource' in graph
assert "mediaState=exactMoments.length?'exact':(relatedWorks.length?'available':'unmapped')" in graph
assert 'journey-layer.css' in index
assert 'journey-layer.js' in index
assert 'journey-anchor-derivation.js' not in index
assert 'id="cinema-journey"' in index
assert 'station.exactMoments?.length' in layer
assert 'graph.deepLink(moment.momentId)' in layer
assert '精確影像' in layer
assert 'journey-station[data-terminal="true"]' in style
print('PARADISE_CINEMA_BIBLE_JOURNEY=PASS stations=%d derived=%d overrides=0 terminal=new-creation' % (len(stations),len(expected)))
