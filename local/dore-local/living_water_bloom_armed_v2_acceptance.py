#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
page=(ROOT/'static/dore-design/living-water-bloom-armed-v2.html').read_text(encoding='utf-8')
spec=json.loads((ROOT/'dore-design/living-water-bloom-armed.v2.json').read_text(encoding='utf-8'))
ledger=json.loads((ROOT/'dore-design/design_arsenal_assimilation.v0.json').read_text(encoding='utf-8'))

assert spec['consumer']=='living-water'
assert spec['beauty_admission']['beautiful_is_floor'] is True
assert spec['beauty_admission']['real_browser_raster_required'] is True
assert ledger['research_streams']['italian-editorial']['first_real_consumer']=='living-water'

for candidate in ('sacred-threshold','living-community','quiet-light','architectural-bloom'):
    assert f'data-candidate="{candidate}"' in page

for intent in ('threshold-opening','ceremonial-reveal','architectural-assembly','stillness','measured-drift','kinetic-typography'):
    assert f'data-dore-motion="{intent}"' in page

assert '/images/living-water-west-church-name.png' in page
assert '/images/jerusalem-wall.png' in page
assert './dore-motion.js' in page
assert 'placeholder' not in page.lower()
assert 'FIRST LAYER ONLY' not in page
assert 'generic fade' not in page.lower()
assert 'water-wave' not in page.lower()
assert 'literal door' not in page.lower()
assert 'production_promoted' in json.dumps(spec)
assert spec['production_promoted'] is False

print('LIVING_WATER_BLOOM_ARMED_V2=PASS')
print('CANDIDATES=4')
print('MOTION_POLICY=native-first')
print('PRODUCTION_PROMOTED=false')
