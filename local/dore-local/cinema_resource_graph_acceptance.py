#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
resources=json.loads((ROOT/'cinema/data/video-resource.v0.json').read_text())
moments=json.loads((ROOT/'cinema/data/video-moment.v0.json').read_text())
coordinates=json.loads((ROOT/'cinema/data/bible-media-coordinate.v0.json').read_text())
journeys=json.loads((ROOT/'cinema/data/bible-journey.v0.json').read_text())
journey_moments=json.loads((ROOT/'cinema/data/bible-journey-moment.v0.json').read_text())
graph=(ROOT/'cinema/resource-graph.js').read_text()
cinema=(ROOT/'cinema/cinema.js').read_text()
coord=(ROOT/'cinema/coordinate-layer.js').read_text()
preview=(ROOT/'cinema/preview-controller.js').read_text()
index=(ROOT/'cinema/index.html').read_text()

SPECIAL={'cinema:video:goodtv:holy-spirit-power-workplace-testimony'}
raw={item['canonicalId']:item for item in resources['items']}
admitted={key:value for key,value in raw.items() if key not in SPECIAL}
coord_ids={item['canonicalId'] for item in coordinates['items'] if item['canonicalId'] not in SPECIAL}
moment_ids={item['workId'] for item in moments['items']}

assert resources['schema']=='holy-light.video-resource.v0'
assert moments['schema']=='dore.bible-media-moment.v1'
assert coordinates['schema']=='dore.bible-media-coordinate.v0'
assert journeys['schema']=='dore.bible-journey.v0'
assert journey_moments['schema']=='dore.bible-journey-moment.v0'
assert len(raw)==11 and len(admitted)==10
assert coord_ids==set(admitted)
assert moment_ids <= set(admitted)
assert all(item['rights']['rehost'] is False for item in admitted.values())
assert 'wikisource' not in json.dumps([resources,coordinates,moments,journeys,journey_moments]).lower()

assert "SCHEMA='dore.bible-media-graph.v0'" in graph
assert "MOMENT_SCHEMA='dore.bible-media-moment.v1'" in graph
assert "JOURNEY_MOMENT_SCHEMA='dore.bible-journey-moment.v0'" in graph
assert "graphType:'work'" in graph
assert "canonical:Object.freeze({id:resource.canonicalId,kind:'work'})" in graph
assert 'mediaCoordinate:Object.freeze' in graph
assert 'queryCoordinate(type,value)' in graph
assert 'queryMoments=' in graph
assert 'momentsForAnchor(type,value)' in graph
assert 'deepLink=momentId' in graph
assert 'projectionByStation' in graph
assert 'exactMoments' in graph
assert 'ParadiseCinemaSpecialResources' in graph
assert 'Promise.all([fetchJson(URLS.resources),fetchJson(URLS.moments),fetchJson(URLS.coordinates),fetchJson(URLS.journeys),fetchJson(URLS.journeyMoments)])' in graph
assert 'resource-graph.js' in index
assert "window.ParadiseCinemaGraph?.ready" in cinema
assert "cinemaResourceAuthority='dore.bible-media-graph.v0'" in cinema
assert "cinemaMomentAuthority=graph.momentSchema" in cinema
assert 'restoreMomentFromUrl' in cinema
assert "window.ParadiseCinemaGraph?.ready" in coord
assert "cinemaCoordinateAuthority='dore.bible-media-graph.v0'" in coord
assert "window.ParadiseCinemaGraph?.ready" in preview
assert "cinemaPreviewAuthority='dore.bible-media-graph.v0'" in preview
assert "fetch('data/video-resource.v0.json'" not in cinema
assert "fetch(DATA_URL" not in coord
assert "fetch('data/video-resource.v0.json'" not in preview

print('PARADISE_CINEMA_RESOURCE_GRAPH=PASS works=10 moments=%d journeys=%d exactJourneyMoments=%d special=1' % (len(moments['items']),len(journeys['journeys']),len(journey_moments['items'])))
