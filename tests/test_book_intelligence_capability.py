import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'local' / 'dore-local' / 'book_intelligence_capability.py'
SPEC = importlib.util.spec_from_file_location('book_intelligence_capability', PATH)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def sample_args():
    return {
        'source': {
            'title': 'Test Book',
            'bookIntent': {
                'category': 'reflection',
                'thesis': 'Author thesis remains authoritative.',
                'audience': 'readers',
            },
        },
        'sections': [
            {'role': 'chapter', 'title': 'One', 'text': 'First argument.'},
            {'role': 'chapter', 'title': 'Two', 'text': 'Second argument.'},
        ],
    }


def test_semantic_adapter_uses_injected_inference_and_preserves_author_thesis():
    seen = {}
    def infer(messages):
        seen['messages'] = messages
        return '{"schema":"dore.book-intelligence-report.v2","category":"essay","inferredThesis":"Different inferred wording","thesisRelationship":"partial","confidence":0.8,"audience":"general","readingMode":"continuous","chapterRoles":[],"argumentRelations":[],"structuralGaps":[],"visualToneHints":[],"evidence":[]}'
    result = MOD.execute(sample_args(), infer)
    report = result['report']
    assert seen['messages']
    assert report['declaredThesis'] == 'Author thesis remains authoritative.'
    assert report['inferredThesis'] == 'Different inferred wording'
    assert report['authority']['mayRewriteThesis'] is False
    assert report['runtime']['semantic'] is True


def test_invalid_inference_degrades_without_breaking_bookmaking():
    result = MOD.execute(sample_args(), lambda _: 'not-json')
    report = result['report']
    assert result['ok'] is True
    assert report['runtime']['degraded'] is True
    assert report['runtime']['reason'] == 'semantic_inference_failed'
    assert report['declaredThesis'] == 'Author thesis remains authoritative.'


def test_missing_inference_is_a_safe_degraded_result():
    result = MOD.execute(sample_args(), None)
    assert result['ok'] is True
    assert result['report']['runtime'] == {
        'semantic': False,
        'degraded': True,
        'reason': 'inference_unavailable',
    }


def test_public_report_does_not_expose_provider_or_model_identity():
    result = MOD.execute(sample_args(), lambda _: '{"category":"essay"}')
    text = repr(result).lower()
    assert 'ollama' not in text
    assert 'gemma' not in text
    assert 'openai' not in text
    assert 'anthropic' not in text
    assert 'provider' not in result['report']
    assert 'model' not in result['report']


def test_adapter_has_no_direct_provider_address():
    source = PATH.read_text()
    assert '127.0.0.1:11434' not in source
    assert '/api/chat' not in source
    assert 'OLLAMA_BASE_URL' not in source
