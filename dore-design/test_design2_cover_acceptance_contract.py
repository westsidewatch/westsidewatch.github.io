#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parent
for f in ('design2_multiwrite_cover.py','design2_cover_render.py','design2_cover_interaction.py','app_visual_v2.py'):assert (R/f).exists()
app=(R/'app_visual_v2.py').read_text()
for token in ("SUPPORTED.update({'multiwrite-home','multiwrite-cover'})","multiwrite_cover_editor':'/editor?page=multiwrite-cover'","assets':'frame+local-image'"):assert token in app,token
print('PASS visible Multiwrite cover acceptance contract')
