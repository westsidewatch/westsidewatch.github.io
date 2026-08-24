import fs from 'node:fs';
import crypto from 'node:crypto';
import {encodeMandarinV2,PHONETIC_ENCODER_V2} from './phonetic-encoders-v2.mjs';

const entities=JSON.parse(fs.readFileSync('static/dore/entity-index.json','utf8')).entities||[];
const han=/\p{Script=Han}/u;
const rows=[];
for(const [i,e] of entities.entries()){
  for(const surface of [e.p,...(e.a||[]).map(a=>a?.v)].filter(Boolean)){
    if(![...surface].some(ch=>han.test(ch)))continue;
    const id=String(e.id||e.k||`entity:${i}`);
    const h=crypto.createHash('sha256').update(`${id}\0${surface}`).digest('hex');
    const bucket=parseInt(h.slice(0,8),16)%10;
    if(bucket<=1)rows.push({id,surface,bucket}); // fixed 20% development partition
  }
}

let totalHan=0,unknown=0,empty=0;
const failures=[];
for(const row of rows){
  const n=[...row.surface].filter(ch=>han.test(ch)).length;
  totalHan+=n;
  const enc=encodeMandarinV2(row.surface);
  unknown+=enc.unknown_han;
  if(!enc.key)empty++;
  if((enc.unknown_han||!enc.key)&&failures.length<20)failures.push({...row,enc});
}
const summary={
  gate:'researcher06-unit08-v2-dev-coverage',
  partition:'sha256(entity-id\\0surface) mod 10 in {0,1}',
  inspected_rows:rows.length,
  total_han:totalHan,
  unknown_han:unknown,
  unknown_rate:totalHan?unknown/totalHan:null,
  empty_keys:empty,
  encoder:PHONETIC_ENCODER_V2,
  failures,
  pass:rows.length>0&&unknown===0&&empty===0,
  boundary:'Development/self-test only. This is not a fresh held-out retrieval claim.'
};
console.log(JSON.stringify(summary,null,2));
if(!summary.pass)process.exitCode=1;
