#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-END-SOURCE').read_text().strip()=='end-source'
print('PASS definitive end source')
