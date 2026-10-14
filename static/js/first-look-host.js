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
 let activeReveal=null;
 const revealShape=()=>{const r=summary?.getBoundingClientRect();const x=r?Math.round(r.left+r.width/2):window.innerWidth-65;const y=r?Math.round(r.top+r.height/2):35;return {small:'circle(0px at '+x+'px '+y+'px)',large:'circle(150vmax at '+x+'px '+y+'px)'};};
 const animateReveal=(opening)=>{
  if(!panel)return Promise.resolve();
  activeReveal?.cancel();activeReveal=null;
  if(reduced.matches||!panel.animate)return Promise.resolve();
  const shape=revealShape();
  const frames=opening?[{clipPath:shape.small,opacity:1},{clipPath:shape.large,opacity:1}]:[{clipPath:shape.large,opacity:1},{clipPath:shape.small,opacity:1}];
  const anim=panel.animate(frames,{duration:opening?850:650,easing:'cubic-bezier(.76,0,.24,1)',fill:'forwards'});
  activeReveal=anim;
  return anim.finished.catch(()=>{}).then(()=>{if(activeReveal===anim){anim.cancel();activeReveal=null}});
 };
 const closeCurtain=async()=>{
  if(!menu?.open||menu.classList.contains('is-closing'))return;
  menu.classList.add('is-closing');
  await animateReveal(false);
  menu.open=false;
  menu.classList.remove('is-closing');
 };
 summary?.addEventListener('click',event=>{
  event.preventDefault();
  if(menu.open){closeCurtain();return;}
  menu.open=true;
  menu.classList.remove('is-closing');
  requestAnimationFrame(()=>animateReveal(true));
 });
 const showPreview=(link)=>{const match=link.getAttribute('href')?.match(/^#first-look-(church|magazine|bible|sermon|book|cinema|life)$/);if(!match||!previewFrame)return;const key=match[1];if(key!==previewKey){previewKey=key;previewFrame.src=previewSources[key];}if(previewCaption)previewCaption.textContent=link.textContent.trim();preview?.classList.add('is-visible');};
 const clearPreview=()=>{preview?.classList.remove('is-visible')};
 menu?.querySelectorAll('.sites-home-nav__panel-links>a').forEach(link=>{
  link.addEventListener('pointerenter',()=>showPreview(link));
  link.addEventListener('focus',()=>showPreview(link));
 });
 menu?.addEventListener('pointerleave',clearPreview);
 menu?.addEventListener('focusout',event=>{if(!menu.contains(event.relatedTarget))clearPreview()});
 menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',event=>{const hash=a.getAttribute('href');menu.open=false;nav.dataset.navHidden='false';if(hash?.startsWith('#')){const target=document.getElementById(hash.slice(1));if(target){event.preventDefault();history.pushState(null,'',hash);requestAnimationFrame(()=>target.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'}));}}}));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.open){closeCurtain();menu.querySelector('summary')?.focus()}});
 document.addEventListener('pointerdown',e=>{if(menu?.open&&!menu.contains(e.target))closeCurtain()});
 update();
})();

/* Keep the viewport behind the full-screen contents still while it is open. */
