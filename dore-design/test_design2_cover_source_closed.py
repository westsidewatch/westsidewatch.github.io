#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-SOURCE-CLOSED').read_text().strip()=='closed'
print('PASS source closed final')
