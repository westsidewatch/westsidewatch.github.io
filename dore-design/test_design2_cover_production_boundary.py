#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'DESIGN-2-COVER-PRODUCTION.md').read_text();assert 'Mac result' in s and 'not this document' in s
print('PASS production boundary')
