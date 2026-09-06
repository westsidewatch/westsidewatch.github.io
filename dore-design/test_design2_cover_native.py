#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'DESIGN-2-COVER-NATIVE.md').read_text()
assert 'canonical structured workspace' in s and 'without flattening' in s
print('PASS native cover architecture')
