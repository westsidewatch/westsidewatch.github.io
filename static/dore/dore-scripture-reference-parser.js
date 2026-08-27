((root,factory)=>{const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.DORE_SCRIPTURE_REFERENCE_PARSER=api;})(typeof globalThis!=='undefined'?globalThis:this,()=>{
'use strict';
const NUM_CHARS='零〇一二三四五六七八九十百兩两0123456789';
const ZH={零:0,'〇':0,一:1,二:2,三:3,四:4,五:5,六:6,七:7,八:8,九:9,兩:2,两:2};
function chineseNumber(value){const s=String(value||'').trim();if(/^\d+$/.test(s))return Number(s);if(!s)return NaN;if(s.includes('百')){const[a,b='']=s.split('百');return(a?ZH[a]:1)*100+(b?chineseNumber(b):0)}if(s.includes('十')){const[a,b='']=s.split('十');return(a?ZH[a]:1)*10+(b?ZH[b]:0)}return s.length===1&&s in ZH?ZH[s]:NaN}
const cleanAlias=s=>String(s||'').toLowerCase().replace(/\s+/g,'');
function create(corpus){const aliases=[];for(const b of corpus.books||[])for(const a of b.aliases||[])aliases.push({raw:a,key:cleanAlias(a),code:b.code});aliases.sort((a,b)=>b.key.length-a.key.length);
function matchBookAtStart(text){const compact=String(text||'').replace(/^\s+/,'');for(const a of aliases){let pos=0,j=0;while(pos<compact.length&&j<a.key.length){if(/\s/.test(compact[pos])){pos++;continue}if(compact[pos].toLowerCase()!==a.key[j])break;pos++;j++}if(j===a.key.length)return{code:a.code,alias:a.raw,rest:compact.slice(pos)}}return null}
function normalizeRest(rest){return String(rest||'').trim().replace(/[：]/g,':').replace(/[．]/g,'.').replace(/[－–—~～]|至|到/g,'-').replace(/\s+/g,'')}
function parseSegment(segment){const book=matchBookAtStart(segment);if(!book)return null;let r=normalizeRest(book.rest);if(!r)return null;let m;
m=r.match(new RegExp(`^第?([${NUM_CHARS}]+)章第?([${NUM_CHARS}]+)節(?:-第?([${NUM_CHARS}]+)節)?$`));
if(!m)m=r.match(new RegExp(`^第?([${NUM_CHARS}]+)第([${NUM_CHARS}]+)節(?:-第?([${NUM_CHARS}]+)節)?$`));
if(m){const c=chineseNumber(m[1]),s=chineseNumber(m[2]),e=m[3]?chineseNumber(m[3]):s;if(Number.isFinite(c)&&Number.isFinite(s)&&Number.isFinite(e)&&e>=s)return{kind:s===e?'verse':'range',book:book.code,chapter:c,start:s,end:e,source:segment}}
r=r.replace(/第/g,'').replace(/章/g,':').replace(/節/g,'');
m=r.match(new RegExp(`^([${NUM_CHARS}]+)[:.]([${NUM_CHARS}]+)(?:-([${NUM_CHARS}]+))?$`));
if(m){const c=chineseNumber(m[1]),s=chineseNumber(m[2]),e=m[3]?chineseNumber(m[3]):s;if(Number.isFinite(c)&&Number.isFinite(s)&&Number.isFinite(e)&&e>=s)return{kind:s===e?'verse':'range',book:book.code,chapter:c,start:s,end:e,source:segment}}
m=r.match(new RegExp(`^([${NUM_CHARS}]+):?$`));if(m){const c=chineseNumber(m[1]);if(Number.isFinite(c))return{kind:'chapter',book:book.code,chapter:c,source:segment}}return null}
function bookStarts(q){const text=String(q||''),found=[];for(let i=0;i<text.length;i++){const tail=text.slice(i),m=matchBookAtStart(tail);if(!m)continue;if(m.rest.match(new RegExp(`^\\s*[第${NUM_CHARS}]`))){found.push(i);i+=Math.max(0,m.alias.length-1)}}return[...new Set(found)]}
function parseQuery(q){const text=String(q||'').trim();if(!text)return null;const starts=bookStarts(text);if(!starts.length)return null;const segments=[];for(let i=0;i<starts.length;i++){const end=i+1<starts.length?starts[i+1]:text.length;const seg=text.slice(starts[i],end).replace(/^[\s,，;；、]+|[\s,，;；、]+$/g,'');if(seg)segments.push(seg)}if(!segments.length)return null;const parsed=segments.map(parseSegment);return parsed.some(x=>!x)?null:parsed}
return{parseSegment,parseQuery,aliases:aliases.slice()}}
return{version:'1.0',create,chineseNumber};
});
