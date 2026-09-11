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

    // The preview layer is the exact outer rectangle of the 4x2 card tracks,
    // not the tall .products viewport. This is the Codrops overlay invariant.
    layer.style.inset='auto';
    layer.style.left=`${minX-rr.left}px`;
    layer.style.top=`${minY-rr.top}px`;
    layer.style.width=`${maxX-minX}px`;
    layer.style.height=`${maxY-minY}px`;
    layer.style.minHeight='0';

    // Each preview overlays exactly one 2-column x 2-row group.
    // With every source card at 8:5, that group is also 8:5.
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

  const settle=()=>requestAnimationFrame(()=>requestAnimationFrame(()=>{
    sync();
    // Let the original Codrops engine recalculate its scale factors
    // against the corrected overlay rectangle.
    window.dispatchEvent(new Event('resize'));
  }));

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',settle,{once:true});
  else settle();
  window.addEventListener('resize',sync,{passive:true});
})();
</script>'''


def focus_screen(screen_no, labels):
    doc = codrops_site_8x5.render(edit=False)
    doc = doc.replace('</body>', GEOMETRY_LOCK + '</body>', 1)
    srcdoc = html_lib.escape(doc, quote=True)
    return (
        '<section class="candidate-focus-screen" data-current="focus" data-layer="first" '
        'data-screen="%s">'
        '<iframe title="GridToFullPreview 8:5 %s" loading="eager" srcdoc="%s"></iframe>'
        '</section>'
    ) % (screen_no, screen_no - 1, srcdoc)


def install(current):
    motion._candidate_focus_screen = focus_screen
