#!/usr/bin/env python3
from pathlib import Path
s=(Path(__file__).resolve().parent/'DESIGN-2-COVER-FIRST-CONSUMER.md').read_text()
for x in ('Pages','structured nodes','direct manipulation','Inspector/Arrange','Frame','local Asset'):assert x in s
print('PASS cover consumer intent')
