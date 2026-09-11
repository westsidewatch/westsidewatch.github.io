"""Runtime registry for Living Water motion/design experiment pages."""
import html as html_lib
import re
import codrops_site_8x5


_LIVING_CURRENT_STYLE = r'''
<style id="living-water-8x5-current">
.products__grid.living-current-field{display:block;position:relative;overflow:hidden;min-height:calc(100vh - 204px)}
.living-current-band{position:absolute;left:0;display:flex;align-items:center;gap:clamp(12px,1.45vw,28px);width:100%;will-change:transform;transform:translate3d(0,0,0)}
.living-current-band .product{flex:1 1 0;min-width:0;margin:0;aspect-ratio:8/5;will-change:transform,opacity;overflow:hidden}
.living-current-band .product>img.dore-source-crop{position:absolute;display:block;max-width:none!important;object-fit:cover!important;filter:saturate(.58) contrast(.92);will-change:left,top,width,height}
.living-current-band:nth-child(1){top:4%}.living-current-band:nth-child(2){top:52%}
.dore-mosaic-layer{position:fixed;z-index:2147483000;pointer-events:none;inset:0}.dore-mosaic-piece{position:fixed;overflow:hidden;margin:0;background:#d7cfbd;will-change:left,top,width,height}.dore-mosaic-piece img{position:absolute;display:block;max-width:none;object-fit:cover;filter:saturate(.58) contrast(.92);will-change:left,top,width,height}
.products[data-motion-phase="assemble"] .product,.products[data-motion-phase="focus"] .product{pointer-events:none}
@media(max-width:900px){.products__grid.living-current-field{display:grid;grid-template-columns:repeat(2,1fr);overflow:visible}.living-current-band{display:contents;transform:none!important}.living-current-band .product{width:auto}}
@media(prefers-reduced-motion:reduce){.living-current-band{transform:none!important}}
</style>
'''

