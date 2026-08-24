import fs from 'node:fs';
import crypto from 'node:crypto';
import {encodeMandarinV2,PHONETIC_ENCODER_V2} from './phonetic-encoders-v2.mjs';

const entities=JSON.parse(fs.readFileSync('static/dore/entity-index.json','utf8'));
const rows=(entities.entities||[]).flatMap((e,i)=>{
  const id=e.id||e.k||`entity:${i}`;
  return [e.p,...(e.a||[]).map(a=>a?.v)].filter(Boolean).map(surface=>({id,surface:String(surface).normalize('NFKC')}));
}).filter(r=>/\p{Script=Han}/u.test(r.surface));

const mod10=s=>parseInt(crypto.createHash('sha256').update(s).digest('hex').slice(0,8),16)%10;
const finalRows=rows.filter(r=>[8,9].includes(mod10(`${r.id}\0${r.surface}`)));

const charsBySyllable=new Map();
for(const {surface} of rows){
  for(const ch of surface){
    if(!/\p{Script=Han}/u.test(ch))continue;
    const enc=encodeMandarinV2(ch);
    if(enc.unknown_han||!enc.key)continue;
    if(!charsBySyllable.has(enc.key))charsBySyllable.set(enc.key,new Set());
    charsBySyllable.get(enc.key).add(ch);
  }
}

function perturb(surface){
  const chars=[...surface];
  for(let i=0;i<chars.length;i++){
    const ch=chars[i];
    if(!/\p{Script=Han}/u.test(ch))continue;
    const enc=encodeMandarinV2(ch);
    const alts=[...(charsBySyllable.get(enc.key)||[])].filter(x=>x!==ch).sort();
    if(!alts.length)continue;
    const pick=alts[mod10(`${surface}\0${i}\0${enc.key}`)%alts.length];
    const out=[...chars];out[i]=pick;
    return {observed:out.join(''),family:'single-han-same-pinyin',position:i,from:ch,to:pick,syllable:enc.key};
  }
  return null;
}

const positives=[];
for(const r of finalRows){
  const p=perturb(r.surface);
  if(!p||p.observed===r.surface)continue;
  positives.push({...r,...p});
  if(positives.length>=80)break;
}

const entityEncoded=rows.map(r=>({...r,enc:encodeMandarinV2(r.surface)})).filter(r=>r.enc.key&&!r.enc.unknown_han);
const negatives=['今天天氣很好','請把燈關掉','明天記得買牛奶','會議改到下午三點','這是一個普通句子'];
const budget=20;
function retrieve(observed){
  const q=encodeMandarinV2(observed);
  if(!q.key||q.unknown_han)return {q,candidates:[]};
  const candidates=[];const seen=new Set();
  for(const r of entityEncoded){
    if(r.enc.key!==q.key)continue;
    if(seen.has(r.id))continue;
    seen.add(r.id);candidates.push(r);
    if(candidates.length>=budget)break;
  }
  return {q,candidates};
}

let hit=0,miss=0,totalCandidates=0,totalHan=0,unknownHan=0;
const cases=[];
for(const f of positives){
  const r=retrieve(f.observed);
  const found=r.candidates.some(c=>c.id===f.id);
  if(found)hit++; else miss++;
  totalCandidates+=r.candidates.length;
  totalHan+=[...f.observed].filter(ch=>/\p{Script=Han}/u.test(ch)).length;
  unknownHan+=r.q.unknown_han||0;
  cases.push({id:f.id,gold_surface:f.surface,observed:f.observed,perturbation:{family:f.family,position:f.position,from:f.from,to:f.to,syllable:f.syllable},candidate_count:r.candidates.length,gold_found:found});
}
let abstainCorrect=0;
for(const observed of negatives){
  const r=retrieve(observed);const ok=r.candidates.length===0;if(ok)abstainCorrect++;
  totalCandidates+=r.candidates.length;
  totalHan+=[...observed].filter(ch=>/\p{Script=Han}/u.test(ch)).length;
  unknownHan+=r.q.unknown_han||0;
  cases.push({negative:true,observed,candidate_count:r.candidates.length,abstain_correct:ok});
}

const evaluated=positives.length+negatives.length;
const summary={
  gate:'researcher06-unit08-v2-fresh-final',
  protocol:{partition:'sha256(entity-id\\0surface) mod 10 in {8,9}',positive_limit:80,perturbation:'first eligible Han replaced by deterministic alternate Han sharing the same v2 tone-free pinyin syllable',candidate_budget:budget,ranking:'stable corpus order among exact phonetic-key matches; dedupe by entity id',negative_controls:'fixed ordinary Mandarin utterances; exact phonetic entity match must abstain'},
  encoder:PHONETIC_ENCODER_V2,
  positives:positives.length,
  negatives:negatives.length,
  recall_at_budget:positives.length?hit/positives.length:null,
  gold_misses:miss,
  mean_candidate_set:evaluated?totalCandidates/evaluated:0,
  negative_abstention_correct:`${abstainCorrect}/${negatives.length}`,
  unknown_han_rate:totalHan?unknownHan/totalHan:0,
  perturbation_families:{'single-han-same-pinyin':positives.length},
  pass:Boolean(positives.length>=40&&miss===0&&abstainCorrect===negatives.length&&unknownHan===0),
  boundary:'Fresh one-shot final for frozen v2 architecture. Any code/parameter change after opening this output invalidates it as unseen evidence.',
  cases
};
console.log(JSON.stringify(summary,null,2));
if(!summary.pass)process.exitCode=1;
