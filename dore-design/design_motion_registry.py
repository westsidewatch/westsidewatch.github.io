"""Runtime registry for Living Water motion/design experiment pages."""
import html as html_lib
import re
import codrops_site_8x5


_LIVING_CURRENT_STYLE = r'''
<style id="living-water-8x5-current">
@keyframes lw-current-a{from{transform:translateX(0)}to{transform:translateX(-12vw)}}
@keyframes lw-current-b{from{transform:translateX(-9vw)}to{transform:translateX(4vw)}}
.products__grid.living-current-field{display:block;position:relative;overflow:hidden;min-height:calc(100vh - 204px)}
.living-current-band{position:absolute;left:-12vw;display:flex;align-items:center;gap:3vw;width:124vw;will-change:transform}
.living-current-band .product{flex:1 1 0;min-width:0;margin:0;will-change:transform,opacity}
.living-current-band:nth-child(1){top:4%;animation:lw-current-a 28s linear infinite alternate}
.living-current-band:nth-child(2){top:52%;animation:lw-current-b 34s linear infinite alternate;animation-delay:-11s}
.products.living-current-focus .living-current-band{animation-play-state:running}
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
  let focusedCard=null;
  let forceLeave=false;
  const hold=card=>{
    clearTimeout(resumeTimer);
    focusedCard=card;
    stage.classList.add('living-current-focus');
  };
  const release=()=>{
    clearTimeout(resumeTimer);
    resumeTimer=setTimeout(()=>{
      if(!stage.matches(':hover'))stage.classList.remove('living-current-focus');
    },560);
  };

  stage.querySelectorAll('.product').forEach(card=>{
    card.addEventListener('mouseenter',()=>hold(card));
    card.addEventListener('mouseleave',event=>{
      if(!forceLeave && stage.matches(':hover')){
        event.stopImmediatePropagation();
        return;
      }
      if(focusedCard===card)focusedCard=null;
      release();
    },true);
  });

  stage.addEventListener('mouseleave',()=>{
    if(!focusedCard)return release();
    const card=focusedCard;
    forceLeave=true;
    card.dispatchEvent(new MouseEvent('mouseleave',{bubbles:false}));
    forceLeave=false;
    focusedCard=null;
    release();
  },true);

  document.documentElement.dataset.livingCurrent='two-full-width-bands-focus-latched';
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
</style>
'''


def _install_living_current(html):
    """Layer two full-width Living Water currents over the accepted Codrops focus motion."""
    if 'id="living-water-8x5-current"' in html:
        return html
    html = html.replace('</head>', _LIVING_CURRENT_STYLE + '</head>', 1)
    return html.replace('</body>', _LIVING_CURRENT_SCRIPT + '</body>', 1)


def _candidate_focus_screen(screen_no):
    """Reuse the locked focus runtime unchanged as one first-layer Candidate 01 viewport."""
    motion_html = _install_living_current(codrops_site_8x5.render(edit=False))
    motion_html = motion_html.replace('</head>', _CANDIDATE_FOCUS_EMBED_STYLE + '</head>', 1)
    srcdoc = html_lib.escape(motion_html, quote=True)
    return (
        '<section class="candidate-focus-screen" data-current="focus" '
        f'data-layer="first" data-screen="{screen_no}">'
        f'<iframe title="Living Water focus current {screen_no - 1}" loading="eager" srcdoc="' + srcdoc + '"></iframe>'
        '</section>'
    )


def _install_candidate_focus(current, html):
    """Candidate 01 order: home, focus one, focus two, then fixed worlds."""
    if 'data-screen="3"' in html:
        return html
    html = html.replace('</head>', _CANDIDATE_FOCUS_HOST_STYLE + '</head>', 1)
    anchor = '</section><section class="world dark">'
    focus_one = _candidate_focus_screen(2)
    focus_two = _candidate_focus_screen(3)
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
