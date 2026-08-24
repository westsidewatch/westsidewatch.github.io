(()=>{
'use strict';
const state={brain:null,loading:null,bypassSearch:false};
const $=s=>document.querySelector(s);
const SENSORY_ORIGIN='https://westsidewatch-github-io.pages.dev';
const norm=s=>String(s??'').toLowerCase().normalize('NFKC').replace(/[\s.,;:!?，。；：！？「」『』()（）\-–—_'"`]/g,'');
const questionLike=q=>/[?？]/.test(q)||/(?:什麼|什么|為何|为何|為什麼|为什么|如何|怎樣|怎样|怎麼|怎么|是否|是不是|有沒有|有没有|有無|有无|能否|可否|哪裡|哪里|何處|何处|誰|谁|幾|几|多少|意思|解釋|解释|關係|关系|區別|区别|背景|原因|目的|代表|象徵|象征|預表|预表|教導|教导|神學|神学|工作|發生|发生|記載|记载|說明|说明|嗎\s*$|吗\s*$)/u.test(q);
const EXPRESSIONS={
 UNKNOWN:{label:'還不知道',lead:'這個問題，我現在還不知道。',line:'我已經聽見了。'},
 QUEUED:{label:'已經記下',lead:'我把這個問題留下來了。',line:'我會去查。'},
 RESEARCHING:{label:'正在研究',lead:'我正在查這個問題。',line:'有足夠把握以前，我不想先給你一個答案。'},
 WORKING:{label:'研究中',lead:'我找到了一些線索，但現在還不能確定。'},
 CANDIDATE_FOR_EXAM:{label:'等待驗證',lead:'我大概知道答案了，但還需要再驗證。'},
 CONSOLIDATED:{label:'已驗證神經'},
 DISPUTED:{label:'存在爭議',lead:'這個問題存在不同的解釋。'},
 REOPENED:{label:'重新考慮',lead:'我以前有一個答案，但新的證據讓我需要重新考慮。'}
};
async function loadBrain(force=false){if(force){state.brain=null;state.loading=null}if(state.brain)return state.brain;if(state.loading)return state.loading;state.loading=fetch(`${SENSORY_ORIGIN}/api/dore/brain`,{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json()}).then(d=>{state.brain=d;return d}).catch(e=>{console.error('Doré brain bridge load failed',e);return null});return state.loading}
function scoreNode(node,q){const nq=norm(q);if(!nq)return 0;let best=0;for(const v of node.questions||[]){const nv=norm(v);if(nv===nq)return 100;if((nv&&nq.includes(nv))||nv.includes(nq))best=Math.max(best,82)}let conceptHits=0;for(const c of node.concepts||[]){const nc=norm(c);if(nc&&nq.includes(nc))conceptHits++}if(conceptHits>=2)best=Math.max(best,72+Math.min(12,conceptHits*3));else if(conceptHits===1)best=Math.max(best,46);return best}
function chooseNode(brain,q){let best=null,bestScore=0;for(const node of brain?.nodes||[]){const s=scoreNode(node,q);if(s>bestScore){best=node;bestScore=s}}return bestScore>=70?{node:best,score:bestScore}:null}
function esc(s){return String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
function renderNode(node){const box=$('#results'),count=$('#result-count'),wrap=$('#results-wrap');if(!box||!count)return;const a=node.answer||{},status=node.status||'WORKING',x=EXPRESSIONS[status]||EXPRESSIONS.WORKING;const lead=x.lead||a.lead||'';const answerLead=x.lead&&a.lead?`<p class="brain-answer-lead">${esc(a.lead)}</p>`:'';const body=(a.body||[]).map(p=>`<p>${esc(p)}</p>`).join('');const refs=(node.scripture||[]).length?`<p class="brain-scripture"><strong>相關經文：</strong>${node.scripture.map(esc).join(' · ')}</p>`:'';const next=(node.next_research||[]).length?`<p class="brain-next"><strong>仍在研究：</strong>${node.next_research.map(esc).join(' · ')}</p>`:'';box.innerHTML=`<article class="brain-answer" data-brain-node="${esc(node.id)}" data-expression-state="${esc(status)}"><header><strong>DORÉ</strong><span>${esc(x.label)}</span></header><h3>${esc(lead)}</h3>${answerLead}${body}${refs}${a.boundary?`<p class="brain-boundary">${esc(a.boundary)}</p>`:''}${next}</article>`;count.textContent=status==='CONSOLIDATED'?'Doré 回答':'Doré · '+x.label;if(wrap)wrap.scrollIntoView({behavior:'smooth',block:'start'})}
async function remember(q){try{const r=await fetch(`${SENSORY_ORIGIN}/api/dore/sensory`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({query:q})});if(!r.ok)return null;const d=await r.json();return d?.ok?d:null}catch{return null}}
function addStyle(){if(document.getElementById('dore-brain-bridge-style'))return;const s=document.createElement('style');s.id='dore-brain-bridge-style';s.textContent=`.brain-answer{padding:2vw .15vw 1.2vw}.brain-answer header{display:flex;align-items:baseline;gap:1vw;border-bottom:1px solid rgba(82,62,20,.2);padding-bottom:.8vw;margin-bottom:1.2vw}.brain-answer header strong{color:#8c6818;font:500 1.35rem "Cormorant Garamond",serif;letter-spacing:.08em}.brain-answer header span{font-size:.72rem;opacity:.58}.brain-answer h3{font-size:1.05rem;font-weight:400;line-height:1.8;margin:0 0 1vw}.brain-answer p{line-height:2;margin:.8vw 0}.brain-answer-lead{font-weight:500}.brain-boundary,.brain-next{font-size:.82rem;opacity:.68}.brain-scripture{font-size:.86rem;color:#725719}@media(max-width:820px){.brain-answer{padding:24px 2px}.brain-answer p{margin:12px 0}.brain-answer header{margin-bottom:16px}}`;document.head.appendChild(s)}
async function resolveQuestion(form,q){const savedPromise=remember(q);const brain=await loadBrain(),hit=chooseNode(brain,q);if(hit){savedPromise.catch(()=>{});renderNode(hit.node);return}savedPromise.catch(()=>{});state.bypassSearch=true;form.requestSubmit()}
function intercept(e){const form=e.target;if(!(form instanceof HTMLFormElement)||form.id!=='search-form')return;if(state.bypassSearch){state.bypassSearch=false;return}const input=$('#search-input'),q=input?.value?.trim();if(!q||!questionLike(q)){if(q)remember(q).catch(()=>{});return}e.preventDefault();e.stopImmediatePropagation();resolveQuestion(form,q)}
addStyle();loadBrain();document.addEventListener('submit',intercept,true);
window.DoreBrainBridge={load:loadBrain,match:async q=>{const b=await loadBrain();return chooseNode(b,q)},render:renderNode,isQuestion:questionLike,expressions:EXPRESSIONS};
})();
