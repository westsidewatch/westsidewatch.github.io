"""Doré Design P1 — hover/tap motion lab for Living Water 8:5 currents."""

PAGE_ID='motion-p1-living-current'

def _page():
    return {
        'id':PAGE_ID,'name':'Motion · P1 Hover Assembly','canvas':{'w':1440,'h':960},'nodes':[],
        'design_experiment':{
            'schema':'dore.design-experiment.v1','track':'motion-language','prototype':'P1','status':'prototype','source':'user-direction-2026-09-09',
            'principles':['hover-is-primary-on-desktop','tap-is-fallback-on-touch','D-codrops-original-reference','E-half-screen-assembly-half-screen-mosaic','grid-never-visible-at-rest','every-selection-replays-full-assembly','piece-count-follows-visible-layout-half','multiple-independent-dore-images','layout-half-keeps-moving'],
            'acceptance':['one-half-remains-multi-image-layout','other-half-is-assembly-stage','desktop-hover-needs-no-click','every-new-hover-replays-full-assembly','piece-count-is-variable','pieces-use-different-visible-dore-images','source-to-target-motion-visible-every-time','layout-half-keeps-moving','touch-tap-fallback','reversible']
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

def _card(kind,title,dore,weight):
    return '<button class="flow-card w%s" data-kind="%s" data-title="%s" data-dore="%s"><span>%s</span><strong>%s</strong></button>'%(weight,kind,title,dore,kind,title)

def _streams():
    rows=[
      [('SCRIPTURE','起初，光進入黑暗。',21,2),('JOURNAL','守望',39,1),('PRAYER','儆醒',46,1),('FEATURE','一座光明的城',75,2),('ONE','查經',93,1)],
      [('DAYLIGHT CAFE','共享',115,2),('STUDY','同行',122,1),('DAWN LIBRARY','黎明書局',127,3),('STORY','看見',164,1)],
      [('VIDEO','影像',170,1),('JOURNAL','見證人',186,2),('DIALOGUE','對話',192,1),('PRAYER','你們要禱告',198,2)],
      [('HYMN','頌讚',216,1),('MARANATHA','主啊，我願你來。',224,3),('CHURCH','Living Water',237,1),('SCRIPTURE','等候黎明',75,2)]
    ]
    return ''.join('<div class="current c%s">%s</div>'%(i+1,''.join(_card(*x) for x in row)) for i,row in enumerate(rows))

def render_p1(edit=False):
    badge='<div class="badge">DORÉ DESIGN · MOTION LAB · P1</div>' if edit else ''
    streams=_streams()
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>P1 Half Screen Assembly</title><style>
*{box-sizing:border-box}html,body{margin:0;background:#181713;color:#eee8d9;font-family:"Cormorant Garamond","Noto Serif TC",serif}.badge{position:fixed;z-index:99;top:10px;left:10px;background:#171714;border:1px solid #6f6748;padding:7px 9px;font:9px ui-monospace,monospace}.intro{padding:48px 5vw 24px;border-bottom:1px solid #494431}.ey,.id{font:10px ui-monospace,monospace;letter-spacing:.15em;color:#cebd74}.intro h1{font-size:clamp(38px,5vw,72px);font-weight:400;margin:.15em 0}.intro p{max-width:940px;color:#bcb4a3;line-height:1.5}.lab{display:grid;gap:30px;padding:30px 3vw 70px}.exp{border:1px solid #4a4533;background:#201f1a;overflow:hidden}.head{display:flex;gap:16px;align-items:baseline;padding:12px 14px;border-bottom:1px solid #403b2d}.head h2{font-size:22px;font-weight:400;margin:0}.note{margin-left:auto;color:#8e8778;font:10px ui-monospace,monospace}.codrops-stage{height:min(74vh,720px);min-height:600px;background:#eee}.codrops-stage iframe{width:100%;height:100%;border:0}.sourcebar,.fusion-note{padding:10px 14px;color:#a49b88;font:10px ui-monospace,monospace}.fusion{height:720px;position:relative;overflow:hidden;background:#11110e;display:grid;grid-template-columns:1fr 1fr}.layout-half{position:relative;overflow:hidden;border-right:1px solid rgba(206,189,116,.20)}.assembly-half{position:relative;overflow:hidden;background:#0d0d0b}.current{position:absolute;left:-14vw;display:flex;gap:10px;width:max-content;will-change:transform}.c1{top:3%;animation:drift1 42s linear infinite}.c2{top:27%;animation:drift2 55s linear infinite}.c3{top:51%;animation:drift3 47s linear infinite}.c4{top:75%;animation:drift4 62s linear infinite}.flow-card{height:145px;width:232px;flex:0 0 auto;border:1px solid rgba(206,189,116,.36);background:#24221b center/cover no-repeat;color:#eee8d9;text-align:left;padding:13px;cursor:pointer;position:relative;overflow:hidden;transition:border-color .16s,transform .16s,opacity .16s}.flow-card.w2{width:476px}.flow-card.w3{width:720px}.flow-card:before{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(9,9,7,.90),rgba(9,9,7,.05) 68%)}.flow-card span,.flow-card strong{position:relative;z-index:1;display:block}.flow-card span{font:8px ui-monospace,monospace;color:#cebd74;letter-spacing:.12em}.flow-card strong{font-size:22px;font-weight:400;margin-top:8px;max-width:18ch}.flow-card.w2 strong{font-size:29px}.flow-card.w3 strong{font-size:34px}.flow-card.selected{border-color:#cebd74;transform:translateY(-4px)}.assembly-piece{position:absolute;background:center/cover no-repeat;border:1px solid rgba(238,232,217,.18);box-shadow:0 12px 34px rgba(0,0,0,.22);opacity:0;will-change:transform,opacity}.assembly-copy{position:absolute;z-index:10;left:8%;right:8%;bottom:7%;pointer-events:none;text-shadow:0 2px 18px #000}.assembly-copy small{font:9px ui-monospace,monospace;letter-spacing:.15em;color:#cebd74}.assembly-copy h3{font-size:clamp(34px,4vw,68px);font-weight:400;margin:.08em 0}.assembly-copy p{margin:.2em 0;color:#d1c9b7;max-width:52ch}.assembly-copy .count{font:9px ui-monospace,monospace;color:#a9a18f}.actions{position:absolute;z-index:11;right:16px;top:16px;display:flex;gap:8px}.actions button{border:1px solid #827752;background:#171611;color:#eee8d9;padding:8px 11px;cursor:pointer}.destination{position:absolute;z-index:20;inset:0;background:#eee8da;color:#191813;padding:10%;clip-path:inset(100% 0 0);transition:clip-path .65s cubic-bezier(.65,0,.2,1)}.destination.on{clip-path:inset(0)}.destination h3{font-size:clamp(52px,8vw,100px);font-weight:400;margin:.1em 0}.destination button{padding:10px 14px;background:transparent;border:1px solid #29271f}@keyframes drift1{from{transform:translateX(0)}to{transform:translateX(-12vw)}}@keyframes drift2{from{transform:translateX(-9vw)}to{transform:translateX(4vw)}}@keyframes drift3{from{transform:translateX(2vw)}to{transform:translateX(-10vw)}}@keyframes drift4{from{transform:translateX(-6vw)}to{transform:translateX(6vw)}}@media(max-width:760px){.fusion{height:680px;grid-template-columns:1fr}.layout-half{height:50%;border-right:0;border-bottom:1px solid rgba(206,189,116,.20)}.assembly-half{height:50%}.flow-card{height:92px;width:148px}.flow-card.w2{width:306px}.flow-card.w3{width:464px}.current{gap:7px}.c1{top:2%}.c2{top:27%}.c3{top:52%}.c4{top:77%}.note{display:none}.assembly-copy h3{font-size:36px}}@media(prefers-reduced-motion:reduce){.current{animation:none!important}}
</style></head><body>'''+badge+'''<header class="intro"><div class="ey">MOTION LAB · P1 · HALF LAYOUT / HALF ASSEMBLY</div><h1>Living Water × Dynamic Assembly</h1><p>D 保留 Codrops 原作。E 改成原版更接近的結構：一半畫面一直保留多張 8:5 流動佈局；另一半專門做拼合。每次 hover 到新內容，都重新從左側當下可見圖片抽取多張，完整飛入並拼成右側整體。</p></header><main class="lab"><section class="exp"><div class="head"><span class="id">D</span><h2>Codrops · Original Reference</h2><span class="note">Gwen Bogaert · GSAP + clip-path</span></div><div class="codrops-stage"><iframe src="https://tympanus.net/Tutorials/GridToFullPreview/" title="Codrops Grid To Full Preview"></iframe></div><div class="sourcebar">成熟原作保留，用作動態基準。</div></section><section class="exp"><div class="head"><span class="id">E</span><h2>Living Water × Half-Screen Assembly</h2><span class="note">left stays plural · right assembles every time</span></div><div class="fusion" id="fusion"><div class="layout-half" id="layoutHalf">'''+streams+'''</div><div class="assembly-half" id="assemblyHalf"><div class="assembly-copy"><small id="pk">HOVER</small><h3 id="pt">移動鼠標開始拼合</h3><p>左半保持多張流動；右半每次都完整重演多張圖的聚合。</p><div class="count" id="pc"></div></div><div class="actions"><button id="clear">清除</button><button id="enter">進入正文</button></div><div class="destination" id="dest"><small>JOURNAL</small><h3 id="dt">守望</h3><p>正文入口。</p><button id="destBack">返回</button></div></div></div><div class="fusion-note">桌面：hover 左側任意 8:5；觸控：tap。右側不是固定四張，而是使用左半當下可見的一組圖片重新拼合。</div></section></main><script src="/one/one-dore-cover-registry.js"></script><script src="/one/one-dore-assets-241.js"></script><script>
(function(){
 var layout=document.getElementById('layoutHalf'),stage=document.getElementById('assemblyHalf'),R=window.ONE_DORE_COVER_REGISTRY||{},commons='https://commons.wikimedia.org/wiki/Special:Redirect/file/',cards=[].slice.call(document.querySelectorAll('.flow-card')),hoverMode=matchMedia('(hover:hover) and (pointer:fine)').matches,current=null,timer=0,run=0;
 function fileFor(id){if(R.files)return R.files[id]||R.files[String(id)];var x=R[id]||R[String(id)];return x&&(x.filename||x.file||x.name)||x}
 function url(id,w){var n=fileFor(id);return n?commons+encodeURIComponent(n)+'?width='+(w||1000):''}
 function visibleCards(){var lr=layout.getBoundingClientRect();return cards.filter(function(c){var r=c.getBoundingClientRect();return r.right>lr.left&&r.left<lr.right&&r.bottom>lr.top&&r.top<lr.bottom})}
 function clearPieces(){stage.querySelectorAll('.assembly-piece').forEach(function(p){p.remove()})}
 function grid(n,w,h){var cols=n<=4?2:(n<=9?3:4),rows=Math.ceil(n/cols),gap=4,cw=(w-gap*(cols-1))/cols,ch=(h-gap*(rows-1))/rows;return Array.from({length:n},function(_,i){return {x:(i%cols)*(cw+gap),y:Math.floor(i/cols)*(ch+gap),w:cw,h:ch}})}
 function activate(c){
   if(!c)return;current=c;run++;var my=run;cards.forEach(function(x){x.classList.toggle('selected',x===c)});
   var set=visibleCards();if(set.length<4)set=cards.slice(0,Math.min(6,cards.length));
   var sr=stage.getBoundingClientRect(),targets=grid(set.length,sr.width,sr.height),old=[].slice.call(stage.querySelectorAll('.assembly-piece'));
   old.forEach(function(p){p.animate([{opacity:1,transform:'scale(1)'},{opacity:0,transform:'scale(.82)'}],{duration:180,fill:'forwards',easing:'ease-in'}).onfinish=function(){p.remove()}});
   set.forEach(function(src,i){
      var r=src.getBoundingClientRect(),t=targets[i],p=document.createElement('i');p.className='assembly-piece';p.style.backgroundImage='url("'+url(src.dataset.dore,1000)+'")';p.style.left=t.x+'px';p.style.top=t.y+'px';p.style.width=t.w+'px';p.style.height=t.h+'px';stage.insertBefore(p,stage.firstChild);
      var dx=(r.left+r.width/2)-(sr.left+t.x+t.w/2),dy=(r.top+r.height/2)-(sr.top+t.y+t.h/2),sx=Math.max(.18,Math.min(1.5,r.width/t.w)),sy=Math.max(.18,Math.min(1.5,r.height/t.h));
      p.animate([{opacity:.35,transform:'translate('+dx+'px,'+dy+'px) scale('+sx+','+sy+')'},{opacity:1,transform:'translate(0,0) scale(1)'}],{duration:620+Math.min(i,8)*34,fill:'forwards',easing:'cubic-bezier(.22,.75,.18,1)'});
   });
   document.getElementById('pk').textContent=c.dataset.kind;document.getElementById('pt').textContent=c.dataset.title;document.getElementById('dt').textContent=c.dataset.title;document.getElementById('pc').textContent=set.length+' 張圖 · 本次重新拼合';
 }
 cards.forEach(function(c){var u=url(c.dataset.dore,900);if(u)c.style.backgroundImage='url("'+u+'")';if(hoverMode)c.addEventListener('mouseenter',function(){clearTimeout(timer);timer=setTimeout(function(){activate(c)},45)});c.addEventListener('click',function(e){if(!hoverMode){e.preventDefault();activate(c)}})});
 document.getElementById('clear').onclick=function(e){e.stopPropagation();run++;clearPieces();cards.forEach(function(x){x.classList.remove('selected')});current=null;document.getElementById('pk').textContent='HOVER';document.getElementById('pt').textContent='移動鼠標開始拼合';document.getElementById('pc').textContent=''};
 document.getElementById('enter').onclick=function(e){e.stopPropagation();if(current)document.getElementById('dest').classList.add('on')};document.getElementById('destBack').onclick=function(e){e.stopPropagation();document.getElementById('dest').classList.remove('on')};
})();</script></body></html>'''