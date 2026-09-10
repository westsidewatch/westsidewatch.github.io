"""Doré Design P1 — upstream Codrops GridToFullPreview source baseline."""
PAGE_ID='motion-p1-living-current'
UPSTREAM='https://cdn.jsdelivr.net/gh/gwen-bo/codrops-grid-to-preview@1027ebb60e38cbb4e7ee7d10ef045b5627a035c2/dist'

def _page():
    return {'id':PAGE_ID,'name':'Motion · P1 Codrops Baseline','canvas':{'w':1440,'h':960},'nodes':[],'design_experiment':{'schema':'dore.design-experiment.v1','track':'motion-language','prototype':'P1','status':'baseline','source':'gwen-bo/codrops-grid-to-preview@1027ebb','principles':['upstream-source-direct','no-custom-motion','no-content-substitution']}}

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
    products=''.join('<li class="product" data-name="%s" data-price="%s" data-index="%d"><div class="product__cta"><p>Add to cart</p></div><img class="loading" src="%sproduct-%d.webp" alt="product-image" width="1024" height="1536"></li>'%x for x in [
      ('Candle holder','25',0,b,1),('Cow vase','40',1,b,2),('Chrome and blue book shelf','200',2,b,3),('Wooden sidetable with smoke glass detail','120',3,b,4),('Yellow armchair','220',4,b,5),('Wooden cabinet with fluted glass','200',5,b,6),('Orange clock','30',6,b,7),('Red chair with chrome legs','50',7,b,8)])
    def imgs(ids):
        s=''
        for i in ids:
            n=i+1
            s+='<img data-id="%d" src="%sproduct-%d.webp" alt="product-image" width="1024" height="1536"><img data-id="%d" src="%sproduct-%d-detail-1.webp" alt="product-image" width="1024" height="1536"><img data-id="%d" src="%sproduct-%d-detail-2.webp" alt="product-image" width="1024" height="1536">'%(i,b,n,i,b,n,i,b,n)
        return s
    preview=lambda side,ids:'<div class="product-preview --%s"><div class="product-preview__images">%s</div><div class="product-preview__details"><p class="product-title">product title</p><p>€ <span class="product-price">0</span></p></div><div class="product-preview__inside masked-preview"></div></div>'%(side,imgs(ids))
    return '''<!DOCTYPE html><html lang="en" class="no-js"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GridToFullPreview | Codrops</title><meta name="author" content="Gwen Bogaert for Codrops"><link rel="stylesheet" href="'''+UPSTREAM+'''/assets/index-cFK5Ucy6.css"><script>document.documentElement.className='js'</script><script type="module" crossorigin src="'''+UPSTREAM+'''/assets/index-B9DYJh5Z.js"></script></head><body class="loading"><main><header class="frame"><h1 class="frame__title">Grid to Full Preview</h1><a class="frame__back" href="https://tympanus.net/codrops/?p=93410">Article</a><a class="frame__archive" href="https://tympanus.net/codrops/demos/">All demos</a><a class="frame__github" href="https://github.com/gwen-bo/codrops-grid-to-preview">GitHub</a><nav class="frame__tags"><a>#grid</a><a>#hover</a><a>#gsap</a></nav></header><div class="content"><nav class="shop-categories"><ul><li class="--active">All <sup>8</sup></li><li>Chairs <sup>2</sup></li><li>Tables <sup>1</sup></li><li>Decoration <sup>3</sup></li><li>Cabinets <sup>2</sup></li></ul></nav><p class="breakpoint-disclaimer">🖥️ Seems like this demo best suited for desktop.</p><div class="products"><ul class="products__grid">'''+products+'''</ul><div class="products__preview">'''+preview('left',[2,3,6,7])+preview('right',[0,1,4,5])+'''</div></div></div></main></body></html>'''
