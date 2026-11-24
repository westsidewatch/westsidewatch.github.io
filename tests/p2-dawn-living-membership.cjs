/* P2 second-layer subject integration contract tests. Run: node tests/p2-dawn-living-membership.cjs */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const src=fs.readFileSync(path.resolve(__dirname,'../static/js/p2-dawn-living-membership.mjs'),'utf8');
const script=src.replace(/^import .*;$/gm,'').replace(/^export /gm,'')+'\nreturn livingSubjectBooks;';
const root={schema:'dawn.library.living-root.v1',identityAuthority:'Dawn',
 projectionOnly:true,admissionAuthority:false,shardCount:2,
 classification:{roots:[{id:'bible',workCount:2,children:[{id:'bible.new-testament',workCount:1}]}]},
 shards:[{ordinal:1,href:'/dawn-library/living/wall-000001.json'},
         {ordinal:2,href:'/dawn-library/living/wall-000002.json'}]};
const makeShard=(ordinal,workRefs)=>({schema:'dawn.library.living-wall-shard.v1',identityAuthority:'Dawn',
 projectionOnly:true,admissionAuthority:false,ordinal,workRefs});
const data=new Map([
 ['/dawn-library/living/root.json',root],
 ['/dawn-library/living/wall-000001.json',makeShard(1,[
 {workId:'OL1W',classification:{roots:['bible'],leaves:['bible.new-testament']}},
 {workId:'OL2W',classification:{roots:['bible'],leaves:['bible.old-testament']}},
 {workId:'OL3W',classification:{roots:[],leaves:[]}}])],
 ['/dawn-library/living/wall-000002.json',makeShard(2,[
 {workId:'OL1W',classification:{roots:['bible'],leaves:['bible.new-testament']}}])]
]);
const hits=[];
const fetchMock=async(url)=>{hits.push(url);return{ok:data.has(url),status:data.has(url)?200:404,
 json:async()=>data.get(url)}};
const works=async(ids)=>new Map(ids.map(id=>[id,{workId:id,title:id,authors:['Author '+id],cover:{url:null}}]));
const resolve=new Function('resourceWorks','fetch','AbortSignal',script)(works,fetchMock,{timeout:()=>({})});
(async()=>{
 const leaf=await resolve('bible.new-testament',{limit:36});
 assert.deepEqual(leaf.books.map(b=>b.workId),['OL1W']);
 assert.equal(leaf.sampleComplete,true);
 assert.equal(leaf.totalShards,2);
 assert.equal(leaf.matchedIds,1);
 const rootSample=await resolve('bible',{limit:1});
 assert.deepEqual(rootSample.books.map(b=>b.workId),['OL1W']);
 assert.equal(rootSample.visited,1);
 const aborted=await resolve('bible',{isCurrent:()=>false});
 assert.equal(aborted,null);
 await assert.rejects(()=>resolve('made.up.subject'),/Unknown canonical subject/);
 assert(!hits.some(url=>url.includes('search-')),'must not use keyword search');
 console.log('PASS: original Living membership, dedupe, bounded sample, cancellation, invalid subject');
})().catch(error=>{console.error(error);process.exitCode=1});
