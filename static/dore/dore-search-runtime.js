(()=>{
'use strict';
if(window.DoreSearchRuntime?.version)return;
const CONVERSATION_KEY='dore.conversation.current.v7';
const MODE_KEY='dore.ai.mode.v2';
const LOCAL_HEALTH='http://127.0.0.1:8788/health';
const LOCAL_CHAT='http://127.0.0.1:8788/chat';
const LOCAL_CONVERSATIONS='http://127.0.0.1:8788/conversations';
const LOCAL_CONVERSATION='http://127.0.0.1:8788/conversation';
const PROJECT_ID='dore-search';
const $=s=>document.querySelector(s);
const uuid=()=>crypto.randomUUID?.()||`${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function conversationId(){let v=localStorage.getItem(CONVERSATION_KEY);if(!v){v=uuid();localStorage.setItem(CONVERSATION_KEY,v)}return v}
function setConversationId(id){if(id)localStorage.setItem(CONVERSATION_KEY,id);return conversationId()}
function newConversation(){const id=uuid();setConversationId(id);renderConversationShell([]);return id}
function snapshot(){const input=$('#search-input');return{query:input?.value?.trim()||'',input,results:$('#results'),count:$('#result-count'),conversation_id:conversationId()}}
function aiMode(){return sessionStorage.getItem(MODE_KEY)==='on'}
function setAiMode(on){if(on)sessionStorage.setItem(MODE_KEY,'on');else sessionStorage.removeItem(MODE_KEY);document.body.classList.toggle('dore-ai-mode',!!on);window.dispatchEvent(new CustomEvent('dore:ai-mode',{detail:{enabled:!!on}}));return !!on}
function isOpenCommand(v=''){return /^(?:(?:問|问)多雷|ask\s+dore)[!！。.?？\s]*$/i.test(String(v).trim())}
function isCloseCommand(v=''){return /^(?:搜索|search)[!！。.?？\s]*$/i.test(String(v).trim())}
function inlineMarkdown(s){return esc(s).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/__([^_]+)__/g,'<strong>$1</strong>').replace(/\*([^*\n]+)\*/g,'<em>$1</em>')}
function markdown(s=''){
 const lines=String(s).replace(/\r\n?/g,'\n').split('\n'),out=[];let list=null;
 const close=()=>{if(list){out.push(`</${list}>`);list=null}};
 for(const raw of lines){const t=raw.trim();if(!t){close();continue}let m;
  if(/^---+$/.test(t)){close();out.push('<hr>');continue}
  m=t.match(/^(#{1,4})\s+(.+)$/);if(m){close();const n=Math.min(4,m[1].length);out.push(`<h${n}>${inlineMarkdown(m[2])}</h${n}>`);continue}
  m=t.match(/^[-*]\s+(.+)$/);if(m){if(list!=='ul'){close();list='ul';out.push('<ul>')}out.push(`<li>${inlineMarkdown(m[1])}</li>`);continue}
  m=t.match(/^\d+[.)]\s+(.+)$/);if(m){if(list!=='ol'){close();list='ol';out.push('<ol>')}out.push(`<li>${inlineMarkdown(m[1])}</li>`);continue}
  close();out.push(`<p>${inlineMarkdown(t)}</p>`)
 }
 close();return out.join('')
}
function installConversationUI(){
 if($('#dore-conversation-toolbar'))return;
 const style=document.createElement('style');style.id='dore-conversation-style';style.textContent=`
 body.dore-ai-mode .capabilities,body.dore-ai-mode .info{display:none}
 body.dore-ai-mode .results-wrap{margin-top:1.2rem}
 #dore-conversation-toolbar{display:none;width:min(68vw,1080px);margin:1rem auto .4rem;align-items:center;justify-content:space-between;gap:.8rem}
 body.dore-ai-mode #dore-conversation-toolbar{display:flex}
 .dore-conv-left,.dore-conv-right{display:flex;align-items:center;gap:.55rem}
 .dore-conv-btn{border:1px solid rgba(116,85,20,.28);background:rgba(255,253,246,.7);color:#765619;border-radius:999px;padding:.5rem .9rem;font:500 .76rem "Noto Serif TC",serif;cursor:pointer}
 .dore-conv-label{font:500 .84rem "Cormorant Garamond","Noto Serif TC",serif;color:#765619;letter-spacing:.04em}
 #dore-history-panel{display:none;width:min(68vw,1080px);margin:.5rem auto 1rem;border:1px solid rgba(95,70,20,.2);background:rgba(255,253,246,.82);backdrop-filter:blur(8px);border-radius:12px;max-height:340px;overflow:auto}
 #dore-history-panel.on{display:block}
 .dore-history-item{padding:.85rem 1rem;border-bottom:1px solid rgba(82,62,20,.12);cursor:pointer}
 .dore-history-item:hover{background:rgba(206,189,116,.16)}
 .dore-history-item strong{display:block;font-size:.82rem;font-weight:500}.dore-history-item span{display:block;margin-top:.25rem;font-size:.68rem;opacity:.58;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
 .dore-chat{display:flex;flex-direction:column;gap:1.35rem;padding:1rem 0 2rem}
 .dore-turn{display:flex;flex-direction:column;gap:.7rem;border-bottom:1px solid rgba(82,62,20,.08);padding-bottom:1.15rem}
 .dore-msg{max-width:86%;padding:.95rem 1.05rem;border-radius:14px;line-height:1.8;font-size:.92rem}
 .dore-msg.user{align-self:flex-end;background:rgba(255,253,246,.82);border:1px solid rgba(116,85,20,.22)}
 .dore-msg.assistant{align-self:flex-start;background:rgba(206,189,116,.18);border:1px solid rgba(116,85,20,.14)}
 .dore-msg.assistant .who{color:#8c6818;font:600 .75rem "Cormorant Garamond",serif;letter-spacing:.12em;margin-bottom:.35rem}
 .dore-msg.pending{opacity:.58}
 body.dore-ai-mode #result-count{font-size:.7rem}
 @media(max-width:820px){#dore-conversation-toolbar,#dore-history-panel{width:calc(100% - 24px)}.dore-msg{max-width:94%}}
 `;document.head.appendChild(style);
 const toolbar=document.createElement('div');toolbar.id='dore-conversation-toolbar';toolbar.innerHTML=`<div class="dore-conv-left"><span class="dore-conv-label">DORÉ · CONVERSATION</span></div><div class="dore-conv-right"><button class="dore-conv-btn" id="dore-history-btn" type="button">歷史</button><button class="dore-conv-btn" id="dore-new-btn" type="button">新對話</button><button class="dore-conv-btn" id="dore-search-btn" type="button">SEARCH</button></div>`;
 const state=$('#dore-ai-state');state?.insertAdjacentElement('afterend',toolbar);
 const panel=document.createElement('div');panel.id='dore-history-panel';toolbar.insertAdjacentElement('afterend',panel);
 $('#dore-history-btn')?.addEventListener('click',async()=>{panel.classList.toggle('on');if(panel.classList.contains('on'))await loadConversationList()});
 $('#dore-new-btn')?.addEventListener('click',()=>{newConversation();panel.classList.remove('on');$('#search-input')?.focus()});
 $('#dore-search-btn')?.addEventListener('click',()=>closeConversationMode());
}
function messageHTML(m){const role=m.role==='assistant'?'assistant':'user';return `<article class="dore-msg ${role}">${role==='assistant'?'<div class="who">DORÉ</div>':''}<div>${role==='assistant'?markdown(m.content):esc(m.content)}</div></article>`}
function groupTurns(messages=[]){const turns=[];let current=null;for(const m of messages){if(m.role==='user'){current=[m];turns.push(current)}else if(current){current.push(m);current=null}else{turns.push([m])}}return turns.reverse()}
function renderConversationShell(messages=[]){const box=$('#results'),count=$('#result-count');if(!box)return;const turns=groupTurns(messages);box.innerHTML=`<div class="dore-chat">${turns.map(t=>`<section class="dore-turn">${t.map(messageHTML).join('')}</section>`).join('')}</div>`;if(count)count.textContent=messages.length?`${messages.length} messages · 最新在上`:'新對話'}
function prependTurn(user){let chat=$('#results .dore-chat');if(!chat){renderConversationShell([]);chat=$('#results .dore-chat')}const turn=document.createElement('section');turn.className='dore-turn';turn.innerHTML=`<article class="dore-msg user"><div>${esc(user)}</div></article><article class="dore-msg assistant pending"><div class="who">DORÉ</div><div>${markdown('Doré 回應中…')}</div></article>`;chat.insertBefore(turn,chat.firstChild);return {turn,wait:turn.querySelector('.dore-msg.assistant')}}
async function localReady(timeoutMs=1100){const c=new AbortController(),t=setTimeout(()=>c.abort(),timeoutMs);try{const r=await fetch(LOCAL_HEALTH,{cache:'no-store',signal:c.signal});if(!r.ok)return false;const d=await r.json();return d?.ok===true&&d?.node==='dore-local'}catch{return false}finally{clearTimeout(t)}}
async function fetchHistory(cid=conversationId()){if(!(await localReady()))return null;try{const u=`${LOCAL_CONVERSATION}?project_id=${encodeURIComponent(PROJECT_ID)}&conversation_id=${encodeURIComponent(cid)}`;const r=await fetch(u,{cache:'no-store'});if(r.status===404)return {messages:[]};const d=await r.json();return r.ok&&d?.ok?d:null}catch{return null}}
async function loadCurrentConversation(){const d=await fetchHistory();renderConversationShell(d?.messages||[])}
async function loadConversationList(){const panel=$('#dore-history-panel');if(!panel)return;panel.innerHTML='<div class="dore-history-item"><span>讀取中…</span></div>';try{if(!(await localReady()))throw new Error('local offline');const r=await fetch(`${LOCAL_CONVERSATIONS}?project_id=${encodeURIComponent(PROJECT_ID)}`,{cache:'no-store'});const d=await r.json();if(!r.ok||!d?.ok)throw new Error('history unavailable');const items=d.conversations||[];panel.innerHTML=items.length?items.map(x=>`<div class="dore-history-item" data-cid="${esc(x.id)}"><strong>${esc(x.title||'New conversation')}</strong><span>${esc(x.preview||x.updated_at||'')}</span></div>`).join(''):'<div class="dore-history-item"><span>尚無歷史對話</span></div>';panel.querySelectorAll('[data-cid]').forEach(el=>el.addEventListener('click',async()=>{setConversationId(el.dataset.cid);panel.classList.remove('on');await loadCurrentConversation();$('#search-input')?.focus()}))}catch{panel.innerHTML='<div class="dore-history-item"><span>Doré Local 暫時無法讀取歷史。</span></div>'}}
async function converse(detail){const created=prependTurn(detail.query),wait=created.wait;const count=$('#result-count');if(count)count.textContent='Doré 回應中 · 最新在上';try{if(!(await localReady()))throw new Error('Doré Local 未連線');const r=await fetch(LOCAL_CHAT,{method:'POST',headers:{'content-type':'application/json',accept:'application/json'},body:JSON.stringify({message:detail.query,conversation_id:detail.conversation_id,project_id:PROJECT_ID})});const d=await r.json();if(!r.ok||!d?.ok)throw new Error(d?.detail||d?.error||`HTTP ${r.status}`);wait.classList.remove('pending');wait.innerHTML=`<div class="who">DORÉ</div><div>${markdown(d.reply||'')}</div>`;if(count)count.textContent='已保存 · Local · 最新在上';window.dispatchEvent(new CustomEvent('dore:conversation-response',{detail:d}));return d}catch(e){wait.classList.remove('pending');wait.innerHTML=`<div class="who">DORÉ</div><div>${esc('Doré 對話目前不可用。 '+String(e?.message||e))}</div>`;if(count)count.textContent='對話失敗';return null}}
async function openConversationMode(){setAiMode(true);installConversationUI();const input=$('#search-input'),button=$('#search-button'),state=$('#dore-ai-state');if(input){input.value='';input.placeholder='和 Doré 對話…';input.focus()}if(button)button.textContent='傳送';if(state){state.classList.add('on');state.textContent='Conversation · Local · 對話會立即保存，可離開後再回來繼續。'}await loadCurrentConversation()}
function closeConversationMode(){setAiMode(false);const input=$('#search-input'),button=$('#search-button'),state=$('#dore-ai-state');if(input){input.value='';input.placeholder='搜索經文、整章、關鍵詞、原文字詞…';input.focus()}if(button)button.textContent='搜索';if(state){state.classList.remove('on');state.textContent=''}$('#dore-history-panel')?.classList.remove('on');const box=$('#results'),count=$('#result-count');if(box)box.innerHTML='';if(count)count.textContent='等待搜索'}
function onSubmit(event){const form=event.target;if(!(form instanceof HTMLFormElement)||form.id!=='search-form')return;const snap=snapshot(),raw=snap.query;if(isOpenCommand(raw)){event.preventDefault();event.stopImmediatePropagation();openConversationMode();return}if(aiMode()){if(isCloseCommand(raw)){event.preventDefault();event.stopImmediatePropagation();closeConversationMode();return}if(!raw)return;event.preventDefault();event.stopImmediatePropagation();if(snap.input)snap.input.value='';converse({...snap,query:raw});return}}
function init(){if(document.documentElement.dataset.doreConversationBound)return;document.documentElement.dataset.doreConversationBound='1';installConversationUI();document.addEventListener('submit',onSubmit,true);if(aiMode())openConversationMode()}
window.DoreSearchRuntime={version:'7.1.0',snapshot,conversationId,setConversationId,newConversation,converse,aiMode,setAiMode,isOpenCommand,isCloseCommand,localReady,loadCurrentConversation,loadConversationList,openConversationMode,closeConversationMode};
init();
})();
