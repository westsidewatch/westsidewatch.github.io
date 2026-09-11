"""Runtime registry for Living Water motion/design experiment pages."""
import html as html_lib
import re
import codrops_site_8x5


_LIVING_CURRENT_STYLE = r'''
<style id="living-water-8x5-current">
.products__grid.living-current-field{display:block;position:relative;overflow:hidden;min-height:calc(100vh - 204px)}
.living-current-band{position:absolute;left:0;display:flex;align-items:center;gap:clamp(12px,1.45vw,28px);width:100%;will-change:transform;transform:translate3d(0,0,0)}
.living-current-band .product{flex:1 1 0;min-width:0;margin:0;aspect-ratio:8/5;will-change:transform,opacity}
.living-current-band:nth-child(1){top:4%}
.living-current-band:nth-child(2){top:52%}
.products[data-motion-phase="drift"] .living-current-band{cursor:default}
.products[data-motion-phase="intent"] .living-current-band,
.products[data-motion-phase="arrest"] .living-current-band,
.products[data-motion-phase="locked"] .living-current-band,
.products[data-motion-phase="focus"] .living-current-band,
.products[data-motion-phase="release"] .living-current-band{cursor:default}
@media(max-width:900px){
 .products__grid.living-current-field{display:grid;grid-template-columns:repeat(2,1fr);overflow:visible}
 .living-current-band{display:contents;transform:none!important}
 .living-current-band .product{width:auto}
}
@media(prefers-reduced-motion:reduce){.living-current-band{transform:none!important}}
</style>
'''

_LIVING_CURRENT_SCRIPT = r'''
<script id="living-water-8x5-current-runtime">
(()=>{
  const stage=document.querySelector('.products');
  const grid=stage?.querySelector('.products__grid');
  if(!stage||!grid||stage.dataset.livingCurrentBound==='true')return;
  stage.dataset.livingCurrentBound='true';

  const cards=[...grid.querySelectorAll(':scope > .product')];
  if(cards.length){
    grid.classList.add('living-current-field');
    const perBand=Math.max(1,Math.ceil(cards.length/2));
    for(let i=0;i<2;i++){
      const slice=cards.slice(i*perBand,(i+1)*perBand);
      if(!slice.length)continue;
      const band=document.createElement('div');
      band.className='living-current-band';
      band.dataset.current=String(i+1);
      grid.appendChild(band);
      slice.forEach(card=>band.appendChild(card));
    }
  }

  const bands=[...grid.querySelectorAll('.living-current-band')];
  if(!bands.length)return;

  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const motion=bands.map((band,index)=>({
    band,index,offset:0,velocity:0,
    cruise:index===0?7.0:-5.5,
    target:0,
    limit:index===0?28:22,
    direction:index===0?1:-1
  }));

  let phase='settled';
  let focusedCard=null;
  let lockRect=null;
  let settleUntil=performance.now()+900;
  let releaseTimer=0;
  let focusIssued=false;
  let last=performance.now();

  const setPhase=value=>{
    phase=value;
    stage.dataset.motionPhase=value;
    document.documentElement.dataset.livingCurrent='phase-lock-'+value;
  };
  setPhase('settled');

  const render=()=>motion.forEach(m=>{
    m.band.style.transform=`translate3d(${m.offset.toFixed(3)}px,0,0)`;
  });

  const beginDrift=()=>{
    if(reduced){setPhase('settled');return}
    focusedCard=null;lockRect=null;focusIssued=false;
    motion.forEach(m=>{m.target=m.cruise*m.direction});
    setPhase('drift');
  };

  const requestFocus=card=>{
    clearTimeout(releaseTimer);
    if(focusedCard===card && ['intent','arrest','locked','focus'].includes(phase))return;
    focusedCard=card;
    lockRect=card.getBoundingClientRect();
    focusIssued=false;
    motion.forEach(m=>{m.target=0});
    setPhase('intent');
    requestAnimationFrame(()=>{if(focusedCard===card)setPhase('arrest')});
  };

  const replayEnter=card=>{
    if(!card||focusIssued)return;
    focusIssued=true;
    lockRect=card.getBoundingClientRect();
    setPhase('locked');
    const ev=new MouseEvent('mouseenter',{bubbles:false,cancelable:true,view:window});
    Object.defineProperty(ev,'dorePhaseReplay',{value:true});
    card.dispatchEvent(ev);
    setPhase('focus');
  };

  const replayLeave=card=>{
    if(!card)return;
    const ev=new MouseEvent('mouseleave',{bubbles:false,cancelable:true,view:window});
    Object.defineProperty(ev,'dorePhaseReplay',{value:true});
    card.dispatchEvent(ev);
  };

  const requestRelease=()=>{
    if(!focusedCard && !['intent','arrest','locked','focus'].includes(phase))return;
    const card=focusedCard;
    clearTimeout(releaseTimer);
    setPhase('release');
    if(card)replayLeave(card);
    focusedCard=null;lockRect=null;focusIssued=false;
    motion.forEach(m=>{m.target=0});
    releaseTimer=setTimeout(()=>{
      motion.forEach(m=>{m.offset=0;m.velocity=0;m.target=0});
      render();
      settleUntil=performance.now()+180;
      setPhase('settled');
      setTimeout(()=>{if(phase==='settled')beginDrift()},180);
    },620);
  };

  cards.forEach(card=>{
    card.addEventListener('mouseenter',event=>{
      if(event.dorePhaseReplay)return;
      event.stopImmediatePropagation();
      requestFocus(card);
    },true);
    card.addEventListener('mouseleave',event=>{
      if(event.dorePhaseReplay)return;
      event.stopImmediatePropagation();
      if(focusedCard===card || ['intent','arrest','locked','focus'].includes(phase))requestRelease();
    },true);
  });

  const outsideLockedRect=event=>{
    if(!focusedCard||!lockRect||!['locked','focus'].includes(phase))return;
    const x=event.clientX,y=event.clientY;
    if(x<lockRect.left||x>lockRect.right||y<lockRect.top||y>lockRect.bottom)requestRelease();
  };
  document.addEventListener('pointermove',outsideLockedRect,{passive:true});
  document.documentElement.addEventListener('mouseleave',requestRelease,true);
  window.addEventListener('blur',requestRelease);

  const tick=now=>{
    const dt=Math.min(.05,(now-last)/1000);last=now;
    if(!reduced){
      if(phase==='settled' && now>=settleUntil)beginDrift();
      motion.forEach(m=>{
        const accel=(phase==='arrest'||phase==='intent'||phase==='release')?30:8;
        const delta=m.target-m.velocity;
        const step=Math.sign(delta)*Math.min(Math.abs(delta),accel*dt);
        m.velocity+=step;
        if(phase==='drift'){
          m.offset+=m.velocity*dt;
          if(Math.abs(m.offset)>=m.limit){
            m.offset=Math.sign(m.offset)*m.limit;
            m.direction*=-1;
            m.target=m.cruise*m.direction;
          }
        } else if(['intent','arrest'].includes(phase)){
          m.offset+=m.velocity*dt;
          const pull=Math.min(1,dt*8.5);
          m.offset+=(0-m.offset)*pull;
        } else if(['locked','focus','release','settled'].includes(phase)){
          const pull=Math.min(1,dt*10);
          m.offset+=(0-m.offset)*pull;
        }
      });
      if(phase==='arrest'){
        const still=motion.every(m=>Math.abs(m.velocity)<.18 && Math.abs(m.offset)<.65);
        if(still){
          motion.forEach(m=>{m.velocity=0;m.offset=0;m.target=0});
          render();
          replayEnter(focusedCard);
        }
      }
      render();
    }
    requestAnimationFrame(tick);
  };
  render();
  requestAnimationFrame(tick);
})();
</script>
'''

