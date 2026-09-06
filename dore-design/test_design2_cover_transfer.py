#!/usr/bin/env python3
from pathlib import Path
assert (Path(__file__).resolve().parent/'DESIGN-2-COVER-TRANSFER').read_text().strip()=='a2a'
print('PASS A2A transfer')
