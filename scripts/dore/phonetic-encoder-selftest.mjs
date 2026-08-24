import {encodeMandarin,encodeEnglish,PHONETIC_ENCODER_VERSIONS} from './phonetic-encoders.mjs';

const cases=[
  ['zh-exact','zh','耶和華','耶和華',true],
  ['zh-trad-simp','zh','馬利亞','马利亚',true],
  ['zh-distinct','zh','馬利亞','耶利米',false],
  ['en-knight-night','en','knight','night',true],
  ['en-ph-f','en','philip','filip',true],
  ['en-distinct','en','moses','peter',false]
];
let pass=0;
for(const [id,lang,a,b,expectSame] of cases){
  const ea=lang==='zh'?encodeMandarin(a):encodeEnglish(a),eb=lang==='zh'?encodeMandarin(b):encodeEnglish(b);
  const same=ea.key===eb.key,ok=same===expectSame;
  if(ok)pass++;
  console.log(JSON.stringify({id,lang,a_key:ea.key,b_key:eb.key,expectSame,same,ok}));
}
const unknown=encodeMandarin('龍');
const fallbackOk=unknown.unknown_han===1&&unknown.key.startsWith('u');
if(fallbackOk)pass++;
console.log(JSON.stringify({id:'zh-unknown-explicit-fallback',key:unknown.key,unknown_han:unknown.unknown_han,ok:fallbackOk}));
const total=cases.length+1;
console.log(JSON.stringify({versions:PHONETIC_ENCODER_VERSIONS,pass,total}));
if(pass!==total)process.exit(1);
