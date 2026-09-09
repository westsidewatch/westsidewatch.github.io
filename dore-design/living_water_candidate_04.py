"""Living Water Candidate 04.
C01 remains the visual/color baseline. C04 inserts one horizontal Living Water navigation field
between C01's opening scene and its existing first-layer section sequence.
"""
import living_water_candidate as c01

PAGE_ID='living-water-candidate-04'

def page():
    return {'id':PAGE_ID,'name':'Living Water · Candidate 04','canvas':{'w':1440,'h':960},'nodes':[],
      'design_experiment':{'schema':'dore.design-experiment.v1','track':'living-water-homepage','candidate':'04','status':'design-candidate','source':'user-direction-2026-09-09',
      'principles':['inherit-c01-color-worlds','homepage-then-horizontal-live-navigation','landscape-only','8:5-horizontal-rhythm','weight-controls-span-and-speed','scroll-preserves-viewing-habit','c01-section-sequence-after-navigation','first-layer-only']}}

def install_workspace(base):
    original=base.workspace
    def workspace():
        w=original()
        if not any(p.get('id')==PAGE_ID for p in w.get('pages',[])):
            w['pages'].append(page());w=base.save(w)
        return w
    base.workspace=workspace

def install_editor(html):
    return html.replace("'living-water-candidate-03'])","'living-water-candidate-03','living-water-candidate-04'])")

CSS=r'''
/* C04 inserted page — all units remain landscape and flow horizontally. */
.live-nav{height:235svh;position:relative;background:#102a43;color:#faf9f5;isolation:isolate}.live-nav-stage{position:sticky;top:0;height:100svh;overflow:hidden;padding:5vh 0 4vh}.live-nav-head{height:24vh;padding:0 6vw 2.4vh;display:grid;grid-template-columns:minmax(0,1.45fr) minmax(260px,.55fr);gap:6vw;align-items:end;border-bottom:1px solid rgba(250,249,245,.2)}.live-nav-head h2{font-size:clamp(54px,7.6vw,116px);font-weight:400;line-height:.78;margin:.1em 0}.live-nav-head p{font-size:clamp(15px,1.25vw,19px);line-height:1.55;max-width:430px;margin:0}.live-water{height:70vh;position:relative;overflow:hidden}.stream{position:absolute;left:0;width:max-content;display:flex;align-items:center;gap:1.2vw;will-change:transform;transform:translate3d(var(--x,0),0,0)}.stream.a{top:3.5vh}.stream.b{top:28vh}.stream.c{top:52.5vh}.tile{height:21vh;aspect-ratio:8/5;position:relative;overflow:hidden;flex:0 0 auto;border:1px solid rgba(255,255,255,.12);box-shadow:0 16px 44px rgba(0,0,0,.12)}.tile.span2{width:calc(21vh * 3.2);aspect-ratio:auto}.tile.span3{width:calc(21vh * 4.8);aspect-ratio:auto}.tile:after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(5,13,18,.7),transparent 64%)}.tile.light:after{background:linear-gradient(0deg,rgba(244,239,226,.9),transparent 64%)}.tile .tcopy{position:absolute;z-index:2;left:1.2vw;right:1.2vw;bottom:1.05vw}.tile h3{font-size:clamp(21px,2.2vw,38px);font-weight:400;line-height:.92;margin:.12em 0}.tile p{font-size:12px;line-height:1.35;max-width:430px;margin:.35em 0 0}.journal-t{background:radial-gradient(circle at 65% 40%,rgba(210,188,105,.42),transparent 25%),linear-gradient(135deg,#07131d,#24485b)}.cafe-t{background:linear-gradient(135deg,#f4efe2,#aaa18b);color:#252525}.prayer-t{background:radial-gradient(circle at 30% 30%,rgba(250,249,245,.35),transparent 24%),linear-gradient(145deg,#425337,#8b9c72)}.library-t{background:repeating-linear-gradient(90deg,rgba(0,0,0,.08) 0 1px,transparent 1px 17px),linear-gradient(135deg,#d2bc69,#8e6f25);color:#171713}.one-t{background:linear-gradient(140deg,#486f83,#102936)}.church-t{background:linear-gradient(140deg,#6f7d68,#263a2d)}.scripture-t{background:radial-gradient(circle at 70% 35%,rgba(206,189,116,.34),transparent 28%),linear-gradient(125deg,#07121c,#183444)}.nav-note{position:absolute;z-index:6;left:6vw;bottom:2.2vh;color:#cebd74}.nav-state{position:absolute;z-index:6;right:6vw;bottom:2.2vh;color:#cebd74}.live-nav:before{content:"";position:absolute;z-index:0;left:-15%;right:-15%;top:31%;height:26vh;border-radius:50%;background:radial-gradient(ellipse,rgba(206,189,116,.09),transparent 64%);filter:blur(18px);pointer-events:none}
@media(max-width:760px){.live-nav-head{height:27vh;grid-template-columns:1fr;padding-left:5vw;padding-right:5vw}.live-nav-head p{display:none}.live-water{height:67vh}.tile{height:18vh}.tile.span2{width:calc(18vh * 3.2)}.tile.span3{width:calc(18vh * 4.8)}.stream.a{top:3vh}.stream.b{top:25vh}.stream.c{top:47vh}.tile p{display:none}.tile .tcopy{left:12px;bottom:10px}.nav-note{left:5vw}.nav-state{right:5vw}}
@media(prefers-reduced-motion:reduce){.stream{transform:none!important}}
'''

