#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
registry=ROOT/'static/dawn-library/cover-registry.json'
data=json.loads(registry.read_text(encoding='utf-8'))
assert data.get('schema')=='dawn.library.cover-registry.v1'
assert data.get('resolvedCount',0)>=1
assert data.get('runtimePolicy',{}).get('browserExternalLookup') is False
covers=data.get('covers') or {}
assert len(covers)==data.get('resolvedCount')
for work_id,row in covers.items():
    pointer=str(row.get('pointer') or '')
    assert pointer.startswith('/dawn-library/covers/'), (work_id,pointer)
    assert (ROOT/'static'/pointer.lstrip('/')).is_file(), pointer
    assert not pointer.startswith(('http://','https://','//'))
print(json.dumps({'resolved':len(covers),'failed':data.get('failedCount',0)}))
