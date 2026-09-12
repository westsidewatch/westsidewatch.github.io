"""Candidate 01 — Codrops GridToFullPreview with exact horizontal 8:5 geometry lock."""
from __future__ import annotations
import html as html_lib
import design_motion_registry as motion
import codrops_site_8x5

GEOMETRY_LOCK = r'''<script id="candidate01-exact-grid-preview-geometry">
(()=>{
  const sync=()=>{
    const root=document.querySelector('.products');
    const grid=document.querySelector('.products__grid');
    const layer=document.querySelector('.products__preview');
    const cards=[...document.querySelectorAll('.products__grid .product')];
    const left=document.querySelector('.product-preview.--left');
    const right=document.querySelector('.product-preview.--right');
    if(!root||!grid||!layer||cards.length<8||!left||!right)return;

    const rr=root.getBoundingClientRect();
    const cr=cards.map(el=>el.getBoundingClientRect());
    const minX=Math.min(...cr.map(r=>r.left));
    const maxX=Math.max(...cr.map(r=>r.right));
    const minY=Math.min(...cr.map(r=>r.top));
    const maxY=Math.max(...cr.map(r=>r.bottom));

    layer.style.inset='auto';
    layer.style.left=`${minX-rr.left}px`;
    layer.style.top=`${minY-rr.top}px`;
    layer.style.width=`${maxX-minX}px`;
    layer.style.height=`${maxY-minY}px`;
    layer.style.minHeight='0';

    const groupW=cr[1].right-cr[0].left;
    const groupH=maxY-minY;
    [left,right].forEach(p=>{
      p.style.width=`${groupW}px`;
      p.style.height=`${groupH}px`;
      p.style.top='0';
      p.style.transform='none';
    });
    left.style.left='0';
    left.style.right='auto';
    right.style.right='0';
    right.style.left='auto';

    document.documentElement.dataset.candidate01Geometry=
      `${Math.round(groupW)}x${Math.round(groupH)}`;
  };
  window.__candidate01SyncGeometry=sync;

  const settle=()=>requestAnimationFrame(()=>requestAnimationFrame(()=>{
    sync();
    window.dispatchEvent(new Event('resize'));
  }));

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',settle,{once:true});
  else settle();
  window.addEventListener('resize',sync,{passive:true});
})();
</script>'''

PAGE2_ASSEMBLY_FIX = r'''<style id="candidate01-page2-assembly-lock">
/* Page 2: four source panes close their real grid gutters into one exact master rectangle. */
html[data-candidate01-page="2"] .product-preview{backface-visibility:hidden;transform-origin:50% 50%;}
html[data-candidate01-page="2"] .product-preview__images{transform-origin:50% 50%;}
</style>
<script id="candidate01-page2-assembly-runtime">
(()=>{
  document.documentElement.dataset.candidate01Page='2';
  const baseSync=window.__candidate01SyncGeometry;
  if(!baseSync)return;
  const lock=()=>{
    baseSync();
    const root=document.querySelector('.products');
    const layer=document.querySelector('.products__preview');
    const cards=[...document.querySelectorAll('.products__grid .product')];
    const left=document.querySelector('.product-preview.--left');
    const right=document.querySelector('.product-preview.--right');
    if(!root||!layer||cards.length<8||!left||!right)return;
    const rr=root.getBoundingClientRect();
    const cr=cards.map(el=>el.getBoundingClientRect());
    const colGap=Math.max(0,cr[1].left-cr[0].right);
    const rowGap=Math.max(0,cr[4].top-cr[0].bottom);
    const minX=Math.min(...cr.map(r=>r.left));
    const maxX=Math.max(...cr.map(r=>r.right));
    const minY=Math.min(...cr.map(r=>r.top));
    const maxY=Math.max(...cr.map(r=>r.bottom));
    const masterLeft=minX-rr.left+colGap/2;
    const masterTop=minY-rr.top+rowGap/2;
    const masterW=maxX-minX-colGap;
    const masterH=maxY-minY-rowGap;
    const halfW=masterW/2;

    layer.style.inset='auto';
    layer.style.left=`${masterLeft}px`;
    layer.style.top=`${masterTop}px`;
    layer.style.width=`${masterW}px`;
    layer.style.height=`${masterH}px`;
    layer.style.minHeight='0';
    [left,right].forEach(p=>{
      p.style.width=`${halfW}px`;
      p.style.height=`${masterH}px`;
      p.style.top='0px';
      p.style.bottom='auto';
      p.style.transform='none';
    });
    left.style.left='0px'; left.style.right='auto';
    right.style.left=`${halfW}px`; right.style.right='auto';

    document.documentElement.dataset.candidate01AssemblyLock=
      `master-${Math.round(masterW)}x${Math.round(masterH)}-gap-${Math.round(colGap)}x${Math.round(rowGap)}`;
  };
  window.__candidate01SyncGeometry=lock;
  requestAnimationFrame(()=>requestAnimationFrame(lock));
  window.addEventListener('resize',lock,{passive:true});
})();
</script>'''

LIVING_CURRENT_STYLE = r'''<style id="candidate01-living-current-return">
/* Keep the four source cards visually present under the Codrops preview mask.
   Web Animations may request opacity:0; this visibility lock prevents the blank-hole regression. */
.products__grid .product{opacity:1!important}
.products__grid .product{translate:0 0;will-change:translate,transform,opacity}
@media(prefers-reduced-motion:reduce){.products__grid .product{translate:0 0!important}}
</style>'''

