"""Doré Design P1 — proven 8:5 Codrops motion with Living Water site content.

Motion engine restored from f6bafa9b029102ca55d1f2204af744a7c44c93cf.
Content only is substituted for Living Water / Westside Watch surfaces.
"""

PAGE_ID='motion-p1-living-current'

def _page():
    return {'id':PAGE_ID,'name':'Motion · P1 Reading Core','canvas':{'w':1440,'h':960},'nodes':[],'design_experiment':{'schema':'dore.design-experiment.v1','track':'motion-language','prototype':'P1','status':'prototype','source':'f6bafa9-accepted-8x5-codrops-engine','principles':['motion-locked','content-substitution-only','8x5','codrops-gsap-timeline','background-field-reorganises','one-coherent-focus-image']}}

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

def _card(kind,title,dore,weight,preview,index):
    safe=preview.replace('&','&amp;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')
    return '<button class="flow-card w%s" data-index="%s" data-kind="%s" data-title="%s" data-dore="%s" data-preview="%s"><span>%s</span><strong>%s</strong></button>'%(weight,index,kind,title,dore,safe,kind,title)

def _streams():
    rows=[
      [('LIVING WATER','活水西區',21,2,'Living Water Assembly West。'),('JOURNAL','米斯巴',39,1,'在守望中辨認正在發生的事。'),('JOURNAL','Feature',46,1,'主題閱讀與編輯策展。'),('ONE','馬太福音第七章',75,2,'不要論斷、祈求尋找叩門、窄門與兩種根基。'),('SEARCH','Doré Search',93,1,'在主站內容、查經與記錄之間找到關聯。')],
      [('MOUNT OF OLIVES','Olive Mountain',115,2,'從橄欖山望向城與黎明。'),('JOURNAL','頌讚',122,1,'詩歌、讚美與敬拜。'),('DAWN LIBRARY','黎明書局',127,3,'從經文開始，讓工具服務研讀，讓資源進入生命。'),('JOURNAL','看見',164,1,'讓值得被看見的內容自然浮現。')],
      [('ONE','四福音合參',170,1,'把平行經文放回同一條敘事線。'),('JOURNAL','伯特利 · 查經',186,2,'從經文出發，進入查考與分享。'),('JOURNAL','守望者 · 對話',192,1,'對話與辨認形成另一種閱讀節奏。'),('ONE','本章故事',198,2,'先以故事進入一章，再展開背景、歷史與串珠。')],
      [('CHURCH','Living Water',216,1,'教會、聚會與群體。'),('WESTSIDE WATCH','Watch for the Dawn',224,3,'黑夜已深，白晝將近。'),('ABOUT','About',237,1,'認識 Living Water Westside Watch。'),('THE GATE','The Gate',75,2,'進入活水西區主站內容與群體。')]
    ]
    out=[];idx=0
    for i,row in enumerate(rows):
        seq=''
        for x in row: seq+=_card(*(x+(idx,)));idx+=1
        out.append('<div class="current c%s"><div class="current-loop">%s</div><div class="current-loop" aria-hidden="true">%s</div></div>'%(i+1,seq,seq))
    return ''.join(out)

