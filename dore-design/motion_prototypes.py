"""Doré Design motion prototypes retained inside the structured workspace."""

PAGE_ID = 'motion-p1-living-current'


def _page():
    # The workspace stores identity + experiment metadata only. The visual lab
    # surface is rendered by render_p1(), so no new workspace node type is needed.
    return {
        'id': PAGE_ID,
        'name': 'Motion · P1 Living Current',
        'canvas': {'w': 1440, 'h': 960},
        'nodes': [],
        'design_experiment': {
            'schema': 'dore.design-experiment.v1',
            'track': 'motion-language',
            'prototype': 'P1',
            'status': 'prototype',
            'runtime_dependencies': [],
            'hypothesis': 'Living Current basic spatial behavior does not require an animation runtime.',
            'acceptance': ['native-scroll', 'scroll-snap', 'keyboard-focus', 'reduced-motion', 'mobile-explicit'],
            'source_issue': 522,
            'source_pr': 524,
        },
    }


def install_workspace(base):
    original = base.workspace

    def workspace():
        w = original()
        if not any(p.get('id') == PAGE_ID for p in w.get('pages', [])):
            w['pages'].append(_page())
            w = base.save(w)
        return w

    base.workspace = workspace


def render_p1(edit=False):
    badge = '<div class="lab-badge">DORÉ DESIGN · MOTION LAB · P1</div>' if edit else ''
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doré Design · P1 Living Current</title><style>
*{box-sizing:border-box}html,body{margin:0;background:#f5f1e7;color:#252525;font-family:"Cormorant Garamond","Noto Serif TC",serif}body{min-height:100vh}.lab-badge{position:fixed;top:12px;left:12px;z-index:20;background:#171717;color:#eee;padding:7px 9px;font:10px ui-monospace,monospace;letter-spacing:.08em}.intro{padding:clamp(38px,7vw,92px) clamp(22px,6vw,88px) 34px}.eyebrow{font:11px ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;color:#806d35}.intro h1{font-size:clamp(42px,6vw,92px);font-weight:500;line-height:.92;margin:.2em 0}.intro p{max-width:760px;font-size:clamp(16px,1.5vw,22px);line-height:1.5}.current-shell{padding:0 0 clamp(46px,8vw,110px)}.current{display:grid;grid-auto-flow:column;grid-auto-columns:min(80vw,1120px);gap:clamp(14px,2vw,28px);overflow-x:auto;overscroll-behavior-inline:contain;scroll-snap-type:x mandatory;padding:14px clamp(22px,6vw,88px) 28px;scrollbar-width:thin}.cover{position:relative;aspect-ratio:8/5;scroll-snap-align:center;overflow:hidden;border:1px solid rgba(42,37,27,.18);background:#d8cfb8;isolation:isolate;outline:none}.cover:focus-visible{box-shadow:0 0 0 4px #a2872a}.cover::before{content:"";position:absolute;inset:0;background:linear-gradient(120deg,rgba(16,42,67,.96),rgba(16,42,67,.45) 55%,rgba(206,189,116,.15));z-index:-2}.cover:nth-child(2)::before{background:linear-gradient(135deg,#a2872a,#d2bc69 42%,#f5f1e7)}.cover:nth-child(3)::before{background:linear-gradient(140deg,#252525,#5b8fa8 62%,#d2bc69)}.cover:nth-child(4)::before{background:linear-gradient(125deg,#738a5a,#f5f1e7 58%,#102a43)}.grain{position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0 13px,rgba(255,255,255,.035) 13px 14px);mix-blend-mode:screen}.meta{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:space-between;padding:clamp(22px,4vw,58px);color:white}.cover:nth-child(2) .meta,.cover:nth-child(4) .meta{color:#252525}.meta small{font:10px ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase}.meta h2{font-size:clamp(34px,5vw,78px);font-weight:500;line-height:.9;margin:0;max-width:70%}.meta p{font-size:clamp(15px,1.5vw,21px);max-width:52%;line-height:1.35}.tail{padding:0 clamp(22px,6vw,88px);font:11px ui-monospace,monospace;color:#72684d;letter-spacing:.08em}.tail strong{color:#252525}@media(max-width:700px){.current{grid-auto-columns:84vw;padding-left:18px;padding-right:18px;scroll-padding-inline:18px}.meta{padding:22px}.meta h2{max-width:90%}.meta p{max-width:86%}.intro{padding-left:18px;padding-right:18px}}@media(prefers-reduced-motion:reduce){.current{scroll-behavior:auto}.cover{transition:none!important;animation:none!important}}
</style></head><body>'''+badge+'''<header class="intro"><div class="eyebrow">Motion Language · Prototype 01</div><h1>Living Current</h1><p>同一空間語法，不同 editorial identity。這一版只測試最基礎的河流：8:5 cover 並列、原生橫向滾動、snap、手機方向感，不用任何動畫框架。</p></header><main class="current-shell"><section class="current" aria-label="Living Current prototype"><article class="cover" tabindex="0"><span class="grain"></span><div class="meta"><small>01 · Scripture</small><h2>Watch for the Dawn</h2><p>Monumental opening field. Slow current.</p></div></article><article class="cover" tabindex="0"><span class="grain"></span><div class="meta"><small>02 · Journal</small><h2>Living Magazine</h2><p>Editorial cover with an independent identity.</p></div></article><article class="cover" tabindex="0"><span class="grain"></span><div class="meta"><small>03 · Report</small><h2>三更報導</h2><p>A faster current can share the same spatial grammar.</p></div></article><article class="cover" tabindex="0"><span class="grain"></span><div class="meta"><small>04 · Library</small><h2>黎明書局</h2><p>Still the same river; a different editorial world.</p></div></article></section><p class="tail"><strong>P1 hypothesis:</strong> native overflow + CSS scroll snap is sufficient for the foundational current.</p></main></body></html>'''


def install_editor(html):
    html = html.replace("'multiwrite-cover'])", "'multiwrite-cover','motion-p1-living-current'])")
    html = html.replace('DORÉ DESIGN 1.9 · PROMOTION PIPELINE', 'DORÉ DESIGN 2.0 · DESIGN LAB')
    return html
