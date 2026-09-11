"""Candidate 01 — original Codrops GridToFullPreview motion, transposed to horizontal 8:5 only."""
from __future__ import annotations
import html as html_lib
import design_motion_registry as motion
import codrops_site_8x5
import visual_editorial_director as ved

EDITORIAL_DIRECTOR = {**ved.contract(), "source_issue": 643}

# IMPORTANT: this screen deliberately does not call motion._install_living_current().
# The later living-current/mosaic layer changed the interaction itself. Candidate 01
# must use the already verified Codrops-derived 8:5 motion engine unchanged.
FOCUS_EMBED_STYLE = r'''<style id="candidate-01-codrops-8x5-embed">
html,body{height:100%;overflow:hidden!important}
.frame,.cats,.dore-badge{display:none!important}
.products{position:relative;height:100vh;min-height:100vh;padding:3.2vw 4vw!important}
.products__grid{height:100%;min-height:100%!important}
.products__grid .product{aspect-ratio:8/5!important}
/* The generic Candidate 01 embed used to hide this; the original focus motion needs it. */
.products__preview{display:grid!important;inset:3.2vw 4vw!important;min-height:0!important}
@media(max-width:900px){
  html,body{overflow:auto!important}
  .products{height:auto;min-height:100vh}
  .products__grid{height:auto;min-height:0!important;grid-template-columns:repeat(2,1fr)!important}
  .products__grid .product{aspect-ratio:8/5!important}
  .products__preview{display:none!important}
}
</style>'''


def focus_screen(screen_no, labels):
    # Use the existing verified horizontal 8:5 Codrops reproduction directly.
    # No drift bands, no mosaic pieces, no extra hover/read state machine.
    doc = codrops_site_8x5.render(edit=False)
    doc = doc.replace('</head>', FOCUS_EMBED_STYLE + '</head>', 1)
    srcdoc = html_lib.escape(doc, quote=True)
    return (
        '<section class="candidate-focus-screen" data-current="focus" data-layer="first" '
        'data-screen="%s" data-editorial-director="%s">'
        '<iframe title="Codrops GridToFullPreview 8:5 %s" loading="eager" srcdoc="%s"></iframe>'
        '</section>'
    ) % (screen_no, EDITORIAL_DIRECTOR['schema'], screen_no - 1, srcdoc)


def install(current):
    motion._candidate_focus_screen = focus_screen
