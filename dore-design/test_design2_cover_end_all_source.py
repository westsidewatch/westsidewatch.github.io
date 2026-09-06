#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-END-ALL-SOURCE').read_text().strip()=='end'
print('PASS end all source work')
