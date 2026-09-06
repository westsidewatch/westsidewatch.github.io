#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'DESIGN-2-COVER-SOURCE-PASS.md').read_text();assert 'PASS' in s and 'does not assert production deployment' in s
print('PASS source gate semantics')
