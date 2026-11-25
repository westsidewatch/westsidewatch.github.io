/* Cloudflare Pages Function: same-origin confidential church intake.
 * GitHub Pages cannot run this endpoint. The client remains disabled until
 * every required binding is configured and a real receipt test passes.
 * NO visitor data is written into GitHub, static assets or response logs. */
const KINDS=Object.freeze({join:'加入教會',decision:'決志與信仰回應',newcomer:'新朋友',prayer:'代禱與關懷'});
const headers={'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'strict-origin'};
const result=(code,payload)=>new Response(JSON.stringify(payload),{status:code,headers});
const available=env=>Boolean(env?.TURNSTILE_SITE_KEY&&env?.TURNSTILE_SECRET_KEY&&env?.RESEND_API_KEY&&env?.CHURCH_INTAKE_TO&&env?.CHURCH_INTAKE_FROM);
const short=(form,key,max)=>String(form.get(key)||'').trim().slice(0,max+1);
const clean=(s,max)=>s.length<=max&&!/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(s);
const reject=(code,message)=>result(code,{ok:false,error:message});
export async function onRequestGet({env}){
 return result(200,{ready:available(env),turnstileSiteKey:available(env)?String(env.TURNSTILE_SITE_KEY):null});
}
export async function onRequestPost({request,env}){
 if(!available(env))return reject(503,'Intake is not enabled');
 const url=new URL(request.url),origin=request.headers.get('Origin');
 if(origin!==url.origin)return reject(403,'Invalid origin');
 if(!String(request.headers.get('content-type')||'').toLowerCase().includes('multipart/form-data'))return reject(415,'Invalid form content');
 if(Number(request.headers.get('content-length')||'0')>50000)return reject(413,'Too much data');
 let form;try{form=await request.formData();}catch{return reject(400,'Invalid form');}
 // Honeypot submissions are discarded. Never claim a volunteer received them.
 if(short(form,'website',120))return result(200,{ok:true});
 const type=short(form,'type',16),name=short(form,'name',90),email=short(form,'email',180),phone=short(form,'phone',40),
   preference=short(form,'preference',12),meeting=short(form,'meeting',100),response=short(form,'response',140),
   message=short(form,'message',1500),token=short(form,'cf-turnstile-response',3000);
 if(!Object.hasOwn(KINDS,type)||!name||(!email&&!phone)||form.get('consent')!=='yes')
   return reject(400,'Required fields missing');
 if(![name,email,phone,preference,meeting,response,message].every((s,i)=>clean(s,[90,180,40,12,100,140,1500][i])))
   return reject(400,'Invalid field length');
 if(email&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))return reject(400,'Invalid email address');
 if(!['email','phone','either'].includes(preference))return reject(400,'Invalid contact preference');
 if(!token)return reject(400,'Security verification required');
 if(env.CHURCH_RATE_LIMIT){
   const ip=request.headers.get('CF-Connecting-IP')||'unknown';
   const limited=await env.CHURCH_RATE_LIMIT.limit({key:ip}).catch(()=>({success:false}));
   if(!limited.success)return reject(429,'Please try again later');
 }
 const verify=await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify',{
   method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},
   body:new URLSearchParams({secret:env.TURNSTILE_SECRET_KEY,response:token,remoteip:request.headers.get('CF-Connecting-IP')||''})
 }).then(r=>r.json()).catch(()=>null);
 if(!verify?.success)return reject(403,'Security verification failed');
 const emailText=[
   '[活水堂西區] 新訪客聯繫｜'+KINDS[type],
   '類別：'+KINDS[type],
   '日期：'+new Date().toISOString(),
   '姓名：'+name,
   'Email：'+(email||'未提供'),
   '電話：'+(phone||'未提供'),
   '聯繫偏好：'+preference,
   '聚會／情況：'+(meeting||'未填'),
   '信仰／代禱回應：'+(response||'未填'),
   '其他內容：'+(message||'未填'),
   '',
   '志工接待：確認類型 → 私下指派同工 → 依聯絡偏好聯繫 → 記錄跟進結果。',
   '此信含個人資料，只限受權同工閱讀。勿轉寄公共群組。'
 ].join('\n');
 const mail={from:String(env.CHURCH_INTAKE_FROM),to:[String(env.CHURCH_INTAKE_TO)],
   subject:'[活水西區訪客] '+KINDS[type],text:emailText};
 if(email)mail.reply_to=email;
 let receipt;try{
   receipt=await fetch('https://api.resend.com/emails',{method:'POST',
     headers:{'Authorization':'Bearer '+env.RESEND_API_KEY,'Content-Type':'application/json'},
     body:JSON.stringify(mail)});
 }catch{return reject(502,'Mail delivery unavailable');}
 if(!receipt.ok)return reject(502,'Mail delivery unavailable');
 // Provider accepts the email request; final inbox receipt must be verified in operations.
 return result(200,{ok:true,received:true});
}
