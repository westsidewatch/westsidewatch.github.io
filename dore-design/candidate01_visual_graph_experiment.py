"""Candidate 01 — original Codrops focus motion, horizontally transposed to 8:5."""
from __future__ import annotations
import html as html_lib
import design_motion_registry as motion
import codrops_site_8x5
import visual_editorial_director as ved

EDITORIAL_DIRECTOR={**ved.contract(),"source_issue":643}

STYLE=r'''<style id="candidate-01-codrops-8x5-restore">
/* Keep the original GridToFullPreview interaction. Only transpose the card ratio. */
.products__grid .product{aspect-ratio:8/5!important}
.products__preview{display:grid!important}
.product-preview{display:block!important}
@media(max-width:900px){.products__grid .product{aspect-ratio:8/5!important}}
</style>'''


def focus_screen(screen_no,labels):
    # Important: do NOT wrap with _install_living_current(). That later layer
    # introduced drift/mosaic assembly and broke the original focus motion.
    doc=codrops_site_8x5.render(edit=False)
    doc=doc.replace('</head>',motion._CANDIDATE_FOCUS_EMBED_STYLE+STYLE+'</head>',1)
    srcdoc=html_lib.escape(doc,quote=True)
    return '<section class="candidate-focus-screen" data-current="focus" data-layer="first" data-screen="%s" data-editorial-director="%s"><iframe title="Codrops 8:5 focus %s" loading="eager" srcdoc="%s"></iframe></section>'%(screen_no,EDITORIAL_DIRECTOR['schema'],screen_no-1,srcdoc)


def install(current):
    motion._candidate_focus_screen=focus_screen