_LIVING_CURRENT_SCRIPT = r'''
<script id="living-water-8x5-current-runtime">
(()=>{
 const stage=document.querySelector('.products'),grid=stage?.querySelector('.products__grid');if(!stage||!grid||stage.dataset.livingCurrentBound==='true')return;stage.dataset.livingCurrentBound='true';
 const cards=[...grid.querySelectorAll(':scope > .product')];if(cards.length){grid.classList.add('living-current-field');const n=Math.max(1,Math.ceil(cards.length/2));for(let i=0;i<2;i++){const slice=cards.slice(i*n,(i+1)*n);if(!slice.length)continue;const band=document.createElement('div');band.className='living-current-band';band.dataset.current=String(i+1);grid.appendChild(band);slice.forEach(c=>band.appendChild(c))}}
 const bands=[...grid.querySelectorAll('.living-current-band')];if(!bands.length)return;
 const slots=[{x:0,y:0},{x:.5,y:0},{x:0,y:.5},{x:.5,y:.5}];
 const cropBand=band=>{const group=[...band.querySelectorAll(':scope > .product')].slice(0,4);if(group.length!==4)return;const src=group[0].querySelector(':scope > img')?.src||'';group.forEach((card,i)=>{const img=card.querySelector(':scope > img');if(!img)return;img.src=src;img.classList.add('dore-source-crop');const s=slots[i];Object.assign(img.style,{width:'200%',height:'200%',left:(-s.x*200)+'%',top:(-s.y*200)+'%'});card.dataset.doreCrop=String(i)})};
 bands.forEach(cropBand);
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches,motion=bands.map((band,i)=>({band,offset:0,velocity:0,cruise:i===0?7:-5.5,target:0,limit:i===0?28:22,direction:i===0?1:-1}));
 let phase='settled',focused=null,originRects=null,mosaic=null,last=performance.now(),settleUntil=last+900,releasePromise=null;
 const setPhase=v=>{phase=v;stage.dataset.motionPhase=v;document.documentElement.dataset.livingCurrent='mosaic-'+v};
 const render=()=>motion.forEach(m=>m.band.style.transform=`translate3d(${m.offset.toFixed(3)}px,0,0)`);
 const beginDrift=()=>{if(reduced)return;motion.forEach(m=>m.target=m.cruise*m.direction);setPhase('drift')};
 const groupFor=card=>[...card.parentElement.querySelectorAll(':scope > .product')].slice(0,4);
 const masterRect=()=>{const padX=Math.max(32,innerWidth*.08),w=Math.min(innerWidth-padX*2,(innerHeight*.72)*1.6),h=w/1.6;return {left:(innerWidth-w)/2,top:(innerHeight-h)/2,width:w,height:h}};
 const cleanup=()=>{mosaic?.layer?.remove();mosaic=null;cards.forEach(c=>c.style.visibility='')};
 const cropFrame=(r,s)=>({width:r.width*2,height:r.height*2,left:-s.x*r.width*2,top:-s.y*r.height*2});
 const buildMosaic=card=>{cleanup();const group=groupFor(card);if(group.length!==4)return null;originRects=group.map(c=>c.getBoundingClientRect());const target=masterRect(),layer=document.createElement('div');layer.className='dore-mosaic-layer';const src=group[0].querySelector(':scope > img')?.src||'';const pieces=group.map((c,i)=>{const r=originRects[i],p=document.createElement('div');p.className='dore-mosaic-piece';Object.assign(p.style,{left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px'});const img=document.createElement('img');img.src=src;const f=cropFrame(r,slots[i]);Object.assign(img.style,{width:f.width+'px',height:f.height+'px',left:f.left+'px',top:f.top+'px'});p.appendChild(img);layer.appendChild(p);c.style.visibility='hidden';return p});document.body.appendChild(layer);mosaic={layer,pieces,target,group};return mosaic};
 const animatePieces=forward=>{if(!mosaic)return Promise.resolve();const {pieces,target}=mosaic;return Promise.all(pieces.map((p,i)=>{const r=originRects[i],s=slots[i],pieceTo=forward?{left:target.left+s.x*target.width,top:target.top+s.y*target.height,width:target.width/2,height:target.height/2}:{left:r.left,top:r.top,width:r.width,height:r.height},img=p.querySelector('img'),imgFrom={left:img.style.left,top:img.style.top,width:img.style.width,height:img.style.height},imgTo=forward?{left:-s.x*target.width,top:-s.y*target.height,width:target.width,height:target.height}:cropFrame(r,s),opts={duration:forward?560:520,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'};const a=p.animate([{left:p.style.left,top:p.style.top,width:p.style.width,height:p.style.height},{left:pieceTo.left+'px',top:pieceTo.top+'px',width:pieceTo.width+'px',height:pieceTo.height+'px'}],opts);const b=img.animate([imgFrom,{left:imgTo.left+'px',top:imgTo.top+'px',width:imgTo.width+'px',height:imgTo.height+'px'}],opts);return Promise.all([a.finished.catch(()=>{}),b.finished.catch(()=>{})])}))};
 const assemble=async card=>{if(focused!==card)return;setPhase('assemble');if(!buildMosaic(card)){setPhase('focus');return}await animatePieces(true);if(focused!==card||phase==='release')return;setPhase('focus')};
 const requestFocus=card=>{if(focused||['assemble','focus','release'].includes(phase))return;focused=card;motion.forEach(m=>m.target=0);setPhase('arrest')};
 const release=()=>{if(!focused||phase==='release')return releasePromise||Promise.resolve();setPhase('release');const run=async()=>{if(mosaic)await animatePieces(false);cleanup();focused=null;originRects=null;motion.forEach(m=>{m.offset=0;m.velocity=0;m.target=0});render();setPhase('settled');settleUntil=performance.now()+220;releasePromise=null};releasePromise=run();return releasePromise};
 cards.forEach(card=>card.addEventListener('mouseenter',e=>{e.stopImmediatePropagation();requestFocus(card)},true));
 const pointInRect=(x,y,r,pad=0)=>r&&x>=r.left-pad&&x<=r.left+r.width+pad&&y>=r.top-pad&&y<=r.top+r.height+pad;
 const pointerPolicy=e=>{if(!focused||phase==='release')return;const x=e.clientX,y=e.clientY;if(phase==='arrest'){const r=focused.getBoundingClientRect();if(!pointInRect(x,y,r,2))release();return}if(phase==='assemble'||phase==='focus'){const onWindow=pointInRect(x,y,mosaic?.target,0);if(!onWindow)release()}};
 document.addEventListener('pointermove',pointerPolicy,{passive:true,capture:true});document.addEventListener('mousemove',pointerPolicy,{passive:true,capture:true});document.addEventListener('pointerdown',e=>{if(focused&&!pointInRect(e.clientX,e.clientY,mosaic?.target,0))release()},{capture:true});document.documentElement.addEventListener('mouseleave',release,true);window.addEventListener('blur',release);
 const tick=now=>{const dt=Math.min(.05,(now-last)/1000);last=now;if(!reduced){if(phase==='settled'&&now>=settleUntil)beginDrift();motion.forEach(m=>{const accel=phase==='arrest'?32:8,delta=m.target-m.velocity;m.velocity+=Math.sign(delta)*Math.min(Math.abs(delta),accel*dt);if(phase==='drift'){m.offset+=m.velocity*dt;if(Math.abs(m.offset)>=m.limit){m.offset=Math.sign(m.offset)*m.limit;m.direction*=-1;m.target=m.cruise*m.direction}}else if(phase==='arrest'){m.offset+=m.velocity*dt;m.offset+=(0-m.offset)*Math.min(1,dt*9)}else if(['assemble','focus','release','settled'].includes(phase)){m.offset+=(0-m.offset)*Math.min(1,dt*12)}});if(phase==='arrest'&&motion.every(m=>Math.abs(m.velocity)<.16&&Math.abs(m.offset)<.55)){motion.forEach(m=>{m.velocity=0;m.offset=0;m.target=0});render();assemble(focused)}render()}requestAnimationFrame(tick)};
 setPhase('settled');render();requestAnimationFrame(tick);
})();
</script>
'''

