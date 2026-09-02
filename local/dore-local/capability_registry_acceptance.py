#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capability_registry import discover,get
registry=json.loads((ROOT/'dore-design'/'knowledge-lab'/'capabilities'/'registry.json').read_text(encoding='utf-8'))
assert registry['schema']=='dore.capability-registry.v1'
search_js=ROOT/'static'/'dore'/'dore-search.js'
assert search_js.exists(),'existing static/dore/dore-search.js must remain present'
text=search_js.read_text(encoding='utf-8')
for marker in ('function parseReference','function interpret','function search'):
 assert marker in text,f'existing Doré Search contract missing: {marker}'
bible=discover(service='bible')
assert {x['id'] for x in bible}>={'bible.scripture-search','bible.original-language-search'}
assert all(x['execution']=='native' for x in bible)
assert all(x['entrypoint']=='/dore/dore-search.js' for x in bible)
assert get('library.books') is None
library=get('library.books',include_planned=True)
assert library and library['status']=='planned' and library['cost']=='free-only'
print('DORE_CAPABILITY_REGISTRY_ACCEPTANCE=PASS')
