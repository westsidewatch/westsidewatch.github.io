"""Site-native 8:5 adaptation of the Codrops Grid to Full Preview interaction."""

PAGE_ID='motion-codrops-site-8x5'


def _page():
    return {
        'id': PAGE_ID,
        'name': 'Motion · Codrops 8:5 Site Lab',
        'canvas': {'w': 1440, 'h': 960},
        'nodes': [],
        'design_experiment': {
            'schema': 'dore.design-experiment.v1',
            'track': 'motion-language',
            'prototype': 'codrops-site-8x5',
            'status': 'design-candidate',
            'source': 'user-direction-2026-09-10',
            'principles': [
                'new-page-do-not-touch-old-p1',
                'source-interaction-preserved',
                '8:5-card-ratio',
                'site-native-content',
                'no-iframe',
                'gsap-grid-to-preview',
                'cross-clip-path',
                '100ms-hover-debounce',
                'reverse-on-leave'
            ],
            'acceptance': [
                'all-eight-cards-8:5',
                'four-by-two-source-geometry',
                'left-right-two-by-two-preview',
                'brand-content-instead-of-products',
                'hover-motion-matches-source-semantics',
                'usable-as-site-component'
            ]
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
    html=html.replace("'multiwrite-cover'])", "'multiwrite-cover','motion-codrops-site-8x5'])")
    return html


def render(edit=False):
    badge='<div class="dore-badge">DORÉ DESIGN · NEW PAGE · 8:5 SITE LAB</div>' if edit else ''
    items=[
        ('ONE','馬太福音第七章','/one/','21'),
        ('JOURNAL','米斯巴','/journal/','39'),
        ('DAWN LIBRARY','黎明書局','/website/dawn-library/','75'),
        ('FEATURE','看見','/journal/','93'),
        ('PRAYER','瑪拉拿','/journal/','122'),
        ('WITNESS','見證人','/journal/','164'),
        ('DIALOGUE','守望者 · 對話','/journal/','186'),
        ('LIVING WATER','活水堂西區','/church/','237'),
    ]
    cards=''.join(
        '<li class="product brand-card" data-name="%s" data-price="%s" data-index="%s"><a href="%s" class="brand-hit"><span class="brand-kicker">%s</span><strong>%s</strong></a></li>' %
        (title,i,i,href,kind,title) for i,(kind,title,href,dore) in enumerate(items)
    )
    preview_images=''.join(
        '<div class="brand-preview-art" data-id="%s"><span>%s</span><strong>%s</strong></div>'%(i,kind,title)
        for i,(kind,title,href,dore) in enumerate(items)
    )
    details='''<div class="product-preview__details"><p class="product-title">content title</p><p>WESTSIDE WATCH</p></div><div class="product-preview__inside masked-preview"></div>'''
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Living Water · 8:5 Grid to Preview</title>
<link rel="stylesheet" href="https://tympanus.net/Tutorials/GridToFullPreview/assets/index-cFK5Ucy6.css">
<style>
:root{--color-bg:#eee8da;--color-text:#252525;--color-link:#252525;--color-link-hover:#252525}
*{box-sizing:border-box}html,body{margin:0;background:#eee8da;color:#252525}.dore-badge{position:fixed;z-index:99999;top:8px;left:8px;background:#181713;color:#cebd74;padding:7px 9px;font:9px ui-monospace,monospace;letter-spacing:.12em}.frame{font-family:"Cormorant Garamond",Georgia,serif}.frame__title{font-size:16px!important}.content{font-family:"Cormorant Garamond","Noto Serif TC",Georgia,serif}.shop-categories ul li{font-size:16px}.products{min-height:100svh;height:auto;padding:7vh 3vw}.products__grid,.products__preview{padding:42px;grid-template-columns:repeat(4,minmax(0,1fr));grid-template-rows:repeat(2,auto);column-gap:3.2vw;row-gap:3.2vw;height:auto}.products__grid{align-content:center}.products__preview{top:50%;bottom:auto;transform:translateY(-50%);height:auto}.product{height:auto;aspect-ratio:8/5;contain:layout paint}.brand-card{border:1px solid rgba(37,37,37,.18);background:#d8d0bc;overflow:hidden}.brand-hit{position:absolute;inset:0!important;width:100%;height:100%;display:flex!important;flex-direction:column;justify-content:flex-end;padding:16px;background:linear-gradient(0deg,rgba(20,19,15,.82),rgba(20,19,15,.06));color:#f4efe3!important;opacity:1!important}.brand-kicker{font:9px ui-monospace,monospace;letter-spacing:.15em;color:#cebd74}.brand-hit strong{font-size:clamp(18px,2vw,30px);font-weight:400;margin-top:7px}.product-preview{height:auto;aspect-ratio:calc(16/5 + .35);overflow:visible}.product-preview__images{height:100%;background:#181713}.brand-preview-art{grid-column:1;grid-row:1;opacity:0;width:100%;height:100%;display:flex;flex-direction:column;justify-content:flex-end;padding:6%;background:radial-gradient(circle at 70% 25%,rgba(206,189,116,.24),transparent 35%),#181713;color:#eee8da}.brand-preview-art span{font:10px ui-monospace,monospace;letter-spacing:.16em;color:#cebd74}.brand-preview-art strong{font-size:clamp(34px,5vw,72px);font-weight:400;margin-top:8px}.product-preview__inside{background:#eee8da}.product-preview__details{font-family:ui-monospace,monospace;color:#252525}.product__cta{display:none!important}@media(max-width:899px){body .products,body .shop-categories{display:block}.breakpoint-disclaimer{display:none!important}.products__grid{grid-template-columns:repeat(2,1fr)}.products__preview{display:none}}
</style></head><body class="loading">'''+badge+'''<main><header class="frame"><h1 class="frame__title">Living Water · Grid to Full Preview</h1><span class="frame__back">8:5 SITE ADAPTATION</span><span class="frame__archive">WESTSIDE WATCH</span><span class="frame__github">ONE · JOURNAL · LIBRARY</span><nav class="frame__tags"><span>#8:5</span><span>#GSAP</span><span>#SITE</span></nav></header><div class="content"><nav class="shop-categories"><ul><li class="--active">All <sup>8</sup></li><li>ONE</li><li>Journal</li><li>Library</li><li>Living Water</li></ul></nav><p class="breakpoint-disclaimer">Desktop motion prototype</p><div class="products"><ul class="products__grid">'''+cards+'''</ul><div class="products__preview"><div class="product-preview --left"><div class="product-preview__images">'''+preview_images+'''</div>'''+details+'''</div><div class="product-preview --right"><div class="product-preview__images">'''+preview_images+'''</div>'''+details+'''</div></div></div></div></main>
<script type="module" src="https://tympanus.net/Tutorials/GridToFullPreview/assets/index-B9DYJh5Z.js"></script>
<script>window.addEventListener('load',function(){document.body.classList.remove('loading')})</script></body></html>'''
