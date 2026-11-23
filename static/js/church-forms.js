/* Volunteer intake — feature-gated until a verified Cloudflare mail backend is live. */
(() => {
 'use strict';
 const types={
 newcomer:{title:'第一次來聚會',description:'歡迎新朋友。請告訴我們你希望參加哪一場聚會，以及怎樣與你聯繫。',
   fields:[['meeting','想參加的聚會','select',['主日崇拜','週一午間查經','週三線上禱告','週五晚間查經','希望先了解教會']],['message','想了解的事情','textarea']]},
 join:{title:'加入教會',description:'希望認識教會、穩定參加聚會，或進一步了解委身與服事，歡迎與同工聯繫。',
   fields:[['meeting','現在的聚會情況','select',['第一次了解','偶爾參加','經常參加','希望同工進一步介紹']],['message','對教會生活的期待','textarea']]},
 decision:{title:'信仰回應與決志',description:'願意認識耶穌、回應福音，或想與同工談一談信仰，歡迎留下你的回應。',
   fields:[['response','我的回應','select',['我願意進一步認識耶穌','我願意決志信主','我想與同工談談福音','我希望參加查經']],['message','想與同工分享','textarea']]},
 prayer:{title:'代禱與關懷',description:'如果你希望有人為你禱告或與你聯繫，請只填寫自己願意分享的內容。',
   fields:[['response','代禱與聯繫需求','select',['希望同工私下代禱','希望有人與我聯繫','希望牧養關懷']],['message','代禱事項（請避免敏感身分資訊）','textarea']]}
 };
 const type=new URLSearchParams(location.search).get('type')||'newcomer';const current=types[type]||types.newcomer;
 const form=document.querySelector('#church-intake'),heading=document.querySelector('#form-title'),description=document.querySelector('#form-description'),
   extra=document.querySelector('#church-intake-extra'),status=document.querySelector('#form-status'),button=document.querySelector('#church-submit');
 heading.textContent=current.title;description.textContent=current.description;
 const setStatus=s=>status.textContent=s;let online=false;
 for(const [key,label,kind,options] of current.fields){
   const wrap=document.createElement('label');wrap.textContent=label;
   const input=kind==='textarea'?document.createElement('textarea'):document.createElement('select');
   input.name=key;if(kind==='textarea'){input.maxLength=1500;input.rows=5}else{
     const empty=document.createElement('option');empty.value='';empty.textContent='請選擇';input.append(empty);
     for(const option of options){const o=document.createElement('option');o.value=o.textContent=option;input.append(o);}
   }
   wrap.append(input);extra.append(wrap);
 }
 function loadTurnstile(sitekey){
   if(!sitekey)throw Error('missing Turnstile sitekey');
   const mount=document.getElementById('church-turnstile');
   const widget=document.createElement('div');widget.className='cf-turnstile';widget.dataset.sitekey=sitekey;widget.dataset.theme='light';mount.append(widget);
   const script=document.createElement('script');script.src='https://challenges.cloudflare.com/turnstile/v0/api.js';script.async=true;script.defer=true;
   script.onerror=()=>{online=false;button.disabled=true;setStatus('無法載入安全驗證，請透過教會郵箱聯繫。');};document.head.append(script);
 }
 fetch('/api/church-intake',{cache:'no-store',headers:{Accept:'application/json'}}).then(async r=>r.ok?r.json():null).then(config=>{
   if(!config?.ready||!config.turnstileSiteKey)throw Error('intake not configured');
   loadTurnstile(config.turnstileSiteKey);online=true;button.disabled=false;setStatus('線上收件已開放。送出前請完成安全驗證。');
 }).catch(()=>{online=false;button.disabled=true;setStatus('線上收件目前未開放。請透過教會聯絡信箱與我們聯繫。');});
 form.addEventListener('submit',async ev=>{
   ev.preventDefault();if(!online)return;
   const data=new FormData(form);const name=String(data.get('name')||'').trim(),email=String(data.get('email')||'').trim(),phone=String(data.get('phone')||'').trim();
   if(!name||(!email&&!phone)||data.get('consent')!=='yes'||!form.checkValidity()){setStatus('請填寫姓名、至少一種聯絡方式，並勾選同意聯繫。');form.reportValidity();return;}
   if(!data.get('cf-turnstile-response')){setStatus('請完成安全驗證後再送出。');return;}
   data.set('type',type in types?type:'newcomer');
   button.disabled=true;setStatus('正在安全送出…');
   try{
     const response=await fetch('/api/church-intake',{method:'POST',body:data,cache:'no-store',headers:{Accept:'application/json'}});
     const result=await response.json().catch(()=>({}));
     if(!response.ok||!result.ok)throw Error('not delivered');
     form.reset();setStatus('已收到教會收件系統的確認。謝謝你的聯繫，同工會依所留方式跟進。');
   }catch(_){setStatus('目前未能確認送達教會，請使用教會郵箱聯繫；不要重複送出敏感資料。');}
   finally{button.disabled=!online;}
 });
})();
