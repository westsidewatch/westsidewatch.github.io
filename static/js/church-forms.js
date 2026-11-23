/* Volunteer intake — feature-gated until a verified Cloudflare mail backend is live. */
(() => {
 'use strict';
 const types={
 newcomer:{title:'第一次來聚會',description:'歡迎新朋友。請告訴我們你希望參加哪一場聚會，以及怎樣與你聯繫。',
   fields:[['meeting','想參加的聚會','select',['主日崇拜','週一午間查經','週三線上禱告','週五晚間查經','希望先了解教會']],['message','想了解的事情','textarea']]},
 join:{title:'加入教會',description:'希望認識教會、穩定參加聚會，或進一步了解委身與服事，歡迎與同工聯繫。',
   fields:[['meeting','現在的聚會情況','select',['第一次了解','偶爾參加','經常參加','希望同工進一步介紹']],['message','對教會生活的期待','textarea']]},
 decision:{title:'信仰回應與決志',description:'從神的愛、基督的十字架與復活，認識福音。你可以決志信靠耶穌，也可以先與牧者查經、提問。',
   fields:[['response','我此刻的信仰回應','select',['我願意悔改，信靠耶穌基督為我的救主與主','我已經相信主耶穌，希望開始門徒生活','我正在尋求，願意與同工一起讀經','我想了解受洗與加入教會的道路','我有疑問，希望先與牧者談一談']],['message','我的問題、感動或希望有人為我禱告的事（選填）','textarea']]},
 prayer:{title:'代禱與關懷',description:'如果你希望有人為你禱告或與你聯繫，請只填寫自己願意分享的內容。',
   fields:[['response','代禱與聯繫需求','select',['希望同工私下代禱','希望有人與我聯繫','希望牧養關懷']],['message','代禱事項（請避免敏感身分資訊）','textarea']]}
 };
 const type=new URLSearchParams(location.search).get('type')||'newcomer';const current=types[type]||types.newcomer;
 const form=document.querySelector('#church-intake'),heading=document.querySelector('#form-title'),description=document.querySelector('#form-description'),
   extra=document.querySelector('#church-intake-extra'),status=document.querySelector('#form-status'),button=document.querySelector('#church-submit');
 heading.textContent=current.title;description.textContent=current.description;
 document.body.dataset.intakeType=type in types?type:'newcomer';
 if(type==='decision'){
   const first=document.createElement('span');first.textContent='信仰回應';
   const second=document.createElement('span');second.textContent='與決志';
   heading.replaceChildren(first,second);
   const gospel=document.getElementById('church-gospel');
   const intro=document.getElementById('church-decision-intro');
   if(gospel)gospel.hidden=false;
   if(intro)intro.hidden=false;
   document.title='信仰回應與決志 · 神召會活水堂西區教會';
 }
 document.querySelectorAll('.church-form__formarea nav a').forEach(a=>{
   const active=new URL(a.href).searchParams.get('type')===type;
   if(active)a.setAttribute('aria-current','page');
 });
 const setStatus=s=>status.textContent=s;let online=false;
 for(const [key,label,kind,options] of current.fields){
   const wrap=document.createElement('label');wrap.textContent=label;
   const input=kind==='textarea'?document.createElement('textarea'):document.createElement('select');
   input.name=key;if(type==='decision'&&key==='response')input.required=true;
   if(kind==='textarea'){input.maxLength=1500;input.rows=5}else{
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
