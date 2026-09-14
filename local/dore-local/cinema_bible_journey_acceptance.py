#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
journey=json.loads((ROOT/'cinema/data/bible-journey.v0.json').read_text())
moments=json.loads((ROOT/'cinema/data/video-moment.v0.json').read_text())
events=json.loads((ROOT/'data/bible-index/biblical-event.v1.json').read_text())
assert journey['schema']=='dore.bible-journey.v0'
assert journey['exactMomentOverrides']==[]
assert not (ROOT/'cinema/data/bible-journey-moment.v0.json').exists()
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
assert [s['order'] for s in stations]==sorted(s['order'] for s in stations)
assert len({s['stationId'] for s in stations})==len(stations)
by_id={e['eventId']:e for e in events['items']}
alias={a:e['eventId'] for e in events['items'] for a in [e['canonicalKey'],*e['aliases']]}
expected={
    'incarnation':('bible:event:incarnation','cinema:moment:lumo-matthew:episode-01'),
    'baptism':('bible:event:baptism-of-jesus','cinema:moment:lumo-matthew:episode-02'),
    'cross':('bible:event:crucifixion','cinema:moment:lumo-matthew:episode-24'),
    'resurrection':('bible:event:resurrection','cinema:moment:lumo-matthew:episode-24'),
}
for station_id,(event_id,moment_id) in expected.items():
    station=next(s for s in stations if s['stationId']==station_id)
    assert station['eventId']==event_id
    assert event_id in by_id
    hits=[]
    for moment in moments['items']:
        if moment['kind']!='official-episode': continue
        ids={alias[a['value']] for a in moment.get('anchors',[]) if a['type']=='event' and a['value'] in alias}
        if event_id in ids: hits.append(moment['momentId'])
    assert hits==[moment_id], (station_id,hits)
graph=(ROOT/'cinema/resource-graph.js').read_text();index=(ROOT/'cinema/index.html').read_text();layer=(ROOT/'cinema/journey-layer.js').read_text();style=(ROOT/'cinema/journey-layer.css').read_text()
assert "journeys:'data/bible-journey.v0.json'" in graph
assert 'journeyMoments' not in graph and 'JOURNEY_MOMENT_SCHEMA' not in graph
assert "stationEvent=station=>station.eventId?eventById.get(station.eventId)||null:null" in graph
assert 'journeyPayload.exactMomentOverrides' in graph
assert "mediaState=exactMoments.length?'exact':(relatedWorks.length?'available':'unmapped')" in graph
assert "dataset.cinemaJourneyDerivation='canonical-event-id-v1'" in graph
assert 'journey-layer.css' in index and 'journey-layer.js' in index and 'id="cinema-journey"' in index
assert 'station.exactMoments?.length' in layer and 'graph.deepLink(moment.momentId)' in layer and '精確影像' in layer
assert 'journey-station[data-terminal="true"]' in style
print('PARADISE_CINEMA_BIBLE_JOURNEY=PASS stations=%d derived=%d overrides=0 identity=eventId compatibility=closed terminal=new-creation' % (len(stations),len(expected)))
