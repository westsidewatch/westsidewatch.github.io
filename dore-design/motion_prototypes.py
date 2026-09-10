"""Doré Design P1 — source-faithful Codrops geometry specimen.

Focus interaction ports the mature MIT-licensed Codrops grid-to-preview geometry by
Gwen Bogaert: https://github.com/gwen-bo/codrops-grid-to-preview
The Living Water flowing-current adapter is intentionally suspended in this repair.
"""

PAGE_ID='motion-p1-living-current'


def _page():
    return {
        'id': PAGE_ID,
        'name': 'Motion · P1 Reading Core',
        'canvas': {'w': 1440, 'h': 960},
        'nodes': [],
        'design_experiment': {
            'schema': 'dore.design-experiment.v1',
            'track': 'motion-language',
            'prototype': 'P1',
            'status': 'prototype',
            'source': 'codrops-grid-to-preview-mit-source-faithful-geometry',
            'principles': [
                'source-geometry-4x2-first',
                'two-registered-preview-halves',
                'hover-100ms',
                'gsap-power2-inout',
                'clip-path-cross',
                'reverse-on-mouseleave',
                'no-horizontal-drift-inside-focus-specimen',
                'gate-one-papyrus-ground',
                'flow-adapter-deferred'
            ],
            'acceptance': [
                'source-geometry-4x2-exact',
                'two-preview-overlays',
                'overlay-grid-registration-exact',
                'gutter-5vw-semantics',
                'hover-delay-100ms',
                'resize-arm-width-source-math',
                'resize-scale-source-math',
                'four-source-cards-move-inward-as-field',
                'clip-path-cross-source-faithful',
                'reverse-clean',
                'custom-fly-in-absent',
                'horizontal-drift-not-mixed-into-focus-geometry'
            ]
        }
    }


def install_workspace(base):
    original = base.workspace
    def workspace():
        w = original()
        for p in w.get('pages', []):
            if p.get('id') == PAGE_ID:
                p.update(_page())
                return base.save(w)
        w['pages'].append(_page())
        return base.save(w)
    base.workspace = workspace


def install_editor(html):
    html = html.replace("'multiwrite-cover'])", "'multiwrite-cover','motion-p1-living-current'])")
    return html.replace('DORÉ DESIGN 1.9 · PROMOTION PIPELINE', 'DORÉ DESIGN 2.0 · DESIGN LAB')


def _cards():
    items = [
        ('SCRIPTURE','起初，光進入黑暗。',21,'起初，光進入黑暗。光照進來，內容開始被看見。'),
        ('JOURNAL','守望',39,'守望，是在流動中辨認方向。'),
        ('PRAYER','儆醒',46,'儆醒，是在變化中仍然認出重要之事。'),
        ('FEATURE','一座光明的城',75,'一座光明的城，在觀看與閱讀之間逐漸顯明。'),
        ('ONE','查經',93,'經文、背景、串珠與歷史彼此流入。'),
        ('DAYLIGHT CAFE','共享',115,'共享讓不同人的看見彼此經過。'),
        ('STUDY','同行',122,'同行讓閱讀不再是孤立事件。'),
        ('DAWN LIBRARY','黎明書局',127,'書、文章與影像在同一個視覺場中交換位置。')
    ]
    out=[]
    for i,(kind,title,dore,preview) in enumerate(items):
        safe=preview.replace('&','&amp;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')
        out.append('<button class="product" data-index="%d" data-kind="%s" data-title="%s" data-dore="%s" data-preview="%s"><span>%s</span><strong>%s</strong></button>'%(i,kind,title,dore,safe,kind,title))
    return ''.join(out)


