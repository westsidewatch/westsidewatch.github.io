import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'dore-design'))
import design2_commands,design2_phase3_shell

def workspace():
    return {'revision':1,'pages':[{'id':'p','nodes':[{'id':'a','type':'text','x':0,'y':0,'w':100,'h':20,'size':20,'text':'A'},{'id':'b','type':'text','x':200,'y':100,'w':100,'h':20,'size':20,'text':'B'},{'id':'c','type':'text','x':400,'y':200,'w':100,'h':20,'size':20,'text':'C'}]}]}

def test_patch_and_nudge_are_document_mutations():
    w=workspace();m=design2_commands.apply(w,{'op':'node.patch','page_id':'p','id':'a','patch':{'x':25,'size':24}})
    assert w['pages'][0]['nodes'][0]['x']==0
    assert m['pages'][0]['nodes'][0]['x']==25
    m=design2_commands.apply(m,{'op':'node.nudge','page_id':'p','ids':['a'],'dx':5,'dy':-2})
    assert (m['pages'][0]['nodes'][0]['x'],m['pages'][0]['nodes'][0]['y'])==(30,-2)

def test_align_and_distribute_use_document_coordinates():
    w=workspace();m=design2_commands.apply(w,{'op':'node.align','page_id':'p','ids':['a','b'],'edge':'left'})
    assert m['pages'][0]['nodes'][1]['x']==0
    m=design2_commands.apply(w,{'op':'node.distribute','page_id':'p','ids':['a','b','c'],'axis':'horizontal'})
    assert [n['x'] for n in m['pages'][0]['nodes']]==[0,200.0,400.0]

def test_phase3_shell_preserves_three_pane_editor():
    html='<html><head></head><body><div class="work"><aside></aside><main class="canvaswrap"></main><aside class="right"></aside></div>DORÉ DESIGN 1.9 · PROMOTION PIPELINE</body></html>'
    out=design2_phase3_shell.augment(html)
    assert 'DIRECT-MANIPULATION WORKBENCH' in out
    assert 'PHASE 3 · CANONICAL CANVAS' in out
    assert 'grid-template-columns:var(--d2-left)' in out
