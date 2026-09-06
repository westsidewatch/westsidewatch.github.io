#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-NO-MORE').read_text().strip()=='no-more'
print('PASS no more source changes')
