#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
pipeline=(ROOT/'promotion_pipeline.py').read_text();ui=(ROOT/'multipage_wysiwyg.py').read_text();registry=json.loads((ROOT/'candidates/registry.json').read_text())
capabilities={'version':'1.9.0','single_candidate_adapter':'promote_storybook_evidence' in pipeline,'candidate_gallery_api':'list_candidates' in pipeline,'editable_candidate_canvas':'homepage_candidates' in (ROOT/'multipage_wysiwyg.py').read_text(),'judgment_contract':'record_judgment' in pipeline,'feedback_declares_return':['storybook','knowledge-lab'],'promoted_candidate_count':len(registry.get('candidates',[]))}
gaps={'three_candidate_promotion':capabilities['promoted_candidate_count']<3,'knowledge_lineage':'reference_lineage' not in pipeline,'pattern_adopt_reject':'pattern_judgment' not in pipeline,'viewport_evidence_in_gallery':'viewport_evidence' not in pipeline,'knowledge_lab_feedback_write':'KNOWLEDGE_FEEDBACK' not in pipeline}
print(json.dumps({'ok':True,'schema':'dore.design-1.9-capability-audit.v1','capabilities':capabilities,'gaps':gaps},ensure_ascii=False))
