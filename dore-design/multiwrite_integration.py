"""Multiwrite design surface for the existing DORÉ DESIGN workspace.

This module deliberately extends the established workspace instead of creating
another editor. It migrates one Multiwrite homepage specimen into Pages and
adds semantic design decisions that can be edited from the normal inspector.
"""
import copy

PAGE_ID = 'multiwrite-home'
SURFACE = 'multiwrite.home.product-story'
COLORS = {
    'paper': '#F5EEDB',
    'first-light': '#CEBD74',
    'watch-night': '#26241F',
    'olive': '#7A7B57',
}
TITLE_SIZES = {'quiet': 32, 'equal': 42, 'display': 62}
RECOMMENDED = {'color': 'paper', 'hierarchy': 'quiet', 'axis': 'center', 'density': '1', 'lines': '1'}
REASONS = {
    'paper': '紙承載正文；讓首屏的金保有稀缺性。',
    'first-light': '初光適合顯現、入口與高價值強調；不宜讓整頁都成為同一強度。',
    'watch-night': '守望夜提供戲劇性與高對比，但會把第二頁推成新的主角。',
    'olive': '橄欖帶生命與安息語義；適合生長、群體與恢復相關內容。',
}


def _decision(d=None):
    out = copy.deepcopy(RECOMMENDED)
    if isinstance(d, dict):
        for k in out:
            if k in d:
                out[k] = str(d[k])
    if out['color'] not in COLORS: out['color'] = 'paper'
    if out['hierarchy'] not in TITLE_SIZES: out['hierarchy'] = 'quiet'
    if out['axis'] not in {'center', 'left'}: out['axis'] = 'center'
    if out['density'] not in {'0', '1', '2'}: out['density'] = '1'
    if out['lines'] not in {'0', '1', '2'}: out['lines'] = '1'
    return out


def _reasoning(d):
    return {
        'color': REASONS[d['color']],
        'hierarchy': '首頁第二屏應低於首屏品牌宣言。' if d['hierarchy'] == 'quiet' else '此層級提高第二屏的展示權重。',
        'axis': '延續 Gate 的中央軸傳統。' if d['axis'] == 'center' else '採用編輯式偏置以增加雜誌感。',
        'principle': '顏色先服從 section 的品牌敘事角色，再決定具體色值。',
    }


def _design(d=None):
    d = _decision(d)
    return {
        'schema': 'dore.design-decision.v1',
        'surface': SURFACE,
        'decision': d,
        'reasoning': _reasoning(d),
        'recommended': copy.deepcopy(RECOMMENDED),
    }


