/* Reuse actual realm homepages; keep requested anchors stable while lazy frames size. */
(()=>{
 const frames=[...document.querySelectorAll('[data-fl-realm-frame]')];let anchor=null,raf;
 const requested=()=>{anchor=/^#first-look-(church|magazine|bible|sermon|book|cinema|life)$/.test(location.hash)||location.hash==='#sites-first-layer'?document.getElementById(location.hash.slice(1)):null;if(anchor)anchor.scrollIntoView({behavior:'instant',block:'start'});schedule()};
 const update=()=>{for(const frame of frames){const rect=frame.getBoundingClientRect(),progress=Math.max(0,Math.min(1,-rect.top/(Math.max(rect.height,1)*.55)));frame.contentWindow?.postMessage({type:'ws-first-look:progress',progress},location.origin)}raf=null};
 const schedule=()=>{if(!raf)raf=requestAnimationFrame(update)};
 window.addEventListener('message',event=>{if(event.origin!==location.origin||event.data?.type!=='ws-first-look:height')return;const frame=frames.find(f=>f.contentWindow===event.source),height=Number(event.data.height);if(frame&&Number.isFinite(height)&&height>=350&&height<=6000){const size=Math.ceil(height)+'px';if(frame.style.height!==size){if(anchor&&Math.abs(anchor.getBoundingClientRect().top)>3)anchor=null;frame.style.height=size;if(anchor)anchor.scrollIntoView({behavior:'instant',block:'start'});schedule()}}});
 for(const event of ['wheel','touchstart','pointerdown','keydown'])window.addEventListener(event,()=>{anchor=null},{passive:true});
 window.addEventListener('hashchange',requested);window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);frames.forEach(f=>f.addEventListener('load',schedule));requested();
})();

