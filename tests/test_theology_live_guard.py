import importlib.util
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LOCAL=ROOT/'local'/'dore-local'
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
if str(LOCAL) not in sys.path: sys.path.insert(0,str(LOCAL))

spec=importlib.util.spec_from_file_location('dore_local_guarded',LOCAL/'dore_local_guarded.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_classifies_christian_prayer():
    task,comparative=mod.classify_ministry_task('請為今天的查經聚會寫一篇禱告')
    assert task=='prayer'
    assert comparative is False


def test_comparative_context_is_not_devotional():
    task,comparative=mod.classify_ministry_task('比較不同宗教的禱告傳統')
    assert task=='prayer'
    assert comparative is True


def test_guard_injects_authority_and_never_returns_failed_candidate(monkeypatch):
    seen=[]
    candidates=['candidate without an admitted close','still not admitted']
    def fake(messages):
        seen.append(messages)
        return candidates.pop(0)
    monkeypatch.setattr(mod,'_RAW_OLLAMA',fake)
    out=mod.guarded_ollama([{'role':'system','content':'base'},{'role':'user','content':'請寫一篇禱告'}])
    assert out not in {'candidate without an admitted close','still not admitted'}
    assert 'CHRISTIAN MINISTRY AUTHORITY' in seen[0][0]['content']
    assert mod.christian_ministry_gate(out,task='prayer').allowed


def test_guard_returns_admitted_candidate(monkeypatch):
    good='願主今天帶領我們。奉主耶穌基督的名禱告，阿們。'
    monkeypatch.setattr(mod,'_RAW_OLLAMA',lambda messages: good)
    out=mod.guarded_ollama([{'role':'system','content':'base'},{'role':'user','content':'請寫禱告'}])
    assert out==good


def test_safe_fallback_is_bilingual_and_positive_authority():
    zh=mod._safe_prayer_fallback('請寫禱告')
    en=mod._safe_prayer_fallback('Please write a prayer')
    assert mod.christian_ministry_gate(zh,task='prayer').allowed
    assert mod.christian_ministry_gate(en,task='prayer').allowed
    assert '耶穌基督' in zh
    assert 'Jesus Christ' in en