NAV=r'''<section class="live-nav" id="liveNav"><div class="live-nav-stage"><header class="live-nav-head"><div><span class="index">LIVE WATER · NOW</span><h2>此刻，<br>值得看什麼。</h2></div><p>先看全站此刻最重要的內容。全部保持橫向；重量決定佔據多少 8:5 節拍，也決定它在水流裡移動得多慢。</p></header><div class="live-water">
<div class="stream a" data-rate="-0.34"><article class="tile scripture-t span2"><div class="tcopy"><span class="index">SCRIPTURE</span><h3>起初，光進入黑暗。</h3><p>最高權重內容更長、更慢，像河中的深水。</p></div></article><article class="tile cafe-t light"><div class="tcopy"><span class="index">DAYLIGHT CAFE</span><h3>Daylight Cafe</h3></div></article><article class="tile prayer-t"><div class="tcopy"><span class="index">WATCH PRAYER</span><h3>守望禱告</h3></div></article><article class="tile journal-t"><div class="tcopy"><span class="index">JOURNAL</span><h3>守望</h3></div></article></div>
<div class="stream b" data-rate="0.20"><article class="tile one-t"><div class="tcopy"><span class="index">ONE</span><h3>查經</h3></div></article><article class="tile library-t light span3"><div class="tcopy"><span class="index">DAWN LIBRARY · HEAVY</span><h3>黎明書局</h3><p>重要內容可連續佔據多個橫向節拍，但仍然留在同一條水流裡。</p></div></article><article class="tile church-t"><div class="tcopy"><span class="index">CHURCH</span><h3>Living Water</h3></div></article></div>
<div class="stream c" data-rate="-0.13"><article class="tile prayer-t span2"><div class="tcopy"><span class="index">PRAYER · SLOW</span><h3>你們要儆醒。</h3></div></article><article class="tile journal-t span2"><div class="tcopy"><span class="index">JOURNAL · FEATURE</span><h3>一座光明的城</h3></div></article><article class="tile cafe-t light"><div class="tcopy"><span class="index">CAFE</span><h3>共享</h3></div></article></div>
</div><div class="nav-note index">8:5 = HORIZONTAL RHYTHM · KEEP SCROLLING</div><div class="nav-state index">FLOW → SECTION WORLDS</div></div></section>'''

JS=r'''<script>(function(){const root=document.getElementById('liveNav');if(!root)return;const streams=[...root.querySelectorAll('.stream')];function move(){const r=root.getBoundingClientRect(),span=Math.max(1,root.offsetHeight-innerHeight),p=Math.min(1,Math.max(0,-r.top/span));streams.forEach((s,i)=>{const rate=parseFloat(s.dataset.rate||0);const travel=Math.min(innerWidth*.62,760);const base=i===1?-innerWidth*.28:-innerWidth*.08;s.style.setProperty('--x',(base+p*travel*rate*3)+'px')})}addEventListener('scroll',move,{passive:true});addEventListener('resize',move);move()})();</script>'''

def render(edit=False):
    html=c01.render(edit=edit)
    html=html.replace('</style>',CSS+'</style>',1)
    marker='<section class="world dark">'
    html=html.replace(marker,NAV+marker,1)
    html=html.replace('</body>',JS+'</body>',1)
    html=html.replace('<title>Living Water · Candidate 01</title>','<title>Living Water · Candidate 04</title>',1)
    html=html.replace('DORÉ DESIGN · LIVING WATER · CANDIDATE 01','DORÉ DESIGN · LIVING WATER · CANDIDATE 04',1)
    return html