/* First-layer floating navigation: native scrolling, no scroll lock or snap. */
(()=>{
 const nav=typeof document.querySelector==='function'?document.querySelector('.sites-home-nav--floating'):null;
 if(!nav)return;
 const menu=nav.querySelector('details');
 let previousY=window.scrollY,scheduled=false;
 const update=()=>{
  const y=Math.max(0,window.scrollY),delta=y-previousY;
  const expanded=Boolean(menu?.open);
  if(Math.abs(delta)>5&&!expanded){
   nav.dataset.navHidden=String(y>120&&delta>0);
  }
  if(y<90||expanded)nav.dataset.navHidden='false';
  const film=document.querySelector('.sites-home-hero');
  const inFilm=film&&film.getBoundingClientRect().bottom>Math.min(120,window.innerHeight*.2);
  nav.dataset.navTone=inFilm?'dark':'light';
  previousY=y;scheduled=false;
 };
 window.addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(update)}},{passive:true});
 window.addEventListener('resize',update,{passive:true});
 menu?.addEventListener('toggle',()=>{if(menu.open)nav.dataset.navHidden='false';document.documentElement.classList.toggle('ws-home-menu-open',Boolean(menu.open));update()});
 const preview=nav.querySelector('.ws-nav-hover-preview');
 const previewFrame=preview?.querySelector('iframe');
 const previewCaption=preview?.querySelector('.ws-nav-hover-preview__caption');
 const previewSources={church:'/first-look-editorial/church.html',magazine:'/first-look-editorial/magazine.html',bible:'/first-look-editorial/bible.html',sermon:'/first-look-editorial/sermon.html',book:'/first-look-editorial/book.html',cinema:'/first-look-editorial/cinema.html',life:'/first-look-editorial/life.html'};
 let previewKey='';
 const summary=menu?.querySelector('summary');
 const panel=menu?.querySelector('.sites-home-nav__panel');
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
 /* Joby study: one reversible WAAPI timeline coordinates four planes,
    panel clip reveal and staggered lines. Independent implementation; upstream
    source and assets are not copied. Production backup stays on main. */
 const root=document.documentElement;
 const planes=[...nav.querySelectorAll('.ws-joby-layers i')];
 const intro=panel?.querySelector('.sites-home-nav__panel-intro');
 const links=[...panel.querySelectorAll('.sites-home-nav__panel-links>a')];
 const entries=[...panel.querySelectorAll('.sites-home-nav__panel-entries>a')];
 let sequence=null,animating=false;
 const timing={duration:1850,easing:'linear',fill:'both'};
 const frames=(from,to,start,end)=>[
  {offset:0,transform:from},{offset:start,transform:from},
  {offset:end,transform:to},{offset:1,transform:to}
 ];
 const makeTimeline=()=>{
  const anim=[];
  const add=(el,keyframes)=>{if(el)anim.push(el.animate(keyframes,{...timing}));};
  planes.forEach((el,i)=>add(el,frames('scaleY(0)','scaleY(1)',i*.065,.43+i*.065)));
  if(panel)add(panel,[
   {offset:0,clipPath:'inset(0 0 100% 0)',opacity:1},
   {offset:.18,clipPath:'inset(0 0 100% 0)',opacity:1},
   {offset:.66,clipPath:'inset(0 0 0% 0)',opacity:1},
   {offset:1,clipPath:'inset(0 0 0% 0)',opacity:1}
  ]);
  const textElements=[intro,...links,...entries].filter(Boolean);
  textElements.forEach((el,i)=>{
   const start=Math.min(.48+i*.028,.77),end=Math.min(start+.16,.97);
   add(el,[
    {offset:0,transform:'translateY(110%)',opacity:0},
    {offset:start,transform:'translateY(110%)',opacity:0},
    {offset:end,transform:'translateY(0%)',opacity:1},
    {offset:1,transform:'translateY(0%)',opacity:1}
   ]);
  });
  anim.forEach(a=>a.pause());
  return anim;
 };
 const reset=()=>{sequence?.forEach(a=>a.cancel());sequence=null;animating=false;};
 const settleClosed=()=>{menu.open=false;root.classList.remove('ws-joby-active','ws-joby-open');reset();};
 const openCurtain=()=>{
  if(animating||menu.open)return;
  menu.open=true;nav.dataset.navHidden='false';root.classList.add('ws-joby-active');
  if(reduced.matches||!Element.prototype.animate){root.classList.add('ws-joby-open');return;}
  animating=true;sequence=makeTimeline();
  root.classList.add('ws-joby-open');
  sequence.forEach(a=>a.play());
  Promise.all(sequence.map(a=>a.finished.catch(()=>null))).then(()=>{animating=false;});
 };
 const closeCurtain=()=>{
  if(!menu.open)return;
  if(reduced.matches||!sequence){settleClosed();return;}
  animating=true;
  sequence.forEach(a=>{a.reverse();});
  Promise.all(sequence.map(a=>a.finished.catch(()=>null))).then(()=>{
   if(!menu.open)return;settleClosed();
  });
 };
 summary?.addEventListener('click',event=>{
  event.preventDefault();
  if(animating)return;
  if(menu.open)closeCurtain();else openCurtain();
 });
 const showPreview=(link)=>{const match=link.getAttribute('href')?.match(/^#first-look-(church|magazine|bible|sermon|book|cinema|life)$/);if(!match||!previewFrame)return;const key=match[1];if(key!==previewKey){previewKey=key;previewFrame.src=previewSources[key];}if(previewCaption)previewCaption.textContent=link.textContent.trim();preview?.classList.add('is-visible');};
 const clearPreview=()=>{preview?.classList.remove('is-visible')};
 menu?.querySelectorAll('.sites-home-nav__panel-links>a').forEach(link=>{
  link.addEventListener('pointerenter',()=>showPreview(link));
  link.addEventListener('focus',()=>showPreview(link));
 });
 menu?.addEventListener('pointerleave',clearPreview);
 menu?.addEventListener('focusout',event=>{if(!menu.contains(event.relatedTarget))clearPreview()});
 menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',event=>{const hash=a.getAttribute('href');menu.open=false;root.classList.remove('ws-joby-active','ws-joby-open');reset();nav.dataset.navHidden='false';if(hash?.startsWith('#')){const target=document.getElementById(hash.slice(1));if(target){event.preventDefault();history.pushState(null,'',hash);requestAnimationFrame(()=>target.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'}));}}}));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.open){closeCurtain();menu.querySelector('summary')?.focus()}});
 document.addEventListener('pointerdown',e=>{if(menu?.open&&!menu.contains(e.target))closeCurtain()});
 update();
})();

/* Keep the viewport behind the full-screen contents still while it is open. */
