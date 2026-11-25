(()=>{if(!document.documentElement.classList.contains('art097'))return;const $=s=>document.querySelector(s),top=$('.church-visit__top'),copy=$('.church-visit__hero-copy'),hero=$('.church-visit__hero'),nav=top.querySelector('nav'),back=top.querySelector('.church-visit__back'),tour=top.querySelector('.church-visit__tour');back.querySelector('.church-visit__back-mark')?.remove();back.querySelector('[lang=en]').textContent='Westside Watch';back.href='/church/';const entries=[['#history','The Congregation','認識活水'],['#sunday','Sunday Worship','主日崇拜'],['#gatherings','Gathering','每週聚會'],['#ministries','Life Together','七個事工'],['#prayer','Prayer & Scripture','禱告查經'],['#invitation','Respond','回應'],['#contact','Correspondence','聯繫']];const old=new Map([...nav.querySelectorAll('a')].map(a=>[a.getAttribute('href'),a]));nav.replaceChildren();entries.forEach(([href,en,zh],i)=>{const a=old.get(href)||document.createElement('a');a.href=href;const n=document.createElement('span');n.className='folio-index-number';n.textContent=String(i+1).padStart(2,'0');const title=document.createElement('span');title.lang='en';title.textContent=en;const cn=document.createElement('span');cn.lang='zh-Hant';cn.textContent=zh;a.replaceChildren(n,title,cn);nav.append(a)});top.classList.add('folio-index');top.replaceChildren(back,nav,tour);copy.append(top);tour.querySelector('span')?.remove();document.querySelectorAll('.church-visit__hero-links a span[aria-hidden],.church-visit__hero-bottom a span[aria-hidden]').forEach(e=>e.remove());document.querySelectorAll('.church-visit__section-head>span').forEach(el=>{const t=el.textContent,parts=t.split(' / ');if(parts.length!==2)return;const n=document.createElement('i');n.textContent=parts[0];const h=document.createElement('b');h.lang='en';h.textContent=parts[1];el.replaceChildren(n,h)});hero.querySelector('.church-visit__hero-folio span:nth-child(2)')?.remove();hero.querySelector('.church-visit__hero-bottom span')?.remove();})();
;
(()=>{if(!document.documentElement.classList.contains('art098'))return;const $=s=>document.querySelector(s);const group=$('.church-visit__scripture-group'),first=$('#church-letterpress'),history=$('#history');const src='/experiments/scripture-studio-motherform-live.html?embed=1&section=01&layout=church-single&impression=';first.src=src+'zh';first.title='約翰福音 7:38 · 中文主讀經文鉛字';const tile=first.closest('aside');tile.classList.add('folio-impression','folio-impression--zh');const second=document.createElement('figure');second.className='folio-impression folio-impression--en';const frame=document.createElement('iframe');frame.id='church-letterpress-en';frame.title='John 7:38 · English-led Scripture impression';frame.src=src+'en';frame.loading='eager';frame.referrerPolicy='same-origin';frame.setAttribute('scrolling','no');second.append(frame);const translation=group.querySelector('.church-visit__scripture-translation');const historyBody=document.createElement('div');historyBody.className='folio-history-spread';const copy=history.querySelector('.church-visit__about-grid');historyBody.append(second,copy);history.append(historyBody);second.insertAdjacentElement('afterend',translation);historyBody.append(copy);const nav=$('.folio-index nav');nav?.setAttribute('aria-label','教會篇章目錄');document.querySelectorAll('.church-visit__section-head>span>b,.folio-index nav a [lang=en],.church-visit__identity-lockup .church-visit__english').forEach(x=>x.setAttribute('data-ws-designable','true'));})();
;
(()=>{if(!document.documentElement.classList.contains('art099'))return;
const $=(s,r=document)=>r.querySelector(s),make=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text)e.textContent=text;return e};
const hero=$('.church-visit__hero'),copy=$('.church-visit__hero-copy'),index=$('.folio-index'),group=$('.church-visit__scripture-group');
const title=$('.church-visit__identity-lockup'),english=$('.church-visit__english');
title.insertBefore(english,title.firstChild);
const brand=$('.church-visit__back');brand.querySelector('[lang=en]').textContent='Living Water West';
const mast=$('.church-visit__hero-folio');const home=make('a','folio-mast-home','Westside Watch');home.href='/';home.lang='en';mast.replaceChildren(home,make('span','','John 7:38'));
mast.removeAttribute('aria-hidden');
const indexHead=make('p','folio-index-caption','Contents');indexHead.lang='en';index.insertBefore(indexHead,index.querySelector('nav'));
const indexNav=index.querySelector('nav');indexNav.querySelectorAll('a').forEach(a=>{const en=a.querySelector('[lang=en]');const zh=a.querySelector('[lang=zh-Hant]');const span=make('span','folio-index-title');span.append(en,zh);a.append(span)});
const relink=(root)=>{root.querySelectorAll('a[href^="/church/visit/#"]').forEach(a=>{a.href='#'+a.getAttribute('href').split('#')[1]})};
const scripture=$('#church-letterpress');scripture.closest('aside').querySelector('.church-visit__water-engraving')?.remove();
const label=make('p','folio-plate-caption','John 7:38');label.lang='en';group.append(label);
const field=make('div','folio-water-field');field.setAttribute('aria-hidden','true');hero.prepend(field);
const history=$('#history');const historyHead=$('.church-visit__section-head',history);const historySpread=$('.folio-history-spread',history);historySpread.insertBefore(historyHead,historySpread.querySelector('.church-visit__about-grid'));
const sunday=$('#sunday');const live=$('#church-sunday-live');
const formatSunday=()=>{const rows=live.querySelector('.ws-church-sunday-rows');if(!rows||live.dataset.folio==='1')return;live.dataset.folio='1';const status=live.querySelector('.ws-sunday-source-status'),theme=live.querySelector('h3'),lead=live.querySelector('.ws-church-lead'),address=live.querySelector('.ws-church-muted'),verses=live.querySelector('.ws-church-scriptures');const programme=make('div','folio-programme'),front=make('div','folio-programme-title'),reading=make('div','folio-programme-reading');front.append(status,theme,lead);reading.append(rows,address);programme.append(front,reading);live.append(programme,verses);rows.querySelectorAll('.ws-church-sunday-row').forEach((row,i)=>{const number=make('span','folio-order',String(i+1).padStart(2,'0'));number.setAttribute('aria-hidden','true');row.prepend(number)});verses.querySelectorAll('p').forEach((v,i)=>{const n=make('span','folio-verse-no',String(i+1).padStart(2,'0'));n.setAttribute('aria-hidden','true');v.prepend(n)})};
new MutationObserver(formatSunday).observe(live,{childList:true});formatSunday();
const meetings=$('#church-gathering-list');
const formatMeetings=()=>{const articles=[...meetings.querySelectorAll('article')];if(!articles.length||meetings.dataset.folio==='1')return;meetings.dataset.folio='1';articles.forEach(a=>{const meta=a.querySelector('span'),parts=meta.textContent.split(' / ');const day=make('span','folio-day',parts[0]);const mode=make('span','folio-mode',parts[1]);meta.replaceChildren(day,mode);const names={'週日':'Sunday','週一':'Monday','週三':'Wednesday','週五':'Friday'};const en=make('b','folio-day-en',names[parts[0]]||'');en.lang='en';meta.prepend(en);const timing=a.querySelector('p');const txt=timing.textContent;const split=txt.split(' · ');timing.replaceChildren(make('span','folio-meeting-time',split[0]));if(split[1])timing.append(make('small','folio-time-note',split.slice(1).join(' · ')))})};
new MutationObserver(formatMeetings).observe(meetings,{childList:true});formatMeetings();
const ministries=$('#church-ministry-list');const formatMinistries=()=>{const articles=[...ministries.querySelectorAll('article')];if(!articles.length||ministries.dataset.folio==='1')return;ministries.dataset.folio='1';articles.forEach(a=>{const m=a.querySelector('small'),parts=m.textContent.split(' / ');const n=make('span','folio-ministry-no',parts[0]);const title=make('b','folio-ministry-en',parts[1]);title.lang='en';m.replaceChildren(n,title);});relink(ministries)};
new MutationObserver(formatMinistries).observe(ministries,{childList:true});formatMinistries();
const gate=$('.church-visit__gate');const qr=$('.church-visit__intake-grid');qr.querySelectorAll('article').forEach(a=>{const text=make('div','folio-response-copy');text.append(a.querySelector('h3'),a.querySelector('p'),a.querySelector('a'));a.append(text)});
relink(document);
})();
;
(()=>{if(!document.documentElement.classList.contains('art100'))return;
const $=s=>document.querySelector(s),main=$('main');
function bind(){const strict=document.documentElement.classList.contains('art102');for(const e of main.querySelectorAll('h2,h3,.ws-church-sunday-row strong,.church-visit__contact-grid strong'))e.dataset.folioZh=!strict||e.matches('.church-visit__section-head > h2')?'title':'air';
for(const e of main.querySelectorAll('.church-visit__seal,.folio-day,.folio-mode,.folio-time-note,.church-visit__gathering>small,.folio-index-title [lang=zh-Hant],.ws-sunday-source-status,.ws-church-scriptures small'))e.dataset.folioZh='air';
for(const e of main.querySelectorAll('.folio-meeting-time'))if(/[\u3400-\u9fff]/.test(e.textContent)){e.lang='zh-Hant';e.dataset.folioZh='air'}else e.lang='en';
for(const e of main.querySelectorAll('.folio-index nav a [lang=en],.church-visit__section-head>span b,.folio-ministry-en,.folio-day-en,.folio-index-caption')){e.lang='en';e.dataset.wsDesignable='true'}
const meetings=$('#church-gathering-list');if(meetings.querySelectorAll('article').length===4&&!meetings.dataset.week){meetings.dataset.week='1';const days={'Sunday':1,'Monday':2,'Wednesday':4,'Friday':6};for(const a of meetings.querySelectorAll('article'))a.style.setProperty('--day-start',String(days[a.querySelector('.folio-day-en')?.textContent]||1));}}
const observer=new MutationObserver(bind);for(const id of ['#church-gathering-list','#church-sunday-live','#church-ministry-list'])observer.observe($(id),{childList:true,subtree:true});bind();
const link=document.createElement('a');link.href='#welcome';link.textContent='返回篇章目錄';$('.church-visit__footer nav').prepend(link);
})();
;
(()=>{if(!document.documentElement.classList.contains('art103'))return;
const $=(s,r=document)=>r.querySelector(s), make=(tag,cls,txt)=>{const e=document.createElement(tag);e.className=cls;if(txt)e.textContent=txt;return e};
const history=$('#history'),hero=$('.church-visit__hero');const hf=$('.church-visit__hero-folio',hero);
const index=$('.folio-index');const caption=$('.folio-index-caption',index);const brand=$('.church-visit__back',index);
brand?.remove();hf.querySelector('a').href='/';
const historyField=make('div','folio-history-field');historyField.setAttribute('aria-hidden','true');history.prepend(historyField);
const live=$('#church-sunday-live');const programme=()=>{const title=$('.folio-programme-title',live),read=$('.folio-programme-reading',live),verses=$('.ws-church-scriptures',live);if(!title||!read||!verses||live.dataset.r103==='1')return;live.dataset.r103='1';title.append(verses);};
new MutationObserver(programme).observe(live,{childList:true,subtree:true});programme();
const gatherings=$('#church-gathering-list');const week=()=>{const rows=[...gatherings.querySelectorAll('article')];if(rows.length!==4||gatherings.dataset.r103==='1')return;gatherings.dataset.r103='1';const rail=make('div','folio-week-rail');rail.setAttribute('aria-hidden','true');for(const name of ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']){const e=make('span','folio-week-day',name);e.lang='en';rail.append(e)}gatherings.prepend(rail);};
new MutationObserver(week).observe(gatherings,{childList:true,subtree:true});week();
const ministries=$('#church-ministry-list');const spread=()=>{const rows=[...ministries.querySelectorAll('article')];if(rows.length!==7||!$('.folio-ministry-en',rows[0])||ministries.dataset.r103==='1')return;ministries.dataset.r103='1';rows.forEach((a,i)=>{const name=$('.folio-ministry-en',a);name.lang='en';const copy=make('div','folio-ministry-copy');copy.append($('h3',a),$('p',a),$('a',a));a.append(copy);if(i===2)a.classList.add('folio-worship-focus')})};
new MutationObserver(spread).observe(ministries,{childList:true,subtree:true});spread();
const prayer=$('#prayer'),inv=$('#invitation');const field=make('div','folio-response-field');field.setAttribute('aria-hidden','true');inv.prepend(field);
const gate=$('.church-visit__gate',inv);const footer=$('.church-visit__footer');const mark=make('span','folio-colophon-mark');mark.setAttribute('aria-hidden','true');footer.prepend(mark);
const closing=$('#contact .church-visit__contact-grid');const email=$('p',closing);email.classList.add('folio-contact-primary');
})();
;
(()=>{if(!document.documentElement.classList.contains('art105'))return;
const mail=document.querySelector('.folio-contact-primary a');if(mail)mail.lang='en';
const rail=document.querySelector('#church-gathering-list');const update=()=>{const days=[...rail.querySelectorAll('.folio-week-day')];if(days.length!==7||rail.dataset.r105==='1')return;rail.dataset.r105='1';const names=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];days.forEach((e,i)=>{e.textContent=names[i]});};
new MutationObserver(update).observe(rail,{childList:true,subtree:true});update();
})();
;
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
;
(()=>{if(!document.documentElement.classList.contains('art107'))return;
const list=document.querySelector('#church-gathering-list');
const order=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
const bind=()=>{const entries=[...list.querySelectorAll('article')];const labels=[...list.querySelectorAll('.folio-week-day')];if(entries.length!==4||labels.length!==7||list.dataset.r107==='1'||entries.some(e=>!e.querySelector('.folio-day-en')))return;
const pairs=entries.map(e=>({e,day:e.querySelector('.folio-day-en').textContent.trim()})).map(x=>({...x,n:order.indexOf(x.day)+1})).sort((a,b)=>a.n-b.n);if(pairs.some(x=>x.n<1)||new Set(pairs.map(x=>x.n)).size!==entries.length)return;
list.dataset.r107='1';pairs.forEach((x,i)=>{const span=Math.min(2,(pairs[i+1]?.n||8)-x.n);x.e.style.setProperty('--day-start',String(x.n));x.e.style.setProperty('--day-span',String(span));x.e.dataset.weekday=x.day;labels[x.n-1].dataset.active='1';});};
new MutationObserver(bind).observe(list,{childList:true,subtree:true});bind();
})();
;
(()=>{if(!document.documentElement.classList.contains('art110'))return;
const M=Object.freeze({"id":"church","en":"Living Water","zh":"活水堂","depths":[1,2,1,3,1,2],"width":48,"height":8,"source":"historical","path":"M0 8V1H8V2H16V1H24V3H32V1H40V2H48V8Z"});
const $=s=>document.querySelector(s);
const round=n=>Math.round(n*1000)/1000;
const px=n=>round(n)+'px';
const pairs=(start,end,origin,unit)=>{
  const at=x=>M.depths[Math.max(0,Math.min(5,Math.floor((x-origin)/unit/8)))];
  const points=[[start,at(start+1e-5)]];
  for(let k=1;k<6;k++){const x=origin+k*8*unit;if(x>start+1e-5&&x<end-1e-5){points.push([x,M.depths[k-1]],[x,M.depths[k]])}}
  points.push([end,at(end-1e-5)]);
  return points;
};
const prayer=$('#prayer'),head=$('#prayer .church-visit__section-head'),glass=$('#prayer .church-visit__about-grid');
const response=$('.church-visit__intake-grid');
function update(){
 const pr=prayer.getBoundingClientRect(),hr=head.getBoundingClientRect(),gr=glass.getBoundingClientRect(),s=getComputedStyle(prayer);
 const left=pr.left+parseFloat(s.paddingLeft),width=pr.width-parseFloat(s.paddingLeft)-parseFloat(s.paddingRight),bay=width/12;
 // Scale the mother beyond the entire page: four columns per tooth on desktop,
 // six on smaller screens. Its deepest turn lies exactly on the centre axis.
 const u=bay*(innerWidth<=900?.75:.5),origin=left+6*bay-24*u;
 const curve=pairs(hr.left,hr.right,origin,u),baseY=4*u;
 head.style.clipPath='polygon(0 0, 100% 0, '+curve.slice().reverse().map(([x,d])=>px(x-hr.left)+' '+px(hr.height-baseY+d*u)).join(', ')+')';
 prayer.dataset.crestCrop=JSON.stringify({mother:M.id,source:'9d7f3e5557738e45749b2121918809efdec4cd9d',orientation:0,scale:round(u),origin:round(origin-left),sourceWindow:[round((hr.left-origin)/u),round((hr.right-origin)/u),0,4],negativeWindow:[round((gr.left-origin)/u),round((hr.right-origin)/u),0,4],axis:round(left+6*bay),vertices:curve.map(([x,d])=>[round(x-left),d])});
 const grid=response.getBoundingClientRect(),items=[...response.querySelectorAll('article')];
 if(innerWidth>900){
  // A second view of the same crest, rotated ninety degrees. Its centre tooth
  // is anchored to the division between the two actual response rows.
  const a=items[0].getBoundingClientRect(),seam=a.bottom;
  const u2=grid.height/32,origin2=seam-24*u2;
  const maxCut=3*u2;response.style.setProperty('--response-safe',px(maxCut+Math.max(16,bay*.18)));
  items.forEach((e,i)=>{if(i%2){e.style.clipPath='none';return}const r=e.getBoundingClientRect();const c=pairs(r.top,r.bottom,origin2,u2);e.style.clipPath='polygon(0 0, '+c.map(([y,d])=>px(r.width-d*u2)+' '+px(y-r.top)).join(', ')+', 0 100%)';e.dataset.crestCrop=JSON.stringify({mother:M.id,orientation:90,scale:round(u2),sourceWindow:[round((r.top-origin2)/u2),round((r.bottom-origin2)/u2)],vertices:c.map(([y,d])=>[round(y-grid.top),d])});});
  response.dataset.crestCrop=JSON.stringify({mother:M.id,orientation:90,scale:round(u2),axis:round(seam-grid.top),sourceWindow:[round((grid.top-origin2)/u2),round((grid.bottom-origin2)/u2)]});
 }else{
  items.forEach(e=>{e.style.removeProperty('clip-path');delete e.dataset.crestCrop});response.style.removeProperty('--response-safe');delete response.dataset.crestCrop;
 }
}
let raf=0;const schedule=()=>{cancelAnimationFrame(raf);raf=requestAnimationFrame(update)};
const ro=new ResizeObserver(schedule);[prayer,head,glass,response,...response.querySelectorAll('article')].forEach(e=>ro.observe(e));window.addEventListener('resize',schedule);document.fonts.ready.then(schedule);update();
})();
;
(()=>{if(!document.documentElement.classList.contains('art116'))return;const $=s=>document.querySelector(s);const seal=(cut)=>{const e=document.createElement('div');e.className='ws-name-seal';e.dataset.wsSeal='water';e.dataset.cut=cut;e.setAttribute('aria-hidden','true');return e};const index=$('.folio-index'),caption=$('.folio-index-caption');if(index&&caption){const opening=document.createElement('div');opening.className='folio-index-opening';opening.dataset.wsSeal='water';caption.before(opening);opening.append(seal('fine'),caption)}const footer=$('.church-visit__footer');footer.append(seal('small'));const list=$('#church-ministry-list');const aperture=()=>{const w=$('.folio-worship-window');if(w){w.dataset.wsSeal='water';w.dataset.wsWindow='square';}};new MutationObserver(aperture).observe(list,{childList:true,subtree:true});aperture();})();
;
(()=>{if(!document.documentElement.classList.contains('art117'))return;const decision=document.querySelector('#invitation a[href="/church/forms/?type=decision"]');if(decision)decision.dataset.crestRole='decision';const live=document.querySelector('#church-sunday-live');const bind=()=>{const address=live.querySelector('.ws-church-muted');if(address)address.dataset.crestRole='sunday-address'};new MutationObserver(bind).observe(live,{childList:true,subtree:true});bind();})();