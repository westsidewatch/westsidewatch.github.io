from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / 'static/multiwrite/index.html').read_text(encoding='utf-8')
BOOK = (ROOT / 'static/multiwrite/book.html').read_text(encoding='utf-8')
STUDY = (ROOT / 'static/multiwrite/study.html').read_text(encoding='utf-8')
RUNTIME = (ROOT / 'static/multiwrite/study.js').read_text(encoding='utf-8')


def test_bible_study_is_a_dedicated_editor_mode():
    assert 'href="./study.html">查經筆記' in HOME
    assert 'href="./study.html">查經筆記' in BOOK
    assert 'class="book-shell study-shell"' in STUDY
    assert 'class="book-layout"' in STUDY
    assert 'class="reader-paper study-paper"' in STUDY
    assert 'id="studyEditor" class="chapter-editor"' in STUDY


def test_home_no_longer_embeds_old_study_workspace():
    assert 'id="homeBibleStudyMount"' not in HOME
    assert 'home-bible-study.js' not in HOME


def test_fuzzy_v2_uses_full_scripture_index_and_real_approximation():
    assert "FULL_INDEX='/dore/search-index.json'" in RUNTIME
    assert 'function dice(' in RUNTIME
    assert 'function subseq(' in RUNTIME
    assert 'const SYN=' in RUNTIME
    assert 'score>=.34' in RUNTIME
    assert '模糊命中' in RUNTIME


def test_search_keeps_capability_identity_and_local_fallback():
    assert "cap.invoke('context.fuzzy-search'" in RUNTIME
    assert 'companionSearch(query,context)' in RUNTIME
    assert 'return localFuzzySearch(query)' in RUNTIME


def test_notes_reuse_existing_study_document():
    assert "DOC_ID='multiwrite:home'" in RUNTIME
    assert 'd.notes=value' in RUNTIME
    assert '已自動儲存' in RUNTIME
