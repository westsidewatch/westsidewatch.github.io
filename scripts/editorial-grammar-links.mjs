import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
const registry=JSON.parse(fs.readFileSync('data/editorial/sevenfold.json','utf8'));
const realms=registry.sequence;
const missing=[];
let count=0;
function valid(target,from){
  assert(typeof target==='string'&&target.startsWith('/')&&!target.startsWith('//'));
  const u=new URL(target,'https://westsidewatch.example');
  const p=decodeURIComponent(u.pathname);
  if(p.includes('..'))throw new Error('Unsafe link '+target);
  const base=path.join('public',p);
  const candidates=[base,path.join(base,'index.html'),base+'.html'];
  count++;
  if(!candidates.some(f=>fs.existsSync(f)))missing.push({from,target});
}
for(const realm of realms){
 const d=JSON.parse(fs.readFileSync('data/editorial/grammar/'+realm+'.json','utf8'));
 valid(registry.sections[realm].source,realm+':source');
 for(const b of d.blocks){
   if(b.type==='index'||b.type==='shelf')
     for(const e of b.entries)valid(e.href,realm+':'+b.id+':'+e.title);
 }
}
if(missing.length){
 console.error('BROKEN_EDITORIAL_LINKS',JSON.stringify(missing,null,2));
 process.exit(1);
}
console.log('EDITORIAL_GRAMMAR_LINKS_PASS',JSON.stringify({realms:realms.length,targets:count}));
