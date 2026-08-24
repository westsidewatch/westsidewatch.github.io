import fs from 'node:fs';
import {encodeMandarin,PHONETIC_ENCODER_VERSIONS} from './phonetic-encoders.mjs';

const entities=JSON.parse(fs.readFileSync('static/dore/entity-index.json','utf8')).entities||[];
const han=/\p{Script=Han}/u;
const surfaces=[];
for(const e of entities){
  for(const s of [e.p,...(e.a||[]).map(a=>a?.v)].filter(Boolean)){
    if([...s].some(ch=>han.test(ch))) surfaces.push({entity:e.id||e.k||null,surface:s});
  }
}

const charCounts=new Map();
let totalHan=0,mappedHan=0,fullyCoveredSurfaces=0;
for(const row of surfaces){
  let unknown=0,hanCount=0;
  for(const ch of row.surface){
    if(!han.test(ch))continue;
    hanCount++; totalHan++;
    const encoded=encodeMandarin(ch);
    const mapped=encoded.unknown_han===0;
    if(mapped)mappedHan++; else unknown++;
    const cur=charCounts.get(ch)||{char:ch,count:0,mapped};
    cur.count++; cur.mapped=mapped;
    charCounts.set(ch,cur);
  }
  if(hanCount>0&&unknown===0)fullyCoveredSurfaces++;
}
const unique=[...charCounts.values()];
const mappedUnique=unique.filter(x=>x.mapped).length;
const unmapped=unique.filter(x=>!x.mapped).sort((a,b)=>b.count-a.count||a.char.localeCompare(b.char));
const summary={
  audit:'researcher06-unit07-mandarin-entity-coverage',
  encoder_version:PHONETIC_ENCODER_VERSIONS.mandarin,
  entity_rows:entities.length,
  chinese_surfaces:surfaces.length,
  total_han_occurrences:totalHan,
  mapped_han_occurrences:mappedHan,
  occurrence_coverage:totalHan?mappedHan/totalHan:null,
  unique_han:unique.length,
  mapped_unique_han:mappedUnique,
  unique_coverage:unique.length?mappedUnique/unique.length:null,
  fully_covered_surfaces:fullyCoveredSurfaces,
  surface_coverage:surfaces.length?fullyCoveredSurfaces/surfaces.length:null,
  unmapped_unique_han:unmapped.length,
  top_unmapped:unmapped.slice(0,100),
  note:'Corpus-wide audit only. No v1 mapping is modified; exposed Unit 06 held-out data is not used as a final test.'
};
console.log(JSON.stringify(summary));
