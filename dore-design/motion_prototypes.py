"""Doré Design P1 — Living Water Reading Core motion lab."""

PAGE_ID='motion-p1-living-current'

def _page():
    return {
        'id':PAGE_ID,'name':'Motion · P1 Reading Core','canvas':{'w':1440,'h':960},'nodes':[],
        'design_experiment':{
            'schema':'dore.design-experiment.v1','track':'motion-language','prototype':'P1','status':'prototype','source':'user-direction-2026-09-09',
            'principles':['full-stage-flow-at-rest','hover-is-primary-on-desktop','tap-is-fallback-on-touch','every-selection-replays-full-assembly','assembly-forms-one-coherent-image','selected-image-is-sliced-not-stacked','no-preallocated-empty-half','reading-field-emerges-after-assembly','content-keeps-flowing-inside-assembled-image','horizontal-reading-current','click-reserved-for-deeper-layer'],
            'acceptance':['full-stage-has-no-empty-preview-half-at-rest','hover-replays-piece-assembly-every-time','pieces-form-one-seamless-selected-image','no-multiple-unrelated-images-in-focus-assembly','assembled-image-remains-visually-readable','theme-preview-flows-horizontally-inside-assembled-image','preview-needs-no-click','background-content-keeps-moving','touch-tap-fallback','reversible']
        }
    }

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

def _card(kind,title,dore,weight,preview):
    safe=preview.replace('&','&amp;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')
    return '<button class="flow-card w%s" data-kind="%s" data-title="%s" data-dore="%s" data-preview="%s"><span>%s</span><strong>%s</strong></button>'%(weight,kind,title,dore,safe,kind,title)

def _streams():
    rows=[
      [('SCRIPTURE','起初，光進入黑暗。',21,2,'起初，光進入黑暗。光照進來，內容開始被看見。'),('JOURNAL','守望',39,1,'守望，是在流動中辨認方向。'),('PRAYER','儆醒',46,1,'儆醒，是在變化中仍然認出重要之事。'),('FEATURE','一座光明的城',75,2,'一座光明的城，在觀看與閱讀之間逐漸顯明。'),('ONE','查經',93,1,'經文、背景、串珠與歷史彼此流入。')],
      [('DAYLIGHT CAFE','共享',115,2,'共享讓不同人的看見彼此經過。'),('STUDY','同行',122,1,'同行讓閱讀不再是孤立事件。'),('DAWN LIBRARY','黎明書局',127,3,'書、文章與影像在同一個視覺場中交換位置。'),('STORY','看見',164,1,'看見，是一個持續發生的過程。')],
      [('VIDEO','影像',170,1,'影像與文字在同一個節奏裡交替浮現。'),('JOURNAL','見證人',186,2,'人物、片段、文字與圖像共同形成觀看。'),('DIALOGUE','對話',192,1,'對話本身就是流動。'),('PRAYER','你們要禱告',198,2,'禱告的內容緩慢經過，讓人定睛閱讀。')],
      [('HYMN','頌讚',216,1,'頌讚有自己的節奏。'),('MARANATHA','主啊，我願你來。',224,3,'等待並不是空白，內容仍然前行。'),('CHURCH','Living Water',237,1,'Living Water 讓閱讀路徑始終保持流動。'),('SCRIPTURE','等候黎明',75,2,'在黑暗中保持方向，直到黎明。')]
    ]
    return ''.join('<div class="current c%s">%s</div>'%(i+1,''.join(_card(*x) for x in row)) for i,row in enumerate(rows))

