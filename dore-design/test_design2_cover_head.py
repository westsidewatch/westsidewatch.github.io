#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'DESIGN-2-COVER-HEAD.md').read_text();assert 'successful older head does not satisfy' in s
print('PASS cover rollout head requirement')
