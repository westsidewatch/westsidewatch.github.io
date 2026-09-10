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
            'source': 'Codrops GridToFullPreview / Gwen Bogaert',
            'principles': [
                'new-page-do-not-touch-old-p1',
                'source-dom-shape-preserved',
                'eight-products-four-by-two',
                '8:5-card-ratio-only',
                'two-opposite-side-previews',
                '100ms-hover-debounce',
                'reverse-on-leave',
                'cross-mask-reveal',
                'self-contained-motion-no-remote-js'
            ],
            'acceptance': [
                'all-eight-cards-8:5',
                'hover-any-card-triggers-motion',
                'cards-shift-inward-2.5vw',
                'opposite-preview-reveals',
                'preview-gallery-cycles-500ms',
                'mouseleave-restores-grid',
                'no-iframe',
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
    return html


def render(edit=False):
    badge='<div class="dore-badge">DORÉ DESIGN · CODROPS 8:5 · MOTION</div>' if edit else ''
    base='https://tympanus.net/Tutorials/GridToFullPreview/assets/products/'
    names=['Candle holder','Cow vase','Chrome and blue book shelf','Wooden sidetable','Yellow armchair','Wooden cabinet','Orange clock','Red chair']
    products=[]
    previews=[]
    for i,name in enumerate(names,1):
        idx=i-1
        products.append(f'''<li class="product" data-name="{name}" data-price="{[25,40,200,120,220,200,30,50][idx]}" data-index="{idx}">
          <div class="product__cta"><p>Open</p></div>
          <img src="{base}product-{i}.webp" alt="{name}">
        </li>''')
        previews.append(''.join([
            f'<img data-id="{idx}" src="{base}product-{i}.webp" alt="{name}">',
            f'<img data-id="{idx}" src="{base}product-{i}-detail-1.webp" alt="{name}">',
            f'<img data-id="{idx}" src="{base}product-{i}-detail-2.webp" alt="{name}">',
        ]))
    products=''.join(products)
    previews=''.join(previews)
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Codrops 8:5 Motion Lab</title>
<style>
*{{box-sizing:border-box}}html,body{{margin:0;min-height:100%;background:#eee8da;color:#252525;font-family:Arial,sans-serif}}body{{overflow-x:hidden}}.dore-badge{{position:fixed;z-index:99;top:8px;left:8px;background:#181713;color:#cebd74;padding:7px 9px;font:9px ui-monospace,monospace;letter-spacing:.12em}}.frame{{height:86px;display:grid;grid-template-columns:1fr auto auto auto;gap:26px;align-items:center;padding:0 4vw;font:11px ui-monospace,monospace}}.frame h1{{font:22px Georgia,serif;font-weight:400;margin:0}}.cats{{display:flex;justify-content:center;gap:20px;padding:4px 0 16px;color:#8d8677;font:13px Georgia,serif}}.cats b{{color:#252525;font-weight:400}}.products{{position:relative;min-height:calc(100vh - 120px);padding:48px}}.products__grid,.products__preview{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-template-rows:repeat(2,auto);gap:5vw;align-content:center}}.products__grid{{list-style:none;margin:0;padding:0;min-height:calc(100vh - 216px)}}.product{{position:relative;aspect-ratio:8/5;overflow:hidden;background:#d7cfbd;transform:translate3d(0,0,0);will-change:transform,opacity}}.product img{{width:100%;height:100%;display:block;object-fit:cover}}.product__cta{{position:absolute;left:12px;bottom:10px;z-index:3;background:#eee8da;color:#252525;padding:5px 8px;font:9px ui-monospace,monospace;opacity:0;transition:opacity .2s}}.product:hover .product__cta{{opacity:1}}.products__preview{{position:absolute;inset:48px;pointer-events:none;min-height:calc(100vh - 216px)}}.product-preview{{position:absolute;top:50%;width:calc(50% - 2.5vw);height:calc(100% - 0px);transform:translateY(-50%);opacity:0;overflow:hidden;background:#171713;will-change:opacity,transform}}.product-preview.--left{{left:0}}.product-preview.--right{{right:0}}.product-preview__images{{position:absolute;inset:0}}.product-preview__images img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0}}.product-preview__details{{position:absolute;z-index:4;left:18px;bottom:16px;color:#f4efe3;font:11px ui-monospace,monospace;text-shadow:0 1px 8px #000}}.product-preview__details p{{margin:4px 0}}.masked-preview{{position:absolute;inset:0;background:#eee8da;clip-path:polygon(45% 0,55% 0,55% 45%,100% 45%,100% 55%,55% 55%,55% 100%,45% 100%,45% 55%,0 55%,0 45%,45% 45%);will-change:clip-path}}.motion-note{{position:fixed;right:12px;bottom:10px;font:9px ui-monospace,monospace;color:#7b7466}}@media(max-width:900px){{.products__grid{{grid-template-columns:repeat(2,1fr)}}.products__preview{{display:none}}.frame{{grid-template-columns:1fr}}.frame span{{display:none}}}}
</style></head><body>{badge}<header class="frame"><h1>Grid to Full Preview · 8:5</h1><span>Codrops source geometry</span><span>100ms hover</span><span>reverse on leave</span></header><nav class="cats"><b>All <sup>8</sup></b><span>Chairs</span><span>Tables</span><span>Decoration</span><span>Cabinets</span></nav><main class="products"><ul class="products__grid">{products}</ul><div class="products__preview"><div class="product-preview --left"><div class="product-preview__images">{previews}</div><div class="product-preview__details"><p class="product-title">product title</p><p>€ <span class="product-price">0</span></p></div><div class="masked-preview"></div></div><div class="product-preview --right"><div class="product-preview__images">{previews}</div><div class="product-preview__details"><p class="product-title">product title</p><p>€ <span class="product-price">0</span></p></div><div class="masked-preview"></div></div></div></main><div class="motion-note">8:5 ratio only · source interaction preserved</div>
<script>
(()=>{{
 const products=[...document.querySelectorAll('.product')];
 const left=document.querySelector('.product-preview.--left');
 const right=document.querySelector('.product-preview.--right');
 let timer=null,active=null,gallery=null,animations=[];
 const thick='polygon(45% 0,55% 0,55% 45%,100% 45%,100% 55%,55% 55%,55% 100%,45% 100%,45% 55%,0 55%,0 45%,45% 45%)';
 const thin='polygon(50% 0,50% 0,50% 50%,100% 50%,100% 50%,50% 50%,50% 100%,50% 100%,50% 50%,0 50%,0 50%,50% 50%)';
 function stopAnims(){{animations.forEach(a=>{{try{{a.cancel()}}catch(e){{}}}});animations=[]}}
 function previewFor(p){{const i=+p.dataset.index;return (i%4===0||i%4===1)?right:left}}
 function sameSideProducts(p){{const i=+p.dataset.index;const leftSide=i%4===0||i%4===1;return products.filter(x=>{{const j=+x.dataset.index;return leftSide?(j%4===0||j%4===1):(j%4===2||j%4===3)}})}}
 function showImages(preview,id){{const all=[...preview.querySelectorAll('.product-preview__images img')];all.forEach(x=>x.style.opacity='0');const imgs=all.filter(x=>x.dataset.id===String(id));let k=0;if(imgs.length)imgs[0].style.opacity='1';clearInterval(gallery);gallery=setInterval(()=>{{imgs.forEach(x=>x.style.opacity='0');if(imgs.length){{k=(k+1)%imgs.length;imgs[k].style.opacity='1'}}}},500)}}
 function enter(p){{
   active=p;stopAnims();clearInterval(gallery);
   const preview=previewFor(p), side=sameSideProducts(p), id=+p.dataset.index;
   preview.querySelector('.product-title').textContent=p.dataset.name;preview.querySelector('.product-price').textContent=p.dataset.price;showImages(preview,id);
   animations.push(preview.animate([{{opacity:0,transform:'translateY(-50%) scale(.94)'}},{{opacity:1,transform:'translateY(-50%) scale(1)'}}],{{duration:650,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}));
   const mask=preview.querySelector('.masked-preview');animations.push(mask.animate([{{clipPath:thick}},{{clipPath:thin}}],{{duration:650,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}));
   side.forEach((x,n)=>{{const j=+x.dataset.index, col=j%4,row=j<4?0:1;const dx=(col%2===0?1:-1)*2.5;const dy=(row===0?1:-1)*2.5;animations.push(x.animate([{{opacity:1,transform:'translate(0,0)'}},{{opacity:0,transform:`translate(${{dx}}vw,${{dy}}vw)`}}],{{duration:650,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}))}})
 }}
 function leave(){{
   if(timer){{clearTimeout(timer);timer=null}};if(!active)return;stopAnims();clearInterval(gallery);const p=active,preview=previewFor(p),side=sameSideProducts(p),mask=preview.querySelector('.masked-preview');
   animations.push(preview.animate([{{opacity:1,transform:'translateY(-50%) scale(1)'}},{{opacity:0,transform:'translateY(-50%) scale(.94)'}}],{{duration:520,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}));
   animations.push(mask.animate([{{clipPath:thin}},{{clipPath:thick}}],{{duration:520,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}));
   side.forEach(x=>{{const cs=getComputedStyle(x);animations.push(x.animate([{{opacity:cs.opacity,transform:cs.transform==='none'?'translate(0,0)':cs.transform}},{{opacity:1,transform:'translate(0,0)'}}],{{duration:520,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}))}});active=null
 }}
 products.forEach(p=>{{p.addEventListener('mouseenter',()=>{{if(timer)clearTimeout(timer);timer=setTimeout(()=>{{enter(p);timer=null}},100)}});p.addEventListener('mouseleave',leave)}})
 document.documentElement.dataset.motion='ready';
}})();
</script></body></html>'''
