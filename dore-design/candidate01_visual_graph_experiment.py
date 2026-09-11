"""Candidate 01 — 4W editorial data with original Codrops GridToFullPreview motion."""
from __future__ import annotations
import html as html_lib, json
import design_motion_registry as motion
import codrops_site_8x5
import visual_editorial_director as ved
import sitewide_editorial_candidates as sitewide

EDITORIAL_DIRECTOR={**ved.contract(),"source_issue":643}
SITEWIDE=sitewide.load()
_POOL=SITEWIDE.candidates


def _rows():
    selected=ved.select(_POOL,per_w=4)
    rows={}
    for w,pairs in selected.items():
        rows[w]=[]
        for c,d in pairs:
            rows[w].append({
                "id":c.id,"title":c.title,"source":c.source,"deck":c.deck,
                "image":c.image,"world":c.world,"weight":d.weight,"shape":d.shape,
                "affinity":d.affinity,"brightness":d.brightness,
                "editorial_score":d.editorial_score,"editorial_reason":d.reason,
                "provenance":SITEWIDE.provenance.get(c.id,{}),
            })
    return rows

ROWS=_rows()

STYLE=r'''<style id="candidate-01-editorial-contract">
.products__grid .product{aspect-ratio:8/5!important}
</style>'''


def script(row_names):
    data=json.dumps({n:ROWS[n] for n in row_names},ensure_ascii=False)
    director=json.dumps(EDITORIAL_DIRECTOR,ensure_ascii=False)
    names=json.dumps(list(row_names))
    return f'''<script id="candidate-01-editorial-contract-runtime">(()=>{{const DIRECTOR={director},ROWS={data},names={names};document.documentElement.dataset.visualEditorialDirector=DIRECTOR.schema;document.documentElement.dataset.editorialRows=names.join(',');window.__DORE_CANDIDATE01_ROWS__=ROWS;window.addEventListener('dore-world-enter',()=>{{}});}})();</script>'''

FOCUS_EMBED_STYLE=r'''<style id="candidate-01-codrops-8x5-embed">
html,body{height:100%;overflow:hidden!important}
.frame,.cats,.dore-badge{display:none!important}
.products{position:relative;height:100vh;min-height:100vh;padding:3.2vw 4vw!important}
.products__grid{height:100%;min-height:100%!important}
.products__grid .product{aspect-ratio:8/5!important}
.products__preview{display:grid!important;inset:3.2vw 4vw!important;min-height:0!important}
@media(max-width:900px){html,body{overflow:auto!important}.products{height:auto;min-height:100vh}.products__grid{height:auto;min-height:0!important;grid-template-columns:repeat(2,1fr)!important}.products__grid .product{aspect-ratio:8/5!important}.products__preview{display:none!important}}
</style>'''


def focus_screen(screen_no,labels):
    row_names=("WATCH","WITNESS") if screen_no==2 else ("WALK","WORSHIP")
    doc=codrops_site_8x5.render(edit=False)
    doc=doc.replace('</head>',STYLE+FOCUS_EMBED_STYLE+'</head>',1)
    doc=doc.replace('</body>',script(row_names)+'</body>',1)
    srcdoc=html_lib.escape(doc,quote=True)
    return '<section class="candidate-focus-screen" data-current="focus" data-layer="first" data-screen="%s" data-editorial-director="%s"><iframe title="4W Living Editorial River %s" loading="eager" srcdoc="%s"></iframe></section>'%(screen_no,EDITORIAL_DIRECTOR['schema'],screen_no-1,srcdoc)


def install(current):
    motion._candidate_focus_screen=focus_screen