_CANDIDATE_FOCUS_HOST_STYLE=r'''<style id="candidate-01-focus-screen-host">.candidate-focus-screen{position:relative;min-height:100svh;height:100svh;overflow:hidden;background:#eee8da;color:#252525}.candidate-focus-screen iframe{display:block;width:100%;height:100%;border:0;background:#eee8da}</style>'''
_CANDIDATE_FOCUS_EMBED_STYLE=r'''<style id="candidate-01-focus-screen-embed">html,body{height:100%;overflow:hidden!important}.frame,.cats,.dore-badge{display:none!important}.products{position:relative;height:100vh;min-height:100vh;padding:3.2vw 4vw!important}.products__grid.living-current-field{height:100%;min-height:100%!important}.products__preview{display:none!important}.lw-movement-label{position:absolute;z-index:20;left:0;right:0;height:2.35rem;display:flex;align-items:center;padding:0 1.2vw;background:transparent;color:#CEBD74;font-family:"Cormorant Garamond","Noto Serif TC",serif;font-size:clamp(11px,.78vw,14px);font-weight:500;letter-spacing:.12em;white-space:nowrap;pointer-events:none;box-sizing:border-box}.lw-movement-label.label-a{top:.35%}.lw-movement-label.label-b{top:48.35%}@media(max-width:900px){.lw-movement-label{position:relative;left:auto;right:auto;top:auto!important;height:auto;min-height:2.2rem;grid-column:1/-1;padding:.45rem .7rem;margin:.15rem 0;background:transparent;font-size:12px}}</style>'''

def _install_living_current(html):
    if 'id="living-water-8x5-current"' in html:return html
    return html.replace('</head>',_LIVING_CURRENT_STYLE+'</head>',1).replace('</body>',_LIVING_CURRENT_SCRIPT+'</body>',1)

def _movement_labels_script(labels):
    first,second=labels
    return f'''\
<script id="candidate-01-4w-labels">(()=>{{const labels={html_lib.escape(repr([first,second]),quote=False)};const attach=()=>{{const grid=document.querySelector('.products__grid.living-current-field'),bands=[...document.querySelectorAll('.living-current-band')];if(!grid||bands.length<2)return false;if(grid.querySelector(':scope > .lw-movement-label'))return true;labels.forEach((text,i)=>{{const label=document.createElement('div');label.className='lw-movement-label '+(i===0?'label-a':'label-b');label.textContent=text;grid.appendChild(label)}});return true}};if(!attach()){{const o=new MutationObserver(()=>{{if(attach())o.disconnect()}});o.observe(document.documentElement,{{childList:true,subtree:true}})}}}})();</script>\
'''

def _candidate_focus_screen(screen_no,labels):
    motion_html=_install_living_current(codrops_site_8x5.render(edit=False)).replace('</head>',_CANDIDATE_FOCUS_EMBED_STYLE+'</head>',1).replace('</body>',_movement_labels_script(labels)+'</body>',1);srcdoc=html_lib.escape(motion_html,quote=True)
    return '<section class="candidate-focus-screen" data-current="focus" data-layer="first" data-screen="%s"><iframe title="Living Water focus current %s" loading="eager" srcdoc="%s"></iframe></section>'%(screen_no,screen_no-1,srcdoc)

def _install_candidate_focus(current,html):
    if 'data-screen="3"' in html:return html
    html=html.replace('</head>',_CANDIDATE_FOCUS_HOST_STYLE+'</head>',1);anchor='</section><section class="world dark">';a=_candidate_focus_screen(2,('第一樂章 WATCH','第二樂章 WITNESS'));b=_candidate_focus_screen(3,('第三樂章 WALK','第四樂章 WORSHIP'));return html.replace(anchor,'</section>'+a+b+'<section class="world dark">',1)

def install(current):
    codrops_site_8x5.install_workspace(current.visual.base);page_ids=[current.motion_prototypes.PAGE_ID,current.living_water_candidate.PAGE_ID,current.living_water_candidate_02.PAGE_ID,current.living_water_candidate_03.PAGE_ID,current.living_water_candidate_04.PAGE_ID,current.living_water_second_layer_lab.PAGE_ID,current.living_water_third_alive_lab.PAGE_ID,codrops_site_8x5.PAGE_ID];current.multipage_wysiwyg.SUPPORTED.update(page_ids);previous_render=current.multipage_wysiwyg.render_canvas
    def render_canvas(page_id='homepage',edit=False):
        if page_id==codrops_site_8x5.PAGE_ID:return _install_living_current(codrops_site_8x5.render(edit=edit))
        if page_id==current.living_water_candidate.PAGE_ID:return _install_candidate_focus(current,current.living_water_candidate.render(edit=edit))
        return previous_render(page_id,edit=edit)
    current.multipage_wysiwyg.render_canvas=render_canvas;ids=['homepage','homepage-concept-index','homepage-concept-dispatch','homepage-concept-folio','journal-vol-00','multiwrite-home','multiwrite-cover',*page_ids];literal="supported=new Set(["+",".join(repr(x) for x in ids)+"])";current.multipage_wysiwyg.EDITOR_HTML=re.sub(r"supported=new Set\(\[[^\]]*\]\)",literal,current.multipage_wysiwyg.EDITOR_HTML,count=1)