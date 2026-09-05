"""Phase 3 Pages / Canvas / Properties shell augmentation."""
CSS='''<style id="d2-phase3-shell">:root{--d2-left:264px;--d2-right:300px}.work{grid-template-columns:var(--d2-left) minmax(0,1fr) var(--d2-right)!important}.side:first-child{box-shadow:inset -1px 0 #b5b0a4}.right{box-shadow:inset 1px 0 #b5b0a4}.canvaswrap{position:relative}.d2-phase{position:absolute;left:26px;top:26px;z-index:4;padding:5px 8px;background:#171717;color:#d0bd78;font-size:9px;letter-spacing:.08em;pointer-events:none}.layer{display:grid;grid-template-columns:14px 1fr;gap:5px;align-items:center}.layer:before{content:'◆';font-size:7px;opacity:.45}.layer.active{outline:1px solid #8c6818;background:#e8dfc8}.right h3{position:sticky;top:-12px;background:#f3f3ef;padding:12px 0 6px;z-index:2}</style>'''
BADGE='<span class="d2-phase">DORÉ DESIGN 2.0 · PHASE 3 · CANONICAL CANVAS</span>'

def augment(html):
    if 'class="work"' not in html or 'class="canvaswrap"' not in html:raise RuntimeError('phase3_shell_marker_missing')
    html=html.replace('</head>',CSS+'</head>',1)
    html=html.replace('<main class="canvaswrap">','<main class="canvaswrap">'+BADGE,1)
    return html.replace('DORÉ DESIGN 1.9 · PROMOTION PIPELINE','DORÉ DESIGN 2.0 · DIRECT-MANIPULATION WORKBENCH',1)
