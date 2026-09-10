"""Doré Design P1 — click-motion lab for Living Water 8:5 currents."""

PAGE_ID='motion-p1-living-current'

def _page():
    return {
        'id': PAGE_ID,
        'name': 'Motion · P1 Click Dynamics',
        'canvas': {'w':1440,'h':960},
        'nodes': [],
        'design_experiment': {
            'schema':'dore.design-experiment.v1','track':'motion-language','prototype':'P1','status':'prototype','source':'user-direction-2026-09-09',
            'principles':['no-light-effects','click-is-primary-motion','D-codrops-original-reference','E-four-living-currents-to-temporary-puzzle','grid-never-visible-at-rest','dore-images-at-rest','continuous-selection-without-return','preview-click-advances','four-pieces-reconstruct-one-image','no-center-void','tap-not-hover'],
            'acceptance':['four-horizontal-currents-visible-at-rest','different-speeds','weighted-8:5-spans','dore-images-visible-at-rest','click-forms-temporary-puzzle','click-preview-advances-to-next-content','same-surface-repeatable-click','currents-keep-moving','puzzle-has-no-black-center-hole','selected-content-identity-preserved','reversible']
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
      [('SCRIPTURE','起初，光進入黑暗。',21,2),('JOURNAL','守望',39,1),('PRAYER','儆醒',46,1),('FEATURE','一座光明的城',75,2)],
      [('ONE','查經',93,1),('DAYLIGHT CAFE','共享',115,2),('STUDY','同行',122,1),('DAWN LIBRARY','黎明書局',127,3)],
      [('STORY','看見',164,1),('VIDEO','影像',170,1),('JOURNAL','見證人',186,2),('DIALOGUE','對話',192,1)],
      [('PRAYER','你們要禱告',198,2),('HYMN','頌讚',216,1),('MARANATHA','主啊，我願你來。',224,3),('CHURCH','Living Water',237,1)]
    ]
    return ''.join('<div class="current c%s">%s</div>'%(i+1,''.join(_card(*x) for x in row)) for i,row in enumerate(rows))

def render_p1(edit=False):
    badge='<div class="badge">DORÉ DESIGN · MOTION LAB · P1</div>' if edit else ''
    streams=_streams()
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>P1 Click Dynamics</title><style>
*{box-sizing:border-box}html,body{margin:0;background:#181713;color:#eee8d9;font-family:"Cormorant Garamond","Noto Serif TC",serif}.badge{position:fixed;z-index:99;top:10px;left:10px;background:#171714;border:1px solid #6f6748;padding:7px 9px;font:9px ui-monospace,monospace}.intro{padding:48px 5vw 24px;border-bottom:1px solid #494431}.ey,.id{font:10px ui-monospace,monospace;letter-spacing:.15em;color:#cebd74}.intro h1{font-size:clamp(38px,5vw,72px);font-weight:400;margin:.15em 0}.intro p{max-width:900px;color:#bcb4a3;line-height:1.5}.lab{display:grid;gap:30px;padding:30px 3vw 70px}.exp{border:1px solid #4a4533;background:#201f1a;overflow:hidden}.head{display:flex;gap:16px;align-items:baseline;padding:12px 14px;border-bottom:1px solid #403b2d}.head h2{font-size:22px;font-weight:400;margin:0}.note{margin-left:auto;color:#8e8778;font:10px ui-monospace,monospace}.codrops-stage{height:min(74vh,720px);min-height:600px;background:#eee}.codrops-stage iframe{width:100%;height:100%;border:0}.sourcebar,.fusion-note{padding:10px 14px;color:#a49b88;font:10px ui-monospace,monospace}.fusion{height:720px;position:relative;overflow:hidden;background:#11110e}.currents{position:absolute;z-index:2;inset:0;overflow:hidden;transition:opacity .35s,filter .35s}.current{position:absolute;left:-10vw;display:flex;gap:12px;width:max-content;will-change:transform}.c1{top:5%;animation:drift1 42s linear infinite}.c2{top:29%;animation:drift2 55s linear infinite}.c3{top:53%;animation:drift3 47s linear infinite}.c4{top:77%;animation:drift4 62s linear infinite}.flow-card{height:142px;width:227px;flex:0 0 auto;border:1px solid rgba(206,189,116,.38);background:#24221b center/cover no-repeat;color:#eee8d9;text-align:left;padding:14px;cursor:pointer;position:relative;overflow:hidden;transition:opacity .25s,border-color .25s,transform .25s}.flow-card.w2{width:466px}.flow-card.w3{width:705px}.flow-card:before{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(9,9,7,.88),rgba(9,9,7,.08) 68%)}.flow-card span,.flow-card strong{position:relative;z-index:1;display:block}.flow-card span{font:8px ui-monospace,monospace;color:#cebd74;letter-spacing:.12em}.flow-card strong{font-size:22px;font-weight:400;margin-top:8px;max-width:18ch}.flow-card.w2 strong{font-size:29px}.flow-card.w3 strong{font-size:34px}.fusion.active .currents{opacity:.48;filter:brightness(.62)}.fusion.active .flow-card.selected{opacity:1;border-color:#cebd74;transform:translateY(-4px)}.puzzle{position:absolute;z-index:5;inset:10% 14%;pointer-events:none;opacity:0;overflow:hidden}.fusion.active .puzzle{opacity:1}.piece{position:absolute;width:50%;height:50%;background-repeat:no-repeat;background-size:200% 200%;border:0;transition:transform .72s cubic-bezier(.65,0,.2,1)}.p1{left:0;top:0;background-position:0 0;transform:translate(-46%,-34%)}.p2{right:0;top:0;background-position:100% 0;transform:translate(46%,-34%)}.p3{left:0;bottom:0;background-position:0 100%;transform:translate(-46%,34%)}.p4{right:0;bottom:0;background-position:100% 100%;transform:translate(46%,34%)}.fusion.active .piece{transform:translate(0,0)}.preview-copy{position:absolute;z-index:8;inset:10% 14%;display:flex;flex-direction:column;justify-content:flex-end;padding:5%;background:linear-gradient(0deg,rgba(10,9,7,.88),transparent 58%);opacity:0;transform:scale(.96);pointer-events:none;transition:opacity .35s .42s,transform .68s cubic-bezier(.65,0,.2,1)}.fusion.active .preview-copy{opacity:1;transform:scale(1);pointer-events:auto;cursor:pointer}.preview-copy small{color:#cebd74;font:9px ui-monospace,monospace;letter-spacing:.15em}.preview-copy h3{font-size:clamp(44px,7vw,90px);font-weight:400;margin:.08em 0}.preview-copy p{max-width:620px;font-size:17px}.actions{display:flex;gap:10px}.actions button{border:1px solid #a4935b;background:#171611;color:#eee8d9;padding:10px 14px;cursor:pointer}.actions .enter{background:#cebd74;color:#171611}.destination{position:absolute;z-index:12;inset:0;background:#eee8da;color:#191813;padding:10%;clip-path:inset(100% 0 0);transition:clip-path .75s cubic-bezier(.65,0,.2,1)}.destination.on{clip-path:inset(0)}.destination h3{font-size:clamp(52px,8vw,100px);font-weight:400;margin:.1em 0}.destination button{padding:10px 14px;background:transparent;border:1px solid #29271f}@keyframes drift1{from{transform:translateX(0)}to{transform:translateX(-12vw)}}@keyframes drift2{from{transform:translateX(-9vw)}to{transform:translateX(4vw)}}@keyframes drift3{from{transform:translateX(2vw)}to{transform:translateX(-10vw)}}@keyframes drift4{from{transform:translateX(-6vw)}to{transform:translateX(6vw)}}@media(max-width:700px){.note{display:none}.fusion{height:640px}.flow-card{height:100px;width:160px}.flow-card.w2{width:332px}.flow-card.w3{width:504px}.puzzle,.preview-copy{inset:14% 5%}.current{gap:8px}}@media(prefers-reduced-motion:reduce){.current{animation:none!important}*{transition-duration:.01ms!important}}
</style></head><body>'''+badge+'''<header class="intro"><div class="ey">MOTION LAB · P1 · CONTINUOUS CLICK</div><h1>Living Water × Grid To Full Preview</h1><p>D 保留 Codrops 原作。E 現在可連續點：第一次點任意 8:5 形成拼圖；之後直接再點中央 preview 本身，就切到下一個內容並重新播放拼圖，不需要返回。</p></header><main class="lab"><section class="exp"><div class="head"><span class="id">D</span><h2>Codrops · Original Reference</h2><span class="note">Gwen Bogaert · GSAP + clip-path</span></div><div class="codrops-stage"><iframe src="https://tympanus.net/Tutorials/GridToFullPreview/" title="Codrops Grid To Full Preview"></iframe></div><div class="sourcebar">成熟原作保留，用作動態基準。</div></section><section class="exp"><div class="head"><span class="id">E</span><h2>Living Water × Puzzle Preview</h2><span class="note">click preview again → next item</span></div><div class="fusion" id="fusion"><div class="currents">'''+streams+'''</div><div class="puzzle"><i class="piece p1"></i><i class="piece p2"></i><i class="piece p3"></i><i class="piece p4"></i></div><div class="preview-copy" id="previewCopy"><small id="pk">JOURNAL</small><h3 id="pt">守望</h3><p>點中央 preview 本身即可繼續下一個內容；每次都重新散開 → 換圖 → 聚合。四股內容流在背景保持運動。</p><div class="actions"><button id="back">返回內容流</button><button class="enter" id="enter">進入正文</button></div></div><div class="destination" id="dest"><small>JOURNAL</small><h3 id="dt">守望</h3><p>正文入口。</p><button id="destBack">返回</button></div></div><div class="fusion-note">第一次點 8:5；之後連續點中央 preview，即可不停切換並重播拼圖。</div></section></main><script src="/one/one-dore-cover-registry.js"></script><script src="/one/one-dore-assets-241.js"></script><script>
(function(){
 var f=document.getElementById('fusion'),preview=document.getElementById('previewCopy'),R=window.ONE_DORE_COVER_REGISTRY||{},commons='https://commons.wikimedia.org/wiki/Special:Redirect/file/',cards=[].slice.call(document.querySelectorAll('.flow-card')),current=-1;
 function fileFor(id){if(R.files)return R.files[id]||R.files[String(id)];var x=R[id]||R[String(id)];return x&&(x.filename||x.file||x.name)||x}
 function url(id,w){var n=fileFor(id);return n?commons+encodeURIComponent(n)+'?width='+(w||1400):''}
 function activate(c){
   current=Math.max(0,cards.indexOf(c));cards.forEach(function(x){x.classList.remove('selected')});c.classList.add('selected');
   var img=url(c.dataset.dore,2000),pieces=document.querySelectorAll('.piece');
   f.classList.remove('active');void f.offsetWidth;pieces.forEach(function(p){p.style.backgroundImage='url("'+img+'")'});
   document.getElementById('pk').textContent=c.dataset.kind;document.getElementById('pt').textContent=c.dataset.title;document.getElementById('dt').textContent=c.dataset.title;
   requestAnimationFrame(function(){requestAnimationFrame(function(){f.classList.add('active')})});
 }
 cards.forEach(function(c){var u=url(c.dataset.dore,1100);if(u)c.style.backgroundImage='url("'+u+'")';c.addEventListener('click',function(e){e.stopPropagation();activate(c)})});
 preview.addEventListener('click',function(){if(current<0)return;activate(cards[(current+1)%cards.length])});
 document.getElementById('back').onclick=function(e){e.stopPropagation();f.classList.remove('active');cards.forEach(function(x){x.classList.remove('selected')});current=-1};
 document.getElementById('enter').onclick=function(e){e.stopPropagation();document.getElementById('dest').classList.add('on')};
 document.getElementById('destBack').onclick=function(e){e.stopPropagation();document.getElementById('dest').classList.remove('on')};
})();</script></body></html>'''