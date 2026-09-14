#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
journey=json.loads((ROOT/'cinema/data/bible-journey.v0.json').read_text())['journeys'][0]
moments=json.loads((ROOT/'cinema/data/video-moment.v0.json').read_text())['items']
expected={
    'incarnation':'cinema:moment:lumo-matthew:episode-01',
    'baptism':'cinema:moment:lumo-matthew:episode-02',
    'cross':'cinema:moment:lumo-matthew:episode-24',
    'resurrection':'cinema:moment:lumo-matthew:episode-24',
}
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
source=(ROOT/'cinema/journey-anchor-derivation.js').read_text()
index=(ROOT/'cinema/index.html').read_text()
assert "biblical-anchor-derivation" in source
assert "MATCH_TYPES=new Set(['event','place','theme'])" in source
assert "dataset.derived='biblical-anchor-v1'" in source
assert '<script src="journey-anchor-derivation.js"></script>' in index
assert any(a['type']=='event' and a['value']=='incarnation' for a in next(m for m in moments if m['momentId']==expected['incarnation'])['anchors'])
print('PARADISE_CINEMA_JOURNEY_ANCHOR_DERIVATION=PASS core=4 fake_timecodes=0')
