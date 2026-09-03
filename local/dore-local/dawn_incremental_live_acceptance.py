#!/usr/bin/env python3
import json
from goal_queue import load as load_goals
from multi_loop_control_plane import agent_cycle,load
goal=next((x for x in load_goals().get('goals',[]) if x.get('goal_id')=='design-reference-library-expansion-20260901'),None) or {'goal_id':'design-reference-library-expansion-20260901','goal':'Storybook reference expansion','metadata':{}}
ctx={'goal_id':goal['goal_id'],'goal':goal['goal'],'project_loop':(goal.get('metadata') or {}).get('project_loop','Storybook'),'metadata':goal.get('metadata') or {}}
results=[]
for _ in range(2):
 state=load();row=state.get('workflows',{}).get('storybook-reference-expansion',{});results.append(agent_cycle(ctx))
 if load().get('workflows',{}).get('storybook-reference-expansion',{}).get('status')=='PASS':break
state=load();row=state.get('workflows',{}).get('storybook-reference-expansion',{});meta=row.get('metadata') or {};families=int(meta.get('current_source_families') or 0);refs=int(meta.get('current_qualified_references') or 0);events=[x.get('event') for x in state.get('events',[])];checks={'workflow_pass':row.get('status')=='PASS','references_at_least_40':refs>=40,'source_families_at_least_6':families>=6,'incremental_asset_consumed':len(row.get('consumed_assets') or [])>=2,'knowledge_reuse_recorded':'KNOWLEDGE_REUSE' in events,'goal_pass_recorded':'GOAL_PASS' in events};out={'ok':all(checks.values()),'code':'DORE_DAWN_INCREMENTAL_LIVE_PASS' if all(checks.values()) else 'DORE_DAWN_INCREMENTAL_LIVE_FAIL','checks':checks,'qualified_references':refs,'source_families':families,'cycles':results};print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out['ok'] else 1)
