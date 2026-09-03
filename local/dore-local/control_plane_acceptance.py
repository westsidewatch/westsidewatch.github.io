#!/usr/bin/env python3
"""Canonical two-loop acceptance using real Storybook research and Dawn sources."""
import json,tempfile
from pathlib import Path
from dawn_library_enrichment import enrich
from multi_loop_control_plane import register,wake,route,share,complete,consume,load,VERSION
with tempfile.TemporaryDirectory() as d:
 state=Path(d)/'state.json';assets=Path(d)/'assets.jsonl';asset=enrich();initial=asset['sources'][:21]
 register('storybook-reference-expansion','Expand qualified references from 21 toward 40',kind='storybook',priority=60,state_path=state,metadata={'references':initial,'current_qualified_references':21,'minimum_qualified_references':40})
 wake('storybook-reference-expansion','parent-goal-active',state_path=state);a=route(state_path=state)
 register('dawn-library-enrichment','Enrich and normalize reusable publishing knowledge',kind='dawn-library',priority=65,state_path=state)
 wake('dawn-library-enrichment','new-repository-source-material',gravity=20,state_path=state);b=route(state_path=state)
 receipt=share('dawn-library-enrichment',asset,state_path=state,asset_path=assets);resumed=complete('dawn-library-enrichment',state_path=state);reuse=consume('storybook-reference-expansion',asset,state_path=state);final=load(state)
 events=[x['event'] for x in final['events']];checks={'storybook_started':a['loop_id']=='storybook-reference-expansion','dawn_woke_and_won_priority':b['loop_id']=='dawn-library-enrichment','a_checkpointed_before_b':['YIELD','ROUTE']==events[events.index('YIELD'):events.index('YIELD')+2],'knowledge_asset_real':asset['source_count']>=21 and asset['provenance_preserved'],'shared_once':receipt['ok'] and not receipt['deduplicated'],'storybook_resumed':resumed and resumed['loop_id']=='storybook-reference-expansion' and 'RESUME' in events,'reuse_not_research_duplicate':reuse['new_references']>0 and asset['knowledge_id'] in final['workflows']['storybook-reference-expansion']['consumed_assets'],'reference_goal_advances_without_false_pass':21<reuse['total']<40 and final['workflows']['storybook-reference-expansion']['status']=='ACTIVE'}
 out={'ok':all(checks.values()),'code':'DORE_MULTI_LOOP_CONTROL_PLANE_1_PASS' if all(checks.values()) else 'DORE_MULTI_LOOP_CONTROL_PLANE_1_FAIL','control_plane':VERSION,'checks':checks,'reference_delta':{'before':21,'after':reuse['total'],'target':40},'knowledge_asset':{'id':asset['knowledge_id'],'sources':asset['source_count']},'events':events};print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out['ok'] else 1)
