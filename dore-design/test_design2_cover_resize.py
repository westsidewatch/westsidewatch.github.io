#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'design2_cover_interaction.py').read_text()
for token in ("['nw','n','ne','e','se','s','sw','w']","kind:'resize'","shiftKey","nwse-resize","nesw-resize","ew-resize","ns-resize", "patch={x:sel.offsetLeft,y:sel.offsetTop,w:sel.offsetWidth,h:sel.offsetHeight}"):
    assert token in s,token
print('PASS cover eight-handle resize contract')
