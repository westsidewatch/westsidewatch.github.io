import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK_MODEL = (ROOT / 'static/multiwrite/book-model.mjs').read_text()
BRIDGE = (ROOT / 'static/multiwrite/book-compile-bridge.mjs').read_text()
BOOK_HTML = (ROOT / 'static/multiwrite/book.html').read_text()
CAPABILITY = json.loads((ROOT / 'dore-core/runtime/book-publishing-capability.v1.json').read_text())
REGISTRY = json.loads((ROOT / 'dore-core/runtime/capability-registry.v1.json').read_text())


def test_book_compile_is_a_core_discoverable_capability():
    entry = next(item for item in REGISTRY['capabilities'] if item['id'] == 'publishing.book-compile')
    assert entry['service'] == 'publishing'
    assert entry['consumers'] == ['multiwrite']
    assert entry['produces'] == ['BookIntent', 'BookModel', 'EditorialReport', 'BookBuild']
    assert CAPABILITY['owner'] == 'dore-core'
    assert CAPABILITY['outputs'] == ['BookIntent', 'BookModel', 'EditorialReport', 'BookBuild']


def test_book_model_is_canonical_before_artifacts():
    assert "dore.book-model.v1" in BOOK_MODEL
    assert "dore.book-build.v1" in BOOK_MODEL
    assert "artifacts: { web: null, epub: null, pdf: null }" in BOOK_MODEL
    assert CAPABILITY['pipeline'].index('book-model') < CAPABILITY['pipeline'].index('publication-build')


def test_internal_provenance_is_excluded_from_public_projection():
    projection = BOOK_MODEL.split('export function publicationProjection', 1)[1]
    assert 'internalProvenance:' not in projection
    assert CAPABILITY['publication_boundary']['public'] == 'publicationMetadata'
    assert CAPABILITY['publication_boundary']['private'] == 'internalProvenance'
    assert 'internalProvenance-in-publicationMetadata' in CAPABILITY['policy']['forbidden']


def test_existing_make_book_export_is_preflighted_by_book_spine():
    assert 'book-compile-bridge.mjs?v=20260912-editorial1' in BOOK_HTML
    assert "document.querySelectorAll('[data-export]')" in BRIDGE
    assert 'await compileCurrentBook()' in BRIDGE
    assert 'return await original.call(button, event)' in BRIDGE


def test_book_spine_preserves_current_multiwrite_storage_contract():
    assert "DB_NAME = 'multiwrite-v1'" in BRIDGE
    assert 'DB_VERSION = 3' in BRIDGE
    assert "BOOK_STORE = 'books'" in BRIDGE
    assert "DRAFT_STORE = 'drafts'" in BRIDGE


def test_auto_repair_policy_is_bounded():
    assert CAPABILITY['policy']['max_auto_repair_attempts'] == 3
    assert "maxAutoRepairAttempts: 3" in BOOK_MODEL


def test_editorial_gate_is_before_theology_and_build():
    assert CAPABILITY['pipeline'].index('editorial-gate') < CAPABILITY['pipeline'].index('theology-gate')
    assert CAPABILITY['pipeline'].index('editorial-gate') < CAPABILITY['pipeline'].index('publication-build')
    assert CAPABILITY['editorial_gate']['report_schema'] == 'dore.editorial-report.v1'
