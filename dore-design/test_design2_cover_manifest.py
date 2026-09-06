#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parent;s=(R/'design2_cover_manifest.py').read_text();app=(R/'app_visual_v2.py').read_text()
for token in ("'consumer':'multiwrite'","'surface':'cover'","'structured':True","'editor':'/editor?page=multiwrite-cover'"):assert token in s,token
assert "/api/design2/multiwrite-cover" in app
print('PASS Multiwrite cover production manifest')
