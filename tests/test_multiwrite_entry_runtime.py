from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / 'static' / 'multiwrite' / 'index.html').read_text()
HOME_RUNTIME = (ROOT / 'static' / 'multiwrite' / 'home-runtime.js').read_text()
IMPORT = (ROOT / 'static' / 'multiwrite' / 'import.js').read_text()
BOOK_HTML = (ROOT / 'static' / 'multiwrite' / 'book.html').read_text()
BOOK_RUNTIME = (ROOT / 'static' / 'multiwrite' / 'book-runtime-v2.js').read_text()
BIBLE = (ROOT / 'static' / 'multiwrite' / 'bible-study.js').read_text()


def test_create_book_is_wired():
    assert 'id="createBook"' in HOME
    assert 'home-runtime.js' in HOME
    assert "createButton?.addEventListener('click'" in HOME_RUNTIME
    assert "location.assign(`/multiwrite/book.html?id=" in HOME_RUNTIME


def test_database_schema_is_v3_everywhere():
    assert "const DB_VERSION = 3;" in IMPORT
    assert "const STUDY_STORE = 'studyDocuments';" in IMPORT
    assert "DB_VERSION=3" in HOME_RUNTIME
    assert "DB_VERSION=3" in BOOK_RUNTIME


def test_local_books_are_clickable_and_reader_can_resolve_them():
    assert 'book-card book-card-link' in HOME_RUNTIME
    assert 'book-card book-card-link' in IMPORT
    assert 'getLocalBook(bookId)' in BOOK_RUNTIME
    assert 'structure:Array.isArray(local.nodes)?local.nodes:[]' in BOOK_RUNTIME
    assert 'book-runtime-v2.js' in BOOK_HTML


def test_bible_study_entry_has_no_missing_controller_focus_call():
    assert 'id="toggleBibleStudy"' in BOOK_HTML
    assert 'controller?.focus()' not in BIBLE
    assert "document.querySelector('#bibleStudyMount input')?.focus()" in BIBLE
