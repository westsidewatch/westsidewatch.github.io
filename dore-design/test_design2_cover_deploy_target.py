#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-DEPLOY-TARGET').read_text().strip()=='multiwrite-cover'
print('PASS cover deploy target')
