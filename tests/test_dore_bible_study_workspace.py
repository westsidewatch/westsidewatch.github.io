from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'static/multiwrite/study.html').read_text()
JS = (ROOT / 'static/multiwrite/study.js').read_text()
CSS = (ROOT / 'static/multiwrite/study.css').read_text()


def test_workspace_has_three_distinct_surfaces():
    assert 'study-structure' in HTML
    assert 'study-reader' in HTML
    assert 'study-ambient' in HTML
    assert 'studySearchMount' not in HTML


def test_outline_is_structured_and_draggable():
    assert "outline" in JS
    assert "content" in JS
    assert "draggable=\"true\"" in JS
    assert "dragstart" in JS
    assert "reorder(fromId,toId)" in JS
    assert "dragend" in JS


def test_old_single_note_migrates_into_first_node():
    assert "typeof base.notes==='string'?base.notes:''" in JS
    assert "delete base.notes" in JS
    assert "dore.study-document.v2" in JS


def test_ambient_search_follows_editor_context_without_duplicate_keyup_work():
    assert "cursorContext()" in JS
    assert "slice(Math.max(0,pos-180),pos)" in JS
    assert "queueAmbient()" in JS
    assert "ambientTimer=setTimeout" in JS
    assert "},160)" in JS
    assert "addEventListener('keyup'" not in JS
    assert "lastAmbientQuery" in JS
    assert "繼續寫即可" in JS


def test_chinese_chapter_intent_is_parsed_before_fuzzy_text_scoring():
    assert "function chapterNumber" in JS
    assert "function parseChapterIntent" in JS
    assert "第?\\s*([零〇一二兩三四五六七八九十百\\d]+)" in JS
    assert "chapterIndex" in JS
    assert "findContextBook" in JS
    assert "buildChapterResult" in JS
    assert "章節命中 100%" in JS


def test_ambient_result_requires_user_click_for_deeper_action():
    assert "ambient-item" in JS
    assert "openAmbient" in JS
    assert "data-action=\"search\"" in JS
    assert "繼續搜索" in JS
    assert "保留" in JS
    assert "加入流程" in JS


def test_fuzzy_search_uses_prefiltered_cached_local_corpus():
    assert "/dore/search-index.json" in JS
    assert "localSimilarity" in JS
    assert "dice(" in JS
    assert "cache:'force-cache'" in JS
    assert "gramIndex" in JS
    assert "function prefilter" in JS
    assert ".slice(0,350)" in JS
    assert "requestIdleCallback" in JS
    assert "model" not in JS.lower()


def test_drag_controls_are_progressively_disclosed():
    assert '.study-drag{opacity:0' in CSS
    assert ':hover .study-drag{opacity:.7' in CSS
