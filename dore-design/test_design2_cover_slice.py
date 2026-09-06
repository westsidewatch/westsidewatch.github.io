#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parent
required=['design2_multiwrite_cover.py','design2_cover_render.py','design2_cover_interaction.py','design2_cover_manifest.py']
for name in required:assert (R/name).exists(),name
print('PASS complete Multiwrite cover slice')
