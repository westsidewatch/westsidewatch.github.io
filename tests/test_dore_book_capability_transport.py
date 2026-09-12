from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLIENT = (ROOT / 'static/multiwrite/book-core-client.mjs').read_text()
SITE = (ROOT / 'local/dore-companion-extension/site_bridge.js').read_text()
BACKGROUND = (ROOT / 'local/dore-companion-extension/background.js').read_text()


def test_multiwrite_book_intelligence_uses_site_bridge():
    assert 'publishing.book-intelligence' in CLIENT
    assert 'dore:book-intelligence' in CLIENT
    assert 'dore:book-intelligence-result' in CLIENT


def test_browser_client_does_not_use_direct_local_endpoint():
    assert '127.0.0.1' not in CLIENT
    assert '8788' not in CLIENT


def test_site_bridge_has_book_intelligence_request_and_result():
    assert "BOOK_CAPABILITY='publishing.book-intelligence'" in SITE
    assert 'dore:book-intelligence' in SITE
    assert 'dore:book-intelligence-result' in SITE
    assert "await send(BOOK_CAPABILITY,args,'multiwrite')" in SITE


def test_companion_allows_book_intelligence_site_capability():
    assert 'publishing.book-intelligence' in BACKGROUND
    assert 'SITE_CAPABILITY_ALLOWLIST' in BACKGROUND


def test_semantic_client_is_bounded_and_degrades_safely():
    assert 'SEMANTIC_TIMEOUT_MS = 20000' in CLIENT
    assert "degradedSemantic('core-timeout')" in CLIENT
    assert "degradedSemantic('core-invalid-response')" in CLIENT
    assert 'mayRewriteThesis:false' in CLIENT or 'mayRewriteThesis: false' in CLIENT
