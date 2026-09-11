#!/usr/bin/env python3
"""Acceptance for Candidate 01 — live 4W Living Editorial River."""
import candidate01_visual_graph_experiment as candidate

assert candidate.EDITORIAL_DIRECTOR['schema']=='dore.visual-editorial-director.v1'
assert candidate.EDITORIAL_DIRECTOR['source_issue']==643
assert candidate.EDITORIAL_DIRECTOR['selection']=='sitewide-highlight'
assert candidate.EDITORIAL_DIRECTOR['classification']=='4w-fuzzy-affinity'
assert candidate.EDITORIAL_DIRECTOR['weight_meaning']=='visual+reading+temporal-capacity'
assert candidate.EDITORIAL_DIRECTOR['world_interface']=='dore.world-surface/1'
assert candidate.EDITORIAL_DIRECTOR['principle']=='editorial judgment, not popularity ranking'

assert candidate._POOL is candidate.SITEWIDE.candidates
assert candidate.SITEWIDE.diagnostics['journal']['count']==0
assert tuple(candidate.ROWS)==('WATCH','WITNESS','WALK','WORSHIP')
assert all(len(items)==4 for items in candidate.ROWS.values()), {k:len(v) for k,v in candidate.ROWS.items()}
items=[item for row in candidate.ROWS.values() for item in row]
assert len(items)==16
assert len({item['id'] for item in items})==16
assert all(item['id'].startswith('site:') for item in items)
assert all('affinity' in item and 'brightness' in item and 'editorial_score' in item and 'editorial_reason' in item for item in items)
assert all(item['provenance'].get('path') for item in items)
assert {item['weight'] for item in items} <= {1,2,3}
assert all(item['shape'] in {'wide','standard','portrait'} for item in items)
assert not any(item['id'] in {'watch-dawn','galilee-storm','remembered-people','one-outpost','maranatha'} for item in items)

runtime=candidate.script(('WATCH','WITNESS'))
assert "setTimeout(()=>card.classList.add('is-reading'),500)" in runtime
assert 'lw-reader-flow' in runtime
assert 'overflow-x:auto' in candidate.STYLE
assert 'dore-world-enter' in runtime
assert 'DIRECTOR.world_interface' in runtime
assert 'SECOND LAYER' in runtime
assert 'editorialHasVisual' in runtime
assert 'img&&hasVisual' in runtime
assert 'data-editorial-has-visual="false"' in candidate.STYLE

screen2=candidate.focus_screen(2,('第一樂章 WATCH','第二樂章 WITNESS'))
screen3=candidate.focus_screen(3,('第三樂章 WALK','第四樂章 WORSHIP'))
for screen,no in ((screen2,2),(screen3,3)):
    assert f'data-screen="{no}"' in screen
    assert 'data-editorial-director="dore.visual-editorial-director.v1"' in screen
    assert '4W Living Editorial River' in screen
    assert '<iframe' in screen

# Second layer is deliberately still an interface only in this cut.
assert 'world-surface' not in candidate.STYLE
assert 'data-second-layer-world' not in screen2+screen3

print('DORE_CANDIDATE01_4W_LIVING_EDITORIAL_RIVER_PASS')
