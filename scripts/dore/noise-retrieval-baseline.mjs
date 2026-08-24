import fs from 'node:fs';
import {encodeMandarin,encodeEnglish,PHONETIC_ENCODER_VERSIONS} from './phonetic-encoders.mjs';

const args=new Set(process.argv.slice(2));
const split=args.has('--test')?'test':'dev';
if(split==='test'&&args.has('--tune')) throw new Error('Refusing to tune on sealed held-out test fixtures');
const fixturePath=`dore-core/knowledge/researcher/fixtures/noise-retrieval-${split}.json`;
const suite=JSON.parse(fs.readFileSync(fixturePath,'utf8'));
const scripture=JSON.parse(fs.readFileSync('static/dore/search-index.json','utf8'));
const entities=JSON.parse(fs.readFileSync('static/dore/entity-index.json','utf8'));
const norm=s=>String(s??'').toLowerCase().normalize('NFKC').replace(/[\s.,;:!?，。；：！？「」『』()（）\-–—_'"`]/g,'');
const verses=(scripture.verses||[]).map(v=>({id:v.r||`${v.b}.${v.c}.${v.v}`,text:[v.z,v.e].filter(Boolean).join(' '),kind:'scripture'}));
const entityRows=(entities.entities||[]).map((e,i)=>({id:e.id||e.k||`entity:${i}`,text:[e.p,...(e.a||[]).map(a=>a?.v)].filter(Boolean).join(' '),kind:'entity'}));
const phoneticKey=(text,language)=>language==='zh'?encodeMandarin(text):encodeEnglish(text);

function pushUnique(c,row,channel,budget,seen){
  const key=`${row.kind}:${row.id}:${channel}`;
  if(seen.has(key)||c.length>=budget)return;
  seen.add(key);c.push({...row,channel});
}

function generate(f){
  const q=norm(f.observed),budget=f.candidate_budget||20,c=[],seen=new Set();
  for(const row of verses){const t=norm(row.text);if(q&&t.includes(q))pushUnique(c,row,'lexical-substring',budget,seen);if(c.length>=budget)break}
  if(c.length<budget)for(const row of entityRows){const t=norm(row.text);if(q&&t.includes(q))pushUnique(c,row,'entity-lexical',budget,seen);if(c.length>=budget)break}

  const queryPhonetic=phoneticKey(f.observed,f.language);
  const phoneticUsable=Boolean(queryPhonetic.key)&&!(f.language==='zh'&&queryPhonetic.unknown_han>0);
  if(phoneticUsable&&c.length<budget){
    for(const row of entityRows){
      const k=phoneticKey(row.text,f.language);
      if(k.key&&k.key===queryPhonetic.key&&!(f.language==='zh'&&k.unknown_han>0))pushUnique(c,row,'entity-phonetic-exact',budget,seen);
      if(c.length>=budget)break;
    }
  }
  if(phoneticUsable&&c.length<budget){
    for(const row of verses){
      const k=phoneticKey(row.text,f.language);
      if(k.key&&k.key===queryPhonetic.key&&!(f.language==='zh'&&k.unknown_han>0))pushUnique(c,row,'scripture-phonetic-exact',budget,seen);
      if(c.length>=budget)break;
    }
  }
  return {candidates:c.slice(0,budget),truncated:c.length>=budget,phonetic:{available:true,versions:PHONETIC_ENCODER_VERSIONS,query:queryPhonetic,policy:'exact-key dev baseline; no fuzzy threshold calibrated'}};
}

let hit=0,required=0,falseNeg=0,totalCandidates=0,abstainCorrect=0,synthetic=0;
for(const f of suite.fixtures){
  if(f.synthetic_encoder_probe){synthetic++;continue}
  const r=generate(f),gold=norm(f.gold_text||f.gold_entity||''),found=gold? r.candidates.some(c=>norm(c.text).includes(gold)):false;const neg=f.abstain==='required';
  if(!neg){required++;if(found)hit++;else falseNeg++}
  if(neg&&r.candidates.length===0)abstainCorrect++;
  totalCandidates+=r.candidates.length;
  console.log(JSON.stringify({id:f.id,split,candidate_count:r.candidates.length,truncated:r.truncated,gold_found:found,abstain_correct:neg?r.candidates.length===0:null,channels:[...new Set(r.candidates.map(c=>c.channel))],phonetic:r.phonetic}));
}
console.log(JSON.stringify({split,fixtures:suite.fixtures.length,evaluated_fixtures:suite.fixtures.length-synthetic,synthetic_encoder_probes_skipped:synthetic,recall_at_budget:required?hit/required:null,gold_misses:falseNeg,mean_candidate_set:(suite.fixtures.length-synthetic)?totalCandidates/(suite.fixtures.length-synthetic):0,negative_abstention_correct:abstainCorrect,phonetic_available:true,encoder_versions:PHONETIC_ENCODER_VERSIONS,note:split==='dev'?'Development calibration surface only; no held-out claim or production promotion.':'Held-out evaluation only; tuning forbidden.'}));