_CANDIDATE_FOCUS_HOST_STYLE = r'''
<style id="candidate-01-focus-screen-host">
.candidate-focus-screen{position:relative;min-height:100svh;height:100svh;overflow:hidden;background:#eee8da;color:#252525}
.candidate-focus-screen iframe{display:block;width:100%;height:100%;border:0;background:#eee8da}
</style>
'''

_CANDIDATE_FOCUS_EMBED_STYLE = r'''
<style id="candidate-01-focus-screen-embed">
html,body{height:100%;overflow:hidden!important}
.frame,.cats,.dore-badge{display:none!important}
.products{position:relative;height:100vh;min-height:100vh;padding:3.2vw 4vw!important}
.products__grid.living-current-field{height:100%;min-height:100%!important}
.products__preview{inset:3.2vw 4vw!important;min-height:calc(100vh - 6.4vw)!important}
.lw-movement-label{position:absolute;z-index:20;left:0;right:0;height:2.35rem;display:flex;align-items:center;padding:0 1.2vw;background:transparent;color:#CEBD74;font-family:"Cormorant Garamond","Noto Serif TC",serif;font-size:clamp(11px,.78vw,14px);font-weight:500;letter-spacing:.12em;white-space:nowrap;pointer-events:none;box-sizing:border-box}
.lw-movement-label.label-a{top:.35%}
.lw-movement-label.label-b{top:48.35%}
@media(max-width:900px){
 .lw-movement-label{position:relative;left:auto;right:auto;top:auto!important;height:auto;min-height:2.2rem;grid-column:1/-1;padding:.45rem .7rem;margin:.15rem 0;background:transparent;font-size:12px}
}
</style>
'''


