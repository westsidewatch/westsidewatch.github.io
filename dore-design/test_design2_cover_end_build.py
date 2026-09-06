#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-END-BUILD').read_text().strip()=='ended'
print('PASS end build')
