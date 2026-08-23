#!/usr/bin/env python3
"""Build Doré BW-1 browser entity index from pinned TIPNR + CUV attestations.

Raw TIPNR is not redistributed. The output contains derived identity records, source
IDs, canonical attestations and conservative Chinese translation aliases inferred
from repeated CUV co-attestation. An inferred alias is routing evidence, not proof
that two source identities are identical.
"""
from __future__ import annotations
import argparse,json,math,re
from collections import Counter
from pathlib import Path
from dore_core.world.tipnr import iter_tipnr_records,to_world_entity,TIPNR_SOURCE

CJK=re.compile(r'[\u3400-\u9fff]+')

def grams(text:str):
    out=set()
    for chunk in CJK.findall(text or ''):
        for n in range(2,6):
            for i in range(max(0,len(chunk)-n+1)):
                out.add(chunk[i:i+n])
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--tipnr',required=True)
    ap.add_argument('--search-index',default='static/dore/search-index.json')
    ap.add_argument('--output',default='static/dore/entity-index.json')
    ap.add_argument('--source-sha',default='unknown')
    args=ap.parse_args()
    scripture=json.loads(Path(args.search_index).read_text(encoding='utf-8'))
    verses=scripture['verses']
    byref={v['r']:v for v in verses}
    verse_grams={v['r']:grams(v.get('z','')) for v in verses if v.get('z')}
    df=Counter(g for gs in verse_grams.values() for g in gs)
    total=max(1,len(verse_grams))
    records=list(iter_tipnr_records(Path(args.tipnr).read_text(encoding='utf-8',errors='replace')))
    entities=[];zh_count=0
    for record in records:
        w=to_world_entity(record,args.source_sha)
        refs=[r for r in record.canonical_refs if r in byref]
        aligned=[verse_grams[r] for r in refs if r in verse_grams]
        zh=[]
        if len(aligned)>=2:
            local=Counter(g for gs in aligned for g in gs)
            required=max(2,math.ceil(len(aligned)*.45))
            scored=[]
            for g,c in local.items():
                if c<required:continue
                coverage=c/len(aligned)
                specificity=math.log((total+1)/(df[g]+1))
                # Prefer complete proper-name forms over their internal substrings.
                score=coverage*specificity*(1+.16*(len(g)-2))
                scored.append((score,len(g),g,c))
            scored.sort(reverse=True)
            if scored:
                best=scored[0][0]
                # Keep a very small routing alias set; longer/more-specific wins ties.
                for score,_,g,c in scored:
                    if score < best*.82 or len(zh)>=3:break
                    if any(g in x and g!=x for x in zh):continue
                    zh.append(g)
        zh_count+=len(zh)
        aliases=[]
        for a in w.aliases:
            aliases.append({'v':a.value,'l':a.language,'k':a.kind,'s':a.source_id,'c':a.confidence})
        for a in zh:
            aliases.append({'v':a,'l':'zh-Hant','k':'aligned_translation_alias','s':'CUV+TIPNR canonical co-attestation','c':0.82})
        entities.append({'id':w.entity_id,'t':w.entity_type,'p':w.preferred_label,'a':aliases,'r':refs,'src':record.source_unique_name})
    payload={
      'schema':'dore.browser-entity-index.v1',
      'source':{'tipnr':TIPNR_SOURCE,'snapshot':args.source_sha,'translation_alignment':'CUV canonical co-attestation'},
      'counts':{'entities':len(entities),'chinese_aliases':zh_count},
      'entities':entities,
    }
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(json.dumps(payload['counts'],ensure_ascii=False))
    if len(entities)<4000:raise SystemExit('entity coverage below BW-1 floor')
    if zh_count<150:raise SystemExit('Chinese aligned-alias coverage too low')

if __name__=='__main__':main()
