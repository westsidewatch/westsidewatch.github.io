#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
journey=json.loads((ROOT/'cinema/data/bible-journey.v0.json').read_text())
projection=json.loads((ROOT/'cinema/data/bible-journey-moment.v0.json').read_text())
moments=json.loads((ROOT/'cinema/data/video-moment.v0.json').read_text())
assert journey['schema']=='dore.bible-journey.v0'
assert projection['schema']=='dore.bible-journey-moment.v0'
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

moment_by_id={m['momentId']:m for m in moments['items']}
station_ids={s['stationId'] for s in stations}
assert projection['items'], 'Journey exact Moment projection must not be empty'
for rel in projection['items']:
    assert rel['journeyId']==item['journeyId']
    assert rel['stationId'] in station_ids
    assert rel['momentId'] in moment_by_id
    assert moment_by_id[rel['momentId']]['kind']=='official-episode'
    assert rel['basis']['kind']=='biblical-event-alignment'

expected={
    'incarnation':('cinema:moment:lumo-matthew:episode-01','Matt.1.1-2.23'),
    'baptism':('cinema:moment:lumo-matthew:episode-02','Matt.3.1-4.25'),
    'cross':('cinema:moment:lumo-matthew:episode-24','Matt.27.32-28.20'),
    'resurrection':('cinema:moment:lumo-matthew:episode-24','Matt.27.32-28.20'),
}
by_station={}
for rel in projection['items']:
    by_station.setdefault(rel['stationId'],[]).append(rel)
for station_id,(moment_id,scripture) in expected.items():
    assert len(by_station.get(station_id,[]))==1
    rel=by_station[station_id][0]
    assert rel['momentId']==moment_id
    assert rel['basis']['scripture']==scripture

assert set(expected) <= set(by_station)
assert len(projection['items']) >= 4

graph=(ROOT/'cinema/resource-graph.js').read_text()
index=(ROOT/'cinema/index.html').read_text()
layer=(ROOT/'cinema/journey-layer.js').read_text()
style=(ROOT/'cinema/journey-layer.css').read_text()
assert "journeys:'data/bible-journey.v0.json'" in graph
assert "journeyMoments:'data/bible-journey-moment.v0.json'" in graph
assert "JOURNEY_MOMENT_SCHEMA='dore.bible-journey-moment.v0'" in graph
assert "journey(journeyId)" in graph
assert "queryStation(journeyId,stationId)" in graph
assert "mediaState=exactMoments.length?'exact':(relatedWorks.length?'available':'unmapped')" in graph
assert 'projectionByStation' in graph
assert 'exactMoments' in graph
assert 'stationMatchesWork' in graph
assert 'journey-layer.css' in index
assert 'journey-layer.js' in index
assert 'id="cinema-journey"' in index
assert "cinema:journey:creation-to-new-creation" in layer
assert 'station.exactMoments?.length' in layer
assert 'graph.deepLink(moment.momentId)' in layer
assert '精確影像' in layer
assert "cinemaJourney='creation-to-new-creation-v1'" in layer
assert "終點已建立；影像座標尚待可靠來源。" in layer
assert '不虛構' in layer
assert 'journey-station[data-terminal="true"]' in style
print('PARADISE_CINEMA_BIBLE_JOURNEY=PASS stations=%d exact=%d core=%d terminal=new-creation' % (len(stations),len(projection['items']),len(expected)))
