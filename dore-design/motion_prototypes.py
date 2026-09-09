"""Doré Design motion prototypes retained inside the structured workspace."""

PAGE_ID = 'motion-p1-living-current'


def _page():
    return {
        'id': PAGE_ID,
        'name': 'Motion · P1 Light Comparison',
        'canvas': {'w': 1440, 'h': 960},
        'nodes': [],
        'design_experiment': {
            'schema': 'dore.design-experiment.v1',
            'track': 'motion-language',
            'prototype': 'P1',
            'status': 'prototype',
            'runtime_dependencies': [
                'martinRenou/threejs-caustics',
                'codrops/RainEffect',
                'Ameobea/three-good-godrays',
                'ReactBits/LightRays',
            ],
            'hypothesis': 'Compare mature light-motion references on the exact same Living Water C04 second page before choosing a production light language.',
            'acceptance': ['same-c04-base', 'four-live-references', 'independent-toggle', 'reduced-motion', 'no-production-dependency'],
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
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doré Design · P1 Light Comparison</title><style>
*{box-sizing:border-box}html,body{margin:0;background:#11110f;color:#f1ede2;font-family:"Cormorant Garamond","Noto Serif TC",serif}body{min-height:100vh}.lab-badge{position:fixed;top:12px;left:12px;z-index:100;background:#171717;color:#eee;padding:7px 9px;font:10px ui-monospace,monospace;letter-spacing:.08em}.intro{padding:clamp(34px,5vw,74px) clamp(20px,5vw,72px) 28px;border-bottom:1px solid rgba(206,189,116,.22)}.eyebrow{font:10px ui-monospace,monospace;letter-spacing:.18em;color:#cebd74}.intro h1{font-size:clamp(38px,5vw,74px);font-weight:400;line-height:.94;margin:.22em 0}.intro p{max-width:960px;font-size:clamp(15px,1.35vw,20px);line-height:1.5;color:#c9c3b5}.legend{display:flex;gap:14px;flex-wrap:wrap;margin-top:18px;font:10px ui-monospace,monospace;letter-spacing:.08em;color:#8f8878}.legend span{padding:7px 9px;border:1px solid rgba(206,189,116,.22)}.experiments{padding:28px clamp(14px,3vw,40px) 70px;display:grid;gap:34px}.experiment{border:1px solid rgba(206,189,116,.22);background:#171714;overflow:hidden}.exp-head{display:grid;grid-template-columns:auto 1fr auto;gap:18px;align-items:center;padding:12px 14px;border-bottom:1px solid rgba(206,189,116,.16);font:10px ui-monospace,monospace;letter-spacing:.08em}.exp-id{color:#cebd74}.exp-title{font-family:"Cormorant Garamond","Noto Serif TC",serif;font-size:20px;letter-spacing:0}.exp-source{color:#8f8878;text-align:right}.stage{height:min(76vh,760px);min-height:520px;position:relative;overflow:hidden;background:#171714}.c04-frame,.fx-frame{position:absolute;border:0;pointer-events:none}.c04-frame{z-index:1;left:0;top:-100vh;width:100%;height:380vh;background:#171714}.fx-frame{z-index:3;inset:0;width:100%;height:100%;opacity:.48;mix-blend-mode:screen;filter:grayscale(1) sepia(.35) saturate(.8);background:transparent}.experiment[data-kind="caustics"] .fx-frame{opacity:.52;mix-blend-mode:screen}.experiment[data-kind="rain"] .fx-frame{opacity:.34;mix-blend-mode:screen}.experiment[data-kind="godrays"] .fx-frame{opacity:.46;mix-blend-mode:screen}.experiment[data-kind="lightrays"] .fx-frame{opacity:.42;mix-blend-mode:screen}.veil{position:absolute;z-index:4;inset:0;pointer-events:none;background:linear-gradient(90deg,rgba(17,17,14,.14),transparent 25%,transparent 75%,rgba(17,17,14,.14))}.controls{display:flex;gap:10px;align-items:center;padding:10px 14px;border-top:1px solid rgba(206,189,116,.14);font:10px ui-monospace,monospace;color:#9b9484}.controls button{appearance:none;border:1px solid rgba(206,189,116,.38);background:#171714;color:#ddd5c1;padding:7px 10px;font:10px ui-monospace,monospace;letter-spacing:.06em;cursor:pointer}.controls button.on{background:#cebd74;color:#171714}.controls a{margin-left:auto;color:#cebd74;text-decoration:none}.note{padding:0 14px 14px;color:#a8a092;font-size:14px;line-height:1.45}.raw{display:none;height:430px;border-top:1px solid rgba(206,189,116,.12)}.raw.open{display:block}.raw iframe{width:100%;height:100%;border:0}.foot{padding:0 clamp(20px,5vw,72px) 70px;color:#8e8777;font:11px ui-monospace,monospace;line-height:1.6}.foot strong{color:#cebd74}@media(max-width:760px){.exp-head{grid-template-columns:auto 1fr}.exp-source{grid-column:1/-1;text-align:left}.stage{height:68vh;min-height:500px}.fx-frame{opacity:.38}.controls{flex-wrap:wrap}.controls a{width:100%;margin-left:0}.intro{padding-left:18px;padding-right:18px}.experiments{padding-left:10px;padding-right:10px}}@media(prefers-reduced-motion:reduce){.fx-frame{display:none}.controls .toggle-fx{display:none}}
</style></head><body>'''+badge+'''<header class="intro"><div class="eyebrow">MOTION LAB · P1 · SAME PAGE / DIFFERENT LIGHT ENGINE</div><h1>Living Water · Light Motion Comparison</h1><p>四個實驗全部使用同一個 Living Water Candidate 04 第二頁作底層。上層只替換成熟的公開 light / water motion reference。此頁只用於視覺比較，不把任何第三方 runtime 帶入正式 C04。</p><div class="legend"><span>底層：C04 page 2</span><span>上層：成熟 live reference</span><span>Toggle 可單獨關閉 effect</span><span>Raw 可看原案例</span></div></header><main class="experiments">
<section class="experiment" data-kind="caustics"><div class="exp-head"><span class="exp-id">A</span><span class="exp-title">ThreeJS Caustics</span><span class="exp-source">martinRenou/threejs-caustics · BSD-3-Clause</span></div><div class="stage"><iframe class="c04-frame" src="/editor-canvas?page=living-water-candidate-04" title="C04 second page base"></iframe><iframe class="fx-frame" src="https://martinrenou.github.io/threejs-caustics/" title="ThreeJS Caustics live effect"></iframe><div class="veil"></div></div><div class="controls"><button class="toggle-fx on" type="button">Effect on</button><button class="toggle-raw" type="button">Raw reference</button><a href="https://martinrenou.github.io/threejs-caustics/" target="_blank" rel="noreferrer">open source demo ↗</a></div><div class="raw"><iframe src="https://martinrenou.github.io/threejs-caustics/" title="ThreeJS Caustics raw reference"></iframe></div><div class="note">比較重點：光是否真的像被水流折射，而不是一層裝飾性 glow。</div></section>
<section class="experiment" data-kind="rain"><div class="exp-head"><span class="exp-id">B</span><span class="exp-title">Codrops Rain / Water Refraction</span><span class="exp-source">codrops/RainEffect · Lucas Bebber</span></div><div class="stage"><iframe class="c04-frame" src="/editor-canvas?page=living-water-candidate-04" title="C04 second page base"></iframe><iframe class="fx-frame" src="https://tympanus.net/Development/RainEffect/" title="Codrops Rain Effect live reference"></iframe><div class="veil"></div></div><div class="controls"><button class="toggle-fx on" type="button">Effect on</button><button class="toggle-raw" type="button">Raw reference</button><a href="https://tympanus.net/Development/RainEffect/" target="_blank" rel="noreferrer">open source demo ↗</a></div><div class="raw"><iframe src="https://tympanus.net/Development/RainEffect/" title="Codrops Rain raw reference"></iframe></div><div class="note">比較重點：水的折射語法能否讓 Doré 原作「活起來」，以及是否過度像玻璃窗雨滴。</div></section>
<section class="experiment" data-kind="godrays"><div class="exp-head"><span class="exp-id">C</span><span class="exp-title">Screen-space God Rays</span><span class="exp-source">Ameobea/three-good-godrays + pmndrs/postprocessing</span></div><div class="stage"><iframe class="c04-frame" src="/editor-canvas?page=living-water-candidate-04" title="C04 second page base"></iframe><iframe class="fx-frame" src="https://three-good-godrays.ameo.design/" title="three-good-godrays live reference"></iframe><div class="veil"></div></div><div class="controls"><button class="toggle-fx on" type="button">Effect on</button><button class="toggle-raw" type="button">Raw reference</button><a href="https://three-good-godrays.ameo.design/" target="_blank" rel="noreferrer">open source demo ↗</a></div><div class="raw"><iframe src="https://three-good-godrays.ameo.design/" title="God Rays raw reference"></iframe></div><div class="note">比較重點：方向性晨光是否成立，還是會把第二頁推向遊戲 / 電影特效。</div></section>
<section class="experiment" data-kind="lightrays"><div class="exp-head"><span class="exp-id">D</span><span class="exp-title">React Bits LightRays</span><span class="exp-source">React Bits · LightRays</span></div><div class="stage"><iframe class="c04-frame" src="/editor-canvas?page=living-water-candidate-04" title="C04 second page base"></iframe><iframe class="fx-frame" src="https://www.reactbits.dev/backgrounds/light-rays" title="React Bits Light Rays live reference"></iframe><div class="veil"></div></div><div class="controls"><button class="toggle-fx on" type="button">Effect on</button><button class="toggle-raw" type="button">Raw reference</button><a href="https://www.reactbits.dev/backgrounds/light-rays" target="_blank" rel="noreferrer">open source demo ↗</a></div><div class="raw"><iframe src="https://www.reactbits.dev/backgrounds/light-rays" title="React Bits Light Rays raw reference"></iframe></div><div class="note">比較重點：現成 light-rays 動態語法是否能帶來「黎明」而不落入通用 AI landing-page 背景。</div></section>
</main><div class="foot"><strong>Rule:</strong> P1 只比較現成成熟動效。選中之前不把這四個第三方 runtime 寫進 Living Water production。</div><script>(function(){document.querySelectorAll('.experiment').forEach(function(exp){var fx=exp.querySelector('.fx-frame'),t=exp.querySelector('.toggle-fx'),r=exp.querySelector('.toggle-raw'),raw=exp.querySelector('.raw');t.addEventListener('click',function(){var on=fx.style.display!=='none';fx.style.display=on?'none':'block';t.textContent=on?'Effect off':'Effect on';t.classList.toggle('on',!on)});r.addEventListener('click',function(){var open=raw.classList.toggle('open');r.textContent=open?'Hide raw':'Raw reference'})})})();</script></body></html>'''


def install_editor(html):
    html = html.replace("'multiwrite-cover'])", "'multiwrite-cover','motion-p1-living-current'])")
    html = html.replace('DORÉ DESIGN 1.9 · PROMOTION PIPELINE', 'DORÉ DESIGN 2.0 · DESIGN LAB')
    return html
