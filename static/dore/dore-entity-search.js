(()=>{
'use strict';
let index=null,loading=null,bypass=false;
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const ZH={'马':'馬','亚':'亞','约':'約','玛':'瑪','罗':'羅','稣':'穌','经':'經','圣':'聖','里':'裡','个':'個','几':'幾','这':'這'};
const fold=s=>String(s??'').toLowerCase().replace(/[\u3400-\u9fff]/g,c=>ZH[c]||c).replace(/[\s·.\-–—，。！？?、:：;；()（）「」『』]/g,'');
const sourceFold=s=>String(s??'').trim().toLowerCase().replace(/[\s._\-–—]+/g,'');
async function ensure(){if(index)return index;if(loading)return loading;loading=fetch('/dore/entity-index.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error(`entity index ${r.status}`);return r.json()}).then(d=>{if(d.schema!=='dore.browser-entity-index.v1')throw new Error('unsupported entity index');index=d;return d}).catch(e=>{console.warn('Doré entity index unavailable',e);return null});return loading}
function parseCount(raw){const q=String(raw||'').replace(/\s+/g,'');let m=q.match(/^(?:聖經|圣经)(?:中|裡|里)?(?:一共|總共|总共)?有(?:幾|几|多少)(?:位|個|个)?(.+?)[？?]?$/);if(!m)m=q.match(/^(?:聖經|圣经)(?:中|裡|里)?(.+?)(?:一共|總共|总共)?有(?:幾|几|多少)(?:位|個|个)?[？?]?$/);return m?m[1].replace(/[？?，,。]+$/,''):null}
function names(e){return [e.p,...(e.a||[]).map(a=>a.v)]}
function exactEntities(mention,type=null){const n=fold(mention);return (index?.entities||[]).filter(e=>(!type||e.t===type)&&names(e).some(x=>fold(x)===n))}
function countEntities(mention){
 const seeds=exactEntities(mention,'person');if(!seeds.length)return[];
 // A translated alias may occur only on some individualised records. Once it
 // resolves to a source name (e.g. a source preferred label), expand across all
 // source-individualised person records sharing that exact source name. This is
 // name-cluster aggregation, not identity merging.
 const sourceNames=new Set();
 for(const e of seeds){if(e.p)sourceNames.add(sourceFold(e.p));for(const a of(e.a||[]))if(a.l==='en'&&a.v)sourceNames.add(sourceFold(a.v))}
 const expanded=(index?.entities||[]).filter(e=>e.t==='person'&&[e.p,...(e.a||[]).filter(a=>a.l==='en').map(a=>a.v)].some(x=>sourceNames.has(sourceFold(x))));
 const byId=new Map([...seeds,...expanded].map(e=>[e.id,e]));return [...byId.values()];
}
function refLabel(ref){return String(ref||'').replace(/^bible\.ref\./,'').replace(/\./g,' ')}
function renderEntities(mention,entities,mode='entity'){
 const box=$('#results'),count=$('#result-count');if(!box||!count)return;
 if(!entities.length){count.textContent='沒有可靠實體結果';box.innerHTML='<div class="empty">找不到足夠可靠的實體候選。</div>';return}
 count.textContent=mode==='count'?`${entities.length} 個來源個體候選`:`${entities.length} 個實體候選`;
 let intro='';if(mode==='count')intro=`<article class="result-card"><header><strong>${esc(mention)}</strong><span>全經 Entity aggregation</span></header><p>目前來源個體化資料辨識出 <strong>${entities.length}</strong> 個人物候選。這是同一來源名稱之下的個體化記錄，不是把身份爭議強行化成單一神學結論；後續研究若支持或反對某些身份合併，Doré 會分層呈現。</p><footer><span>BW-1 entity-count</span><span>STEPBible TIPNR · canonical attestations</span></footer></article>`;
 box.innerHTML=intro+entities.slice(0,40).map(e=>{const zh=(e.a||[]).find(a=>a.l==='zh-Hant')?.v;const refs=(e.r||[]).slice(0,8);return `<article class="result-card"><header><strong>${esc(zh||e.p)}</strong><span>${esc(e.t)} · ${esc(e.p)}</span></header><p>${refs.length?`經文見證：${refs.map(refLabel).map(esc).join(' · ')}`:'目前僅有來源個體化見證'}</p><p class="english">Aliases: ${esc((e.a||[]).slice(0,8).map(a=>a.v).join(' · '))}</p><footer><span>entity-reflex</span><span>${esc(e.src||'STEPBible/TIPNR')}</span></footer></article>`}).join('');
 $('#results-wrap')?.scrollIntoView({behavior:'smooth',block:'start'});
}
async function handler(ev){
 if(bypass){bypass=false;return}
 const input=$('#search-input');if(!input)return;const raw=input.value.trim();if(!raw)return;
 const countMention=parseCount(raw);
 const maybeName=/^[\u3400-\u9fffA-Za-z\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff· .\-]{2,40}$/.test(raw);
 if(!countMention&&!maybeName)return;
 ev.preventDefault();ev.stopImmediatePropagation();
 const d=await ensure();if(!d){bypass=true;$('#search-form')?.requestSubmit();return}
 if(countMention){const es=countEntities(countMention);if(es.length){renderEntities(countMention,es,'count');history.replaceState(null,'',`#q=${encodeURIComponent(raw)}`);return}bypass=true;$('#search-form')?.requestSubmit();return}
 const es=exactEntities(raw);if(es.length){renderEntities(raw,es,'entity');history.replaceState(null,'',`#q=${encodeURIComponent(raw)}`);return}
 bypass=true;$('#search-form')?.requestSubmit();
}
function init(){const form=$('#search-form');if(form&&!form.dataset.doreEntityBound){form.dataset.doreEntityBound='1';form.addEventListener('submit',handler,true)}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
