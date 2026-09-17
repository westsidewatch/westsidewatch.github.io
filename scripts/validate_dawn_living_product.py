#!/usr/bin/env python3
"""Dawn Living Library product acceptance — scale/boundary/static runtime contract."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text())
canonical=load('static/dawn-library/canonical-index.json')
living=load('static/dawn-library/living-library.json')
root=load('static/dawn-library/living/root.json')
taxonomy=load('static/dawn-library/classification.json')
js=(ROOT/'static/dawn-library/product/product.js').read_text()
html=(ROOT/'static/dawn-library/product/index.html').read_text()
runtime=(ROOT/'static/dawn-library/living/runtime.js').read_text()
count=canonical['workCount']
assert count>100_000, f'collection regression: {count}'
assert root['canonicalWorkCount']==living['canonicalWorkCount']==count
assert root['projectionOnly'] is True and root['admissionAuthority'] is False
assert root['loadingContract']['millionCardDom'] is False
assert root['shardSize']<=25_000 and root['shardCount']>=1
assert sum(s['workCount'] for s in root['shards'])==count
assert len(taxonomy['roots'])==7 and taxonomy['admissionAuthority'] is False
# Runtime owns the bounded window/prefetch cache; product owns the seven independent tracks.
assert 'windowCards=84' in runtime and 'prefetchAhead=1' in runtime and 'releaseFarFrom' in runtime
assert 'new DawnLivingWall' in js and 'windowCards:84' in js and 'prefetchAhead:1' in js and 'TRACKS=[' in js
assert 'prefers-reduced-motion' in html and '@media(max-width:680px)' in html
assert 'work-focus' in html and 'focusState' in js and 'relatedRefs' in js
assert 'resourceWorks' in js and '../living/root.json' in js
assert 'openlibrary.org' not in js.lower() and 'wikisource' not in js.lower()
for forbidden in ('admissionAuthority=true','admissionAuthority: true','admissionAuthority = true'):
    assert forbidden not in js
assert not re.search(r'resourceWorks\([^\n]*(canonicalWorkCount|workCount)',js)
print(json.dumps({'status':'PASS','canonicalWorks':count,'livingShards':root['shardCount'],'visibleWindow':84,'tracks':7,'classificationRoots':7,'millionCardDom':False},ensure_ascii=False))
