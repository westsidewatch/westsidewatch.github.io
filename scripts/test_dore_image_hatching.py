#!/usr/bin/env python3
"""Test real grayscale input to three deterministic vector hatching styles."""
import importlib.util,tempfile,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('hatching',root/'scripts/dore_image_hatching.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as d:
    p=Path(d)/'test.pgm'
    p.write_bytes(b'P2\n# fixture\n24 24\n255\n'+(' '.join(str(min(255,int(((x-12)**2+(y-12)**2)**0.5*15))) for y in range(24) for x in range(24))).encode())
    w,h,pixels=m.read_pgm(p)
    assert (w,h)==(24,24)
    for style in ('parallel','cross','wood'):
        a=m.engrave(w,h,pixels,style,3)
        b=m.engrave(w,h,pixels,style,3)
        assert a==b and a.count('<path')>0 and '#CEBD74' not in a
        print(style,len(a),hashlib.sha256(a.encode()).hexdigest()[:12])
    try:m.engrave(w,h,pixels,spacing=0)
    except ValueError:pass
    else:raise AssertionError('bad spacing accepted')
print('PASS: raster-to-hatch deterministic SVG contract')
