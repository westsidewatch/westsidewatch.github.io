(()=>{
  const gif='/one/share/matthew-03-baptism-motion-r4-mobile.gif';
  const style=document.createElement('link');style.rel='stylesheet';style.href='/one/one-baptism-motion.css?v=20260821b';document.head.append(style);
  const intro=document.querySelector('.now__intro');
  if(!intro)return;
  intro.insertAdjacentHTML('beforeend',`<div class="baptism-motion" aria-hidden="true"><span class="baptism-motion__light"></span><span class="baptism-motion__dove-blank"></span><span class="baptism-motion__dove"></span><span class="baptism-motion__river baptism-motion__river--one"></span><span class="baptism-motion__river baptism-motion__river--two"></span></div>`);
  intro.insertAdjacentHTML('afterend','<div class="animated-cover-share" hidden><button type="button">生成／分享動態封面 GIF</button><small>可直接傳送到查經群；不支援系統分享時會下載 GIF。</small></div>');
  const wrap=document.querySelector('.animated-cover-share'),button=wrap.querySelector('button');
  const sync=()=>{const active=new URLSearchParams(location.search).get('book')==='40'&&new URLSearchParams(location.search).get('chapter')==='3';document.querySelector('.now')?.classList.toggle('has-baptism-motion',active);wrap.hidden=!active};
  new MutationObserver(sync).observe(document.querySelector('#now-kicker'),{childList:true,subtree:true,characterData:true});sync();
  button.onclick=async()=>{const old=button.textContent;button.disabled=true;button.textContent='正在生成 GIF…';try{const response=await fetch(gif,{cache:'no-store'});if(!response.ok)throw new Error(String(response.status));const blob=await response.blob(),file=new File([blob],'ONE-馬太福音-第3章-動態-R4.gif',{type:'image/gif'}),payload={title:'ONE · 馬太福音第 3 章',text:'ONE 動態封面｜馬太福音第 3 章',files:[file]};if(navigator.share&&(!navigator.canShare||navigator.canShare({files:[file]}))){await navigator.share(payload);button.textContent='已開啟分享'}else{const link=document.createElement('a'),url=URL.createObjectURL(blob);link.href=url;link.download=file.name;document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);button.textContent='GIF 已下載'}}catch(error){button.textContent=error?.name==='AbortError'?'已取消分享':'請重試'}finally{button.disabled=false;setTimeout(()=>button.textContent=old,1800)}};
})();
