import fs from 'node:fs';

const args=new Set(process.argv.slice(2));
const split=args.has('--test')?'test':'dev';
if(split==='test'&&args.has('--tune')) throw new Error('Refusing to tune on sealed held-out test fixtures');
const fixturePath=`dore-core/knowledge/researcher/fixtures/noise-retrieval-${split}.json`;
const suite=JSON.parse(fs.readFileSync(fixturePath,'utf8'));
const scripture=JSON.parse(fs.readFileSync('static/dore/search-index.json','utf8'));
const entities=JSON.parse(fs.readFileSync('static/dore/entity-index.json','utf8'));
const norm=s=>String(s??'').toLowerCase().normalize('NFKC').replace(/[\s.,;:!?，。；：！？「」『』()（）\-–—_'"`]/g,'');
const flat=(x,out=[])=>{if(Array.isArray(x))for(const v of x)flat(v,out);else if(x&&typeof x==='object'){if(typeof x.text==='string')out.push({id:x.id||x.ref||x.reference||`text:${out.length}`,text:x.text,kind:'scripture'});for(const v of Object.values(x))if(v&&typeof v==='object')flat(v,out)}return out};
const verses=flat(scripture);
const entityRows=flat(entities).map(x=>({...x,kind:'entity'}));
function generate(f){const q=norm(f.observed),budget=f.candidate_budget||20,c=[];for(const row of verses){const t=norm(row.text);if(q&&t.includes(q))c.push({...row,channel:'lexical-substring'});if(c.length>=budget)break}if(c.length<budget)for(const row of entityRows){const t=norm(row.text);if(q&&t.includes(q))c.push({...row,channel:'entity-lexical'});if(c.length>=budget)break}return {candidates:c.slice(0,budget),truncated:c.length>=budget,phonetic:{available:false,reason:'versioned encoder not yet committed'}}}
let hit=0,required=0,falseNeg=0,totalCandidates=0,abstainCorrect=0;
for(const f of suite.fixtures){const r=generate(f),gold=norm(f.gold_text||f.gold_entity||''),found=gold? r.candidates.some(c=>norm(c.text).includes(gold)):false;const neg=f.abstain==='required';if(!neg){required++;if(found)hit++;else falseNeg++}if(neg&&r.candidates.length===0)abstainCorrect++;totalCandidates+=r.candidates.length;console.log(JSON.stringify({id:f.id,split,candidate_count:r.candidates.length,truncated:r.truncated,gold_found:found,abstain_correct:neg?r.candidates.length===0:null,channels:[...new Set(r.candidates.map(c=>c.channel))],phonetic:r.phonetic}))}
console.log(JSON.stringify({split,fixtures:suite.fixtures.length,recall_at_budget:required?hit/required:null,gold_misses:falseNeg,mean_candidate_set:suite.fixtures.length?totalCandidates/suite.fixtures.length:0,negative_abstention_correct:abstainCorrect,phonetic_available:false,note:'Structural baseline only; no production calibration or capability promotion.'}));
