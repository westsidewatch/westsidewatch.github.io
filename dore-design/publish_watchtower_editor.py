#!/usr/bin/env python3
from pathlib import Path
import datetime
import json

HOME = Path.home() / '.dore' / 'design'
HOME.mkdir(parents=True, exist_ok=True)
WS = HOME / 'westside-watch.workspace.json'
HIST = HOME / 'workspace-history'
HIST.mkdir(exist_ok=True)
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

DEFAULT = {
    'schema': 'dore.design.workspace.v1',
    'id': 'westside-watch',
    'name': 'Westside Watch — Doré Design',
    'revision': 1,
    'updated_at': NOW,
    'tokens': {
        'paper': '#FAF9F5', 'ink': '#252525', 'night': '#102A43',
        'gold': '#A2872A', 'morning': '#D2BC69'
    },
    'pages': []
}

w = json.loads(WS.read_text(encoding='utf-8')) if WS.exists() else DEFAULT
rev = int(w.get('revision', 1))
if WS.exists():
    backup = HIST / f'westside-watch.r{rev:05d}.json'
    if not backup.exists():
        backup.write_text(json.dumps(w, ensure_ascii=False, indent=2), encoding='utf-8')

pid = 'new-westside-watchtower-fold'
page = {
    'id': pid,
    'name': 'New Westside · Watchtower Fold',
    'canvas': {'w': 1440, 'h': 1000},
    'experimental_only': True,
    'product_acceptance': False,
    'style_acceptance': False,
    'nodes': [
        {'id':'wt-kicker','type':'text','text':'WESTSIDE WATCH · VAUGHAN / TORONTO','x':40,'y':28,'w':430,'size':14},
        {'id':'wt-zh','type':'text','text':'西望','x':670,'y':24,'w':110,'size':25},
        {'id':'wt-rule-top','type':'rule','x':28,'y':60,'w':1384,'h':1},
        {'id':'wt-eyebrow','type':'text','text':'01 / A PLACE OF WATCHING   ·   ROM 13:12','x':42,'y':100,'w':510,'size':14},
        {'id':'wt-title','type':'text','role':'hero','text':'WATCH\nFOR THE\nDAWN.','x':42,'y':170,'w':530,'size':112},
        {'id':'wt-title-zh','type':'text','text':'守望黎明','x':48,'y':555,'w':360,'size':55},
        {'id':'wt-deck','type':'text','text':'在黑夜仍然守望，在清晨尚未來到以前保存光。\n文章、聖經、教會生活與研究，不是五個並列的按鈕，\n而是一座可以行走的城。','x':48,'y':690,'w':500,'size':23},
        {'id':'wt-threshold','type':'block','x':650,'y':105,'w':720,'h':720,'eyebrow':'A CITY BEFORE MORNING · 五個入口','title':'THRESHOLD CITY','body':'一條在黑暗中被晨光切開的行走路徑。'},
        {'id':'wt-dawn-axis','type':'rule','x':795,'y':125,'w':4,'h':650},
        {'id':'wt-journal','type':'text','text':'01   JOURNAL\n守望，一座光明的城','x':735,'y':245,'w':520,'size':42},
        {'id':'wt-one','type':'text','text':'02   ONE\n逐卷逐章查考聖經','x':865,'y':355,'w':430,'size':38},
        {'id':'wt-church','type':'text','text':'03   LIVING WATER WEST\n教會生活與聚會','x':705,'y':470,'w':530,'size':36},
        {'id':'wt-library','type':'text','text':'04   黎明書局\n閱讀、研究與資源','x':905,'y':585,'w':390,'size':38},
        {'id':'wt-gate','type':'text','text':'05   THE GATE\n進入西區守望','x':790,'y':700,'w':430,'size':38},
        {'id':'wt-verse-rule','type':'rule','x':28,'y':850,'w':1384,'h':1},
        {'id':'wt-verse','type':'text','role':'hero','text':'THE NIGHT IS FAR SPENT,\nTHE DAY IS AT HAND.','x':42,'y':880,'w':680,'size':44},
        {'id':'wt-note','type':'text','text':'Experimental only · no user style acceptance · no production promotion','x':860,'y':925,'w':500,'size':13}
    ]
}

w['pages'] = [p for p in w.setdefault('pages', []) if p.get('id') != pid] + [page]
w['revision'] = rev + 1
w['updated_at'] = NOW
TMP = WS.with_suffix('.tmp')
TMP.write_text(json.dumps(w, ensure_ascii=False, indent=2), encoding='utf-8')
TMP.replace(WS)

check = json.loads(WS.read_text(encoding='utf-8'))
found = next((p for p in check.get('pages', []) if p.get('id') == pid), None)
assert found and len(found.get('nodes', [])) == 17
assert found.get('experimental_only') is True
assert found.get('product_acceptance') is False
assert found.get('style_acceptance') is False
print(json.dumps({
    'ok': True,
    'code': 'WATCHTOWER_EDITOR_PAGE_PUBLISHED',
    'workspace': str(WS),
    'page_id': pid,
    'page_name': found['name'],
    'revision': check['revision'],
    'node_count': len(found['nodes'])
}, ensure_ascii=False))
