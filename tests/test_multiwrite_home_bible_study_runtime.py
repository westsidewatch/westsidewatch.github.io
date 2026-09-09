from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "static" / "multiwrite" / "index.html"
RUNTIME = ROOT / "static" / "multiwrite" / "home-bible-study.js"
CORPUS = ROOT / "static" / "dore" / "browser-fuzzy-corpus.json"


def test_home_has_real_note_editor():
    text = HOME.read_text(encoding="utf-8")
    assert 'id="homeBibleNotes"' in text
    assert 'id="homeBibleNoteStatus"' in text
    assert '查經筆記' in text


def test_notes_persist_in_study_document():
    text = RUNTIME.read_text(encoding="utf-8")
    assert "notes: ''" in text
    assert "doc.notes = value" in text
    assert "已自動儲存" in text
    assert "setTimeout(async () =>" in text
    assert "600" in text


def test_search_has_browser_fallback_without_companion():
    text = RUNTIME.read_text(encoding="utf-8")
    assert "context.fuzzy-search" in text
    assert "browserFuzzySearch" in text
    assert "BROWSER_CORPUS_URL" in text
    assert "return browserFuzzySearch(query)" in text


def test_acceptance_phrase_resolves_matthew_634():
    text = CORPUS.read_text(encoding="utf-8")
    assert '"id":"Matt.6.34"' in text
    assert "一天的憂慮一天當就夠了" in text
    assert '"canonical_reference":"Matt.6.34"' in text
