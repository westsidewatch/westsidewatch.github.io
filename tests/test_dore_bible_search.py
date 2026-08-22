from dore_core.language.base import LanguageUnit
from dore_core.search import BibleSearchIndex, SearchQuery

def unit(ref,surface,lang="en",witness="w",analyses=()):
    return LanguageUnit(witness,ref,1,surface,surface,lang,analyses,("source:test","snapshot:test"))

def test_reference_search():
    idx=BibleSearchIndex.from_units([unit("bible.ref.MAT.5.17","Think not")])
    hits=idx.search(SearchQuery("MAT 5:17",mode="reference"))
    assert hits and hits[0].canonical_ref_id=="bible.ref.MAT.5.17"

def test_text_and_fuzzy_search():
    idx=BibleSearchIndex.from_units([unit("bible.ref.JHN.1.1","In the beginning was the Word")])
    assert idx.search(SearchQuery("beginning was the Word",mode="text"))
    assert idx.search(SearchQuery("begining was the word",mode="fuzzy"))

def test_lemma_and_morphology_search():
    idx=BibleSearchIndex.from_units([unit("bible.ref.JHN.1.1","λόγος","grc","g",(("lemma","λόγος"),("morphology","N-NSM")))])
    assert idx.search(SearchQuery("λόγος",mode="lemma"))
    assert idx.search(SearchQuery("N-NSM",mode="morphology"))

def test_filters_and_provenance():
    idx=BibleSearchIndex.from_units([unit("bible.ref.GEN.1.1","beginning","en","a"),unit("bible.ref.GEN.1.1","起初","zh-Hant","c")])
    hits=idx.search(SearchQuery("起初",language="zh-Hant"))
    assert len(hits)==1 and hits[0].witness_id=="c" and hits[0].provenance

def test_no_guessing_below_fuzzy_threshold():
    idx=BibleSearchIndex.from_units([unit("bible.ref.GEN.1.1","beginning")])
    assert idx.search(SearchQuery("completely unrelated",mode="fuzzy"))==[]
