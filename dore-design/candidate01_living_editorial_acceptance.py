#!/usr/bin/env python3
"""Acceptance for Candidate 01 — live 4W Living Editorial River."""
import sitewide_editorial_candidates_acceptance  # noqa: F401
import candidate01_visual_graph_experiment as candidate
import design_motion_registry as motion

assert candidate.EDITORIAL_DIRECTOR['schema']=='dore.visual-editorial-director.v1'
assert candidate.EDITORIAL_DIRECTOR['source_issue']==643
assert candidate.EDITORIAL_DIRECTOR['selection']=='sitewide-highlight'
assert candidate.EDITORIAL_DIRECTOR['classification']=='4w-fuzzy-affinity'
assert candidate.EDITORIAL_DIRECTOR['world_interface']=='dore.world-surface/1'
assert tuple(candidate.ROWS)==('WATCH','WITNESS','WALK','WORSHIP')
assert all(len(items)==4 for items in candidate.ROWS.values())
items=[item for row in candidate.ROWS.values() for item in row]
assert len(items)==16 and len({item['id'] for item in items})==16
assert all(item['provenance'].get('path') for item in items)

runtime=candidate.script(('WATCH','WITNESS'))
assert 'lw-reader-flow' in runtime and 'dore-world-enter' in runtime
assert 'aspect-ratio:5/8' not in candidate.STYLE
assert 'aspect-ratio:8/5' in candidate.STYLE
assert 'flex-grow:1.65' not in candidate.STYLE and 'flex-grow:2.35' not in candidate.STYLE and 'flex-grow:3.4' not in candidate.STYLE

# The focus transition must have a visible, reversible geometric source: four
# current cards become four crops of one master image, merge, then reverse.
style=motion._LIVING_CURRENT_STYLE
script=motion._LIVING_CURRENT_SCRIPT
assert '.dore-mosaic-piece' in style
assert '.dore-mosaic-master' in style
assert 'groupFor=card=>' in script
assert 'getBoundingClientRect()' in script
assert 'originRects=group.map' in script
assert 'const slots=[{x:0,y:0},{x:.5,y:0},{x:0,y:.5},{x:.5,y:.5}]' in script
assert 'masterRect=()=>' in script
assert 'buildMosaic' in script
assert 'animatePieces(true)' in script
assert 'animatePieces(false)' in script
assert "setPhase('assemble')" in script
assert "setPhase('focus')" in script
assert "setPhase('release')" in script
assert "mosaic.master.animate([{opacity:0},{opacity:1}]" in script
assert "mosaic.master.animate([{opacity:1},{opacity:0}]" in script
assert "cards.forEach(c=>c.style.visibility='')" in script
assert '@keyframes lw-current-' not in style
assert 'animation:lw-current-' not in style
assert 'requestAnimationFrame(tick)' in script
# The old independent Codrops preview is hidden in Candidate focus screens so a
# second window cannot appear from nowhere on top of the mosaic.
assert '.products__preview{display:none!important}' in motion._CANDIDATE_FOCUS_EMBED_STYLE

screen2=candidate.focus_screen(2,('第一樂章 WATCH','第二樂章 WITNESS'))
screen3=candidate.focus_screen(3,('第三樂章 WALK','第四樂章 WORSHIP'))
for screen,no in ((screen2,2),(screen3,3)):
    assert f'data-screen="{no}"' in screen
    assert 'data-editorial-director="dore.visual-editorial-director.v1"' in screen
    assert '4W Living Editorial River' in screen
    assert '<iframe' in screen
    assert 'dore-mosaic-piece' in screen
    assert 'mosaic-assemble' in screen

assert 'world-surface' not in candidate.STYLE
assert 'data-second-layer-world' not in screen2+screen3
print('DORE_CANDIDATE01_REVERSIBLE_MOSAIC_FOCUS_PASS')
