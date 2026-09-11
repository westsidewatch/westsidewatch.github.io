#!/usr/bin/env python3
"""Static/runtime contract acceptance for Candidate 01 — 4W Living Editorial River."""
import candidate01_visual_graph_experiment as candidate

assert candidate.EDITORIAL_DIRECTOR == {
    'schema':'dore.visual-editorial-director.v1',
    'source_issue':643,
    'selection':'sitewide-highlight',
    'classification':'4w-fuzzy-affinity',
    'weight_meaning':'visual+reading+temporal-capacity',
    'world_interface':'dore.world-surface/1',
}
assert tuple(candidate.ROWS) == ('WATCH','WITNESS','WALK','WORSHIP')
assert all(len(items)==4 for items in candidate.ROWS.values())
items=[item for row in candidate.ROWS.values() for item in row]
assert len(items)==16
assert {item['weight'] for item in items} == {1,2,3}
assert {'wide','standard','portrait'} <= {item['shape'] for item in items}
assert {'journal','one','dawn-library','church','dore-folio'} <= {item['world'] for item in items}

runtime=candidate.script(('WATCH','WITNESS'))
assert "setTimeout(()=>card.classList.add('is-reading'),500)" in runtime
assert "lw-reader-flow" in runtime
assert "overflow-x:auto" in candidate.STYLE
assert "dore-world-enter" in runtime
assert "DIRECTOR.world_interface" in runtime
assert "SECOND LAYER" in runtime

screen2=candidate.focus_screen(2,('第一樂章 WATCH','第二樂章 WITNESS'))
screen3=candidate.focus_screen(3,('第三樂章 WALK','第四樂章 WORSHIP'))
for screen,no in ((screen2,2),(screen3,3)):
    assert f'data-screen="{no}"' in screen
    assert 'data-editorial-director="dore.visual-editorial-director.v1"' in screen
    assert '4W Living Editorial River' in screen
    assert '<iframe' in screen
# This cut defines but does not implement a second-layer immersive world.
assert 'world-surface' not in candidate.STYLE
assert 'data-second-layer-world' not in screen2+screen3

print('DORE_CANDIDATE01_4W_LIVING_EDITORIAL_RIVER_PASS')
