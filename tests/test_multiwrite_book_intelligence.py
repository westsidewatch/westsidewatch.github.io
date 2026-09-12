from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTELLIGENCE = (ROOT / 'static/multiwrite/book-intelligence.mjs').read_text()
BRIDGE = (ROOT / 'static/multiwrite/book-compile-bridge.mjs').read_text()
MODEL = (ROOT / 'static/multiwrite/book-model.mjs').read_text()


def test_intelligence_runs_before_model_and_editorial_gate():
    assert 'dore.book-intelligence-report.v1' in INTELLIGENCE
    assert 'analyzeBookIntelligence({ source, sections })' in BRIDGE
    assert BRIDGE.index('analyzeBookIntelligence({ source, sections })') < BRIDGE.index('buildBookModel({')
    assert BRIDGE.index('buildBookModel({') < BRIDGE.index('analyzeBookForPublication(bookModel)')


def test_author_declared_intent_is_not_silently_rewritten():
    assert "thesisSource: thesis ? 'author-declared' : 'not-established'" in INTELLIGENCE
    assert 'mayRewriteThesis: false' in INTELLIGENCE
    assert 'substantiveInferenceRequiresReview: true' in INTELLIGENCE
    assert 'bookIntentFromIntelligence' in BRIDGE


def test_intelligence_evidence_stays_internal():
    assert 'intelligenceSchema: intelligenceReport.schema' in BRIDGE
    projection = MODEL.split('export function publicationProjection', 1)[1]
    assert 'intelligenceReport' not in projection