def render_p1(edit=False):
    badge='<div class="badge">DORÉ DESIGN · MOTION LAB · P1</div>' if edit else ''
    streams=_streams()
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Living Water Reading Core</title><style>
*{box-sizing:border-box}html,body{margin:0;background:#181713;color:#eee8d9;font-family:"Cormorant Garamond","Noto Serif TC",serif}.badge{position:fixed;z-index:99;top:10px;left:10px;background:#171714;border:1px solid #6f6748;padding:7px 9px;font:9px ui-monospace,monospace}.intro{padding:48px 5vw 24px;border-bottom:1px solid #494431}.ey,.id{font:10px ui-monospace,monospace;letter-spacing:.15em;color:#cebd74}.intro h1{font-size:clamp(38px,5vw,72px);font-weight:400;margin:.15em 0}.intro p{max-width:980px;color:#bcb4a3;line-height:1.5}.lab{display:grid;gap:30px;padding:30px 3vw 70px}.exp{border:1px solid #4a4533;background:#201f1a;overflow:hidden}.head{display:flex;gap:16px;align-items:baseline;padding:12px 14px;border-bottom:1px solid #403b2d}.head h2{font-size:22px;font-weight:400;margin:0}.note{margin-left:auto;color:#8e8778;font:10px ui-monospace,monospace}.codrops-stage{height:min(74vh,720px);min-height:600px;background:#eee}.codrops-stage iframe{width:100%;height:100%;border:0}.sourcebar,.fusion-note{padding:10px 14px;color:#a49b88;font:10px ui-monospace,monospace}.fusion{height:720px;position:relative;overflow:hidden;background:#11110e}.flow-field{position:absolute;inset:0;overflow:hidden}.current{position:absolute;left:-8vw;display:flex;gap:14px;width:max-content;will-change:transform;transition:opacity .35s,filter .35s}.c1{top:4%;animation:drift1 44s linear infinite}.c2{top:28%;animation:drift2 57s linear infinite}.c3{top:52%;animation:drift3 49s linear infinite}.c4{top:76%;animation:drift4 64s linear infinite}.flow-card{height:145px;width:232px;flex:0 0 auto;border:1px solid rgba(206,189,116,.30);background:#24221b center/cover no-repeat;color:#eee8d9;text-align:left;padding:13px;cursor:pointer;position:relative;overflow:hidden;transition:border-color .18s,transform .22s,opacity .18s}.flow-card.w2{width:476px}.flow-card.w3{width:720px}.flow-card:before{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(9,9,7,.82),rgba(9,9,7,.04) 70%)}.flow-card span,.flow-card strong{position:relative;z-index:1;display:block}.flow-card span{font:8px ui-monospace,monospace;color:#cebd74;letter-spacing:.12em}.flow-card strong{font-size:22px;font-weight:400;margin-top:8px}.flow-card.w2 strong{font-size:29px}.flow-card.w3 strong{font-size:34px}.flow-card.selected{border-color:#cebd74;transform:translateY(-4px)}.focus-stage{position:absolute;z-index:20;right:2.5%;top:6%;width:50%;height:88%;pointer-events:none;opacity:0;transition:opacity .18s}.fusion.focused .focus-stage{opacity:1;pointer-events:auto}.fusion.focused .current{opacity:.34;filter:grayscale(1) contrast(.92)}.focus-piece{position:absolute;overflow:hidden;opacity:0;will-change:transform,opacity}.focus-piece:before{content:"";position:absolute;inset:0;background-image:var(--focus-image);background-size:300% 200%;background-repeat:no-repeat;background-position:var(--bgx) var(--bgy)}.focus-stage:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(0,0,0,.03),rgba(0,0,0,.10) 45%,rgba(0,0,0,.66) 100%)}.focus-copy{position:absolute;z-index:5;left:5%;right:5%;bottom:7%;overflow:hidden}.focus-kicker{font:9px ui-monospace,monospace;letter-spacing:.16em;color:#cebd74}.focus-title{font-size:clamp(34px,4.6vw,68px);line-height:.94;font-weight:400;margin:.10em 0 .28em;text-shadow:0 2px 20px #000}.reading-viewport{position:relative;overflow:hidden;height:104px;border-top:1px solid rgba(206,189,116,.45);padding-top:13px}.reading-current{display:flex;width:max-content;gap:42px;animation:readX 24s linear infinite;will-change:transform}.reading-item{width:330px;flex:0 0 auto;font-size:16px;line-height:1.52;color:#eee8d9;text-shadow:0 2px 15px #000}.focus-stage:hover .reading-current{animation-duration:38s}.focus-hint{position:absolute;z-index:6;right:4%;top:4%;font:9px ui-monospace,monospace;color:#b2aa96}.clear{position:absolute;z-index:30;right:14px;top:14px;border:1px solid #827752;background:#171611;color:#eee8d9;padding:8px 11px;cursor:pointer;opacity:0;pointer-events:none}.fusion.focused .clear{opacity:1;pointer-events:auto}@keyframes readX{from{transform:translateX(0)}to{transform:translateX(-50%)}}@keyframes drift1{from{transform:translateX(0)}to{transform:translateX(-12vw)}}@keyframes drift2{from{transform:translateX(-8vw)}to{transform:translateX(5vw)}}@keyframes drift3{from{transform:translateX(3vw)}to{transform:translateX(-10vw)}}@keyframes drift4{from{transform:translateX(-6vw)}to{transform:translateX(7vw)}}@media(max-width:760px){.fusion{height:680px}.focus-stage{left:4%;right:4%;width:auto;top:9%;height:82%}.flow-card{height:92px;width:148px}.flow-card.w2{width:306px}.flow-card.w3{width:464px}.current{gap:8px}.c1{top:2%}.c2{top:27%}.c3{top:52%}.c4{top:77%}.note{display:none}.focus-title{font-size:38px}.reading-item{width:260px;font-size:14px}}@media(prefers-reduced-motion:reduce){.current,.reading-current{animation:none!important}}
</style></head><body>'''+badge+'''<header class="intro"><div class="ey">MOTION LAB · P1 · READING CORE</div><h1>Living Water × Focus Assembly</h1><p>D 保留 Codrops 原作。E 取消預留空半版：初始整屏都是內容流。Hover 後，被定睛的主題由多個切片重新拼成一張完整圖；拼好後，主題內容在這張圖內以緩慢橫向流動繼續展示。</p></header><main class="lab"><section class="exp"><div class="head"><span class="id">D</span><h2>Codrops · Original Reference</h2><span class="note">Gwen Bogaert · GSAP + clip-path</span></div><div class="codrops-stage"><iframe src="https://tympanus.net/Tutorials/GridToFullPreview/" title="Codrops Grid To Full Preview"></iframe></div><div class="sourcebar">成熟原作保留，用作動態基準。</div></section><section class="exp"><div class="head"><span class="id">E</span><h2>Living Water × One Image Assembly + Reading Current</h2><span class="note">flow → focus → one image → content keeps flowing</span></div><div class="fusion" id="fusion"><div class="flow-field" id="flowField">'''+streams+'''</div><div class="focus-stage" id="focusStage"><div class="focus-hint">定睛觀看</div><div class="focus-copy"><div class="focus-kicker" id="fk"></div><h3 class="focus-title" id="ft"></h3><div class="reading-viewport"><div class="reading-current" id="readingCurrent"></div></div></div></div><button class="clear" id="clear">清除</button></div><div class="fusion-note">初始整屏流動；hover 任意內容後，切片拼成一張完整主題圖，主題預覽在圖內緩慢橫向流動。Click 暫不處理，保留給第二層閱讀轉場。</div></section></main><script src="/one/one-dore-cover-registry.js"></script><script src="/one/one-dore-assets-241.js"></script><script>
(function(){
 var fusion=document.getElementById('fusion'),field=document.getElementById('flowField'),stage=document.getElementById('focusStage'),reading=document.getElementById('readingCurrent'),R=window.ONE_DORE_COVER_REGISTRY||{},commons='https://commons.wikimedia.org/wiki/Special:Redirect/file/',cards=[].slice.call(document.querySelectorAll('.flow-card')),hoverMode=matchMedia('(hover:hover) and (pointer:fine)').matches,current=null,timer=0,run=0;
 function fileFor(id){if(R.files)return R.files[id]||R.files[String(id)];var x=R[id]||R[String(id)];return x&&(x.filename||x.file||x.name)||x}
 function url(id,w){var n=fileFor(id);return n?commons+encodeURIComponent(n)+'?width='+(w||1200):''}
 function esc(s){var d=document.createElement('div');d.textContent=s||'';return d.innerHTML}
 function clearPieces(){stage.querySelectorAll('.focus-piece').forEach(function(p){p.remove()})}
 function readingItems(c){var peers=cards.filter(function(x){return x!==c&&x.dataset.kind===c.dataset.kind}).slice(0,2),arr=[c].concat(peers);if(arr.length<3)arr=arr.concat(cards.filter(function(x){return arr.indexOf(x)<0}).slice(0,3-arr.length));var one=arr.map(function(x){return '<div class="reading-item"><b>'+esc(x.dataset.title)+'</b><br>'+esc(x.dataset.preview)+'</div>'}).join('');return one+one}
 function activate(c){
   if(!c)return;current=c;run++;var my=run;cards.forEach(function(x){x.classList.toggle('selected',x===c)});fusion.classList.add('focused');clearPieces();
   document.getElementById('fk').textContent=c.dataset.kind;document.getElementById('ft').textContent=c.dataset.title;reading.innerHTML=readingItems(c);reading.style.animation='none';void reading.offsetWidth;reading.style.animation='';
   var img=url(c.dataset.dore,1400),sr=stage.getBoundingClientRect(),cols=3,rows=2,gap=2,cw=(sr.width-gap*(cols-1))/cols,ch=(sr.height-gap*(rows-1))/rows,source=c.getBoundingClientRect();
   for(var i=0;i<6;i++){
      var col=i%cols,row=Math.floor(i/cols),p=document.createElement('i');p.className='focus-piece';p.style.left=(col*(cw+gap))+'px';p.style.top=(row*(ch+gap))+'px';p.style.width=cw+'px';p.style.height=ch+'px';p.style.setProperty('--focus-image','url("'+img+'")');p.style.setProperty('--bgx',(col*50)+'%');p.style.setProperty('--bgy',(row*100)+'%');stage.insertBefore(p,stage.firstChild);
      var tx=(source.left+source.width/2)-(sr.left+col*(cw+gap)+cw/2),ty=(source.top+source.height/2)-(sr.top+row*(ch+gap)+ch/2),rot=(i-2.5)*2.2;
      p.animate([{opacity:.08,transform:'translate('+tx+'px,'+ty+'px) scale(.42) rotate('+rot+'deg)'},{opacity:1,transform:'translate(0,0) scale(1) rotate(0deg)'}],{duration:650+i*52,fill:'forwards',easing:'cubic-bezier(.2,.76,.2,1)'});
   }
 }
 cards.forEach(function(c){var u=url(c.dataset.dore,900);if(u)c.style.backgroundImage='url("'+u+'")';if(hoverMode)c.addEventListener('mouseenter',function(){clearTimeout(timer);timer=setTimeout(function(){activate(c)},55)});c.addEventListener('click',function(e){if(!hoverMode){e.preventDefault();activate(c)}})});
 document.getElementById('clear').onclick=function(e){e.stopPropagation();run++;fusion.classList.remove('focused');clearPieces();reading.innerHTML='';cards.forEach(function(x){x.classList.remove('selected')});current=null};
})();</script></body></html>'''
