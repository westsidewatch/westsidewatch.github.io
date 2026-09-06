#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-DEPLOY-NEXT').read_text().strip()=='deploy'
print('PASS deployment next final')
