const fs=require('fs');
const vm=require('vm');
const assert=require('assert');

const refs=[
 ['bible.ref.JDG.21.8','士師記',21,8,'會眾中有基列雅比的一個人沒有到營中來。'],
 ['bible.ref.1SA.11.1','撒母耳記上',11,1,'亞捫人的拿轄上來，對著基列雅比安營。'],
 ['bible.ref.1SA.31.11','撒母耳記上',31,11,'基列雅比的居民聽見非利士人向掃羅所行的事。'],
 ['bible.ref.2SA.2.4','撒母耳記下',2,4,'有人告訴大衛說：葬埋掃羅的是基列雅比人。'],
 ['bible.ref.1CH.10.11','歷代志上',10,11,'基列雅比人聽見非利士人向掃羅所行的一切事。'],
 ['bible.ref.MAT.4.1','馬太福音',4,1,'當時，耶穌被聖靈引到曠野，受魔鬼的試探。'],
 ['bible.ref.MRK.1.12','馬可福音',1,12,'聖靈就把耶穌催到曠野裡去。'],
 ['bible.ref.LUK.4.1','路加福音',4,1,'耶穌被聖靈充滿，從約旦河回來，聖靈將他引到曠野。'],
 ['bible.ref.DEU.8.3','申命記',8,3,'人活著不是單靠食物。'],
 ['bible.ref.DEU.6.16','申命記',6,16,'你們不可試探耶和華你們的神。'],
 ['bible.ref.DEU.6.13','申命記',6,13,'你要敬畏耶和華你的神，事奉他。'],
 ['bible.ref.GEN.1.2','創世記',1,2,'神的靈運行在水面上。'],
 ['bible.ref.JDG.3.10','士師記',3,10,'耶和華的靈降在他身上。'],
 ['bible.ref.1SA.16.13','撒母耳記上',16,13,'耶和華的靈就大大感動大衛。'],
 ['bible.ref.PSA.51.11','詩篇',51,11,'不要從我收回你的聖靈。'],
 ['bible.ref.ISA.63.10','以賽亞書',63,10,'他們竟悖逆，使主的聖靈擔憂。'],
 ['bible.ref.EZK.36.27','以西結書',36,27,'我必將我的靈放在你們裡面。']
].map(([r,name,c,v,z])=>({r,b:r.split('.')[2],c,v,z,e:'',n:[name]}));
const seed=JSON.parse(fs.readFileSync('static/dore/bible-intelligence-seed.v1.json','utf8'));
const context={console,globalThis:null,fetch:async url=>({ok:true,json:async()=>String(url).includes('bible-intelligence-seed')?seed:{schema:'dore.browser-search-core.v1',verses:refs}})};
context.globalThis=context;
vm.createContext(context);
vm.runInContext(fs.readFileSync('static/dore/dore-bible-intelligence.js','utf8'),context);
const D=context.DoreBibleIntelligence;
assert(D,'Doré Bible Intelligence API must be exported');

(async()=>{
  await D.loadSeed();
  const g=await D.query('雅比城和掃羅死後有什麼關係？');
  assert(g&&g.concept_id==='gilead-jabesh-saul','alias 雅比城 must resolve through registry, not a hard-coded regex');
  assert(g.evidence.some(x=>x.reference==='bible.ref.JDG.21.8'));
  assert(g.evidence.some(x=>x.reference==='bible.ref.1SA.31.11'));
  assert(g.evidence.some(x=>x.reference==='bible.ref.2SA.2.4'));
  const chain=D.related('bible.ref.JDG.21.8',{depth:4,limit:20});
  assert(chain.some(x=>x.reference==='bible.ref.1SA.31.11'&&x.path.length>=3),'Gilead-Jabesh graph must support multi-hop history');

  const w=await D.query('耶穌受試探和申命記六到八章有什麼關係？');
  for(const r of ['bible.ref.MAT.4.1','bible.ref.MRK.1.12','bible.ref.LUK.4.1','bible.ref.DEU.8.3','bible.ref.DEU.6.16','bible.ref.DEU.6.13'])assert(w.evidence.some(x=>x.reference===r),`missing ${r}`);

  const s=await D.query('為什麼舊約裡沒有聖靈？');
  assert(s.lead.includes('前提不成立'),'false premise must be challenged');
  for(const r of ['bible.ref.GEN.1.2','bible.ref.PSA.51.11','bible.ref.ISA.63.10'])assert(s.evidence.some(x=>x.reference===r),`missing ${r}`);

  const simp=await D.query('旧约圣灵在哪里？');
  assert(simp&&simp.concept_id==='ot-spirit-false-premise','Simplified Chinese alias must fold to Traditional');
  const english=await D.query('jabesh-gilead Saul');
  assert(english&&english.concept_id==='gilead-jabesh-saul','English alias must resolve through shared registry');
  assert(D.related('bible.ref.JDG.21.8',{depth:2}).every(x=>x.source_dataset&&x.provenance),'graph results must retain provenance');

  const stats=D.stats();
  assert(stats.sources.some(x=>x.id==='crossreferences-org-tsk'&&x.license==='CC-BY-4.0'),'TSK source provenance/license must be registered');
  assert(stats.sources.some(x=>x.id==='openbible-crossrefs'&&x.license==='CC-BY-4.0'),'OpenBible source provenance/license must be registered');
  assert(stats.concepts.includes('gilead-jabesh-saul')&&stats.concepts.includes('ot-spirit-false-premise'),'concept registry must be externally seeded');

  const graphView=await D.graphSearch('雅比城');
  assert(graphView&&graphView.kind==='bible-intelligence-graph');
  assert(graphView.evidence.some(x=>x.depth>0&&Array.isArray(x.path)),'graphSearch must expose scored paths');

  const evidence={
    registry_alias:g.concept_id,
    gilead_multi_hop:chain.find(x=>x.reference==='bible.ref.1SA.31.11'),
    wilderness_refs:w.evidence.map(x=>x.reference),
    old_testament_spirit:{lead:s.lead,refs:s.evidence.map(x=>x.reference)},
    simplified_alias:simp.concept_id,
    english_alias:english.concept_id,
    provenance_sources:stats.sources.map(x=>({id:x.id,license:x.license,status:x.status})),
    graph_path_count:graphView.evidence.filter(x=>x.depth>0).length,
    traceable_graph:true
  };
  console.log(JSON.stringify({schema:'dore.search2.semantic-benchmark.v2',status:'PASS',evidence,engine:stats},null,2));
})().catch(err=>{console.error(err);process.exit(1)});