def _page():
    # 1200×2280 follows the established DORÉ DESIGN long-page canvas shown in the workspace.
    nodes = [
        {'id':'mw-brand','type':'text','text':'DORÉ','x':540,'y':88,'w':120,'size':14,'semantic_zone':'hero'},
        {'id':'mw-corner-lt','type':'text','text':'WORDS\nENDURE\nBEYOND\nTIME','x':72,'y':90,'w':150,'size':13,'semantic_zone':'hero'},
        {'id':'mw-corner-rt','type':'text','text':'FAITH\nWRITES\nHISTORY\nSTILL','x':978,'y':90,'w':150,'size':13,'semantic_zone':'hero'},
        {'id':'mw-title','type':'text','role':'hero','text':'多寫','x':430,'y':210,'w':340,'size':104,'semantic_zone':'hero'},
        {'id':'mw-slogan','type':'text','text':'讓所寫的，成為書。\nWrite on. Make it a book.','x':390,'y':370,'w':420,'size':25,'semantic_zone':'hero'},
        {'id':'mw-psalm','type':'text','text':'「我心裡湧出美辭；我論到我為王做的事；我的舌頭是快手筆。」\n“My heart is inditing a good matter: I speak of the things which I have made touching the king: my tongue is the pen of a ready writer.”\n詩篇 45:1 · Psalm 45:1','x':285,'y':505,'w':630,'size':16,'semantic_zone':'hero'},
        {'id':'mw-intro','type':'text','text':'一本書，不必等到最後才成為書。從第一行開始，它就在這裡有章節、有版本，也有回去的路。','x':350,'y':700,'w':500,'size':16,'semantic_zone':'hero'},
        {'id':'mw-corner-lb','type':'text','text':'TAKE\nNO THOUGHT\nFOR THE\nMORROW','x':72,'y':840,'w':170,'size':13,'semantic_zone':'hero'},
        {'id':'mw-scroll','type':'text','text':'SCROLL\n⌄','x':550,'y':870,'w':100,'size':12,'semantic_zone':'hero'},
        {'id':'mw-corner-rb','type':'text','text':'SOLI\nDEO\nGLORIA','x':1010,'y':840,'w':120,'size':13,'semantic_zone':'hero'},
        {'id':'mw-story-bg','type':'block','eyebrow':'','title':'','body':'','x':0,'y':1010,'w':1200,'h':650,'semantic_zone':'story-bg'},
        {'id':'mw-story-kicker','type':'text','text':'01\nTHE WRITING PLACE','x':420,'y':1080,'w':360,'size':14,'semantic_zone':'story'},
        {'id':'mw-story-title','type':'text','text':'寫作、閱讀與成書，\n在同一個地方發生。','x':340,'y':1170,'w':520,'size':32,'semantic_zone':'story-title'},
        {'id':'mw-story-body','type':'text','text':'不是先寫成一份文件，再把文件交給出版。你打開的是正在成形的書；讀到哪裡，就可以從哪裡繼續。','x':350,'y':1310,'w':500,'size':16,'semantic_zone':'story'},
        {'id':'mw-path-return','type':'text','text':'I\n回歸\n多年以前寫下的，不必重新開始。原稿仍是原稿。','x':115,'y':1460,'w':270,'size':16,'semantic_zone':'story'},
        {'id':'mw-path-update','type':'text','text':'II\n更新\n章節不是檔案清單，而是一本可以閱讀的書。','x':465,'y':1460,'w':270,'size':16,'semantic_zone':'story'},
        {'id':'mw-path-book','type':'text','text':'III\n成書\n字體、紙張、頁邊與輸出，都從同一份書稿出發。','x':815,'y':1460,'w':270,'size':16,'semantic_zone':'story'},
        {'id':'mw-library-rule','type':'rule','x':110,'y':1770,'w':980,'h':1,'semantic_zone':'library'},
        {'id':'mw-library','type':'text','text':'MY LIBRARY\n我的書\n每一本都從這裡打開。正在寫的、從舊稿匯入的，都留在同一座書庫裡。','x':180,'y':1840,'w':840,'size':24,'semantic_zone':'library'},
    ]
    return {
        'id': PAGE_ID,
        'name': '多寫 · Homepage',
        'canvas': {'w': 1200, 'h': 2280},
        'nodes': nodes,
        'product': 'multiwrite',
        'design': _design(),
    }


def install_workspace(base):
    """Patch the established workspace in place; do not create another app."""
    original_workspace = base.workspace
    original_mutate = base.mutate

    def workspace():
        w = original_workspace()
        if not any(p.get('id') == PAGE_ID for p in w.get('pages', [])):
            w['pages'].append(_page())
            w = base.save(w)
        else:
            p = next(p for p in w['pages'] if p.get('id') == PAGE_ID)
            if not isinstance(p.get('design'), dict):
                p['design'] = _design()
                w = base.save(w)
        return w

    def mutate(w, payload):
        if payload.get('op') != 'design_decision':
            return original_mutate(w, payload)
        pid = payload.get('page_id')
        p = next((x for x in w.get('pages', []) if x.get('id') == pid), None)
        if not p: raise ValueError('page_not_found')
        if pid != PAGE_ID: raise ValueError('semantic_design_not_supported')
        d = _decision(payload.get('decision'))
        p['design'] = _design(d)
        title = next((n for n in p.get('nodes', []) if n.get('id') == 'mw-story-title'), None)
        if title: title['size'] = TITLE_SIZES[d['hierarchy']]
        return base.save(w)

    base.workspace = workspace
    base.mutate = mutate


