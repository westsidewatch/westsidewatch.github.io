"""Runtime registry for Living Water motion/design experiment pages."""
import re
import codrops_site_8x5


_LIVING_CURRENT_STYLE = r'''
<style id="living-water-8x5-current">
@keyframes lw-current-a{from{translate:0 0}to{translate:-2.8vw 0}}
@keyframes lw-current-b{from{translate:-2.2vw 0}to{translate:.4vw 0}}
@keyframes lw-current-c{from{translate:.6vw 0}to{translate:-2.4vw 0}}
@keyframes lw-current-d{from{translate:-1.8vw 0}to{translate:.8vw 0}}
.products__grid .product{will-change:translate,transform,opacity}
.products__grid .product:nth-child(1),.products__grid .product:nth-child(5){animation:lw-current-a 44s linear infinite alternate}
.products__grid .product:nth-child(2),.products__grid .product:nth-child(6){animation:lw-current-b 57s linear infinite alternate;animation-delay:-17s}
.products__grid .product:nth-child(3),.products__grid .product:nth-child(7){animation:lw-current-c 49s linear infinite alternate;animation-delay:-31s}
.products__grid .product:nth-child(4),.products__grid .product:nth-child(8){animation:lw-current-d 64s linear infinite alternate;animation-delay:-43s}
.products.living-current-focus .product{animation-play-state:paused}
@media(prefers-reduced-motion:reduce){.products__grid .product{animation:none!important}}
</style>
'''

_LIVING_CURRENT_SCRIPT = r'''
<script id="living-water-8x5-current-runtime">
(()=>{
  const stage=document.querySelector('.products');
  if(!stage||stage.dataset.livingCurrentBound==='true')return;
  stage.dataset.livingCurrentBound='true';
  let resumeTimer=0;
  const cards=[...stage.querySelectorAll('.product')];
  const hold=()=>{clearTimeout(resumeTimer);stage.classList.add('living-current-focus')};
  const release=()=>{clearTimeout(resumeTimer);resumeTimer=setTimeout(()=>{if(!stage.querySelector('.product:hover'))stage.classList.remove('living-current-focus')},560)};
  cards.forEach(card=>{card.addEventListener('mouseenter',hold);card.addEventListener('mouseleave',release)});
  document.documentElement.dataset.livingCurrent='ready';
})();
</script>
'''


def _install_living_current(html):
    """Layer the old Living Water current over the accepted Codrops focus motion."""
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

    # Add the new renderer without disturbing the accepted 8:5 focus engine.
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
