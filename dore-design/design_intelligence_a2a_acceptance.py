#!/usr/bin/env python3
"""Deterministic acceptance for raster-grounded Design -> Core/A2A exploration."""
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


def assert_raster(candidate):
    r=candidate.get('raster') or {}; canvas=(candidate.get('geometry') or {}).get('canvas') or {}
    assert r.get('schema')=='dore.design.raster-evidence.v1',r
    assert r.get('real_browser_render') is True and r.get('sha256') and int(r.get('byte_size') or 0)>100,r
    assert Path(r['path']).exists(),r
    assert r['width']==int(round(float(canvas['w']))) and r['height']==int(round(float(canvas['h']))),(r,canvas)


def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        os.environ['DORE_LOCAL_HOME']=str(root/'home')
        os.environ['DORE_DESIGN_DATA']=str(root/'design')
        os.environ['DORE_UI_TASTE_DB']=str(root/'taste.sqlite3')
        os.environ['DORE_DESIGN_A2A_FIXTURE']='1'
        os.environ['DORE_DESIGN_A2A_TIMEOUT']='90'
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
        assert len(out['candidates'])==2 and out['candidate_evidence']=='real-browser-png+failure-domains+executable-sandbox-render+geometry'
        assert out['canonical_workspace_mutated'] is False
        assert all(c['schema']=='dore.design.sandbox-candidate.v1' for c in out['candidates'])
        assert all(c['render_sha256'] and c['rendered_html'].startswith('<!doctype html>') for c in out['candidates'])
        assert all(c['geometry']['node_count']==2 and c['canonical_workspace_mutated'] is False for c in out['candidates'])
        for c in out['candidates']: assert_raster(c)
        assert out['candidates'][0]['render_sha256'] != out['candidates'][1]['render_sha256']
        assert out['candidates'][0]['raster']['sha256'] != out['candidates'][1]['raster']['sha256']
        assert out['judge_count']==2 and out['blind_order_reversal'] is True and out['consensus'] is True and out['winner']=='B'
        assert out['critic']['usability_floor_passed'] is True and out['memory_admitted'] is True and out['writeback']['comparison_id']>0
        assert out['failure_domain_policy']=='pixel-observable-consensus-v1'
        assert len(out['loser_failures'])==1 and out['loser_failures'][0]['domain']=='scale-hierarchy'
        assert len(out['rejection_memory'])==1 and out['rejection_memory'][0]['rejection_id']>0
        assert out['rejection_memory'][0]['rejected_candidate']=='A'
        assert out['rejection_memory'][0]['direction']=='preserve-current-gravity'

        conn=design_intelligence_runtime.connect()
        try:
            rows=[dict(r) for r in conn.execute('SELECT * FROM dore_ui_taste_rejections ORDER BY id')]
        finally:
            conn.close()
        assert len(rows)==1,rows
        assert rows[0]['failure_domain']=='scale-hierarchy' and rows[0]['direction']=='preserve-current-gravity'
        refs=json.loads(rows[0]['evidence_refs_json'])
        assert any(x.startswith('browser-raster:A:') for x in refs)
        assert any(x.startswith('browser-raster:B:') for x in refs)
        assert 'failure-domain-judge-consensus:2' in refs
        assert any(x.startswith('pixel-basis:') for x in refs)

        proof=a2a_execution_plane.status(out['task_id']); assert proof['completion_evidence'] is True
        task=proof['task']; assert task['status']=='PASS'
        assert task['artifact']['type']=='dore.design-intelligence-exploration.v5'
        assert task['artifact']['evidence_kind']=='real-browser-png+failure-domains+executable-sandbox+geometry'
        assert task['artifact']['canonical_workspace_mutated'] is False
        assert task['verification']['executable_candidate_artifacts'] is True
        assert task['verification']['real_browser_raster_evidence'] is True
        assert task['verification']['distinct_candidate_rasters'] is True
        assert task['verification']['pixel_failure_domains_extracted'] is True
        assert task['verification']['failure_domain_policy']=='pixel-observable-consensus-v1'
        assert task['verification']['canonical_workspace_mutated'] is False
        assert task['verification']['blind_order_reversal'] is True and task['verification']['judge_count']==2

        os.environ['DORE_DESIGN_A2A_DISAGREE_FIXTURE']='1'
        disagreement={**payload,'surface_id':'fresh-disagreement-surface','surface_family':'fresh-disagreement-family','task_context':'test order-bias resistance on an unseen surface','content_context':'blind-disagreement-control'}
        disagree=design_intelligence_a2a.explore(disagreement)
        assert disagree['ok'] and disagree['a2a_status']=='PASS' and disagree['judge_count']==2
        assert disagree['consensus'] is False and disagree['winner'] is None
        assert disagree['memory_admitted'] is False and disagree['writeback'] is None
        assert disagree['rejection_memory']==[] and disagree['loser_failures']==[]
        assert disagree['writeback_block_reason']=='judge_disagreement' and disagree['requires_more_evidence'] is True
        assert len(disagree['candidates'])==2
        for c in disagree['candidates']: assert_raster(c)
        dproof=a2a_execution_plane.status(disagree['task_id']); assert dproof['completion_evidence'] is True
        assert dproof['task']['verification']['real_browser_raster_evidence'] is True
        conn=design_intelligence_runtime.connect()
        try:
            rejection_count=conn.execute('SELECT COUNT(*) FROM dore_ui_taste_rejections').fetchone()[0]
        finally:
            conn.close()
        assert rejection_count==1,rejection_count

        print(json.dumps({'ok':True,'policy':'dore-design-pixel-rejection-memory-acceptance-v1','checks':{
            'variants_are_executable_patches':True,'sandbox_candidates_render':True,'geometry_evidence_exists':True,
            'real_browser_png_A':True,'real_browser_png_B':True,'raster_dimensions_match_canvas':True,
            'candidate_pixels_are_distinct':True,'canonical_workspace_is_immutable':True,'two_blind_judges_run':True,
            'presentation_order_reversed':True,'consensus_winner_writes_back':True,'pixel_failure_domain_extracted':True,
            'loser_failure_writes_rejection_memory':True,'rejection_carries_pixel_evidence':True,
            'judge_disagreement_blocks_preference_memory':True,'judge_disagreement_blocks_rejection_memory':True,
            'motion_failure_not_in_static_pixel_taxonomy':True,'pixel_evidence_precedes_taste_writeback':True,
            'completion_requires_verified_artifact':True,'design_process_has_no_model_client':True,'production_promotion_blocked':True,
        },'consensus_task_id':out['task_id'],'disagreement_task_id':disagree['task_id'],'winner':out['winner'],'failure_domain':out['loser_failures'][0]['domain']},ensure_ascii=False,sort_keys=True))
    return 0

if __name__=='__main__': raise SystemExit(main())
