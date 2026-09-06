#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-IMPLEMENTED').read_text().strip()=='implemented'
print('PASS cover implemented marker')
