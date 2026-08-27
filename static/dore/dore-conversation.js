(()=>{
'use strict';
const API='/api/dore/live';
const PROJECT='dore-search';
const KEY='dore.conversation.id.v1';
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
function id(){let v=sessionStorage.getItem(KEY);if(!v){v='web-'+Date.now().toString(36)+'-'+crypto.getRandomValues(new Uint32Array(2)).join('-');sessionStorage.setItem(KEY,v)}return v}
function newConversation(){sessionStorage.removeItem(KEY);location.reload()}
function render(role,text){const log=$('#dore-conversation-log');if(!log)return;const article=document.createElement('article');article.className='dore-turn '+role;article.innerHTML=`<b>${role==='user'?'你':'DORÉ'}</b><p>${esc(text).replace(/\n/g,'<br>')}</p>`;log.appendChild(article);article.scrollIntoView({behavior:'smooth',block:'nearest'})}
async function send(text){const input=$('#dore-conversation-input'),button=$('#dore-conversation-send'),status=$('#dore-conversation-status');button.disabled=true;input.disabled=true;status.textContent='Doré 正在回答…';render('user',text);try{const r=await fetch(API,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({project_id:PROJECT,conversation_id:id(),actor_id:'web-user',content:text,title:'Doré Search Conversation'})});const data=await r.json().catch(()=>({}));if(!r.ok||!data?.ok)throw new Error(data?.detail||data?.error||`HTTP ${r.status}`);render('assistant',data.answer);status.textContent=data?.memory?.automatic?'本輪對話已進入 Doré 記憶。':'回答完成。'}catch(e){render('assistant','目前無法完成這次對話。請稍後再試。');status.textContent='對話失敗：'+e.message}finally{button.disabled=false;input.disabled=false;input.focus()}}
function bind(){const form=$('#dore-conversation-form');if(!form)return;form.addEventListener('submit',e=>{e.preventDefault();const input=$('#dore-conversation-input'),text=input.value.trim();if(!text)return;input.value='';send(text)});$('#dore-new-conversation')?.addEventListener('click',newConversation)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind,{once:true});else bind();
})();