(()=>{
'use strict';
const ENDPOINT='/api/dore/video-subtitle';
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
function videoUrl(q){try{const u=new URL(String(q).trim());return /^https?:$/.test(u.protocol)&&/(youtube\.com|youtu\.be|vimeo\.com|facebook\.com|fb\.watch|instagram\.com|westsidewatch\.ca)/i.test(u.hostname)}catch{return false}}
function show(html,label){const box=$('#results'),count=$('#result-count'),wrap=$('#results-wrap');if(!box||!count)return;box.innerHTML=html;count.textContent=label;if(wrap)wrap.scrollIntoView({behavior:'smooth',block:'start'})}
function renderPending(url,d){show(`<article class="video-subtitle-answer"><header><strong>DORÉ</strong><span>SUBTITLE LAB</span></header><h3>我認出這是一個影片。</h3><p>影片：${esc(url)}</p><p>${esc(d.message||'我已建立字幕工作，但目前還需要可用的轉錄執行器才能從遠端影片直接產生字幕。')}</p><p class="video-boundary">${esc(d.boundary||'不會把未取得或未轉錄的字幕假裝成已生成。')}</p></article>`,'Doré · 字幕工作已建立')}
function renderReady(url,d){const text=d.corrected_srt||d.srt||'';show(`<article class="video-subtitle-answer"><header><strong>DORÉ</strong><span>SUBTITLE LAB · READY</span></header><h3>字幕已生成並經 Doré 校對。</h3><p>影片：${esc(url)}</p><pre class="subtitle-output">${esc(text)}</pre></article>`,'Doré · 校對版字幕')}
async function submit(url){show(`<article class="video-subtitle-answer"><header><strong>DORÉ</strong><span>SUBTITLE LAB</span></header><h3>正在建立字幕工作…</h3><p>${esc(url)}</p></article>`,'Doré · 處理影片');try{const r=await fetch(ENDPOINT,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({url})});const d=await r.json().catch(()=>({}));if(r.ok&&d.status==='ready')renderReady(url,d);else renderPending(url,d)}catch(e){show(`<article class="video-subtitle-answer"><header><strong>DORÉ</strong><span>SUBTITLE LAB</span></header><h3>字幕工作目前無法啟動。</h3><p>${esc(e.message||e)}</p></article>`,'Doré · 字幕工作錯誤')}}
function intercept(e){const form=e.target;if(!(form instanceof HTMLFormElement)||form.id!=='search-form')return;const q=$('#search-input')?.value?.trim();if(!q||!videoUrl(q))return;e.preventDefault();e.stopImmediatePropagation();submit(q)}
const style=document.createElement('style');style.textContent='.video-subtitle-answer{padding:2vw .15vw 1.2vw}.video-subtitle-answer header{display:flex;gap:1vw;align-items:baseline;border-bottom:1px solid rgba(82,62,20,.2);padding-bottom:.8vw;margin-bottom:1.2vw}.video-subtitle-answer header strong{color:#8c6818;font:500 1.35rem "Cormorant Garamond",serif}.video-subtitle-answer header span,.video-boundary{font-size:.75rem;opacity:.62}.video-subtitle-answer p{line-height:1.9}.subtitle-output{white-space:pre-wrap;line-height:1.8;padding:1rem;border:1px solid rgba(82,62,20,.16);background:rgba(255,249,227,.18)}';document.head.appendChild(style);
document.addEventListener('submit',intercept,true);
function loadImageCommandRouter(){if(window.DoreImageCommand||document.getElementById('dore-image-command-router'))return;const s=document.createElement('script');s.id='dore-image-command-router';s.src='/dore/dore-image-command.js?v=20260905a';s.async=false;document.head.appendChild(s)}
loadImageCommandRouter();
window.DoreVideoSubtitle={isVideoUrl:videoUrl,submit};
})();
