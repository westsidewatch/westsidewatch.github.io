(()=>{if(!document.documentElement.classList.contains('art106'))return;
const $=(s,r=document)=>r.querySelector(s),make=(tag,cls,text)=>{const el=document.createElement(tag);el.className=cls;if(text)el.textContent=text;return el};
const live=$('#church-sunday-live');const minutes=s=>{const m=s.match(/(\d{1,2}):(\d{2})/g)||[];return m.map(t=>{const [h,n]=t.split(':').map(Number);return h*60+n})};
const clock=t=>String(Math.floor(t/60)).padStart(2,'0')+':'+String(t%60).padStart(2,'0');
const score=()=>{const rows=[...live.querySelectorAll('.ws-church-sunday-row')],reading=$('.folio-programme-reading',live);if(!reading||rows.length<1||live.dataset.r106==='1'||!$('.folio-order',rows[0]))return;const times=rows.map(r=>minutes($('time',r)?.textContent||''));if(times.some(a=>!a.length))return;const start=Math.min(...times.flat()),end=Math.max(...times.flat()),total=end-start;if(total<=0)return;live.dataset.r106='1';
const axis=make('div','folio-score-axis');axis.lang='en';axis.setAttribute('aria-hidden','true');[start,Math.round((start+end)/2),end].forEach(t=>axis.append(make('span','',clock(t))));reading.prepend(axis);
rows.forEach((r,i)=>{const ts=times[i];const el=make('span','folio-score-measure');el.setAttribute('aria-hidden','true');el.style.setProperty('--score-start',((ts[0]-start)/total*100)+'%');el.style.setProperty('--score-width',((ts.length>1?(ts[1]-ts[0])/total:0)*100)+'%');if(ts.length===1)el.dataset.instant='1';el.dataset.start=String(ts[0]);el.dataset.end=ts.length>1?String(ts[1]):'';r.append(el)});};
new MutationObserver(score).observe(live,{childList:true,subtree:true});score();
const gatherings=$('#church-gathering-list');const week=()=>{const rail=[...gatherings.querySelectorAll('.folio-week-day')],rows=[...gatherings.querySelectorAll('article')];if(rail.length!==7||rows.length!==4||gatherings.dataset.week!=='1'||gatherings.dataset.r106==='1')return;gatherings.dataset.r106='1';rows.forEach(row=>{const n=Number(row.style.getPropertyValue('--day-start'));if(n>=1&&n<=7){rail[n-1].dataset.active='1';row.dataset.dayActive='1'}})};
new MutationObserver(week).observe(gatherings,{childList:true,subtree:true});week();
const ministries=$('#church-ministry-list');const frame=()=>{const worship=$('.folio-worship-focus',ministries);if(!worship||ministries.dataset.r106==='1')return;ministries.dataset.r106='1';const field=make('div','folio-worship-window');field.setAttribute('aria-hidden','true');worship.append(field);};
new MutationObserver(frame).observe(ministries,{childList:true,subtree:true});frame();
// Replace inherited visitor-facing implementation language without changing facts or links.
const history=$('#history .church-visit__about-grid>div:nth-child(2)>p');if(history)history.textContent='我們珍惜每一代會眾的信仰腳蹤，以及牧養、聚會與傳福音的歷程。若希望深入了解教會的歷史與見證，歡迎直接與我們聯繫。';
const gate=$('.church-visit__gate p');if(gate)gate.textContent='歡迎透過西區的夜晚認識教會的團契與讀經生活。參加社群聚會前，可向教會確認最新邀請方式。';
const link=$('.church-visit__gate-link');if(link)link.textContent='西區的夜晚';
const note=$('#invitation .church-visit__muted');if(note)note.textContent='個人資料不會公開展示。目前若需聯繫同工，請使用下方教會信箱。';
})();