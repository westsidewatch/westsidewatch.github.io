#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Refresh is deliberately pre-canonical. Canonical Resource Fabric may only
# grow through gate_dawn_canonical_promotion.py -> promote_dawn_canonical_batch.py.
STEPS = (
    'scripts/discover_dawn_10k_openlibrary_works.py',
    'scripts/build_dawn_10k_work_queue.py',
    'scripts/build_dawn_resource_queue.py',
)

def run(path: str) -> None:
    subprocess.run([sys.executable, path], cwd=ROOT, check=True)

def main() -> int:
    for step in STEPS:
        run(step)
    source=json.loads((ROOT/'data/dawn-10k-openlibrary-works.json').read_text(encoding='utf-8'))
    queue=json.loads((ROOT/'data/dawn-10k-work-queue.json').read_text(encoding='utf-8'))
    resource_queue=json.loads((ROOT/'data/dawn-resource-queue.json').read_text(encoding='utf-8'))
    canonical_path=ROOT/'static/dawn-library/canonical-resource-index.json'
    canonical=json.loads(canonical_path.read_text(encoding='utf-8')) if canonical_path.exists() else {'resourceCount':0}
    if source.get('contentDownloaded') is not False: raise SystemExit('bulk corpus must remain metadata-only')
    if not (source.get('policy') or {}).get('wikisourceForbidden'): raise SystemExit('Wikisource gate missing')
    if (source.get('metrics') or {}).get('works',0) < 10000: raise SystemExit('bulk corpus below 10k')
    if (source.get('metrics') or {}).get('chineseMatchedWorksAdded',0) < 1: raise SystemExit('Chinese corpus empty')
    if queue.get('deduplicatedWorks',0) < 10000 or queue.get('authorityBackedWorks',0) < 9000: raise SystemExit('queue below accepted bulk baseline')
    if resource_queue.get('resourceCount',0) < queue.get('deduplicatedWorks',0): raise SystemExit('resource queue lost legacy works')
    print(json.dumps({'schema':'dawn.bulk-corpus-refresh.v3','phase':'pre-canonical','sourceWorks':source['metrics']['works'],'chineseWorks':source['metrics']['chineseMatchedWorksAdded'],'queueWorks':queue['deduplicatedWorks'],'authorityBackedWorks':queue['authorityBackedWorks'],'resourceQueue':resource_queue['resourceCount'],'canonicalBaseline':canonical.get('resourceCount',0),'canonicalMutation':'forbidden-before-promotion'},ensure_ascii=False))
    return 0

if __name__=='__main__': raise SystemExit(main())
