from pathlib import Path
import re

PAGE = Path('static/dore-design/living-water-bloom-round2.html').read_text(encoding='utf-8')
SPEC = Path('dore-design/living-water-bloom-round2.v1.json').read_text(encoding='utf-8')

for candidate in ('sacred-threshold', 'living-community', 'quiet-light', 'architectural-bloom'):
    assert f'data-candidate="{candidate}"' in PAGE, candidate
    assert candidate in SPEC, candidate

assert 'productionPromoted:false' in PAGE
assert 'canonicalWorkspaceMutated:false' in PAGE
assert 'beautyFirst:true' in PAGE
assert 'generic-card-grid' in SPEC
assert 'literal-door-illustration' in SPEC
assert 'real-browser-raster' in SPEC
assert 'beautiful-gate' in SPEC
assert 'cross-context-transfer' in SPEC

# Round 02 must be materially divergent, not four palette variants.
assert PAGE.count('grid-template') >= 4
assert 'threshold' in PAGE and 'river' in PAGE and 'quiet' in PAGE and 'assembly' in PAGE

# Production must remain locked; the page is an experiment surface only.
assert not re.search(r'productionPromoted\s*:\s*true', PAGE)

print('DORE_LIVING_WATER_BLOOM_ROUND2=PASS')
