#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
journey=json.loads((ROOT/'cinema/data/bible-journey.v0.json').read_text())
assert journey['schema']=='dore.bible-journey.v0'
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

graph=(ROOT/'cinema/resource-graph.js').read_text()
index=(ROOT/'cinema/index.html').read_text()
layer=(ROOT/'cinema/journey-layer.js').read_text()
style=(ROOT/'cinema/journey-layer.css').read_text()
assert "journeys:'data/bible-journey.v0.json'" in graph
assert "journey(journeyId)" in graph
assert "queryStation(journeyId,stationId)" in graph
assert "mediaState:relatedWorks.length?'available':'unmapped'" in graph
assert 'stationMatchesWork' in graph
assert 'journey-layer.css' in index
assert 'journey-layer.js' in index
assert 'id="cinema-journey"' in index
assert "cinema:journey:creation-to-new-creation" in layer
assert "終點已建立；影像座標尚待可靠來源。" in layer
assert '不虛構' in layer
assert 'journey-station[data-terminal="true"]' in style
print('PARADISE_CINEMA_BIBLE_JOURNEY=PASS stations=%d terminal=new-creation' % len(stations))
