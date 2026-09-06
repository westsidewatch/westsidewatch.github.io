#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'design2_multiwrite_cover.py').read_text()
for token in ("'canvas':{'w':1200,'h':1500}","'role':'frame'","'semantic_zone':'cover-title'","'size':108","w['pages'].insert(0,p)","return base.save(w)"):
    assert token in s,token
print('PASS Multiwrite cover workspace geometry')
