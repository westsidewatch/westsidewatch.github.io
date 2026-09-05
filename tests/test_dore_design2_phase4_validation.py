import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'dore-design'))
import design2_publication,design2_snapshot,design2_validation


def ws(node):
    return {'id':'ws','revision':3,'pages':[{'id':'home','nodes':[node]}]}


def test_rejects_executable_url_scheme():
    snap=design2_snapshot.snapshot(ws({'id':'a','type':'text','text':'x','href':'javascript:alert(1)'}),'home')
    result=design2_validation.validate_snapshot(snap)
    assert not result['ok']
    assert any('unsafe_url' in e for e in result['errors'])


def test_rejects_duplicate_node_ids():
    w={'id':'ws','revision':4,'pages':[{'id':'home','nodes':[{'id':'a','type':'text','text':'1'},{'id':'a','type':'text','text':'2'}]}]}
    result=design2_validation.validate_snapshot(design2_snapshot.snapshot(w,'home'))
    assert 'duplicate_node_id' in result['errors']


def test_candidate_validation_is_persisted(tmp_path):
    row=design2_publication.create_candidate(ws({'id':'a','type':'text','text':'safe','href':'/about'}),'home',tmp_path/'r.json')
    assert row['status']=='validated'
    assert row['validation']['ok'] is True
