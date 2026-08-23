"""Post-foundation self-exam of Doré's public Search behavior.
This exam intentionally records failures; it does not patch triggering queries.
"""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]
search=(ROOT/'static/dore/dore-search.js').read_text()
entity=(ROOT/'static/dore/dore-entity-search.js').read_text()

cases=[]
def check(name, family, ok, signal, evidence):
    cases.append({'name':name,'family':family,'pass':bool(ok),'signal':None if ok else signal,'evidence':evidence})

# Architecture/static behavioral probes. These inspect what the deployed browser runtime
# can actually route, rather than whether Foundation registries merely exist.
check('scripture-reference-routing','PASSAGE_LOOKUP','parseReference(q)' in search,None,'reference parser is wired')
check('original-language-routing','ORIGINAL_LANGUAGE','translated-to-original' in search,None,'original-language intent is wired')
check('entity-count-routing','ENTITY_COUNT','parseCount(raw)' in entity,None,'count intent exists in entity runtime')
check('entity-layer-does-not-replace-scripture','ENTITY_LOOKUP','form.addEventListener(\'submit\',handler,false)' in entity,None,'entity layer is additive')

# Known public regression: plain Scripture text search still uses substring inclusion.
substring='zh.includes(n)||en.includes(n)' in search
check('exact-name-boundary','ENTITY_LOOKUP',not substring,'LEXICAL_COLLISION','plain textSearch uses substring inclusion' if substring else 'boundary-safe matching')

# Question families discussed as unseen stimuli: do not require their answers; test routing.
presence_router=bool(re.search(r'PRESENCE_BY_SCOPE|presence[-_ ]by[-_ ]scope',search+entity,re.I))
theme_router=bool(re.search(r'CONCEPT_THEME|concept[-_ ]theme|semantic[-_ ]theme',search+entity,re.I))
check('scope-presence-question-routing','PRESENCE_BY_SCOPE',presence_router,'INTENT_UNRESOLVED','no generic scope/presence router in public runtime')
check('concept-theme-routing','CONCEPT_THEME',theme_router,'INTENT_UNRESOLVED','no generic concept/theme router in public runtime')

# Autonomous feedback: public runtime should be able to emit/retain learning signals.
feedback=bool(re.search(r'LearningSignal|learning[-_ ]signal|CAPABILITY_MISSING|INTENT_UNRESOLVED',search+entity,re.I))
check('public-search-learning-signal','AUTONOMOUS_LEARNING',feedback,'CAPABILITY_MISSING','public Search has no learning-signal feedback path')

passed=sum(c['pass'] for c in cases); failed=len(cases)-passed
report={
 'status':'PASS' if failed==0 else 'FAIL',
 'exam':'DORE_SEARCH_POST_BIBLICAL_WORLD_SELF_EXAM_1',
 'summary':{'passed':passed,'failed':failed,'total':len(cases)},
 'cases':cases,
 'diagnosis':{
   'foundation':'BIBLICAL_WORLD_COMPLETE may remain valid as a Foundation milestone.',
   'product':'Public Doré Search is not graduated merely because Foundation is complete.',
   'next_rule':'Repair capability families, not trigger-specific queries; rerun with unseen transfer cases.'
 }
}
out=ROOT/'reports/DORÉ-SEARCH-SELF-EXAM.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0)  # diagnostic exam records FAIL without blocking unrelated Foundation CI
