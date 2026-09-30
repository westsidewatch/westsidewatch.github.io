#!/usr/bin/env python3
"""Fail when implementation / engineering copy leaks into public-facing pages.

Public UI may describe books, people, places, subjects and reader actions. It must
not explain how the site is built, wired, staged, migrated or planned.
"""
from pathlib import Path
import re, sys

ROOT=Path(__file__).resolve().parents[1]
SURFACES=(ROOT/'static',ROOT/'layouts',ROOT/'content')
EXT={'.html','.htm','.md','.js','.mjs','.jsx','.ts','.tsx','.json'}
# Deliberately narrow, high-signal phrases. Internal docs/scripts are outside SURFACES.
FORBIDDEN=(
 r'canonical\s*(?:館藏|資料|data|work)',
 r'不另建第二套資料',
 r'第二套資料',
 r'layout\s*重建',
 r'最終索引密度',
 r'第三頁需求',
 r'先恢復結構',
 r'materialize',
 r'Doré Language Runtime',
 r'正在同步\s*canonical',
 r'READING\s*·\s*RESOLVING',
 r'AUTHORITY\s*·\s*RESOLVED',
 r'TRANSLATION\s*·\s*\$\{',
 r'後臺',r'backend',r'workflow',r'shard(?:s)?',r'renderer lifecycle',
)
rx=re.compile('|'.join(f'(?:{x})' for x in FORBIDDEN),re.I)
fail=[]
for base in SURFACES:
    if not base.exists(): continue
    for p in base.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in EXT: continue
        # Data contracts are not rendered copy; the boundary applies to public surfaces.
        rel=p.relative_to(ROOT)
        if any(part in {'canonical','resource-fabric','cover-preview','contracts','schemas'} for part in rel.parts): continue
        try:text=p.read_text('utf-8')
        except UnicodeDecodeError:continue
        for n,line in enumerate(text.splitlines(),1):
            if rx.search(line):fail.append(f'{rel}:{n}: {rx.search(line).group(0)}')
if fail:
    print('PUBLIC COPY BOUNDARY: FAIL')
    print('\n'.join(fail[:200]))
    print(f'\n{len(fail)} implementation-language leak(s) found.')
    sys.exit(1)
print('PUBLIC COPY BOUNDARY: PASS')
