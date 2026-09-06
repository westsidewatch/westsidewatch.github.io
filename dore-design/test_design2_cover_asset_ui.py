#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R/'design2_cover_asset_ui.py').read_text();app=(R/'app_visual_v2.py').read_text()
for token in ('Place artwork','Replace selected','Full bleed','Inside frame','Apply fit','Apply crop',"role:'cover-art'",'crop_x','crop_y'):assert token in s,token
for token in ('design2_cover_asset_ui.install',"geometry+arrange+cover-image","frame+local-image+cover-art"):assert token in app,token
print('PASS cover image tool contract')
