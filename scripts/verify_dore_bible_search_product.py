#!/usr/bin/env python3
"""Static production acceptance for the Doré Bible Search external work node."""
from __future__ import annotations
import json
from pathlib import Path
OUT=Path('reports/DORÉ-BIBLE-SEARCH-WORK-NODE.json')
def check(condition,label,failures):
    if not condition:failures.append(label)
def main():
    failures=[]
    page=Path('static/dore/search/index.html').read_text(encoding='utf-8')
    redirect=Path('static/dore/index.html').read_text(encoding='utf-8')
    js=Path('static/dore/dore-search.js').read_text(encoding='utf-8')
    gallery=Path('static/dore/dore-gallery.js').read_text(encoding='utf-8')
    intelligence=Path('static/dore/dore-bible-intelligence.js').read_text(encoding='utf-8')
    join=Path('join/index.html').read_text(encoding='utf-8')
    one_js=Path('static/one/one-opening-simple.js').read_text(encoding='utf-8')
    one_css=Path('static/one/one-opening-simple.css').read_text(encoding='utf-8')
    home=Path('layouts/index.html').read_text(encoding='utf-8')
    assets=Path('static/one/one-dore-assets-241.js').read_text(encoding='utf-8')
    core_path=Path('static/dore/search-index.json');orig_path=Path('static/dore/original-index.json')
    core=json.loads(core_path.read_text(encoding='utf-8'));orig=json.loads(orig_path.read_text(encoding='utf-8'))
    check(core.get('schema')=='dore.browser-search-core.v1','core_schema',failures)
    check(orig.get('schema')=='dore.browser-original-index.v1','original_schema',failures)
    check(len(core.get('verses',[]))>=31000,'verse_coverage',failures)
    refs={v['r']:v for v in core.get('verses',[])}
    check('bible.ref.JHN.3.16' in refs,'john_3_16',failures);check('bible.ref.JER.33.3' in refs,'jeremiah_33_3',failures)
    check(bool(orig.get('lemma')) and bool(orig.get('morphology')),'original_language_indexes',failures)
    check('rgba(206,189,116,.78)' in page and ("url('/background.jpg')" in page or 'SITE-BACKGROUND' in page),'join_background_contract',failures)
    check('耶利米書 33:3' in page,'search_verse',failures)
    check('馬太福音第三章' in page and 'byChapter' in js and "kind:'chapter'" in js,'chapter_reference_ui',failures)
    check('/dore/original-index.json' in js and 'ensureOriginal' in js,'lazy_original_index',failures)
    check('one-dore-assets-241.js' in page and 'Array.from({length:241}' in gallery and '241-complete' in assets,'dore_241_original_archive',failures)
    check('/dore/search/' in redirect,'root_redirect_to_search',failures)
    check('href="/dore/search/"' in join,'join_direct_search_entry',failures)
    check('dore-inline-search' in one_js and 'location.href="/dore/search/?q="' in one_js and 'dore-inline-search' in one_js,'one_direct_visible_search_entry',failures)
    check('href="/dore/search/"' in home,'main_site_direct_search_entry',failures)
    check('dore-bible-intelligence.js' in gallery and 'intelligenceRuntime.async=false' in gallery,'search2_runtime_loaded_before_brain',failures)
    check('DoreBibleIntelligence' in intelligence and 'ingestScriptureThreads' in intelligence and 'related(ref,opts={})' in intelligence,'shared_bible_intelligence_graph',failures)
    check('crossReferenceShared' in one_js and 'shared.related' in one_js and 'shared.query' in one_js,'one_consumes_shared_bible_intelligence',failures)
    check('gilead-jabesh-saul' in intelligence and 'wilderness-temptation-deuteronomy' in intelligence and 'ot-spirit-false-premise' in intelligence,'search2_semantic_reflexes',failures)
    verdict='PASS' if not failures else 'FAIL'
    result={'schema':'dore.work-node.bible-search.v2','verdict':verdict,'work_node':'DORE_BIBLE_SEARCH','status':'AVAILABLE' if verdict=='PASS' else 'NOT_READY','function_url':'/dore/search/','failures':failures,'entrances':['JOIN','ONE','WESTSIDE_WATCH_MAIN'],'capabilities':['canonical_reference','chapter_reference','cuv_webu_keyword','fuzzy_recall_candidates','original_surface','lemma','morphology','provenance_display','dore_original_archive_241','shared_bible_intelligence_graph','weighted_multi_hop_relations','semantic_study_intents','one_shared_intelligence_bridge'],'performance':{'core_index_bytes':core_path.stat().st_size,'original_index_bytes':orig_path.stat().st_size,'original_index_loading':'lazy','dore_archive_loading':'two-slot_lazy_cycle'},'governance':'External work-node acceptance. This verifies the integrated Search 2 increment, not completion of the permanent Bible Intelligence Loop or issue #281.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
    if verdict!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
