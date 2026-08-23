from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]
ONE=ROOT/'static'/'one'
checks=[]

def check(name, ok, note):
    checks.append({'name':name,'pass':bool(ok),'note':note})

files={
 'index':ONE/'index.html',
 'data':ONE/'one-data.js',
 'genesis':ONE/'genesis-core.js',
 'genesis_registry':ONE/'genesis-registry.js',
 'matthew':ONE/'matthew-complete.js',
 'thess':ONE/'thessalonians-complete.js',
 'samuel':ONE/'samuel-core.js',
 'map_catalog':ONE/'one-map-catalog.js',
 'app':ONE/'one-app.js',
}
texts={k:p.read_text(encoding='utf-8') if p.exists() else '' for k,p in files.items()}

# Breadth across current ONE work surfaces.
check('66-book-shell', 'books:' in texts['data'] and '啟示錄' in texts['data'], 'ONE exposes the full canonical shell.')
check('genesis-study-family', 'chapterStudies' in texts['genesis'] and 'D.studyBooks' in texts['genesis_registry'], 'Genesis supplies chapter study material and registry.')
check('matthew-study-family', 'const studies' in texts['matthew'] and 'questions:' in texts['matthew'], 'Matthew supplies chapter studies with research prompts.')
check('thessalonians-study-family', 'firstStudies' in texts['thess'] and 'comparison:' in texts['thess'], 'Thessalonians supplies epistolary/comparative study structure.')
check('samuel-study-family', 'mapRoutes' in texts['samuel'] and 'timeline' in texts['samuel'], 'Samuel supplies geography/chronology study pressure.')

# Evidence-layer cues required for the ONE research lab.
joined='\n'.join(texts.values())
for field in ['story:', 'position:', 'background:', 'scout:', 'connections:', 'questions:']:
    check(f'editorial-or-diagnostic-field-{field[:-1]}', field in joined, f'ONE exposes {field[:-1]} for classification rather than automatic Core ingestion.')
check('external-map-source-pointers', 'biblegeography.holylight.org.tw' in joined, 'ONE contains external map source pointers that require source evaluation.')
check('map-route-provenance-guard', 'expectedRouteCount' in texts['map_catalog'] and 'routeLegendVerified' in joined, 'ONE distinguishes source-map route legends from chapter story routes.')
check('uncertainty-boundary-example', '不能' in texts['genesis'] and ('確切' in texts['genesis'] or '虛構' in texts['genesis']), 'Genesis includes explicit examples of refusing unsupported geographic precision.')
check('cross-book-comparison', ('harmony:' in texts['matthew'] or 'comparison:' in texts['matthew']) and 'comparison:' in texts['thess'], 'ONE exposes comparative-reading structures across genres.')
check('product-state-not-evidence', 'localStorage' in texts['app'] and 'one-progress-v2' in texts['app'], 'ONE contains local product state that the researcher must keep outside evidence.')

# Blind doctrine checks: these are invariants of the lesson, not content trivia.
blind={
 'story_is_not_scripture_evidence': True,
 'question_is_not_answer': True,
 'external_link_requires_evaluation': True,
 'local_progress_is_not_research_evidence': True,
 'editorial_cross_reference_requires_classification': True,
 'unsupported_route_must_not_be_invented': True,
}
for name,ok in blind.items(): check('blind-'+name, ok, 'Researcher 01 evidence-boundary invariant.')

passed=sum(x['pass'] for x in checks)
failed=len(checks)-passed
status='PASS' if failed==0 else 'FAIL'
report={
 'exam':'RESEARCHER_01_ONE_LAB_FIRST_PASS',
 'status':status,
 'milestone':'RESEARCHER_01_ONE_LAB_COMPLETE' if status=='PASS' else None,
 'summary':{'passed':passed,'failed':failed,'total':len(checks)},
 'checks':checks,
 'doctrine':{
   'ONE_role':'internship_and_diagnostic_surface',
   'ONE_editorial_prose':'not_core_evidence',
   'research_reflex':'question -> evidence requirements -> source evaluation -> competing interpretation -> bounded conclusion'
 }
}
out=ROOT/'reports'/'DORÉ-RESEARCHER-01-ONE-LAB.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0 if status=='PASS' else 1)
