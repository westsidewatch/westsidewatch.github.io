#!/usr/bin/env python3
"""Export admitted observation evidence. Exports are interchange surfaces, never canonical authority."""
import json, sys
from pathlib import Path

def claims(obs):
    for layer in ('visualFacts','componentGrammar','compositionGrammar','editorialGrammar','motionGrammar','responsiveBehavior','inferredRationale'):
        for c in obs.get(layer,[]): yield layer,c

def main(argv):
    if len(argv)<3:
        print('usage: export_design_evidence.py evidence.json output-dir'); return 1
    src=Path(argv[1]); out=Path(argv[2]); out.mkdir(parents=True,exist_ok=True)
    e=json.loads(src.read_text())
    if e.get('schema')!='dore.design-observation-evidence.v1': print('FAIL: wrong evidence schema'); return 1
    a=e.get('authority',{})
    if a.get('mayPromoteCanonical') is not False or a.get('requiresBeautifulGate') is not True: print('FAIL: authority boundary'); return 1
    lines=['# DESIGN.md','', '> Doré observational export. Evidence, not canonical design authority.','',f"Source: {e.get('source',{}).get('url',e.get('source',{}).get('id','unknown'))}",'','## Observations','']
    for layer,c in claims(e.get('observations',{})):
        lines += [f"### {layer}",f"- {c.get('statement','')} (confidence: {c.get('confidence','n/a')})",f"  - evidence: {', '.join(c.get('evidenceRefs',[]))}",'']
    (out/'DESIGN.md').write_text('\n'.join(lines))
    # Token export is intentionally conservative: only explicitly structured visualFacts tokens are exported.
    tokens={}
    for item in e.get('observations',{}).get('visualFacts',[]):
        if isinstance(item,dict) and 'token' in item and 'value' in item: tokens[item['token']]=item['value']
    (out/'design.tokens.json').write_text(json.dumps({'schema':'dore.design-token-export.v1','authority':'export-only','tokens':tokens},ensure_ascii=False,indent=2))
    print(f"PASS: exported DESIGN.md and {len(tokens)} explicit tokens; no inferred token values.")
    return 0
if __name__=='__main__': sys.exit(main(sys.argv))
