#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
index=(ROOT/'cinema/index.html').read_text()
policy=(ROOT/'cinema/special-resource-policy.js').read_text()
goodtv=(ROOT/'cinema/goodtv/index.html').read_text()
assert 'special-resource-policy.js' in index
assert index.index('special-resource-policy.js') < index.index('cinema.js')
assert 'goodtv/' in index
assert 'cinema:video:goodtv:holy-spirit-power-workplace-testimony' in policy
assert 'video-resource.v0.json' in policy and 'bible-media-coordinate.v0.json' in policy
assert 'payload.items=api.filter(payload.items)' in policy
assert '不計入天堂電影院的 canonical media resource framework' in goodtv
assert 'https://www.goodtv.tv/watch?episode=81076&series=196524&type=2' in goodtv
assert '不擷取、不重託管' in goodtv
print('PARADISE_CINEMA_SPECIAL_SOURCE_BOUNDARY=PASS')
