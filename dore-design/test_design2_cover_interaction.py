#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parent;s=(R/'design2_cover_interaction.py').read_text();app=(R/'app_visual_v2.py').read_text()
for token in ('pointerdown','pointermove','pointerup',"op:'set_node'",'ArrowLeft','dore-selection-set'):assert token in s,token
assert 'design2_cover_interaction.augment' in app
assert "multiwrite_cover':'editable-direct-manipulation'" in app
print('PASS Multiwrite cover direct manipulation')