def _install_living_current(html):
    """Layer two phase-locked Living Water currents over the accepted Codrops focus motion."""
    if 'id="living-water-8x5-current"' in html:
        return html
    html = html.replace('</head>', _LIVING_CURRENT_STYLE + '</head>', 1)
    return html.replace('</body>', _LIVING_CURRENT_SCRIPT + '</body>', 1)


def _movement_labels_script(labels):
    """Place pale-gold 4W names above the two existing currents without changing their positions."""
    first, second = labels
    return f'''\n<script id="candidate-01-4w-labels">\n(()=>{{\n  const labels={html_lib.escape(repr([first, second]), quote=False)};\n  const attach=()=>{{\n    const grid=document.querySelector('.products__grid.living-current-field');\n    const bands=[...document.querySelectorAll('.living-current-band')];\n    if(!grid||bands.length<2)return false;\n    if(grid.querySelector(':scope > .lw-movement-label'))return true;\n    labels.forEach((text,i)=>{{\n      const label=document.createElement('div');\n      label.className='lw-movement-label '+(i===0?'label-a':'label-b');\n      label.textContent=text;\n      grid.appendChild(label);\n    }});\n    return true;\n  }};\n  if(!attach()){{\n    const observer=new MutationObserver(()=>{{if(attach())observer.disconnect();}});\n    observer.observe(document.documentElement,{{childList:true,subtree:true}});\n  }}\n}})();\n</script>\n'''


def _candidate_focus_screen(screen_no, labels):
    """Reuse the locked focus runtime and label its two existing currents."""
    motion_html = _install_living_current(codrops_site_8x5.render(edit=False))
    motion_html = motion_html.replace('</head>', _CANDIDATE_FOCUS_EMBED_STYLE + '</head>', 1)
    motion_html = motion_html.replace('</body>', _movement_labels_script(labels) + '</body>', 1)
    srcdoc = html_lib.escape(motion_html, quote=True)
    return (
        '<section class="candidate-focus-screen" data-current="focus" '
        f'data-layer="first" data-screen="{screen_no}">'
        f'<iframe title="Living Water focus current {screen_no - 1}" loading="eager" srcdoc="' + srcdoc + '"></iframe>'
        '</section>'
    )


def _install_candidate_focus(current, html):
    """Candidate 01: home, two 4W-labelled focus screens, then fixed worlds."""
    if 'data-screen="3"' in html:
        return html
    html = html.replace('</head>', _CANDIDATE_FOCUS_HOST_STYLE + '</head>', 1)
    anchor = '</section><section class="world dark">'
    focus_one = _candidate_focus_screen(2, ('第一樂章 WATCH', '第二樂章 WITNESS'))
    focus_two = _candidate_focus_screen(3, ('第三樂章 WALK', '第四樂章 WORSHIP'))
    return html.replace(
        anchor,
        '</section>' + focus_one + focus_two + '<section class="world dark">',
        1,
    )


def install(current):
    # Register the new 8:5 Codrops adaptation as a real workspace page.
    codrops_site_8x5.install_workspace(current.visual.base)

    page_ids = [
        current.motion_prototypes.PAGE_ID,
        current.living_water_candidate.PAGE_ID,
        current.living_water_candidate_02.PAGE_ID,
        current.living_water_candidate_03.PAGE_ID,
        current.living_water_candidate_04.PAGE_ID,
        current.living_water_second_layer_lab.PAGE_ID,
        current.living_water_third_alive_lab.PAGE_ID,
        codrops_site_8x5.PAGE_ID,
    ]
    current.multipage_wysiwyg.SUPPORTED.update(page_ids)

    # Keep standalone Third Alive intact; Candidate 01 only reuses the two locked focus viewports.
    previous_render = current.multipage_wysiwyg.render_canvas
    def render_canvas(page_id='homepage', edit=False):
        if page_id == codrops_site_8x5.PAGE_ID:
            return _install_living_current(codrops_site_8x5.render(edit=edit))
        if page_id == current.living_water_candidate.PAGE_ID:
            return _install_candidate_focus(current, current.living_water_candidate.render(edit=edit))
        return previous_render(page_id, edit=edit)
    current.multipage_wysiwyg.render_canvas = render_canvas

    # The editor has a separate client-side supported Set. Keep every motion /
    # Living Water experiment clickable instead of rendering it grey/disabled.
    ids = [
        'homepage','homepage-concept-index','homepage-concept-dispatch','homepage-concept-folio',
        'journal-vol-00','multiwrite-home','multiwrite-cover',
        *page_ids,
    ]
    literal = "supported=new Set([" + ",".join(repr(x) for x in ids) + "])"
    current.multipage_wysiwyg.EDITOR_HTML = re.sub(
        r"supported=new Set\(\[[^\]]*\]\)",
        literal,
        current.multipage_wysiwyg.EDITOR_HTML,
        count=1,
    )
