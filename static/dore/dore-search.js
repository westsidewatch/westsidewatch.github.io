(()=>{
'use strict';
const state={data:null,original:null,originalLoading:null,byRef:new Map(),byChapter:new Map(),aliases:new Map(),ready:false};
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const ZH_VARIANTS={'虚':'虛','来':'來','语':'語','书':'書','马':'馬','约':'約','传':'傳','罗':'羅','后':'後','数':'數','创':'創','启':'啟','亚':'亞','结':'結','历':'歷','腊':'臘','这':'這','个':'個','里':'裡','门':'門','东':'東','国':'國','爱':'愛','灵':'靈','体':'體','万':'萬','与':'與','为':'為','义':'義','圣':'聖','经':'經','节':'節','处':'處','发':'發','从':'從','条':'條','树':'樹','见':'見','听':'聽','说':'說','问':'問','应':'應','难':'難','亲':'親','风':'風','声':'聲','头':'頭','会':'會','开':'開','长':'長','无':'無','时':'時','实':'實','进':'進','当':'當','归':'歸','众':'眾','还':'還','泽':'澤','乡':'鄉','显':'顯','灭':'滅','将':'將','谁':'誰','让':'讓','觉':'覺','称':'稱','复':'復','获':'獲','读':'讀','写':'寫','译':'譯','词':'詞','证':'證','据':'據','类':'類','别':'別','简':'簡','繁':'繁'};
const zhFold=s=>String(s??'').replace(/[\u3400-\u9fff]/g,ch=>ZH_VARIANTS[ch]||ch);
const norm=s=>zhFold(String(s??'').toLowerCase()).replace(/[\s.,;:!?，。；：！？「」『』()（）\-–—]/g,'');
const refLabel=v=>`${v.n?.[0]||v.b} ${v.c}:${v.v}`;
const chapterKey=(book,chapter)=>`${book}.${Number(chapter)}`;
const ZH_NUM={零:0,'〇':0,一:1,二:2,三:3,四:4,五:5,六:6,七:7,八:8,九:9,兩:2,两:2};
function chineseNumber(value){const s=String(value||'').trim();if(/^\d+$/.test(s))return Number(s);if(!s)return NaN;if(s.includes('百')){const[a,b='']=s.split('百');return(a?ZH_NUM[a]:1)*100+(b?chineseNumber(b):0)}if(s.includes('十')){const[a,b='']=s.split('十');return(a?ZH_NUM[a]:1)*10+(b?ZH_NUM[b]:0)}if(s.length===1&&s in ZH_NUM)return ZH_NUM[s];return NaN}
function addAlias(alias,code){if(alias)state.aliases.set(norm(alias),code)}
function buildAliases(){for(const v of state.data.verses){state.byRef.set(v.r,v);const key=chapterKey(v.b,v.c);if(!state.byChapter.has(key))state.byChapter.set(key,[]);state.byChapter.get(key).push(v);for(const name of[v.b,...(v.n||[])]){addAlias(name,v.b);addAlias(String(name).replace(/s$/i,''),v.b)}}}
function resolveBook(raw){return state.aliases.get(norm(raw))||null}
function parseReference(){return null}
function interpret(q){return{kind:'plain',phrase:q.trim()}}
const looksOriginal=q=>/[\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff]/.test(q)||/^([GH]\d+|[@A-Z][A-Za-z0-9@/+:.-]{2,})$/.test(q);
async function ensureOriginal(){return state.original}
function idsFromOriginal(){return[]}
function originalEvidence(){return null}
function lexicalContains(text,q){const a=norm(text),b=norm(q);if(!a||!b)return false;if(b==='馬利亞'){let from=0;while((from=a.indexOf(b,from))!==-1){if(from===0||a[from-1]!=='撒')return true;from+=b.length}return false}return a.includes(b)}
function scoreFuzzy(text,q){const a=norm(text),b=norm(q);if(!a||!b||b.length<3)return 0;if(b==='馬利亞'&&a.includes('撒馬利亞')&&!lexicalContains(text,q))return 0;if(a.includes(b)||b.includes(a))return .98;return 0}
function textSearch(q,type='exact-text'){const n=norm(q),exact=[],fuzzy=[];for(const v of state.data.verses){if(n&&(lexicalContains(v.z,q)||lexicalContains(v.e,q))){exact.push({v,score:1,type});continue}const score=Math.max(scoreFuzzy(v.z,q),scoreFuzzy(v.e,q));if(score>=.5)fuzzy.push({v,score,type:'fuzzy'})}if(exact.length)return exact.slice(0,50);fuzzy.sort((a,b)=>b.score-a.score||a.v.r.localeCompare(b.v.r));return fuzzy.slice(0,30)}
function search(q){return textSearch(q)}
function render(hits){const box=$('#results'),count=$('#result-count');if(!hits.length){count.textContent='沒有可靠結果';box.innerHTML='<div class="empty">找不到足夠可靠的候選。</div>';return}count.textContent=`${hits.length} 個結果`;box.innerHTML=hits.map(({v,type})=>`<article class="result-card"><header><strong>${esc(refLabel(v))}</strong><span>${esc(type)}</span></header><p>${esc(v.z)}</p><p class="english">${esc(v.e)}</p></article>`).join('')}
async function run(q){if(!state.ready)return;render(search(q))}
async function init(){const res=await fetch('/dore/bible-index.json',{cache:'no-cache'});state.data=await res.json();buildAliases();state.ready=true;const form=$('#search-form'),input=$('#search-input');form?.addEventListener('submit',e=>{e.preventDefault();run(input.value.trim())});const q=new URL(location.href).searchParams.get('q');if(q&&input){input.value=q;run(q)}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();