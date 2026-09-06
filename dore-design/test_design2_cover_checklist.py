#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'DESIGN-2-COVER-CHECKLIST.md').read_text()
assert '- [x] direct manipulation' in s and '- [ ] A2A production rollout' in s and '- [ ] human visual acceptance' in s
print('PASS cover checklist boundary')
