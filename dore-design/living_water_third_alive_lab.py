"""DORÉ Design — Third Alive / 4W weighted-length experiment.

Standalone Design experiment only. It is deliberately NOT inserted into
Candidate 01 or the locked first-layer homepage structure.
"""

PAGE_ID = "living-water-third-alive-lab"
PAGE_TITLE = "Living Water · Third Alive Lab"

MOVEMENTS = (
    ("第一樂章", "WATCH", "守望", (1, 2, 1, 3, 1)),
    ("第二樂章", "WITNESS", "見證", (2, 1, 1, 2, 3)),
    ("第三樂章", "WALK", "同行", (1, 3, 2, 1, 2)),
    ("第四樂章", "WORSHIP", "敬拜", (3, 1, 2, 2, 1)),
)


def page():
    return {"id":PAGE_ID,"name":PAGE_TITLE,"canvas":{"w":1440,"h":960},"nodes":[],"design_experiment":{"schema":"dore.design-experiment.v1","track":"living-water-third-alive","status":"motion-lab","scope":"standalone","concept":"third-alive-4w-weighted-length-navigation","candidate_01_untouched":True,"movements":["WATCH","WITNESS","WALK","WORSHIP"],"atomic_unit":"5:8","weights":[1,2,3]}}


def install_workspace(base):
    original=base.workspace
    def workspace():
        w=original()
        if not any(p.get('id')==PAGE_ID for p in w.get('pages',[])):
            w['pages'].append(page());w=base.save(w)
        return w
    base.workspace=workspace


def install_editor(html):
    """Register Third Alive directly in the editor's supported Set.

    Do not depend on the order or presence of other Living Water labs.
    """
    if f"supported.add('{PAGE_ID}')" in html:
        return html
    marker="const qs=new URLSearchParams(location.search);"
    injection=f"supported.add('{PAGE_ID}');"+marker
    return html.replace(marker,injection,1) if marker in html else html


def _card(movement,index,span):
    return (f'<article class="alive-card span-{span}" tabindex="0" data-movement="{movement}" data-weight="{span}" aria-label="{movement} weighted content {index+1}">'+'<div class="engraving-lines"></div>'+f'<span class="weight-mark">{span}×5:8</span></article>')


def render(edit=False):
    rows=[]
    for no,(movement,word,zh,spans) in enumerate(MOVEMENTS,start=1):
        cards=''.join(_card(word,i,span) for i,span in enumerate(spans))
        rows.append(f'<section class="current current-{no}" data-w="{word}"><header class="movement-mark"><span>{movement}</span> <b>{word}</b><i>{zh}</i></header><div class="current-track">{cards}{cards}</div></section>')
    badge='<div class="lab-badge">DORÉ DESIGN · THIRD ALIVE · 4W</div>' if edit else ''
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{PAGE_TITLE}</title><style>
:root{{--gold:#CEBD74;--ink:#252525;--stone:#d8d1c3;--night:#171817}}*{{box-sizing:border-box}}html,body{{margin:0;min-height:100%;background:var(--night);color:#eee;font-family:Georgia,"Noto Serif TC",serif;overflow-x:hidden}}.stage{{min-height:100vh;padding:5vh 0 6vh;background:radial-gradient(circle at 50% 42%,#292a27 0,#1d1e1c 48%,#121311 100%)}}.lab-badge{{position:fixed;z-index:99;top:12px;left:12px;padding:7px 10px;background:#f4eddc;color:#111;font:10px ui-monospace,monospace;letter-spacing:.12em}}.lab-note{{padding:0 4vw 2.4vh;color:#aaa;font:11px/1.4 Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase}}.current{{position:relative;margin:0 0 1.7vh;overflow:hidden;border-top:1px solid rgba(206,189,116,.14);border-bottom:1px solid rgba(206,189,116,.08);padding:2.6vh 0 2.2vh}}.movement-mark{{position:relative;z-index:3;margin:0 4vw 1.2vh;color:rgba(206,189,116,.72);font:11px/1.2 Arial,sans-serif;letter-spacing:.16em}}.movement-mark b{{font-weight:500;margin-left:.55em;letter-spacing:.22em}}.movement-mark i{{font-style:normal;margin-left:.8em;opacity:.58;letter-spacing:.08em}}.current-track{{display:flex;align-items:stretch;gap:12px;width:max-content;padding:0 12px;animation:flow 38s linear infinite}}.current-2 .current-track{{animation-duration:46s;animation-direction:reverse}}.current-3 .current-track{{animation-duration:52s}}.current-4 .current-track{{animation-duration:43s;animation-direction:reverse}}.alive-card{{position:relative;flex:0 0 auto;height:clamp(108px,15vw,190px);width:calc(clamp(108px,15vw,190px)*.625);overflow:hidden;border:1px solid rgba(206,189,116,.18);background:linear-gradient(145deg,#4a4840,#252622 62%,#191a18);transition:transform .35s ease,border-color .35s ease}}.alive-card.span-2{{width:calc(clamp(108px,15vw,190px)*1.25 + 12px)}}.alive-card.span-3{{width:calc(clamp(108px,15vw,190px)*1.875 + 24px)}}.alive-card:hover,.alive-card:focus{{outline:none;transform:translateY(-4px);border-color:rgba(206,189,116,.58)}}.engraving-lines{{position:absolute;inset:0;opacity:.34;background:repeating-linear-gradient(164deg,transparent 0 7px,rgba(225,216,190,.22) 8px 9px),radial-gradient(ellipse at 70% 40%,rgba(206,189,116,.16),transparent 48%)}}.weight-mark{{position:absolute;right:9px;bottom:7px;color:rgba(206,189,116,.42);font:9px/1 Arial,sans-serif;letter-spacing:.1em}}@keyframes flow{{to{{transform:translateX(-50%)}}}}@media(max-width:720px){{.stage{{padding-top:3vh}}.current{{padding-top:2vh}}.alive-card{{height:132px;width:82.5px}}.alive-card.span-2{{width:177px}}.alive-card.span-3{{width:271.5px}}}}@media(prefers-reduced-motion:reduce){{.current-track{{animation:none}}}}
</style></head><body>{badge}<main class="stage"><div class="lab-note">Independent Design experiment · Third Alive · weighted 5:8 navigation</div>{''.join(rows)}</main></body></html>'''
