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
    page=Path('static/dore/index.html').read_text(encoding='utf-8')
    js=Path('static/dore/dore-search.js').read_text(encoding='utf-8')
    join=Path('join/index.html').read_text(encoding='utf-8')
    one=Path('static/one/one-opening-simple.js').read_text(encoding='utf-8')
    home=Path('layouts/index.html').read_text(encoding='utf-8')
    core_path=Path('static/dore/search-index.json');orig_path=Path('static/dore/original-index.json')
    core=json.loads(core_path.read_text(encoding='utf-8'));orig=json.loads(orig_path.read_text(encoding='utf-8'))
    check(core.get('schema')=='dore.browser-search-core.v1','core_schema',failures)
    check(orig.get('schema')=='dore.browser-original-index.v1','original_schema',failures)
    check(len(core.get('verses',[]))>=31000,'verse_coverage',failures)
    refs={v['r']:v for v in core.get('verses',[])}
    check('bible.ref.JHN.3.16' in refs,'john_3_16',failures);check('bible.ref.JER.33.3' in refs,'jeremiah_33_3',failures)
    check(bool(orig.get('lemma')) and bool(orig.get('morphology')),'original_language_indexes',failures)
    check('linear-gradient(rgba(206,189,116,.78),rgba(206,189,116,.78)),url("/background.jpg")' in page,'join_background_contract',failures)
    check('耶利米書 33:3' in page and 'Jeremiah 33:3' in page,'search_verse',failures)
    check(page.count('class="dore-art')>=2 and 'setInterval' in js,'dore_art_cycle',failures)
    check('original-index.json' in js and 'ensureOriginal' in js,'lazy_original_index',failures)
    check('href="/dore/"' in join,'join_entry',failures)
    check('dore.href="/dore/"' in one,'one_entry',failures)
    check('href="/dore/"' in home,'main_site_entry',failures)
    verdict='PASS' if not failures else 'FAIL'
    result={'schema':'dore.work-node.bible-search.v1','verdict':verdict,'work_node':'DORE_BIBLE_SEARCH','status':'AVAILABLE' if verdict=='PASS' else 'NOT_READY','failures':failures,'entrances':['JOIN','ONE','WESTSIDE_WATCH_MAIN'],'capabilities':['canonical_reference','cuv_webu_keyword','fuzzy_recall_candidates','original_surface','lemma','morphology','provenance_display'],'performance':{'core_index_bytes':core_path.stat().st_size,'original_index_bytes':orig_path.stat().st_size,'original_index_loading':'lazy'},'governance':'This is an external work-node acceptance, not an educational milestone.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
    if verdict!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
