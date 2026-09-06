#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'DESIGN-2-COVER-PRODUCTION-CHECK.md').read_text()
for x in ('deployed head','Phase 6','acceptance endpoint','visual acceptance'):assert x in s
print('PASS cover production check contract')
