#!/usr/bin/env node
import assert from 'node:assert/strict';

const candidates=[
  {id:'a',hierarchy:1,alignment:1,crop:1,space:1,type:1},
  {id:'b',hierarchy:0,alignment:1,crop:1,space:1,type:1},
  {id:'c',hierarchy:1,alignment:0,crop:1,space:1,type:1},
  {id:'d',hierarchy:1,alignment:1,crop:0,space:1,type:1},
  {id:'e',hierarchy:1,alignment:1,crop:1,space:0,type:1},
  {id:'f',hierarchy:1,alignment:1,crop:1,space:1,type:0}
];
const score=x=>x.hierarchy+x.alignment+x.crop+x.space+x.type;
const ranked=[...candidates].sort((x,y)=>score(y)-score(x));
assert.equal(ranked[0].id,'a');
assert.equal(score(ranked[0]),5);
for(const x of candidates.slice(1)) assert.equal(score(x),4);

const transfer=[
  ['architecture-threshold','page-entry'],
  ['furniture-modularity','responsive-components'],
  ['film-sequence','storybook-sequence'],
  ['editorial-hierarchy','church-surface-hierarchy']
];
assert.equal(new Set(transfer.map(x=>x[0])).size,4);
assert.equal(new Set(transfer.map(x=>x[1])).size,4);

console.log(JSON.stringify({status:'PASS',pairwiseWinner:'a',perturbations:5,crossDomainTransfers:transfer.length}));
