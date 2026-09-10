"""Doré Design P1 — exact Codrops motion baseline.

Temporary reset requested 2026-09-10: do not reinterpret the interaction yet.
Both reference and working specimen render the upstream Codrops demo itself so the
motion baseline is pixel/behaviour identical before Living Water adaptation resumes.
Upstream: https://github.com/gwen-bo/codrops-grid-to-preview (MIT)
"""

PAGE_ID='motion-p1-living-current'
UPSTREAM_DEMO='https://tympanus.net/Tutorials/GridToFullPreview/'


def _page():
    return {
        'id':PAGE_ID,
        'name':'Motion · P1 Reading Core',
        'canvas':{'w':1440,'h':960},
        'nodes':[],
        'design_experiment':{
            'schema':'dore.design-experiment.v1',
            'track':'motion-language',
            'prototype':'P1',
            'status':'prototype',
            'source':'codrops-grid-to-preview-exact-baseline',
            'principles':['upstream-motion-unchanged','no-custom-assembly','no-content-adaptation-yet']
        }
    }


def install_workspace(base):
    original=base.workspace
    def workspace():
        w=original()
        for p in w.get('pages',[]):
            if p.get('id')==PAGE_ID:
                p.update(_page())
                return base.save(w)
        w['pages'].append(_page())
        return base.save(w)
    base.workspace=workspace


def install_editor(html):
    html=html.replace("'multiwrite-cover'])","'multiwrite-cover','motion-p1-living-current'])")
    return html.replace('DORÉ DESIGN 1.9 · PROMOTION PIPELINE','DORÉ DESIGN 2.0 · DESIGN LAB')


def render_p1(edit=False):
    badge='<div class="badge">DORÉ DESIGN · P1 · EXACT UPSTREAM BASELINE</div>' if edit else ''
    return '''<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>P1 · Exact Codrops Baseline</title>
<style>
*{box-sizing:border-box}html,body{margin:0;background:#eee;color:#111;font-family:Arial,sans-serif}.badge{position:fixed;z-index:9999;top:8px;left:8px;padding:6px 8px;background:rgba(255,255,255,.9);border:1px solid #111;font:9px ui-monospace,monospace}.stage{width:100vw;height:100svh;overflow:hidden}.stage iframe{display:block;width:100%;height:100%;border:0;background:#eee}
</style></head><body>'''+badge+'''<main class="stage"><iframe src="'''+UPSTREAM_DEMO+'''" title="Codrops Grid To Full Preview — exact upstream motion baseline" allow="fullscreen"></iframe></main></body></html>'''
