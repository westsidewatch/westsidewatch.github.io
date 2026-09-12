#!/usr/bin/env python3
import candidate01_visual_graph_experiment as candidate
screen2=candidate.focus_screen(2,())
screen3=candidate.focus_screen(3,())
assert 'candidate01-page2-assembly-runtime' in screen2
assert 'candidate01-page2-assembly-runtime' not in screen3
assert 'wantRight' in screen2
assert 'return [p]' not in screen2
assert "translateY(-50%) scale(.94)" not in screen2
assert "translateY(-50%) scale(1)" not in screen2
assert 'translate3d(0,1.25px,0) scale(.998)' in screen2
assert 'colGap' in screen2 and 'rowGap' in screen2
assert 'masterW=maxX-minX-colGap' in screen2
assert 'masterH=maxY-minY-rowGap' in screen2
assert 'masterTop=minY-rr.top+rowGap/2' in screen2
assert 'offset:.82' in screen2
print('DORE_CANDIDATE01_PAGE2_ASSEMBLY_PASS')
