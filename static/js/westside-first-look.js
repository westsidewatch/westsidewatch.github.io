/* Shared First Look: one stage contract, realm-owned content, verified scripture. */
(()=>{'use strict';
 const corpus={"schema": "westside.first-look.scripture.v1", "translation": "KJV", "verifiedAt": "2026-10-12", "timezone": "America/Toronto", "rights": "public-domain", "verses": [{"realm": "church", "reference": "John 7:38", "text": "He that believeth on me, as the scripture hath said, out of his belly shall flow rivers of living water.", "source": "https://ebible.org/eng-kjv/JHN07.htm", "verified": true}, {"realm": "sermon", "reference": "Romans 10:17", "text": "So then faith cometh by hearing, and hearing by the word of God.", "source": "https://ebible.org/eng-kjv/ROM10.htm", "verified": true}, {"realm": "magazine", "reference": "Psalm 102:18", "text": "This shall be written for the generation to come: and the people which shall be created shall praise the LORD.", "source": "https://ebible.org/eng-kjv/PSA102.htm", "verified": true}, {"realm": "bible", "reference": "Luke 24:32", "text": "And they said one to another, Did not our heart burn within us, while he talked with us by the way, and while he opened to us the scriptures?", "source": "https://ebible.org/eng-kjv/LUK24.htm", "verified": true}, {"realm": "book", "reference": "Psalm 119:105", "text": "Thy word is a lamp unto my feet, and a light unto my path.", "source": "https://ebible.org/eng-kjv/PSA119.htm", "verified": true}, {"realm": "cinema", "reference": "John 1:5", "text": "And the light shineth in darkness; and the darkness comprehended it not.", "source": "https://ebible.org/eng-kjv/JHN01.htm", "verified": true}, {"realm": "life", "reference": "Matthew 6:34", "text": "Take therefore no thought for the morrow: for the morrow shall take thought for the things of itself. Sufficient unto the day is the evil thereof.", "source": "https://ebible.org/eng-kjv/MAT06.htm", "verified": true}], "identities": {"church": {"realm": "church", "reference": "John 7:38", "text": "He that believeth on me, as the scripture hath said, out of his belly shall flow rivers of living water.", "source": "https://ebible.org/eng-kjv/JHN07.htm", "verified": true}, "sermon": {"realm": "sermon", "reference": "Romans 10:17", "text": "So then faith cometh by hearing, and hearing by the word of God.", "source": "https://ebible.org/eng-kjv/ROM10.htm", "verified": true}, "magazine": {"realm": "magazine", "reference": "Romans 13:12", "text": "The night is far spent, the day is at hand: let us therefore cast off the works of darkness, and let us put on the armour of light.", "source": "https://ebible.org/eng-kjv/ROM13.htm", "verified": true}, "bible": {"realm": "bible", "reference": "Luke 24:45", "text": "Then opened he their understanding, that they might understand the scriptures,", "source": "https://ebible.org/eng-kjv/LUK24.htm", "verified": true}, "book": {"realm": "book", "reference": "Psalm 119:105", "text": "Thy word is a lamp unto my feet, and a light unto my path.", "source": "https://ebible.org/eng-kjv/PSA119.htm", "verified": true}, "cinema": {"realm": "cinema", "reference": "John 1:5", "text": "And the light shineth in darkness; and the darkness comprehended it not.", "source": "https://ebible.org/eng-kjv/JHN01.htm", "verified": true}, "life": {"realm": "life", "reference": "Matthew 6:34", "text": "Take therefore no thought for the morrow: for the morrow shall take thought for the things of itself. Sufficient unto the day is the evil thereof.", "source": "https://ebible.org/eng-kjv/MAT06.htm", "verified": true}}};
 const aliases={olive:'sermon',journal:'magazine','dawn-library':'book','daylight-cafe':'life',emmaus:'bible'};
 const realm=aliases[document.body.dataset.wsScope]||document.body.dataset.wsScope;
 const stage=document.querySelector('[data-ws-first-look-stage]');if(!stage||!corpus.verses.some(v=>v.realm===realm))return;
 stage.classList.add('ws-first-look-stage');stage.dataset.wsFirstLookRealm=realm;
 const dateKey=(date=new Date())=>{const p=Object.fromEntries(new Intl.DateTimeFormat('en-CA',{timeZone:corpus.timezone,year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(date).map(x=>[x.type,x.value]));return `${p.year}-${p.month}-${p.day}`};
 const ordinal=key=>Math.floor(Date.parse(key+'T12:00:00Z')/86400000);
 const verseFor=key=>corpus.verses[((ordinal(key)%corpus.verses.length)+corpus.verses.length)%corpus.verses.length];
 const create=(tag,cls,text)=>{const e=document.createElement(tag);e.className=cls;if(text)e.textContent=text;return e};
 const band=create('aside','ws-scripture-scroll fl-scripture');band.setAttribute('aria-label','經文長卷');
 const identity=corpus.identities[realm],anchor=create('p','fl-scripture-anchor',identity.text+' ');
 const cite=create('a','',identity.reference+' · KJV');cite.href=identity.source;anchor.append(cite);band.append(anchor);
 const viewport=create('div','fl-scripture-viewport'),track=create('div','ws-scripture-scroll__track');viewport.append(track);band.append(viewport);
 const pause=create('button','fl-scripture-pause','暫停經文流動');pause.type='button';pause.setAttribute('aria-pressed','false');band.append(pause);
 pause.onclick=()=>{const stopped=pause.getAttribute('aria-pressed')!=='true';pause.setAttribute('aria-pressed',String(stopped));pause.textContent=stopped?'繼續經文流動':'暫停經文流動';track.style.animationPlayState=stopped?'paused':''};
 stage.after(band);
 const render=(key=dateKey())=>{const verse=verseFor(key);track.replaceChildren();for(let i=0;i<2;i++){const group=create('span','ws-scripture-scroll__group');if(i)group.setAttribute('aria-hidden','true');group.append(create('span','ws-scripture-scroll__text',verse.text),create('span','ws-scripture-scroll__reference',verse.reference+' · KJV · '+key));track.append(group)}band.dataset.torontoDate=key;
  document.querySelectorAll('[data-fl-date]').forEach(e=>{e.textContent=key;e.setAttribute('datetime',key)});
  document.querySelectorAll('[data-fl-daily-verse]').forEach(e=>e.textContent=verse.text+' — '+verse.reference+' · KJV');
  const daily=document.querySelector('[data-fl-daily-home]');if(daily){daily.dataset.day=String(((ordinal(key)%7)+7)%7);daily.style.setProperty('--ws-light-x',String(24+(((ordinal(key)%7)+7)%7)*8)+'%')}
 };
 render();let selectedDate=null;
 const dateInput=document.querySelector('[data-fl-date-input]');if(dateInput){dateInput.value=dateKey();dateInput.onchange=()=>{if(/^\d{4}-\d{2}-\d{2}$/.test(dateInput.value)){selectedDate=dateInput.value;render(selectedDate)}}}
 document.querySelectorAll('[data-fl-date-step]').forEach(b=>b.onclick=()=>{const date=new Date((selectedDate||dateKey())+'T12:00:00Z');date.setUTCDate(date.getUTCDate()+Number(b.dataset.flDateStep));selectedDate=date.toISOString().slice(0,10);if(dateInput)dateInput.value=selectedDate;render(selectedDate)});
 const today=document.querySelector('[data-fl-today]');if(today)today.onclick=()=>{selectedDate=null;if(dateInput)dateInput.value=dateKey();render()};
 let timer=setInterval(()=>{if(!selectedDate&&band.dataset.torontoDate!==dateKey())render()},60000);window.addEventListener('pagehide',()=>clearInterval(timer),{once:true});
 document.querySelectorAll('[data-fl-reader]').forEach(root=>{
  const buttons=[...root.querySelectorAll('[data-fl-select]')],panels=[...root.querySelectorAll('[data-fl-panel]')];
  const select=button=>{buttons.forEach(b=>b.setAttribute('aria-selected',String(b===button)));panels.forEach(p=>p.hidden=p.dataset.flPanel!==button.dataset.flSelect)};
  buttons.forEach((b,i)=>{b.onclick=()=>select(b);b.onkeydown=e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const n=e.key==='Home'?0:e.key==='End'?buttons.length-1:(i+(e.key==='ArrowRight'?1:-1)+buttons.length)%buttons.length;buttons[n].focus();select(buttons[n])}});
 });
 // Keep the continuous speaker selector discoverable during immersive playback.
 if(realm==='sermon'){
  const toggle=create('button','fl-media-switch','講員與系列');toggle.type='button';toggle.setAttribute('aria-pressed','false');
  toggle.onclick=()=>{const open=stage.classList.toggle('fl-controls-open');toggle.setAttribute('aria-pressed',String(open));toggle.textContent=open?'隱藏講員與系列':'講員與系列'};
  stage.addEventListener('ws-one-look:select',()=>{stage.classList.remove('fl-controls-open');toggle.setAttribute('aria-pressed','false');toggle.textContent='講員與系列'});stage.append(toggle);
 }
 // Scroll/touch reveal stays within the existing church stage; final entry is explicit.
 if(realm==='church'){
  const reduce=matchMedia('(prefers-reduced-motion: reduce)');let frame;
  const update=()=>{const rect=stage.getBoundingClientRect(),progress=reduce.matches?1:Math.max(0,Math.min(1,-rect.top/(rect.height*.55)));stage.style.setProperty('--fl-door-open',progress);frame=null};
  const schedule=()=>{if(!frame)frame=requestAnimationFrame(update)};
  window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);reduce.addEventListener('change',schedule);
  window.addEventListener('message',e=>{if(e.origin===location.origin&&e.source===parent&&e.data?.type==='ws-first-look:progress'){const p=Number(e.data.progress);if(Number.isFinite(p))stage.style.setProperty('--fl-door-open',reduce.matches?1:Math.max(0,Math.min(1,p)))}});update();
 }
 // Embedded First Looks reuse this page's real content and keep intentional deep links.
 if(new URLSearchParams(location.search).get('first-look')==='embed'){
  document.documentElement.classList.add('fl-embedded');document.documentElement.style.setProperty('--fl-viewport-height',innerHeight+'px');
  // The embedded chapter has its own editorial navigation. Remove the site's outer header from the iframe rather than trying to conceal it from the parent document.
  const outerHeader=document.querySelector('body > .sites-layer-header');if(outerHeader)outerHeader.remove();
  let branch=stage;while(branch.parentElement&&branch.parentElement!==document.documentElement){const parent=branch.parentElement;for(const sibling of parent.children){if(sibling!==branch&&sibling!==band&&!['SCRIPT','STYLE','LINK'].includes(sibling.tagName))sibling.hidden=true}branch=parent;if(parent===document.body)break}
  const navigation=create('nav','fl-realm-nav');navigation.setAttribute('aria-label','First Look 分站');
  for(const [key,label] of [['church','LivingWaterWest'],['magazine','Magazine'],['bible','Emmaus'],['sermon','Olive'],['book','Dawn Library'],['cinema','Cinema'],['life','Life']]){const a=create('a','',label);a.href='/#first-look-'+key;a.target='_top';navigation.append(a)}stage.prepend(navigation);
  document.querySelectorAll('a[href]').forEach(a=>{const url=new URL(a.href,location.href);if(url.pathname!==location.pathname||url.hash){url.searchParams.delete('first-look');a.href=url.href;a.target='_top'}});
  let pending;const send=()=>{cancelAnimationFrame(pending);pending=requestAnimationFrame(()=>parent.postMessage({type:'ws-first-look:height',height:Math.ceil(Math.max(stage.getBoundingClientRect().bottom,band.getBoundingClientRect().bottom)+scrollY+24)},location.origin))};
  new ResizeObserver(send).observe(document.body);send();
 }
 window.WestsideFirstLook=Object.freeze({dateKey,verseFor});
})();
