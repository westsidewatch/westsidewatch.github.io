const fs=require('fs');
const vm=require('vm');
const assert=require('assert');
const path=require('path');

const root=process.cwd();
const manifest=JSON.parse(fs.readFileSync(path.join(root,'static/dore/crossrefs/manifest.json'),'utf8'));
assert.strictEqual(manifest.schema,'dore.crossrefs.manifest.v1');
assert.strictEqual(manifest.license,'CC BY 4.0');
assert.strictEqual(manifest.contains_bible_text,false);
assert.strictEqual(manifest.bidirectional,true);
assert(manifest.stats.directed_edges>=1_000_000,`expected >=1m directed edges, got ${manifest.stats.directed_edges}`);
assert(manifest.stats.unique_verses>=30_000,`expected >=30k verses, got ${manifest.stats.unique_verses}`);
assert(manifest.stats.books>=60,`expected broad canon coverage, got ${manifest.stats.books}`);

const readShard=book=>JSON.parse(fs.readFileSync(path.join(root,'static/dore/crossrefs',`${book}.json`),'utf8'));
const gen=readShard('GEN');
assert.strictEqual(gen.schema,'dore.crossrefs.book.v1');
const gen11=gen.refs['1.1'];
assert(Array.isArray(gen11)&&gen11.length>5,'GEN.1.1 must have real cross-reference rows');
assert(gen11.some(row=>row[2]&1),'GEN.1.1 should include OpenBible provenance');

// Semantic bidirectionality: choose a real generated edge and prove the reverse edge exists.
const witness=gen11[0];
const [target]=witness;
const [targetBook,targetCh,targetVs]=target.split('.');
const targetShard=readShard(targetBook);
const reverse=(targetShard.refs[`${Number(targetCh)}.${Number(targetVs)}`]||[]).find(row=>row[0]==='GEN.1.1');
assert(reverse,`bidirectional reverse edge missing: ${target} -> GEN.1.1`);

// Browser-runtime proof against the actual generated shards, not a hand-coded fixture.
const D={
  canonicalRef(ref){const s=String(ref).replace(/^bible\.ref\./,'');return `bible.ref.${s}`;},
  registerSource(source){this.source=source;},
  related(){return[];}
};
const fetch=async url=>{
  let file;
  if(url==='/dore/crossrefs/manifest.json')file=path.join(root,'static/dore/crossrefs/manifest.json');
  else {const m=url.match(/^\/dore\/crossrefs\/([^/]+)\.json$/);if(m)file=path.join(root,'static/dore/crossrefs',`${m[1]}.json`);}
  if(!file||!fs.existsSync(file))return{ok:false,status:404,json:async()=>null};
  return{ok:true,status:200,json:async()=>JSON.parse(fs.readFileSync(file,'utf8'))};
};
const context={console,fetch,DoreBibleIntelligence:D,globalThis:null,window:null,CustomEvent:class{},setTimeout};
context.globalThis=context;context.window=context;
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(root,'static/dore/dore-open-crossrefs.js'),'utf8'),context);

(async()=>{
  assert(D.openCrossrefs,'open cross-reference runtime must attach to Doré');
  const direct=await D.openRelated('bible.ref.GEN.1.1',{limit:25});
  assert(direct.length>5,'runtime must return real GEN.1.1 cross references');
  assert(direct.every(x=>x.source_dataset==='neuu-bible-crossrefs'),'runtime results must name upstream dataset');
  assert(direct.every(x=>x.provenance?.license==='CC BY 4.0'),'runtime results must retain license provenance');
  assert(direct.some(x=>x.source_mask&1),'runtime must surface OpenBible-backed rows');
  const merged=await D.relatedAsync('bible.ref.GEN.1.1',{depth:1,limit:25});
  assert(merged.length>=direct.length,'Doré relatedAsync must consume open graph');
  const trace=await D.traceOpenCrossref('bible.ref.GEN.1.1',`bible.ref.${target}`,{depth:1,limit:150});
  assert(trace&&trace.reference===`bible.ref.${target}`,'trace must recover a real generated edge');
  const stats=await D.openCrossrefs.stats();
  assert(stats.directed_edges>=1_000_000&&stats.unique_verses>=30_000);
  console.log(JSON.stringify({
    schema:'dore.crossrefs.ingestion.acceptance.v1',
    verdict:'PASS',
    dataset:stats.dataset,
    license:stats.license,
    directed_edges:stats.directed_edges,
    unique_verses:stats.unique_verses,
    books:stats.books,
    witness:{from:'GEN.1.1',to:target,votes:witness[1],source_mask:witness[2],reverse:true},
    runtime:{direct_results:direct.length,traceable:true,one_shared_api_required:true}
  },null,2));
})().catch(err=>{console.error(err);process.exit(1)});
