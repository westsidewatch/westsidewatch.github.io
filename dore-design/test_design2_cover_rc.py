#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-RELEASE-CANDIDATE').read_text().strip()=='rc1'
print('PASS cover rc1')
