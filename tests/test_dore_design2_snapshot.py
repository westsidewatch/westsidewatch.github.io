import copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'dore-design'))
import design2_snapshot

def ws():
    return {'id':'w1','revision':12,'tokens':{'gold':'#cebd74'},'pages':[{'id':'multiwrite-home','name':'Home','nodes':[{'id':'t1','type':'text','text':'Hello','x':10,'y':20}]}]}

def test_snapshot_is_revision_bound_and_verifiable():
    s=design2_snapshot.snapshot(ws(),'multiwrite-home')
    assert s['revision']==12
    assert s['page_id']=='multiwrite-home'
    assert design2_snapshot.verify(s)

def test_snapshot_is_detached_from_mutable_workspace():
    w=ws();s=design2_snapshot.snapshot(w,'multiwrite-home')
    w['pages'][0]['nodes'][0]['text']='Changed'
    assert s['page']['nodes'][0]['text']=='Hello'
    assert design2_snapshot.verify(s)

def test_snapshot_detects_tampering():
    s=design2_snapshot.snapshot(ws(),'multiwrite-home')
    bad=copy.deepcopy(s);bad['page']['nodes'][0]['text']='tampered'
    assert not design2_snapshot.verify(bad)
