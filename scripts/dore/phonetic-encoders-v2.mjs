import {pinyin} from 'pinyin-pro';

export const PHONETIC_ENCODER_V2={
  mandarin:{id:'mandarin-pinyin-pro-v2-research',source:'pinyin-pro@3.29.3',tone:'none',status:'research-only'},
  english:{id:'english-metaphone-lite-v1',source:'local',status:'unchanged-control'}
};

const stripMarks=s=>String(s??'').normalize('NFKD').replace(/\p{M}/gu,'').toLowerCase();
const letters=s=>stripMarks(s).replace(/[^a-z]/g,'');

export function encodeMandarinV2(text){
  const source=String(text??'').normalize('NFKC');
  if(!source)return {version:PHONETIC_ENCODER_V2.mandarin.id,key:'',unknown_han:0,source:PHONETIC_ENCODER_V2.mandarin.source};
  const out=pinyin(source,{toneType:'none',type:'array'});
  const tokens=[];let unknown=0;let oi=0;
  for(const ch of source){
    if(/\p{Script=Han}/u.test(ch)){
      const syllable=String(out[oi++]??'').toLowerCase().replace(/ü/g,'v');
      if(/^[a-zv]+$/.test(syllable)&&syllable!==ch)tokens.push(syllable);
      else {tokens.push(`u${ch.codePointAt(0).toString(16)}`);unknown++;}
    } else if(/[A-Za-z0-9]/.test(ch))tokens.push(ch.toLowerCase());
  }
  return {version:PHONETIC_ENCODER_V2.mandarin.id,key:tokens.join(' '),unknown_han:unknown,source:PHONETIC_ENCODER_V2.mandarin.source};
}

export function encodeEnglishControl(text){
  const raw=letters(text);
  if(!raw)return {version:PHONETIC_ENCODER_V2.english.id,key:''};
  let s=raw.replace(/^kn/,'n').replace(/^wr/,'r').replace(/^wh/,'w')
    .replace(/ph/g,'f').replace(/ght/g,'t').replace(/gh/g,'')
    .replace(/tion/g,'xn').replace(/tch/g,'ch').replace(/dg(?=[eiy])/g,'j')
    .replace(/c(?=[eiy])/g,'s').replace(/c/g,'k').replace(/q/g,'k').replace(/x/g,'ks')
    .replace(/v/g,'f').replace(/z/g,'s');
  const first=s[0];
  s=first+s.slice(1).replace(/[aeiouy]/g,'').replace(/(.)\1+/g,'$1');
  return {version:PHONETIC_ENCODER_V2.english.id,key:s};
}
