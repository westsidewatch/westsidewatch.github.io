#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-PREDEPLOY-DONE').read_text().strip()=='done'
print('PASS predeploy done')
