"""Runtime registry for Living Water motion/design experiment pages."""
import re
import codrops_site_8x5


_LIVING_CURRENT_STYLE = r'''
<style id="living-water-8x5-current">
@keyframes lw-current-a{from{transform:translateX(0)}to{transform:translateX(-12vw)}}
@keyframes lw-current-b{from{transform:translateX(-9vw)}to{transform:translateX(4vw)}}
.products__grid.living-current-field{display:block;position:relative;overflow:hidden;min-height:calc(100vh - 204px)}
.living-current-band{position:absolute;left:-12vw;display:flex;align-items:center;gap:3vw;width:124vw;will-change:transform}
.living-current-band .product{flex:1 1 0;min-width:0;margin:0;will-change:transform,opacity}
.living-current-band:nth-child(1){top:4%;animation:lw-current-a 42s linear infinite alternate}
.living-current-band:nth-child(2){top:52%;animation:lw-current-b 55s linear infinite alternate;animation-delay:-17s}
.products.living-current-focus .living-current-band{animation-play-state:paused}
@media(max-width:900px){
 .products__grid.living-current-field{display:grid;grid-template-columns:repeat(2,1fr);overflow:visible}
 .living-current-band{display:contents;animation:none!important}
 .living-current-band .product{width:auto}
}
@media(prefers-reduced-motion:reduce){.living-current-band{animation:none!important}}
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

  let resumeTimer=0;
  const hold=()=>{clearTimeout(resumeTimer);stage.classList.add('living-current-focus')};
  const release=()=>{
    clearTimeout(resumeTimer);
    resumeTimer=setTimeout(()=>{
      if(!stage.querySelector('.product:hover'))stage.classList.remove('living-current-focus');
    },560);
  };
  stage.querySelectorAll('.product').forEach(card=>{
    card.addEventListener('mouseenter',hold);
    card.addEventListener('mouseleave',release);
  });
  document.documentElement.dataset.livingCurrent='two-full-width-bands-ready';
})();
</script>
'''


def _install_living_current(html):
    """Layer two full-width Living Water currents over the accepted Codrops focus motion."""
    if 'id="living-water-8x5-current"' in html:
        return html
    html = html.replace('</head>', _LIVING_CURRENT_STYLE + '</head>', 1)
    return html.replace('</body>', _LIVING_CURRENT_SCRIPT + '</body>', 1)


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
        codrops_site_8x5.PAGE_ID,
    ]
    current.multipage_wysiwyg.SUPPORTED.update(page_ids)

    # Add the current field without disturbing the accepted 8:5 focus engine.
    previous_render = current.multipage_wysiwyg.render_canvas
    def render_canvas(page_id='homepage', edit=False):
        if page_id == codrops_site_8x5.PAGE_ID:
            return _install_living_current(codrops_site_8x5.render(edit=edit))
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
