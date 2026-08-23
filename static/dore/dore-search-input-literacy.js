(()=>{
'use strict';
const state={corpus:null,index:null,aliases:[],byChapter:new Map(),ready:false};
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const NUM_CHARS='零〇一二三四五六七八九十百兩两0123456789';
const ZH={零:0,'〇':0,一:1,二:2,三:3,四:4,五:5,六:6,七:7,八:8,九:9,兩:2,两:2};
const cleanAlias=s=>String(s||'').toLowerCase().replace(/\s+/g,'');
const escapeRe=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
function chineseNumber(value){const s=String(value||'').trim();if(/^\d+$/.test(s))return Number(s);if(!s)return NaN;if(s.includes('百')){const[a,b='']=s.split('百');return(a?ZH[a]:1)*100+(b?chineseNumber(b):0)}if(s.includes('十')){const[a,b='']=s.split('十');return(a?ZH[a]:1)*10+(b?ZH[b]:0)}return s.length===1&&s in ZH?ZH[s]:NaN}
function build(){for(const v of state.index.verses||[]){const key=`${v.b}.${Number(v.c)}`;if(!state.byChapter.has(key))state.byChapter.set(key,[]);state.byChapter.get(key).push(v)}state.aliases=[];for(const b of state.corpus.books||[])for(const a of b.aliases||[])state.aliases.push({raw:a,key:cleanAlias(a),code:b.code});state.aliases.sort((a,b)=>b.key.length-a.key.length)}
function matchBookAtStart(text){const compact=String(text||'').replace(/^\s+/,'');const lower=compact.toLowerCase();for(const a of state.aliases){let pos=0,j=0;while(pos<compact.length&&j<a.key.length){if(/\s/.test(compact[pos])){pos++;continue}if(compact[pos].toLowerCase()!==a.key[j])break;pos++;j++}if(j===a.key.length)return{code:a.code,alias:a.raw,rest:compact.slice(pos)}}return null}
function normalizeRest(rest){return String(rest||'').trim().replace(/[：]/g,':').replace(/[．]/g,'.').replace(/[－–—~～]|至|到/g,'-').replace(/\s+/g,'')}
function parseSegment(segment){const book=matchBookAtStart(segment);if(!book)return null;let r=normalizeRest(book.rest);if(!r)return null;let m;
// Explicit Chinese form: 帖後3章八節到十節 / 賽三第四節.
m=r.match(new RegExp(`^第?([${NUM_CHARS}]+)章第?([${NUM_CHARS}]+)節(?:-第?([${NUM_CHARS}]+)節)?$`));
if(!m)m=r.match(new RegExp(`^第?([${NUM_CHARS}]+)第([${NUM_CHARS}]+)節(?:-第?([${NUM_CHARS}]+)節)?$`));
if(m){const c=chineseNumber(m[1]),s=chineseNumber(m[2]),e=m[3]?chineseNumber(m[3]):s;if(Number.isFinite(c)&&Number.isFinite(s)&&Number.isFinite(e)&&e>=s)return{kind:s===e?'verse':'range',book:book.code,chapter:c,start:s,end:e,source:segment}}
// Mixed/compact form: 林前8:9-15 / 創2.5 / 帖後3章8-10.
r=r.replace(/第/g,'').replace(/章/g,':').replace(/節/g,'');
m=r.match(new RegExp(`^([${NUM_CHARS}]+)[:.]([${NUM_CHARS}]+)(?:-([${NUM_CHARS}]+))?$`));
if(m){const c=chineseNumber(m[1]),s=chineseNumber(m[2]),e=m[3]?chineseNumber(m[3]):s;if(Number.isFinite(c)&&Number.isFinite(s)&&Number.isFinite(e)&&e>=s)return{kind:s===e?'verse':'range',book:book.code,chapter:c,start:s,end:e,source:segment}}
// Chapter only: 帖後三 / 帖後3 / 帖後第三章.
m=r.match(new RegExp(`^([${NUM_CHARS}]+):?$`));if(m){const c=chineseNumber(m[1]);if(Number.isFinite(c))return{kind:'chapter',book:book.code,chapter:c,source:segment}}
return null}
function bookStarts(q){const text=String(q||'');const found=[];for(let i=0;i<text.length;i++){const tail=text.slice(i);const m=matchBookAtStart(tail);if(!m)continue;const after=m.rest;const next=after.match(new RegExp(`^\\s*[第${NUM_CHARS}]`));if(next){found.push(i);i+=Math.max(0,m.alias.length-1)}}return[...new Set(found)]}
function parseQuery(q){const text=String(q||'').trim();if(!text)return null;const starts=bookStarts(text);if(!starts.length)return null;const segments=[];for(let i=0;i<starts.length;i++){const end=i+1<starts.length?starts[i+1]:text.length;const seg=text.slice(starts[i],end).replace(/^[\s,，;；、]+|[\s,，;；、]+$/g,'');if(seg)segments.push(seg)}if(!segments.length)return null;const parsed=segments.map(parseSegment);if(parsed.some(x=>!x))return null;return parsed}
function hitsFor(p){const verses=(state.byChapter.get(`${p.book}.${p.chapter}`)||[]).slice().sort((a,b)=>Number(a.v)-Number(b.v));if(p.kind==='chapter')return verses;return verses.filter(v=>Number(v.v)>=p.start&&Number(v.v)<=p.end)}
function render(parsed){const seen=new Set(),hits=[];for(const p of parsed)for(const v of hitsFor(p)){if(seen.has(v.r))continue;seen.add(v.r);hits.push({v,p})}if(!hits.length)return false;const box=$('#results'),count=$('#result-count');if(!box||!count)return false;count.textContent=`${hits.length} 個結果 · ${parsed.length} 段經文`;box.innerHTML=hits.map(({v,p})=>`<article class="result-card"><header><strong>${esc(v.n?.[0]||v.b)} ${v.c}:${v.v}</strong><span>${esc(v.n?.[1]||v.b)} ${v.c}:${v.v}</span></header>${v.z?`<p lang="zh-Hant">${esc(v.z)}</p>`:''}${v.e?`<p class="english" lang="en">${esc(v.e)}</p>`:''}<footer><span>scripture-input-literacy · ${esc(p.kind)}</span><span>CUV / WEBU · Doré evidence corpus</span></footer></article>`).join('');$('#results-wrap')?.scrollIntoView({behavior:'smooth',block:'start'});return true}
async function execute(q){const parsed=parseQuery(q);if(!parsed)return false;return render(parsed)}
async function init(){try{const[c,i]=await Promise.all([fetch('/dore/scripture-input-literacy.json',{cache:'no-cache'}).then(r=>r.json()),fetch('/dore/search-index.json',{cache:'no-cache'}).then(r=>r.json())]);state.corpus=c;state.index=i;build();state.ready=true;window.DORE_SCRIPTURE_INPUT_LITERACY={version:'1.0',parseQuery,parseSegment,execute,corpus:c};const form=$('#search-form'),input=$('#search-input');if(form&&input&&!form.dataset.doreInputLiteracy){form.dataset.doreInputLiteracy='1';form.addEventListener('submit',e=>{if(!state.ready)return;const parsed=parseQuery(input.value);if(!parsed)return;e.preventDefault();e.stopImmediatePropagation();const u=new URL(location.href);u.searchParams.set('q',input.value.trim());history.replaceState({},'',u);render(parsed)},true)}const q=new URLSearchParams(location.search).get('q');if(q)setTimeout(()=>execute(q),80)}catch(err){console.warn('Doré Scripture Input Literacy unavailable',err)}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
