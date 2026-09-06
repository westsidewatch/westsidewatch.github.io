#!/usr/bin/env python3
"""Static smoke checks for native arrangement math and persistence surface."""
from pathlib import Path
s=(Path(__file__).resolve().parent/'design2_layer_ops.py').read_text()
checks=['(min(xs)+max(rights)-w0)/2','(canvas_w-float(n.get(\'w\',0)))/2','gap=(end-start-total)/(len(ordered)-1)','pos+=float(n.get(\'w\',0))+gap','return base.save(w)']
for x in checks:assert x in s,x
print('PASS design2 arrange math smoke')
