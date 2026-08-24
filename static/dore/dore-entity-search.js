(()=>{
'use strict';
let index=null,loading=null;
const $=s=>document.querySelector(s);
const ZH={'马':'馬','亚':'亞','约':'約','玛':'瑪','罗':'羅','稣':'穌','经':'經','圣':'聖','里':'裡','个':'個','几':'幾','这':'這'};
const fold=s=>String(s??'').toLowerCase().replace(/[\u3400-\u9fff]/g,c=>ZH[c]||c).replace(/[\s·.\-–—，。！？?、:：;；()（）「」『』]/g,'');
async function ensure(){if(index)return index;if(loading)return loading;loading=fetch('/dore/entity-index.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error(`entity index ${r.status}`);return r.json()}).then(d=>{if(d.schema!=='dore.browser-entity-index.v1')throw new Error('unsupported entity index');index=d;return d}).catch(e=>{console.warn('Doré entity index unavailable',e);return null});return loading}
function parseCount(raw){const q=String(raw||'').replace(/\s+/g,'');let m=q.match(/^(?:聖經|圣经)(?:中|裡|里)?(?:一共|總共|总共)?有(?:幾|几|多少)(?:位|個|个)?(.+?)[？?]?$/);if(!m)m=q.match(/^(?:聖經|圣经)(?:中|裡|里)?(.+?)(?:一共|總共|总共)?有(?:幾|几|多少)(?:位|個|个)?[？?]?$/);return m?m[1].replace(/[？?，,。]+$/,''):null}
function names(e){return [e.p,...(e.a||[]).map(a=>a.v)]}
function exactEntities(mention,type=null){const n=fold(mention);return (index?.entities||[]).filter(e=>(!type||e.t===type)&&names(e).some(x=>fold(x)===n))}
function sourceNameCluster(entities,type=null){const sourceNames=new Set(entities.map(e=>fold(e.p)).filter(Boolean));if(!sourceNames.size)return entities;return (index?.entities||[]).filter(e=>(!type||e.t===type)&&sourceNames.has(fold(e.p)))}
function entityMeta(raw){const direct=exactEntities(raw);if(!direct.length)return null;const people=sourceNameCluster(direct.filter(e=>e.t==='person'),'person');const places=sourceNameCluster(direct.filter(e=>e.t==='place'),'place');return{direct,people,places}}
function renderEntityContext(raw,meta){const box=$('#results');if(!box||!meta)return;box.querySelector('.entity-context-card')?.remove();const card=document.createElement('article');card.className='result-card entity-context-card';const labels=[meta.people.length?`${meta.people.length} 個人物個體`:null,meta.places.length?`${meta.places.length} 個地點`:null].filter(Boolean).join(' · ');card.innerHTML=`<header><strong>${raw.replace(/[&<>"']/g,'')}</strong><span>BW-1 Entity identity</span></header><p>${labels||`${meta.direct.length} 個實體候選`}。下方仍保留完整經文搜尋結果；Entity 是附加的身份層，不取代 Scripture Search。</p><footer><span>STEPBible TIPNR entity context</span><span>經文結果由原 Scripture Search 提供</span></footer>`;box.prepend(card)}
async function handler(event){const raw=String(event?.detail?.query||'').trim();if(!raw)return;const countMention=parseCount(raw);const maybeName=/^[\u3400-\u9fffA-Za-z\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff· .\-]{2,40}$/.test(raw);if(!countMention&&!maybeName)return;const d=await ensure();if(!d)return;const mention=countMention||raw;const direct=exactEntities(mention,countMention?'person':null);if(!direct.length)return;const meta=countMention?{direct,people:sourceNameCluster(direct,'person'),places:[]}:entityMeta(raw);renderEntityContext(mention,meta)}
function init(){if(window.__doreEntityRuntimeBound)return;window.__doreEntityRuntimeBound=true;window.addEventListener('dore:search-query',handler,false)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
