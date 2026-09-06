#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'DESIGN-2-COVER-FINAL-SOURCE.md').read_text();assert 'Proceed to production rollout' in s
print('PASS source gate closed')
