#!/usr/bin/env python3
from multiwrite_wysiwyg import render_canvas

html=render_canvas(edit=True)
need=['id="d2-selection"','pointerdown','pointermove','pointerup','data-h="nw"','data-h="se"','op:\'set_node\'','ArrowLeft','ArrowRight','ArrowUp','ArrowDown']
missing=[x for x in need if x not in html]
assert not missing, missing
print('PASS design2 direct manipulation contract')
