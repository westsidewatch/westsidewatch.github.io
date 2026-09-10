"""Doré Design P1 — accepted 8:5 motion, Living Water content substitution."""
PAGE_ID='motion-p1-living-current'

def _page():
    return {'id':PAGE_ID,'name':'Motion · P1 Reading Core','canvas':{'w':1440,'h':960},'nodes':[],'design_experiment':{'schema':'dore.design-experiment.v1','track':'motion-language','prototype':'P1','status':'prototype','source':'accepted-8x5-codrops-adaptation','principles':['lock-motion','8x5','site-content-only','content-substitution']}}

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

def _card(kind,title,weight,preview):
    safe=preview.replace('&','&amp;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')
    return '<button class="flow-card w%s" data-kind="%s" data-title="%s" data-preview="%s"><span>%s</span><strong>%s</strong></button>'%(weight,kind,title,safe,kind,title)

def _streams():
    rows=[
      [('ONE','馬太福音第七章',2,'不要論斷、祈求尋找叩門、窄門、兩種根基。'),('JOURNAL','米斯巴',1,'在守望中辨認正在發生的事。'),('JOURNAL','Feature',2,'較長篇幅的主題閱讀與編輯策展。'),('ONE','四福音合參',1,'把四福音的平行經文放回同一條敘事線。')],
      [('DAWN LIBRARY','黎明書局',3,'從經文開始，讓工具服務研讀，讓資源進入生命。'),('JOURNAL','頌讚',1,'詩歌、讚美與敬拜內容。'),('ONE','本章故事',2,'先以故事進入一章，再展開背景、歷史與串珠。'),('JOURNAL','看見',1,'讓值得被看見的內容自然浮現。')],
      [('JOURNAL','以琳',1,'停留、補給與閱讀。'),('ONE','馬太福音第六章',2,'天父、主禱文、先求祂的國和祂的義。'),('JOURNAL','伯特利 · 查經',2,'從經文出發，進入查考與分享。'),('WESTSIDE WATCH','Watch for the Dawn',2,'黑夜已深，白晝將近。')],
      [('JOURNAL','以斯帖 · 見證人',2,'人物與見證在閱讀流中經過。'),('JOURNAL','守望者 · 對話',1,'對話與辨認形成另一種閱讀節奏。'),('JOURNAL','安提阿',1,'教會、差遣與群體。'),('JOURNAL','瑪拉拿 · 禱告',3,'主啊，我願你來。等待不是空白，內容仍然前行。')]
    ]
    out=[]
    for i,row in enumerate(rows):
        seq=''.join(_card(*x) for x in row)
        out.append('<div class="current c%s"><div class="current-loop">%s</div><div class="current-loop" aria-hidden="true">%s</div></div>'%(i+1,seq,seq))
    return ''.join(out)

