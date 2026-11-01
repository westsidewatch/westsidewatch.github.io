
/* Opt-in extension for the existing P2 03–04 draft lab, no main-site change.
 * The existing p2-emmaus-olive-preview.js remains the sole 01–04 scroll owner;
 * 05–07 use the same document scroll position, same measured Magazine union,
 * same film-surround #p2-realm-background and no new iframe or video.
 */
(()=>{'use strict';
const $=s=>document.querySelector(s),clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
const q=new URLSearchParams(location.search);
// The draft P2 preview shows all five chapters by default. Explicit five=0 preserves the baseline for A/B checks.
if(q.get('five')==='0')return;
const stage=$('#proof-stage'),track=$('#proof-track'),background=$('#p2-realm-background'),base=$('#proof-original');
if(!stage||!track||!background||!base){console.warn('[P2 five v15] original 03/04 P2 stage not found');return}
const originalTrackHeight=getComputedStyle(track).height;
// Preserve the existing original Magazine measurements; unlike earlier failed
// trials never manufacture an alternate inner 8.5% or arbitrary folio rect.
const srcRoot='/images/p2-realms/v15/';
const sections=[
 {key:'book',start:12,end:13.57,num:'05',title:'DAWN',subtitle:'BOOKSHOP',zh:'黎明書局',desc:'出版、編目與閱讀的秩序。從文字出發，走向知識與理解。',href:'/dawn-library/',cta:'進入黎明書局',image:'05-library-engraving-v1-5.svg'},
 {key:'cinema',start:13.57,end:15.14,num:'06',title:'PARADISE',subtitle:'CINEMA',zh:'天堂電影院',desc:'幕布緩緩開啟。影像成為進入敘事與思考的門。',href:'/cinema/',cta:'進入天堂電影院',image:'06-cinema-engraving-v1-5.svg'},
 {key:'life',start:15.14,end:16.74,num:'07',title:'DAYLIGHT',subtitle:'CAFÉ',zh:'白晝咖啡館',desc:'五穀與新酒，並土地七種供應。生活的豐盛從被領受開始。',href:'/daylight-cafe/',cta:'進入白晝咖啡館',image:'07-cafe-engraving-v1-5.svg'}
];
const el=document.createElement('div');el.id='p2-five-overlay-root';
stage.append(el);
for(const sec of sections){
 const child=document.createElement('section');child.className='p2-five-realm p2-five-realm--'+sec.key;child.dataset.realm=sec.key;
 child.setAttribute('aria-label',sec.num+' '+sec.zh);child.setAttribute('aria-hidden','true');child.inert=true;
 // All text is live semantic HTML, no typesetting baked into SVG.
 const head=document.createElement('div');head.className='p2-five-realm__main';
 const meta=document.createElement('div');meta.className='p2-five-realm__meta';meta.innerHTML='<span>'+sec.num+' / 07</span><span>WESTSIDE / '+sec.key.toUpperCase()+'</span>';head.append(meta);
 const title=document.createElement('h2');title.className='p2-five-realm__title';title.textContent=sec.title;head.append(title);
 const sub=document.createElement('p');sub.className='p2-five-realm__zh';sub.textContent=sec.zh;head.append(sub);
 const desc=document.createElement('p');desc.className='p2-five-realm__desc';desc.textContent=sec.desc;head.append(desc);
 const link=document.createElement('a');link.className='p2-five-realm__link';link.href=sec.href;link.textContent=sec.cta+' ↗';head.append(link);
 const foot=document.createElement('div');foot.className='p2-five-realm__foot';foot.innerHTML='<span>'+sec.subtitle+'</span><span>'+sec.num+' / 07</span>';head.append(foot);
 const side=document.createElement('aside');side.className='p2-five-realm__side';
 if(sec.key==='cinema'){
  const scene=document.createElement('div');scene.className='p2-cinema-stage';
  const light=document.createElement('div');light.className='p2-cinema-stage__light';const words=document.createElement('span');words.textContent='THE VEIL / OPENING';light.append(words);scene.append(light);
  const curtain=document.createElement('div');curtain.className='p2-cinema-curtain';
  curtain.append(document.createElement('div'),document.createElement('div'));
  curtain.firstChild.className='p2-cinema-curtain__half';curtain.lastChild.className='p2-cinema-curtain__half';scene.append(curtain);side.append(scene);
 }else{const im=document.createElement('img');im.src=srcRoot+sec.image;im.loading='lazy';im.alt='';im.decoding='async';side.append(im)}
 const label=document.createElement('div');label.className='p2-five-realm__corner';label.textContent='WESTSIDE WATCH / VOL.00';side.append(label);
 const cap=document.createElement('div');cap.className='p2-five-realm__cap';cap.innerHTML='<span>ENGRAVED FIELD</span><span>'+sec.num+'</span>';side.append(cap);
 child.append(head,side);el.append(child);sec.node=child;
}
const jumpBar=$('.proof-controls__buttons');
if(jumpBar)for(const sec of sections){const b=document.createElement('button');b.type='button';b.textContent=sec.num+' '+sec.zh;b.dataset.p2FiveJump=sec.key;
 b.addEventListener('click',()=>{const top=track.getBoundingClientRect().top+scrollY;
 scrollTo({top:top+(sec.start+.26)*innerHeight,behavior:'instant'})});jumpBar.append(b)}
document.body.dataset.p2FiveV15='on';
// In the original 03/04 preview, the video negative-space clip is already
// measured from source #dual-contents + #dual-cover + #dual-continuum.
function actualSpread(){
 const sourceFrame=base.contentDocument?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)');
 const doc=sourceFrame?.contentDocument;
 if(!doc)return null;
 const target=['dual-contents','dual-cover','dual-continuum'].map(id=>doc.getElementById(id)).filter(Boolean);
 if(target.length<2)return null;
 const fr=sourceFrame.getBoundingClientRect(),br=base.getBoundingClientRect(),sr=stage.getBoundingClientRect();
 const bb=target.map(node=>{const r=node.getBoundingClientRect();return {x:br.left-sr.left+fr.left+r.left,y:br.top-sr.top+fr.top+r.top,w:r.width,h:r.height}});
 const x=Math.min(...bb.map(r=>r.x)),y=Math.min(...bb.map(r=>r.y));
 return {x,y,w:Math.max(...bb.map(r=>r.x+r.w))-x,h:Math.max(...bb.map(r=>r.y+r.h))-y};
}
let seenFolio=false,lastActive='',requestId=0,hasMeasured=false;
function update(){requestId=0;
 const vh=Math.max(1,innerHeight),d=clamp(-track.getBoundingClientRect().top/vh,0,18);
 const last=sections.find(sec=>d>=sec.start&&d<sec.end);
 let rect=actualSpread();
 // The fixture mode is exclusively for local adapter QA; never used on P2.
 if(!rect&&document.body.dataset.p2TestFixture==='on'){
  const fixture=$('#p2-fixture-magazine');if(fixture){const r=fixture.getBoundingClientRect(),sr=stage.getBoundingClientRect();rect={x:r.left-sr.left,y:r.top-sr.top,w:r.width,h:r.height}}
 }
 if(rect){seenFolio=true;hasMeasured=true}
 for(const sec of sections){
  const active=sec===last&&!!rect;
  const n=sec.node;
  if(rect){n.style.left=rect.x.toFixed(2)+'px';n.style.top=rect.y.toFixed(2)+'px';n.style.width=rect.w.toFixed(2)+'px';n.style.height=rect.h.toFixed(2)+'px'}
  if(active){const amount=smooth((d-sec.start)/.24);n.classList.add('is-active');n.style.opacity=String(amount);
   n.style.visibility='visible';n.inert=false;n.setAttribute('aria-hidden','false');
   if(sec.key==='cinema'){
    const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
    // A scroll-owned parting: hand stops = curtain stops; reverse restores.
    const open=smooth((d-sec.start-.37)/(.81));n.style.setProperty('--p2-curtain-open',String(reduced?1:open));
   }
  }else{n.classList.remove('is-active');n.style.opacity='0';n.style.visibility='hidden';n.inert=true;n.setAttribute('aria-hidden','true')}
 }
 // Original 03/04 script still sets bible/sermon while painting. At later
 // distances it has already finished 04 and the FIVE adapter owns the realm.
 if(last&&rect){
  if(background.dataset.realm!==last.key)background.dataset.realm=last.key;
  background.style.opacity='1';
  // Use the existing clipPath set by original P2 paint only if it is valid.
  // There is no replacement guessing rectangle. A frozen magazine proof with
  // missing source DOM is intentionally not considered a passing integration.
  if(document.body.dataset.p2TestFixture==='on'){
   const sr=stage.getBoundingClientRect(),x=rect.x,y=rect.y,r=x+rect.w,b=y+rect.h;
   background.style.clipPath=`path("M 0 0 H ${sr.width} V ${sr.height} H 0 Z M ${x} ${y} V ${b} H ${r} V ${y} Z")`;
  }
 }
 if(lastActive!==(last?.key||'')){
  lastActive=last?.key||'';document.body.dataset.p2FiveActive=lastActive||'earlier';
 }
}
function schedule(){if(!requestId)requestId=requestAnimationFrame(update)}
addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule);
base.addEventListener('load',schedule);
// At same scroll position the existing P2 animator may reset background.realm.
// Reassert only on chapter 05–07, never mutating earlier scenes.
new MutationObserver(()=>{if(document.body.dataset.p2FiveActive==='earlier')return;schedule()}).observe(background,{attributes:true,attributeFilter:['data-realm']});
schedule();
window.p2FiveIntegrationV15={chapterBounds:sections.map(({key,start,end})=>({key,start,end})),get hasMeasuredFolio(){return hasMeasured},get activeRealm(){return lastActive},get originalTrackHeight(){return originalTrackHeight}};
})();

