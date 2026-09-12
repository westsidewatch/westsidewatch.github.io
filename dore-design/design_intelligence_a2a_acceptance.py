#!/usr/bin/env python3
"""Deterministic acceptance for executable Design -> Core/A2A exploration."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


def base_snapshot():
    return {
        'schema':'dore.design.publish-snapshot.v1','workspace_id':'acceptance','revision':1,'page_id':'sandbox-page',
        'page':{'id':'sandbox-page','canvas':{'w':1200,'h':800},'nodes':[
            {'id':'hero','type':'text','text':'WATCH FOR THE DAWN','x':100,'y':120,'w':760,'h':110,'size':72,'text_align':'left'},
            {'id':'rule','type':'rule','x':100,'y':270,'w':900,'h':1},
        ]},'tokens':{},'sha256':'acceptance-base','created_at':0,
    }


def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        os.environ['DORE_LOCAL_HOME']=str(root/'home')
        os.environ['DORE_UI_TASTE_DB']=str(root/'taste.sqlite3')
        os.environ['DORE_DESIGN_A2A_FIXTURE']='1'
        os.environ['DORE_DESIGN_A2A_TIMEOUT']='60'
        os.environ.pop('DORE_DESIGN_A2A_DISAGREE_FIXTURE',None)

        import importlib
        import a2a_execution_plane
        import design_intelligence_a2a
        import design_intelligence_runtime
        importlib.reload(a2a_execution_plane); importlib.reload(design_intelligence_a2a)

        payload={
            'surface_id':'candidate-01-page2','surface_family':'living-water-candidate',
            'task_context':'repair four-pane assembly hierarchy without changing the accepted motion language',
            'primary_axis':'visual-hierarchy','viewport_context':'desktop-1440','content_context':'four-pane-focus-current',
            'constraints':['preserve 8:5 identity','preserve accepted motion','no production promotion'],
            'candidates':['seed-A','seed-B'],'base_snapshot':base_snapshot(),
        }
        before=design_intelligence_runtime.route_task(payload); assert before['decision']=='explore',before
        out=design_intelligence_a2a.explore(payload)
        assert out['ok'] and out['decision']=='explore' and out['a2a_status']=='PASS' and out['completion_evidence'] is True
        assert out['inference_boundary']=='core-a2a-only' and out['production_promoted'] is False
        assert out['provider']=='deterministic-ci-fixture' and [v['id'] for v in out['variants']]==['A','B']
        assert len(out['candidates'])==2 and out['candidate_evidence']=='executable-sandbox-render+geometry'
        assert out['canonical_workspace_mutated'] is False
        assert all(c['schema']=='dore.design.sandbox-candidate.v1' for c in out['candidates'])
        assert all(c['render_sha256'] and c['rendered_html'].startswith('<!doctype html>') for c in out['candidates'])
        assert all(c['geometry']['node_count']==2 and c['canonical_workspace_mutated'] is False for c in out['candidates'])
        assert out['candidates'][0]['render_sha256'] != out['candidates'][1]['render_sha256']
        assert out['judge_count']==2 and out['blind_order_reversal'] is True and out['consensus'] is True and out['winner']=='B'
        assert out['critic']['usability_floor_passed'] is True and out['memory_admitted'] is True and out['writeback']['comparison_id']>0

        proof=a2a_execution_plane.status(out['task_id']); assert proof['completion_evidence'] is True
        task=proof['task']; assert task['status']=='PASS'
        assert task['artifact']['type']=='dore.design-intelligence-exploration.v3'
        assert task['artifact']['evidence_kind']=='executable-sandbox-render+geometry'
        assert task['artifact']['canonical_workspace_mutated'] is False
        assert task['verification']['executable_candidate_artifacts'] is True
        assert task['verification']['canonical_workspace_mutated'] is False
        assert task['verification']['blind_order_reversal'] is True and task['verification']['judge_count']==2

        os.environ['DORE_DESIGN_A2A_DISAGREE_FIXTURE']='1'
        disagreement={**payload,'surface_id':'fresh-disagreement-surface','surface_family':'fresh-disagreement-family','task_context':'test order-bias resistance on an unseen surface','content_context':'blind-disagreement-control'}
        disagree=design_intelligence_a2a.explore(disagreement)
        assert disagree['ok'] and disagree['a2a_status']=='PASS' and disagree['judge_count']==2
        assert disagree['consensus'] is False and disagree['winner'] is None
        assert disagree['memory_admitted'] is False and disagree['writeback'] is None
        assert disagree['writeback_block_reason']=='judge_disagreement' and disagree['requires_more_evidence'] is True
        assert len(disagree['candidates'])==2 and all(c['render_sha256'] for c in disagree['candidates'])
        dproof=a2a_execution_plane.status(disagree['task_id']); assert dproof['completion_evidence'] is True

        print(json.dumps({'ok':True,'policy':'dore-design-executable-sandbox-acceptance-v1','checks':{
            'variants_are_executable_patches':True,'sandbox_candidates_render':True,'geometry_evidence_exists':True,
            'candidate_renders_are_distinct':True,'canonical_workspace_is_immutable':True,'two_blind_judges_run':True,
            'presentation_order_reversed':True,'consensus_winner_writes_back':True,'judge_disagreement_blocks_memory':True,
            'disagreement_preserves_candidate_artifacts':True,'completion_requires_verified_artifact':True,
            'design_process_has_no_model_client':True,'production_promotion_blocked':True,
        },'consensus_task_id':out['task_id'],'disagreement_task_id':disagree['task_id'],'winner':out['winner']},ensure_ascii=False,sort_keys=True))
    return 0

if __name__=='__main__': raise SystemExit(main())
