#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'DESIGN-2-COVER-ROLL-OUT.md').read_text()
for token in ('ok:true','status:completed','Phase 6','acceptance endpoint'):assert token in s
print('PASS cover rollout contract')
