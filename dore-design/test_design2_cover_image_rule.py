#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'DESIGN-2-COVER-IMAGE.md').read_text()
assert 'never replaces the editable cover structure' in s and 'independent Design nodes' in s
print('PASS cover artwork rule')
