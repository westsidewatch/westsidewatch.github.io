const HAN_PINYIN_V1=new Map(Object.entries({
  '耶':'ye','和':'he','華':'hua','华':'hua','是':'shi','我':'wo','的':'de','牧':'mu','者':'zhe',
  '利':'li','米':'mi','亞':'ya','亚':'ya','馬':'ma','马':'ma','太':'tai','福':'fu','音':'yin',
  '約':'yue','约':'yue','翰':'han','保':'bao','羅':'luo','罗':'luo','彼':'bi','得':'de','摩':'mo','西':'xi',
  '撒':'sa','母':'mu','耳':'er','以':'yi','賽':'sai','赛':'sai','雅':'ya','各':'ge','路':'lu','加':'jia',
  '使':'shi','徒':'tu','行':'xing','傳':'zhuan','传':'zhuan','詩':'shi','诗':'shi','篇':'pian',
  '主':'zhu','神':'shen','愛':'ai','爱':'ai','世':'shi','人':'ren','光':'guang','生':'sheng','命':'ming'
}));

export const PHONETIC_ENCODER_VERSIONS={mandarin:'mandarin-pinyin-lite-v1',english:'english-metaphone-lite-v1'};

const stripMarks=s=>String(s??'').normalize('NFKD').replace(/\p{M}/gu,'').toLowerCase();
const letters=s=>stripMarks(s).replace(/[^a-z]/g,'');

export function encodeMandarin(text){
  const out=[];let unknown=0;
  for(const ch of String(text??'').normalize('NFKC')){
    if(/\p{Script=Han}/u.test(ch)){
      const py=HAN_PINYIN_V1.get(ch);
      if(py) out.push(py); else {out.push(`u${ch.codePointAt(0).toString(16)}`);unknown++;}
    } else if(/[A-Za-z0-9]/.test(ch)) out.push(ch.toLowerCase());
  }
  return {version:PHONETIC_ENCODER_VERSIONS.mandarin,key:out.join(' '),unknown_han:unknown};
}

export function encodeEnglish(text){
  const raw=letters(text);
  if(!raw)return {version:PHONETIC_ENCODER_VERSIONS.english,key:''};
  let s=raw
    .replace(/^kn/,'n').replace(/^wr/,'r').replace(/^wh/,'w')
    .replace(/ph/g,'f').replace(/ght/g,'t').replace(/gh/g,'')
    .replace(/tion/g,'xn').replace(/tch/g,'ch').replace(/dg(?=[eiy])/g,'j')
    .replace(/c(?=[eiy])/g,'s').replace(/c/g,'k').replace(/q/g,'k').replace(/x/g,'ks')
    .replace(/v/g,'f').replace(/z/g,'s');
  const first=s[0];
  s=first+s.slice(1).replace(/[aeiouy]/g,'').replace(/(.)\1+/g,'$1');
  return {version:PHONETIC_ENCODER_VERSIONS.english,key:s};
}

export function phoneticSimilarity(a,b,language){
  const ea=language==='zh'?encodeMandarin(a):encodeEnglish(a);
  const eb=language==='zh'?encodeMandarin(b):encodeEnglish(b);
  const ka=ea.key.replace(/\s+/g,''),kb=eb.key.replace(/\s+/g,'');
  if(!ka||!kb)return {score:0,a:ea,b:eb};
  if(ka===kb)return {score:1,a:ea,b:eb};
  let prefix=0;while(prefix<ka.length&&prefix<kb.length&&ka[prefix]===kb[prefix])prefix++;
  const score=Math.max(0,prefix/Math.max(ka.length,kb.length));
  return {score,a:ea,b:eb};
}
