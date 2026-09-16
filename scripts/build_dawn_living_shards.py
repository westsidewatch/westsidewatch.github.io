#!/usr/bin/env python3
"""Split Dawn Living Library work refs into deterministic lazy-load shards.
Projection only: shards never own Work identity or admission authority.
"""
import json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'static/dawn-library/living-library.json'
OUT=ROOT/'static/dawn-library/living'
SHARD_SIZE=10000

def main():
    living=json.loads(SRC.read_text())
    assert living.get('projectionOnly') is True and living.get('admissionAuthority') is False
    refs=living['livingWall']['workRefs']; OUT.mkdir(parents=True,exist_ok=True)
    for old in OUT.glob('wall-*.json'): old.unlink()
    shards=[]
    for start in range(0,len(refs),SHARD_SIZE):
        chunk=refs[start:start+SHARD_SIZE]; n=start//SHARD_SIZE+1
        name=f'wall-{n:06d}.json'; payload={'schema':'dawn.library.living-wall-shard.v1','identityAuthority':'Dawn','projectionOnly':True,'admissionAuthority':False,'ordinal':n,'offset':start,'workCount':len(chunk),'workRefs':chunk}
        raw=(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n').encode()
        (OUT/name).write_bytes(raw)
        shards.append({'ordinal':n,'href':f'/static/dawn-library/living/{name}','offset':start,'workCount':len(chunk),'sha256':hashlib.sha256(raw).hexdigest()})
    root={'schema':'dawn.library.living-root.v1','identityAuthority':'Dawn','projectionOnly':True,'admissionAuthority':False,'canonicalWorkCount':living['canonicalWorkCount'],'shardSize':SHARD_SIZE,'shardCount':len(shards),'classification':living['classification'],'facets':living['facets'],'livingWall':{k:v for k,v in living['livingWall'].items() if k!='workRefs'},'editorialLayers':living['editorialLayers'],'shards':shards,'loadingContract':{'mode':'lazy-visible-window','initialShards':1,'prefetchAhead':1,'millionCardDom':False}}
    assert sum(x['workCount'] for x in shards)==root['canonicalWorkCount']==len(refs)
    (OUT/'root.json').write_text(json.dumps(root,ensure_ascii=False,separators=(',',':'))+'\n')
    print(json.dumps({'canonicalWorkCount':len(refs),'shardCount':len(shards),'shardSize':SHARD_SIZE,'mode':'lazy-visible-window'}))
if __name__=='__main__':main()