def render_p1(edit=False):
    badge='<div class="badge">DORÉ DESIGN · MOTION LAB · P1</div>' if edit else ''
    cards=_cards()
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Living Water Reading Core</title><style>
*{box-sizing:border-box}html,body{margin:0;background-image:linear-gradient(rgba(206,189,116,.78),rgba(206,189,116,.78)),url("/api/dore/assets/site-file?code=SITE-BACKGROUND");background-size:cover;background-position:center;background-attachment:fixed;color:#252525;font-family:"Cormorant Garamond","Noto Serif TC",serif}.badge{position:fixed;z-index:99;top:10px;left:10px;background:rgba(239,228,185,.84);border:1px solid rgba(37,37,37,.42);padding:7px 9px;font:9px ui-monospace,monospace}.intro{padding:48px 5vw 24px;border-bottom:1px solid rgba(37,37,37,.28)}.ey,.id{font:10px ui-monospace,monospace;letter-spacing:.15em;color:#8e6817}.intro h1{font-size:clamp(38px,5vw,72px);font-weight:400;margin:.15em 0}.intro p{max-width:980px;color:#4e4738;line-height:1.5}.lab{display:grid;gap:30px;padding:30px 3vw 70px}.exp{border:1px solid rgba(37,37,37,.42);background:rgba(239,228,185,.34);overflow:hidden}.head{display:flex;gap:16px;align-items:baseline;padding:12px 14px;border-bottom:1px solid rgba(37,37,37,.24);background:rgba(239,228,185,.48)}.head h2{font-size:22px;font-weight:400;margin:0}.note{margin-left:auto;color:#6f654f;font:10px ui-monospace,monospace}.codrops-stage{height:min(74vh,720px);min-height:600px;background:#eee}.codrops-stage iframe{width:100%;height:100%;border:0}.sourcebar,.fusion-note{padding:10px 14px;color:#645c49;font:10px ui-monospace,monospace;background:rgba(239,228,185,.42)}
.fusion{height:720px;position:relative;overflow:hidden;background-image:linear-gradient(rgba(206,189,116,.58),rgba(206,189,116,.58)),url("/api/dore/assets/site-file?code=SITE-BACKGROUND");background-size:cover;background-position:center;padding:5vw}.grid{position:relative;width:100%;height:100%;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-template-rows:repeat(2,minmax(0,1fr));gap:5vw}.product{position:relative;overflow:hidden;border:1px solid rgba(142,104,23,.34);background:#24221b center/cover no-repeat;color:#f3eddd;text-align:left;padding:14px;cursor:pointer;box-shadow:0 10px 26px rgba(70,53,19,.14);will-change:transform,opacity}.product:before{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(9,9,7,.84),rgba(9,9,7,.04) 70%)}.product span,.product strong{position:relative;z-index:1;display:block}.product span{font:8px ui-monospace,monospace;color:#e3cf82;letter-spacing:.12em}.product strong{font-size:clamp(18px,2vw,30px);font-weight:400;margin-top:8px}.preview{position:absolute;z-index:20;top:5vw;height:calc(100% - 10vw);width:calc((100% - 15vw)/2 + 5vw);opacity:0;pointer-events:none;transform-origin:center center;will-change:transform,opacity}.preview.--left{left:5vw}.preview.--right{right:5vw}.masked-preview{position:absolute;inset:0;overflow:hidden;background:#161510;clip-path:polygon(45% 0%,55% 0%,55% 45%,100% 45%,100% 55%,55% 55%,55% 100%,45% 100%,45% 55%,0% 55%,0% 45%,45% 45%);will-change:clip-path}.preview-image{position:absolute;inset:0;background:center/cover no-repeat}.preview-image:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.02),rgba(0,0,0,.08) 48%,rgba(0,0,0,.62))}.preview-copy{position:absolute;z-index:4;left:6%;right:6%;bottom:7%;color:#f4efdf;overflow:hidden}.preview-kicker{font:9px ui-monospace,monospace;letter-spacing:.16em;color:#e3cf82}.preview-title{font-size:clamp(32px,4.2vw,62px);line-height:.95;font-weight:400;margin:.1em 0 .28em;text-shadow:0 2px 20px #000}.reading-viewport{overflow:hidden;height:96px;padding-top:12px}.reading-current{display:flex;width:max-content;gap:42px;animation:readX 24s linear infinite}.reading-item{width:310px;flex:0 0 auto;font-size:15px;line-height:1.5;text-shadow:0 2px 15px #000}@keyframes readX{from{transform:translateX(0)}to{transform:translateX(-50%)}}@media(max-width:760px){.fusion{height:650px;padding:18px}.grid{gap:18px;grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:repeat(4,minmax(0,1fr))}.preview{left:18px!important;right:18px!important;top:18px;width:auto;height:calc(100% - 36px)}.note{display:none}.preview-title{font-size:38px}.reading-item{width:250px;font-size:14px}}@media(prefers-reduced-motion:reduce){.reading-current{animation:none!important}}
</style></head><body>'''+badge+'''<header class="intro"><div class="ey">MOTION LAB · P1 · SOURCE GEOMETRY</div><h1>Living Water × Codrops Geometry</h1><p>E 暫時停止四條水平水流，只驗證 Codrops 原版所依賴的固定 4×2 幾何、左右 preview 精確對位、100ms hover、GSAP timeline、clip-path cross 和 reverse。這一層跑穩後再接回 Living Water 的流。</p></header><main class="lab"><section class="exp"><div class="head"><span class="id">D</span><h2>Codrops · Original Reference</h2><span class="note">Gwen Bogaert · GSAP + clip-path · MIT</span></div><div class="codrops-stage"><iframe src="https://tympanus.net/Tutorials/GridToFullPreview/" title="Codrops Grid To Full Preview"></iframe></div><div class="sourcebar">成熟原作保留，用作動態基準。</div></section><section class="exp"><div class="head"><span class="id">E</span><h2>Living Water × Source-Faithful 4×2 Focus Geometry</h2><span class="note">fixed geometry first · flow adapter later</span></div><div class="fusion" id="fusion"><div class="grid" id="grid">'''+cards+'''</div><div class="preview --left" id="previewLeft"><div class="masked-preview"><div class="preview-image"></div></div><div class="preview-copy"><div class="preview-kicker"></div><h3 class="preview-title"></h3><div class="reading-viewport"><div class="reading-current"></div></div></div></div><div class="preview --right" id="previewRight"><div class="masked-preview"><div class="preview-image"></div></div><div class="preview-copy"><div class="preview-kicker"></div><h3 class="preview-title"></h3><div class="reading-viewport"><div class="reading-current"></div></div></div></div></div><div class="fusion-note">這一版只驗證成熟原版動效幾何。Click 仍保留給之後第二層閱讀；內容流仍是暫時形態。</div></section></main><script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script><script src="/one/one-dore-cover-registry.js"></script><script src="/one/one-dore-assets-241.js"></script><script>
/* Source-faithful geometry and timeline semantics adapted from the MIT-licensed
   Codrops grid-to-preview by Gwen Bogaert: product-grid.js + product-preview.js. */
(function(){
 var gsap=window.gsap;if(!gsap)return;
 var products=[].slice.call(document.querySelectorAll('.product')),R=window.ONE_DORE_COVER_REGISTRY||{},commons='https://commons.wikimedia.org/wiki/Special:Redirect/file/',hoverDelay=null,activeProduct=null;
 function fileFor(id){if(R.files)return R.files[id]||R.files[String(id)];var x=R[id]||R[String(id)];return x&&(x.filename||x.file||x.name)||x}
 function url(id,w){var n=fileFor(id);return n?commons+encodeURIComponent(n)+'?width='+(w||1400):''}
 function esc(s){var d=document.createElement('div');d.textContent=s||'';return d.innerHTML}
 products.forEach(function(p){var u=url(p.dataset.dore,1000);if(u)p.style.backgroundImage='url("'+u+'")'});
 function readingHTML(product){var peers=products.filter(function(x){return x!==product&&x.dataset.kind===product.dataset.kind}).slice(0,2),arr=[product].concat(peers);if(arr.length<3)arr=arr.concat(products.filter(function(x){return arr.indexOf(x)<0}).slice(0,3-arr.length));var one=arr.map(function(x){return '<div class="reading-item"><b>'+esc(x.dataset.title)+'</b><br>'+esc(x.dataset.preview)+'</div>'}).join('');return one+one}
 function Controller(container,controlled){
   this.container=container;this.products=controlled;this.masked=container.querySelector('.masked-preview');this.image=container.querySelector('.preview-image');this.kicker=container.querySelector('.preview-kicker');this.title=container.querySelector('.preview-title');this.reading=container.querySelector('.reading-current');this.timeline=null;this.armWidth={x:10,y:10};this.scaleFactor={x:1,y:1};this.onResize();
 }
 Controller.prototype.buildTimeline=function(){
   var self=this,x=this.armWidth.x,y=this.armWidth.y;
   this.timeline=gsap.timeline({paused:true,defaults:{ease:'power2.inOut'}})
     .addLabel('preview',0).addLabel('products',0)
     .to(this.container,{opacity:1},'preview')
     .to(this.container,{scaleX:this.scaleFactor.x,scaleY:this.scaleFactor.y,transformOrigin:'center center'},'preview')
     .to(this.products,{opacity:0,x:function(i){return i%2===0?'2.5vw':'-2.5vw'},y:function(i){return i<2?'2.5vw':'-2.5vw'}},'products')
     .fromTo(this.masked,{clipPath:'polygon('+(50-x/2)+'% 0%,'+(50+x/2)+'% 0%,'+(50+x/2)+'% '+(50-y/2)+'%,100% '+(50-y/2)+'%,100% '+(50+y/2)+'%,'+(50+x/2)+'% '+(50+y/2)+'%,'+(50+x/2)+'% 100%,'+(50-x/2)+'% 100%,'+(50-x/2)+'% '+(50+y/2)+'%,0% '+(50+y/2)+'%,0% '+(50-y/2)+'%,'+(50-x/2)+'% '+(50-y/2)+'%)'},{clipPath:'polygon(50% 0%,50% 0%,50% 50%,100% 50%,100% 50%,50% 50%,50% 100%,50% 100%,50% 50%,0% 50%,0% 50%,50% 50%)'},'preview');
 };
 Controller.prototype.onResize=function(){
   var rect=this.container.getBoundingClientRect(),vw=window.innerWidth/100,armWidthPx=5*vw;
   this.armWidth={x:(armWidthPx/rect.width)*100,y:(armWidthPx/rect.height)*100};
   var widthInVw=rect.width/vw,heightInVw=rect.height/vw,shrinkVw=5;
   this.scaleFactor={x:(widthInVw-shrinkVw)/widthInVw,y:(heightInVw-shrinkVw)/heightInVw};
   if(this.timeline)this.timeline.kill();this.buildTimeline();
 };
 Controller.prototype.setProduct=function(product){
   if(product){
     this.kicker.textContent=product.dataset.kind;this.title.textContent=product.dataset.title;this.reading.innerHTML=readingHTML(product);this.image.style.backgroundImage='url("'+url(product.dataset.dore,1600)+'")';
     this.timeline.play(0);
   }else{this.timeline.reverse()}
 };
 var leftHalf=products.filter(function(_,i){return i%4===0||i%4===1}),rightHalf=products.filter(function(_,i){return i%4===2||i%4===3});
 var previewForLeftProduct=new Controller(document.getElementById('previewRight'),rightHalf);
 var previewForRightProduct=new Controller(document.getElementById('previewLeft'),leftHalf);
 function getPreview(product){var i=Number(product.dataset.index);return (i%4===0||i%4===1)?previewForLeftProduct:previewForRightProduct}
 function enter(product){if(hoverDelay){clearTimeout(hoverDelay);hoverDelay=null}hoverDelay=setTimeout(function(){activeProduct=product;getPreview(product).setProduct(product);hoverDelay=null},100)}
 function leave(){if(hoverDelay){clearTimeout(hoverDelay);hoverDelay=null}if(activeProduct){getPreview(activeProduct).setProduct(null);activeProduct=null}}
 products.forEach(function(product){product.addEventListener('mouseenter',function(){enter(product)});product.addEventListener('mouseleave',leave)});
 window.addEventListener('resize',function(){previewForLeftProduct.onResize();previewForRightProduct.onResize()});
})();
</script></body></html>'''
