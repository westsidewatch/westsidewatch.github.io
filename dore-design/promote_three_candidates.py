#!/usr/bin/env python3
import json
from pathlib import Path
import knowledge_compression as kc,promotion_pipeline as pp
ROOT=Path(__file__).resolve().parent.parent;E=ROOT/'dore-design/knowledge-lab/evidence/storybook-autonomy/latest.json';S=ROOT/'dore-design/promotion/specimens';S.mkdir(parents=True,exist_ok=True);base=pp.sha256(pp.BASELINE);results=[]
for d in kc.compress()['directions']:
 spec={'schema':'dore.storybook-promotion-specimen.v2','candidate_id':d['candidate_id'],'name':d['name'],'source_story_id':d['story_id'],'source_story_file':'dore-design/knowledge-lab/storybook/src/stories/HomepageConcepts.stories.jsx','target_page_id':d['page'],'renderer':'homepage-candidate','template_entrypoint':'dore-design/homepage_candidates.py','editable_bindings':['home-title.text','home-deck.text','watch-kicker.text','verse.text','journal-tower.title','journal-tower.body','one-territory.title','church-territory.title','library-territory.title'],'assets':['inline:'+d['direction'],'static/images/westside-watch-masthead-landscape.svg'],'references':d['reference_lineage'],'source_families':d['families'],'reference_lineage':d['reference_lineage'],'pattern_judgment':d['pattern_judgment'],'knowledge_corpus':{'sha256':d['corpus_sha256'],'source_count':d['corpus_source_count'],'goal_status':'PASS'},'baseline_262_sha256':base,'baseline_composition_signature':'threshold-editorial-fortress-5x8','composition_signature':d['signature']}
 p=S/(d['direction']+'.v1.json');p.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n');results.append(pp.promote_storybook_evidence(p,E))
print(json.dumps({'ok':all(x.get('ok') for x in results),'results':results},ensure_ascii=False));raise SystemExit(0 if all(x.get('ok') for x in results) else 1)
