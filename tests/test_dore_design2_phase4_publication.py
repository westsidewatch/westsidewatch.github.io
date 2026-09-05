import json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'dore-design'))
import design2_publication,design2_renderer,design2_snapshot,design2_staging


def workspace(rev,text):
    return {'id':'ws','revision':rev,'tokens':{'paper':'#fff'},'pages':[{'id':'homepage','name':'Home','canvas':{'width':800,'height':600},'nodes':[{'id':'t1','type':'text','x':10,'y':20,'w':300,'h':40,'size':32,'text':text,'text_align':'left'}]}]}


def manifest(candidate):
    html=design2_renderer.render_snapshot(candidate['snapshot'])
    return design2_staging.build_manifest(candidate,'homepage',html)


def test_candidate_is_immutable_when_workspace_changes(tmp_path):
    reg=tmp_path/'publication.json'
    w=workspace(7,'First')
    c=design2_publication.create_candidate(w,'homepage',reg)
    w['pages'][0]['nodes'][0]['text']='Changed after snapshot'
    html=design2_renderer.render_snapshot(c['snapshot'])
    assert 'First' in html
    assert 'Changed after snapshot' not in html
    assert design2_snapshot.verify(c['snapshot'])


def test_publish_and_rollback_preserve_previous_release(tmp_path):
    reg=tmp_path/'publication.json'
    c1=design2_publication.create_candidate(workspace(1,'One'),'homepage',reg)
    r1=design2_publication.promote(c1['id'],reg,manifest(c1))
    c2=design2_publication.create_candidate(workspace(2,'Two'),'homepage',reg)
    r2=design2_publication.promote(c2['id'],reg,manifest(c2))
    assert r2['previous']['candidate_id']==c1['id']
    restored=design2_publication.rollback(reg)
    assert restored['candidate_id']==c1['id']
    state=json.loads(reg.read_text())
    assert state['current_release']['candidate_id']==c1['id']


def test_staging_manifest_locks_target_and_render_hash(tmp_path):
    reg=tmp_path/'publication.json'
    c=design2_publication.create_candidate(workspace(3,'Three'),'homepage',reg)
    html=design2_renderer.render_snapshot(c['snapshot'])
    m=design2_staging.build_manifest(c,'homepage',html)
    assert design2_staging.same_render(m,html)
    assert not design2_staging.same_render(m,html+'changed')
