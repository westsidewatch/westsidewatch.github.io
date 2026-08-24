import fs from 'node:fs';
import {pinyin} from 'pinyin-pro';

const entities=JSON.parse(fs.readFileSync('static/dore/entity-index.json','utf8')).entities||[];
const han=/\p{Script=Han}/u;
const surfaces=[];
for(const e of entities){
  for(const s of [e.p,...(e.a||[]).map(a=>a?.v)].filter(Boolean)){
    if([...s].some(ch=>han.test(ch))) surfaces.push({entity:e.id||e.k||null,surface:s});
  }
}

let fullyCovered=0,totalHan=0,convertedHan=0;
const failures=[];
for(const row of surfaces){
  const chars=[...row.surface].filter(ch=>han.test(ch));
  totalHan+=chars.length;
  const out=pinyin(row.surface,{toneType:'none',type:'array'});
  let ok=true;
  for(const [i,ch] of chars.entries()){
    const syllable=out[i];
    const converted=Boolean(syllable)&&syllable!==ch&&/^[a-züv]+$/i.test(syllable);
    if(converted)convertedHan++; else ok=false;
  }
  if(ok)fullyCovered++;
  else if(failures.length<100)failures.push({entity:row.entity,surface:row.surface,output:out});
}

console.log(JSON.stringify({
  audit:'researcher06-unit07-pinyin-pro-reference-coverage',
  reference:'pinyin-pro@3.29.3',
  entity_rows:entities.length,
  chinese_surfaces:surfaces.length,
  total_han_occurrences:totalHan,
  converted_han_occurrences:convertedHan,
  occurrence_coverage:totalHan?convertedHan/totalHan:null,
  fully_covered_surfaces:fullyCovered,
  surface_coverage:surfaces.length?fullyCovered/surfaces.length:null,
  sample_failures:failures,
  note:'Research reference only; no production dependency or v1 mutation.'
}));
