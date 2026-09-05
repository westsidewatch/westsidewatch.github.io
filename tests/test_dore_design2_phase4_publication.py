import copy,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'dore-design'))
import design2_publication,design2_renderer,design2_snapshot


def workspace(rev,text):
    return {'id':'ws','revision':rev,'tokens':{'paper':'#fff'},'pages':[{'id':'home','name':'Home','canvas':{'width':800,'height':600},'nodes':[{'id':'t1','type':'text','x':10,'y':20,'w':300,'h':40,'size':32,'text':text,'text_align':'left'}]}]}


def test_candidate_is_immutable_when_workspace_changes(tmp_path):
    reg=tmp_path/'publication.json'
    w=workspace(7,'First')
    c=design2_publication.create_candidate(w,'home',reg)
    w['pages'][0]['nodes'][0]['text']='Changed after snapshot'
    html=design2_renderer.render_snapshot(c['snapshot'])
    assert 'First' in html
    assert 'Changed after snapshot' not in html
    assert design2_snapshot.verify(c['snapshot'])


def test_publish_and_rollback_preserve_previous_release(tmp_path):
    reg=tmp_path/'publication.json'
    c1=design2_publication.create_candidate(workspace(1,'One'),'home',reg)
    r1=design2_publication.promote(c1['id'],reg)
    c2=design2_publication.create_candidate(workspace(2,'Two'),'home',reg)
    r2=design2_publication.promote(c2['id'],reg)
    assert r2['previous']['candidate_id']==c1['id']
    restored=design2_publication.rollback(reg)
    assert restored['candidate_id']==c1['id']
    state=json.loads(reg.read_text())
    assert state['current_release']['candidate_id']==c1['id']