LIVING_CURRENT_SCRIPT = r'''<script id="candidate01-living-current-runtime">
(()=>{
  const cards=[...document.querySelectorAll('.products__grid .product')];
  if(cards.length<8||document.documentElement.dataset.candidate01CurrentBound==='true')return;
  document.documentElement.dataset.candidate01CurrentBound='true';
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const rows=[cards.slice(0,4),cards.slice(4,8)];
  const state=[
    {offset:0,velocity:0,cruise:7,direction:1,limit:28},
    {offset:0,velocity:0,cruise:5.5,direction:-1,limit:22}
  ];
  let last=performance.now(),arrested=false,resumeAt=0;

  const render=()=>rows.forEach((row,i)=>row.forEach(card=>card.style.translate=`${state[i].offset.toFixed(3)}px 0`));
  const zero=()=>{state.forEach(s=>{s.offset=0;s.velocity=0});render();window.__candidate01SyncGeometry?.()};
  const arrest=()=>{arrested=true;resumeAt=0};
  const release=()=>{resumeAt=performance.now()+560};

  document.addEventListener('mouseover',e=>{
    if(e.target.closest?.('.product'))arrest();
  },true);
  document.addEventListener('mouseout',e=>{
    const from=e.target.closest?.('.product');
    const to=e.relatedTarget?.closest?.('.product');
    if(from&&!to)release();
  },true);
  window.addEventListener('blur',()=>{arrested=true;zero()});

  const tick=now=>{
    const dt=Math.min(.05,(now-last)/1000);last=now;
    if(!reduced){
      if(resumeAt&&now>=resumeAt){arrested=false;resumeAt=0}
      state.forEach(s=>{
        if(arrested){
          s.velocity*=Math.max(0,1-dt*18);
          s.offset+=(0-s.offset)*Math.min(1,dt*28);
          if(Math.abs(s.offset)<.08){s.offset=0;s.velocity=0}
        }else{
          const target=s.cruise*s.direction;
          const delta=target-s.velocity;
          s.velocity+=Math.sign(delta)*Math.min(Math.abs(delta),8*dt);
          s.offset+=s.velocity*dt;
          if(Math.abs(s.offset)>=s.limit){s.offset=Math.sign(s.offset)*s.limit;s.direction*=-1}
        }
      });
      render();
      if(arrested&&state.every(s=>Math.abs(s.offset)<.1))window.__candidate01SyncGeometry?.();
    }
    requestAnimationFrame(tick);
  };
  render();requestAnimationFrame(tick);
  document.documentElement.dataset.livingCurrent='horizontal-two-row';
})();
</script>'''


def _page2_motion_source(doc: str) -> str:
    """Patch only Candidate 01 screen 2 back to the four-pane Codrops assembly contract."""
    replacements = (
        (
            "function side(p){return [p]}",
            "function side(p){let c=(+p.dataset.index)%4,wantRight=c<2;return products.filter(x=>wantRight?((+x.dataset.index)%4)>=2:((+x.dataset.index)%4)<2)}",
        ),
        (
            "{opacity:0,transform:'translateY(-50%) scale(.94)'},{opacity:1,transform:'translateY(-50%) scale(1)'}",
            "{opacity:0,transform:'translate3d(0,0,0) scale(.94)',offset:0},{opacity:1,transform:'translate3d(0,1.25px,0) scale(.998)',offset:.82},{opacity:1,transform:'translate3d(0,0,0) scale(1)',offset:1}",
        ),
        (
            "{opacity:1,transform:'translateY(-50%) scale(1)'},{opacity:0,transform:'translateY(-50%) scale(.94)'}",
            "{opacity:1,transform:'translate3d(0,0,0) scale(1)'},{opacity:0,transform:'translate3d(0,0,0) scale(.94)'}",
        ),
        (
            "{opacity:1,transform:'translate(0,0)'},{opacity:0,transform:`translate(${dx}vw,${dy}vw)`}",
            "{opacity:1,transform:'translate3d(0,0,0)',offset:0},{opacity:.06,transform:`translate3d(${dx*0.965}vw,${dy*0.965}vw,0)`,offset:.82},{opacity:0,transform:`translate3d(${dx}vw,${dy}vw,0)`,offset:1}",
        ),
    )
    for old, new in replacements:
        if old not in doc:
            raise RuntimeError(f"Candidate 01 Page 2 motion seam changed: {old[:60]}")
        doc = doc.replace(old, new)
    return doc


def focus_screen(screen_no, labels):
    doc = codrops_site_8x5.render(edit=False)
    if screen_no == 2:
        doc = _page2_motion_source(doc)
    doc = doc.replace('</head>', LIVING_CURRENT_STYLE + '</head>', 1)
    tail = GEOMETRY_LOCK + (PAGE2_ASSEMBLY_FIX if screen_no == 2 else '') + LIVING_CURRENT_SCRIPT
    doc = doc.replace('</body>', tail + '</body>', 1)
    srcdoc = html_lib.escape(doc, quote=True)
    return (
        '<section class="candidate-focus-screen" data-current="focus" data-layer="first" '
        'data-screen="%s">'
        '<iframe title="GridToFullPreview 8:5 %s" loading="eager" srcdoc="%s"></iframe>'
        '</section>'
    ) % (screen_no, screen_no - 1, srcdoc)


def install(current):
    motion._candidate_focus_screen = focus_screen