def render_p1(edit=False):
    badge='<div class="badge">DORÉ DESIGN · P1 · 8:5 CODROPS ENGINE</div>' if edit else ''
    streams=_streams()
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Living Water Reading Core</title><style>
*{box-sizing:border-box}html,body{margin:0;background-image:linear-gradient(rgba(206,189,116,.78),rgba(206,189,116,.78)),url("/api/dore/assets/site-file?code=SITE-BACKGROUND");background-size:cover;background-position:center;background-attachment:fixed;color:#252525;font-family:"Cormorant Garamond","Noto Serif TC",serif}.badge{position:fixed;z-index:99;top:10px;left:10px;background:rgba(239,228,185,.84);border:1px solid rgba(37,37,37,.42);padding:7px 9px;font:9px ui-monospace,monospace}.fusion{height:100svh;min-height:680px;position:relative;overflow:hidden;background-image:linear-gradient(rgba(206,189,116,.58),rgba(206,189,116,.58)),url("/api/dore/assets/site-file?code=SITE-BACKGROUND");background-size:cover;background-position:center}.flow-field{position:absolute;inset:0;overflow:hidden}.current{position:absolute;left:-10vw;display:flex;gap:14px;width:max-content;min-width:220vw;will-change:transform,opacity;transition:none}.current-loop{display:flex;gap:14px;flex:0 0 auto;padding-right:14px}.c1{top:4%;animation:drift1 44s linear infinite}.c2{top:28%;animation:drift2 57s linear infinite}.c3{top:52%;animation:drift3 49s linear infinite}.c4{top:76%;animation:drift4 64s linear infinite}.flow-card{height:145px;width:232px;flex:0 0 auto;border:1px solid rgba(142,104,23,.36);background:#24221b center/cover no-repeat;color:#f3eddd;text-align:left;padding:13px;cursor:pointer;position:relative;overflow:hidden;box-shadow:0 10px 26px rgba(70,53,19,.14);will-change:transform,opacity}.flow-card.w2{width:476px}.flow-card.w3{width:720px}.flow-card:before{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(9,9,7,.82),rgba(9,9,7,.04) 70%)}.flow-card span,.flow-card strong{position:relative;z-index:1;display:block}.flow-card span{font:8px ui-monospace,monospace;color:#e3cf82;letter-spacing:.12em}.flow-card strong{font-size:22px;font-weight:400;margin-top:8px}.flow-card.w2 strong{font-size:29px}.flow-card.w3 strong{font-size:34px}.focus-stage{position:absolute;z-index:20;top:5%;width:47.5%;height:90%;opacity:0;pointer-events:none;transform-origin:center center;will-change:transform,opacity}.focus-stage.--left{left:2.5%}.focus-stage.--right{right:2.5%}.focus-image{position:absolute;inset:0;background:center/cover no-repeat;clip-path:polygon(45% 0,55% 0,55% 45%,100% 45%,100% 55%,55% 55%,55% 100%,45% 100%,45% 55%,0 55%,0 45%,45% 45%);will-change:clip-path}.focus-image:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.01),rgba(0,0,0,.08) 48%,rgba(0,0,0,.62))}.focus-copy{position:absolute;z-index:5;left:5%;right:5%;bottom:7%;overflow:hidden;color:#f4efdf}.focus-kicker{font:9px ui-monospace,monospace;letter-spacing:.16em;color:#e3cf82}.focus-title{font-size:clamp(34px,4.6vw,68px);line-height:.94;font-weight:400;margin:.10em 0 .28em;text-shadow:0 2px 20px #000}.reading-viewport{overflow:hidden;height:104px;padding-top:13px}.reading-current{display:flex;width:max-content;gap:42px;animation:readX 24s linear infinite}.reading-item{width:330px;flex:0 0 auto;font-size:16px;line-height:1.52;text-shadow:0 2px 15px #000}.focus-stage:hover .reading-current{animation-duration:38s}@keyframes readX{from{transform:translateX(0)}to{transform:translateX(-50%)}}@keyframes drift1{from{transform:translateX(0)}to{transform:translateX(-28vw)}}@keyframes drift2{from{transform:translateX(-22vw)}to{transform:translateX(4vw)}}@keyframes drift3{from{transform:translateX(6vw)}to{transform:translateX(-24vw)}}@keyframes drift4{from{transform:translateX(-18vw)}to{transform:translateX(8vw)}}@media(max-width:760px){.fusion{height:680px}.flow-card{height:92px;width:148px}.flow-card.w2{width:306px}.flow-card.w3{width:464px}.focus-stage{left:4%!important;right:4%!important;width:auto;height:82%;top:9%}.current{min-width:260vw}.focus-title{font-size:38px}.reading-item{width:260px;font-size:14px}}@media(prefers-reduced-motion:reduce){.current,.reading-current{animation:none!important}}
</style></head><body>'''+badge+'''<main class="fusion" id="fusion"><div class="flow-field">'''+streams+'''</div><div class="focus-stage --left" id="focusLeft"><div class="focus-image"></div><div class="focus-copy"><div class="focus-kicker"></div><h3 class="focus-title"></h3><div class="reading-viewport"><div class="reading-current"></div></div></div></div><div class="focus-stage --right" id="focusRight"><div class="focus-image"></div><div class="focus-copy"><div class="focus-kicker"></div><h3 class="focus-title"></h3><div class="reading-viewport"><div class="reading-current"></div></div></div></div></main><script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script><script src="/one/one-dore-cover-registry.js"></script><script src="/one/one-dore-assets-241.js"></script><script>
/* Motion block below is restored verbatim from the proven 8:5 implementation. */
(function(){
 var gsap=window.gsap;if(!gsap)return;var fusion=document.getElementById('fusion'),R=window.ONE_DORE_COVER_REGISTRY||{},commons='https://commons.wikimedia.org/wiki/Special:Redirect/file/',cards=[].slice.call(document.querySelectorAll('.flow-card:not([aria-hidden="true"] .flow-card)')),allCards=[].slice.call(document.querySelectorAll('.flow-card')),hoverMode=matchMedia('(hover:hover) and (pointer:fine)').matches,active=null,delay=null,tl=null;
 function fileFor(id){if(R.files)return R.files[id]||R.files[String(id)];var x=R[id]||R[String(id)];return x&&(x.filename||x.file||x.name)||x}function url(id,w){var n=fileFor(id);return n?commons+encodeURIComponent(n)+'?width='+(w||1400):''}function esc(s){var d=document.createElement('div');d.textContent=s||'';return d.innerHTML}
 function readHTML(c){var peers=cards.filter(function(x){return x!==c&&x.dataset.kind===c.dataset.kind}).slice(0,2),arr=[c].concat(peers);if(arr.length<3)arr=arr.concat(cards.filter(function(x){return arr.indexOf(x)<0}).slice(0,3-arr.length));var one=arr.map(function(x){return '<div class="reading-item"><b>'+esc(x.dataset.title)+'</b><br>'+esc(x.dataset.preview)+'</div>'}).join('');return one+one}
 function sideFor(c){var r=c.getBoundingClientRect();return (r.left+r.width/2)<innerWidth/2?document.getElementById('focusRight'):document.getElementById('focusLeft')}
 function reset(kill){if(delay){clearTimeout(delay);delay=null}if(tl){kill?tl.kill():tl.reverse();tl=null}active=null}
 function focus(c){if(!c)return;reset(true);active=c;var stage=sideFor(c),other=stage.id==='focusLeft'?document.getElementById('focusRight'):document.getElementById('focusLeft'),img=stage.querySelector('.focus-image'),copy=stage.querySelector('.focus-copy');other.style.opacity=0;img.style.backgroundImage='url("'+url(c.dataset.dore,1600)+'")';stage.querySelector('.focus-kicker').textContent=c.dataset.kind;stage.querySelector('.focus-title').textContent=c.dataset.title;stage.querySelector('.reading-current').innerHTML=readHTML(c);var sr=c.getBoundingClientRect(),fr=fusion.getBoundingClientRect(),cx=sr.left+sr.width/2-fr.left,cy=sr.top+sr.height/2-fr.top;
   var affected=allCards.filter(function(x){return x!==c}),toRight=stage.id==='focusRight';
   tl=gsap.timeline({defaults:{ease:'power2.inOut',duration:.72}}).addLabel('preview',0).addLabel('products',0)
    .set(stage,{pointerEvents:'auto'},0).fromTo(stage,{opacity:0,scaleX:.82,scaleY:.82},{opacity:1,scaleX:1,scaleY:1,transformOrigin:'center center'},'preview')
    .fromTo(img,{clipPath:'polygon(45% 0,55% 0,55% 45%,100% 45%,100% 55%,55% 55%,55% 100%,45% 100%,45% 55%,0 55%,0 45%,45% 45%)'},{clipPath:'polygon(50% 0,50% 0,50% 50%,100% 50%,100% 50%,50% 50%,50% 100%,50% 100%,50% 50%,0 50%,0 50%,50% 50%)'},'preview')
    .to(affected,{opacity:.13,x:function(i,x){var r=x.getBoundingClientRect();var center=r.left+r.width/2;return toRight?(center>fr.width*.5?-42:-18):(center<fr.width*.5?42:18)},y:function(i,x){var r=x.getBoundingClientRect();return (r.top+r.height/2)<cy?18:-18},stagger:{amount:.08}},'products')
    .to(c,{opacity:0,scale:.92},'products').fromTo(copy,{opacity:0,y:18},{opacity:1,y:0,duration:.42},.34);
 }
 function leave(){if(delay){clearTimeout(delay);delay=null}if(!active)return;if(tl){var old=tl;tl.eventCallback('onReverseComplete',function(){gsap.set(allCards,{clearProps:'opacity,transform'});document.querySelectorAll('.focus-stage').forEach(function(s){gsap.set(s,{opacity:0,pointerEvents:'none',clearProps:'transform'});});old.kill();});tl.reverse()}active=null}
 allCards.forEach(function(c){var u=url(c.dataset.dore,900);if(u)c.style.backgroundImage='url("'+u+'")'});cards.forEach(function(c){if(hoverMode){c.addEventListener('mouseenter',function(){if(delay)clearTimeout(delay);delay=setTimeout(function(){focus(c);delay=null},100)});c.addEventListener('mouseleave',leave)}else c.addEventListener('click',function(e){e.preventDefault();focus(c)})});
 window.addEventListener('resize',function(){if(active)focus(active)});
})();</script></body></html>'''
