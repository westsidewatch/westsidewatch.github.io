#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'DESIGN-2-COVER-VISIBLE.md').read_text()
for x in ('多寫 · Cover','Pages','select a cover element','move it'):assert x in s
print('PASS visible cover target')
