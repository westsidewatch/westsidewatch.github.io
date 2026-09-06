#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parent
cover=(R/'design2_multiwrite_cover.py').read_text()
app=(R/'app_visual_v2.py').read_text()
for token in ("PAGE_ID='multiwrite-cover'","'name':'多寫 · Cover'","'mwc-frame'","'mwc-title'","'mwc-subtitle'","'mwc-rule'"):
    assert token in cover,token
for token in ("'multiwrite-cover'","multiwrite_cover':'editable-page'","/editor?page=multiwrite-cover"):
    assert token in app,token
print('PASS editable Multiwrite cover contract')
