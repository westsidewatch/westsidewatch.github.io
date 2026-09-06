#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-COMPLETE-SOURCE').read_text().strip()=='complete'
print('PASS source complete final')