def render_p1(edit=False):
    badge='<div class="badge">DORÉ DESIGN · P1 · 8:5 SITE CONTENT</div>' if edit else ''
    streams=_streams()
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Living Water · Reading Current</title><style>
*{box-sizing:border-box}html,body{margin:0;background-image:linear-gradient(rgba(206,189,116,.72),rgba(206,189,116,.72)),url("/api/dore/assets/site-file?code=SITE-BACKGROUND");background-size:cover;background-position:center;background-attachment:fixed;color:#252525;font-family:"Cormorant Garamond","Noto Serif TC",serif}.badge{position:fixed;z-index:99;top:10px;left:10px;background:rgba(239,228,185,.88);border:1px solid rgba(37,37,37,.35);padding:7px 9px;font:9px ui-monospace,monospace}.fusion{height:100svh;min-height:680px;position:relative;overflow:hidden}.flow-field{position:absolute;inset:0;overflow:hidden}.current{position:absolute;left:-10vw;display:flex;gap:14px;width:max-content;min-width:220vw;will-change:transform;transition:opacity .35s,filter .35s}.current-loop{display:flex;gap:14px;flex:0 0 auto;padding-right:14px}.c1{top:4%;animation:drift1 44s linear infinite}.c2{top:28%;animation:drift2 57s linear infinite}.c3{top:52%;animation:drift3 49s linear infinite}.c4{top:76%;animation:drift4 64s linear infinite}.flow-card{aspect-ratio:8/5;height:19vh;min-height:118px;width:auto;flex:0 0 auto;border:1px solid rgba(142,104,23,.36);background:linear-gradient(135deg,rgba(247,239,210,.94),rgba(205,188,126,.74));color:#252525;text-align:left;padding:13px;cursor:pointer;position:relative;overflow:hidden;transition:.22s;box-shadow:0 10px 26px rgba(70,53,19,.10)}.flow-card.w2{width:calc((19vh * 1.6) * 2 + 14px)}.flow-card.w3{width:calc((19vh * 1.6) * 3 + 28px)}.flow-card span,.flow-card strong{display:block}.flow-card span{font:8px ui-monospace,monospace;color:#8e6817;letter-spacing:.12em}.flow-card strong{font-size:22px;font-weight:400;margin-top:8px}.flow-card.w2 strong{font-size:29px}.flow-card.w3 strong{font-size:34px}.flow-card.selected{border-color:#8e6817;transform:translateY(-4px)}.focus-stage{position:absolute;z-index:20;right:2.5%;top:6%;width:50%;height:88%;pointer-events:none;opacity:0;transition:opacity .18s;box-shadow:0 20px 52px rgba(71,52,16,.22);background:linear-gradient(135deg,#8e6817,#d6c47f,#5f4c20);overflow:hidden}.fusion.focused .focus-stage{opacity:1;pointer-events:auto}.fusion.focused .current{opacity:.34;filter:grayscale(1) contrast(.92)}.focus-copy{position:absolute;z-index:5;left:6%;right:6%;bottom:7%}.focus-kicker{font:9px ui-monospace,monospace;letter-spacing:.16em;color:#f0d989}.focus-title{font-size:clamp(34px,4.6vw,68px);line-height:.94;font-weight:400;margin:.10em 0 .28em;color:#fffaf0;text-shadow:0 2px 20px #000}.reading-viewport{overflow:hidden;height:104px;padding-top:13px}.reading-current{display:flex;width:max-content;gap:42px;animation:readX 24s linear infinite}.reading-item{width:330px;flex:0 0 auto;font-size:16px;line-height:1.52;color:#fffaf0;text-shadow:0 2px 15px #000}.clear{position:absolute;z-index:30;right:14px;top:14px;border:1px solid rgba(142,104,23,.58);background:rgba(239,228,185,.84);padding:8px 11px;cursor:pointer;opacity:0;pointer-events:none}.fusion.focused .clear{opacity:1;pointer-events:auto}@keyframes readX{to{transform:translateX(-50%)}}@keyframes drift1{to{transform:translateX(-28vw)}}@keyframes drift2{from{transform:translateX(-22vw)}to{transform:translateX(4vw)}}@keyframes drift3{from{transform:translateX(6vw)}to{transform:translateX(-24vw)}}@keyframes drift4{from{transform:translateX(-18vw)}to{transform:translateX(8vw)}}@media(max-width:760px){.flow-card{height:92px}.focus-stage{left:4%;right:4%;width:auto;top:9%;height:82%}.focus-title{font-size:38px}.reading-item{width:260px;font-size:14px}}@media(prefers-reduced-motion:reduce){.current,.reading-current{animation:none!important}}
</style></head><body>'''+badge+'''<main class="fusion" id="fusion"><div class="flow-field">'''+streams+'''</div><div class="focus-stage" id="focusStage"><div class="focus-copy"><div class="focus-kicker" id="fk"></div><h1 class="focus-title" id="ft"></h1><div class="reading-viewport"><div class="reading-current" id="readingCurrent"></div></div></div></div><button class="clear" id="clear">清除</button></main><script>
(function(){var fusion=document.getElementById('fusion'),reading=document.getElementById('readingCurrent'),cards=[].slice.call(document.querySelectorAll('.flow-card')),hoverMode=matchMedia('(hover:hover) and (pointer:fine)').matches,timer=0;function esc(s){var d=document.createElement('div');d.textContent=s||'';return d.innerHTML}function activate(c){cards.forEach(function(x){x.classList.toggle('selected',x.dataset.title===c.dataset.title)});fusion.classList.add('focused');document.getElementById('fk').textContent=c.dataset.kind;document.getElementById('ft').textContent=c.dataset.title;var peers=cards.filter(function(x){return x!==c&&!x.closest('[aria-hidden="true"]')}).slice(0,2),arr=[c].concat(peers),one=arr.map(function(x){return '<div class="reading-item"><b>'+esc(x.dataset.title)+'</b><br>'+esc(x.dataset.preview)+'</div>'}).join('');reading.innerHTML=one+one}function reset(){fusion.classList.remove('focused');cards.forEach(function(x){x.classList.remove('selected')})}cards.forEach(function(c){c.addEventListener('mouseenter',function(){if(!hoverMode)return;clearTimeout(timer);timer=setTimeout(function(){activate(c)},100)});c.addEventListener('click',function(){activate(c)})});document.getElementById('clear').onclick=reset;})();
</script></body></html>'''