def augment_html(html):
    panel = '''<div id="doreSemantic" hidden><h3>DORÉ · Semantic Design</h3><div class="semantic-card"><div class="small">多寫 · Product Story</div><label>Background role<select id="sdColor"><option value="paper">Living Paper</option><option value="first-light">First Light</option><option value="watch-night">Watch Night</option><option value="olive">Olive</option></select></label><label>Title hierarchy<select id="sdHierarchy"><option value="quiet">Quiet</option><option value="equal">Equal</option><option value="display">Display</option></select></label><label>Axis<select id="sdAxis"><option value="center">Centered · Gate tradition</option><option value="left">Editorial left</option></select></label><label>Density<select id="sdDensity"><option value="0">Compact</option><option value="1">Balanced</option><option value="2">Airy</option></select></label><label>Lines<select id="sdLines"><option value="0">None</option><option value="1">Quiet</option><option value="2">Strong</option></select></label><button onclick="applyDoreRecommendation()">DORÉ RECOMMENDS</button><button onclick="saveSemanticDesign()">Apply</button><p id="sdReason" class="small"></p></div></div>'''
    if '<h3>Verification</h3>' not in html:
        raise RuntimeError('multiwrite_semantic_panel_marker_missing')
    html = html.replace('<h3>Verification</h3>', panel + '<h3>Verification</h3>', 1)
    css = '''.semantic-card{border:1px solid #c9c5b9;background:#fff;padding:10px;margin:6px 0 12px}.semantic-card label{display:block;font-size:11px;margin:8px 0}.semantic-card select{width:100%;margin-top:3px;padding:5px}.semantic-card button{margin:4px 4px 0 0}.semantic-card #sdReason{line-height:1.45;margin-top:8px}'''
    html = html.replace('</style>', css + '</style>', 1)
    script = r'''<script>(function(){const MW='multiwrite-home',REC={color:'paper',hierarchy:'quiet',axis:'center',density:'1',lines:'1'},BG={paper:'#F5EEDB','first-light':'#CEBD74','watch-night':'#26241F',olive:'#7A7B57'},WHY={paper:'紙承載正文；讓首屏的金保有稀缺性。','first-light':'初光適合顯現、入口與高價值強調。','watch-night':'守望夜提供戲劇性，但會把第二頁推成新的主角。',olive:'橄欖帶生命與安息語義。'};function decision(){return {color:sdColor.value,hierarchy:sdHierarchy.value,axis:sdAxis.value,density:sdDensity.value,lines:sdLines.value}}function sync(p){let box=document.getElementById('doreSemantic');if(!box)return;box.hidden=p?.id!==MW;if(box.hidden)return;let d=p.design?.decision||REC;sdColor.value=d.color;sdHierarchy.value=d.hierarchy;sdAxis.value=d.axis;sdDensity.value=d.density;sdLines.value=d.lines;sdReason.textContent=(p.design?.reasoning?.color||WHY[d.color])+' '+(p.design?.reasoning?.axis||'');let stageEl=document.querySelector('#stage .stage');if(!stageEl)return;let els=[...stageEl.querySelectorAll('.node')];p.nodes.forEach((n,i)=>{let e=els[i];if(!e)return;if(n.semantic_zone==='story-bg'){e.style.background=BG[d.color];e.style.borderTop='1px solid rgba(80,60,20,.15)';e.style.padding=0;e.style.zIndex='0'}else if(n.semantic_zone==='story'||n.semantic_zone==='story-title'){e.style.zIndex='1';e.style.textAlign=d.axis==='center'?'center':'left';if(n.semantic_zone==='story-title')e.style.fontSize=({quiet:32,equal:42,display:62}[d.hierarchy])+'px'}if(n.semantic_zone==='story'){e.style.lineHeight=d.density==='0'?'1.2':d.density==='2'?'1.7':'1.45'}})}window.saveSemanticDesign=async function(){w=await api('/api/workspace',{op:'design_decision',page_id:active,decision:decision()});render()};window.applyDoreRecommendation=async function(){sdColor.value=REC.color;sdHierarchy.value=REC.hierarchy;sdAxis.value=REC.axis;sdDensity.value=REC.density;sdLines.value=REC.lines;await saveSemanticDesign()};const oldRender=render;render=function(){oldRender();sync(pg())};})();</script>'''
    return html.replace('</body>', script + '</body>', 1)
