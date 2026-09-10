"""Doré Design P1 — 8:5 Codrops adaptation restored in Design."""
PAGE_ID='motion-p1-living-current'
UPSTREAM='https://cdn.jsdelivr.net/gh/gwen-bo/codrops-grid-to-preview@1027ebb60e38cbb4e7ee7d10ef045b5627a035c2/dist'

def _page():
    return {'id':PAGE_ID,'name':'Motion · P1 Codrops 8:5','canvas':{'w':1440,'h':960},'nodes':[],'design_experiment':{'schema':'dore.design-experiment.v1','track':'motion-language','prototype':'P1','status':'prototype','source':'codrops-grid-to-preview-8x5-adaptation','principles':['4x2-grid','8x5-cards','two-preview-halves','hover-100ms','gsap-power2-inout','clip-path-cross','reverse-on-mouseleave']}}

def install_workspace(base):
    original=base.workspace
    def workspace():
        w=original()
        for p in w.get('pages',[]):
            if p.get('id')==PAGE_ID:p.update(_page());return base.save(w)
        w['pages'].append(_page());return base.save(w)
    base.workspace=workspace

def install_editor(html):
    html=html.replace("'multiwrite-cover'])","'multiwrite-cover','motion-p1-living-current'])")
    return html.replace('DORÉ DESIGN 1.9 · PROMOTION PIPELINE','DORÉ DESIGN 2.0 · DESIGN LAB')

def render_p1(edit=False):
    b=UPSTREAM+'/assets/products/'
    data=[('Candle holder','25',1),('Cow vase','40',2),('Chrome and blue book shelf','200',3),('Wooden sidetable with smoke glass detail','120',4),('Yellow armchair','220',5),('Wooden cabinet with fluted glass','200',6),('Orange clock','30',7),('Red chair with chrome legs','50',8)]
    products=''.join('<li class="product" data-name="%s" data-price="%s" data-index="%d"><div class="product__cta"><p>Add to cart</p></div><img class="loading" src="%sproduct-%d.webp" alt="product-image"></li>'%(name,price,i,b,n) for i,(name,price,n) in enumerate(data))
    def imgs(ids):
        s=''
        for i in ids:
            n=i+1
            s+='<img data-id="%d" src="%sproduct-%d.webp" alt="product-image"><img data-id="%d" src="%sproduct-%d-detail-1.webp" alt="product-image"><img data-id="%d" src="%sproduct-%d-detail-2.webp" alt="product-image">'%(i,b,n,i,b,n,i,b,n)
        return s
    preview=lambda side,ids:'<div class="product-preview --%s"><div class="product-preview__images">%s</div><div class="product-preview__details"><p class="product-title">product title</p><p>€ <span class="product-price">0</span></p></div><div class="product-preview__inside masked-preview"></div></div>'%(side,imgs(ids))
    return '''<!DOCTYPE html><html lang="en" class="no-js"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Codrops 8:5 · DORÉ Design</title><link rel="stylesheet" href="'''+UPSTREAM+'''/assets/index-cFK5Ucy6.css"><style>
/* DORÉ Design 8:5 adaptation: keep the upstream interaction engine; change only card geometry. */
.products__grid{grid-template-rows:repeat(2,minmax(0,1fr))!important}.product{aspect-ratio:8/5!important;min-height:0!important}.product img{width:100%!important;height:100%!important;object-fit:cover!important}.products{align-items:start!important}.products__preview{height:100%!important}.product-preview{height:100%!important}.product-preview__images,.product-preview__inside{height:100%!important}.product-preview__images img{width:100%!important;height:100%!important;object-fit:cover!important}
</style><script>document.documentElement.className='js'</script><script type="module" crossorigin src="'''+UPSTREAM+'''/assets/index-B9DYJh5Z.js"></script></head><body class="loading"><main><header class="frame"><h1 class="frame__title">Grid to Full Preview · 8:5</h1><span class="frame__back">DORÉ DESIGN</span><nav class="frame__tags"><a>#8:5</a><a>#hover</a><a>#gsap</a></nav></header><div class="content"><nav class="shop-categories"><ul><li class="--active">All <sup>8</sup></li></ul></nav><div class="products"><ul class="products__grid">'''+products+'''</ul><div class="products__preview">'''+preview('left',[2,3,6,7])+preview('right',[0,1,4,5])+'''</div></div></div></main></body></html>'''
