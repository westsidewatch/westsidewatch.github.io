from dore_core.bible.theological_boundary import christian_ministry_gate, christian_ministry_instruction


def test_rejects_prayer_without_explicit_christian_close():
    r=christian_ministry_gate('求主帶領我們。',task='prayer')
    assert not r.allowed
    assert r.code=='christian_close_required'


def test_accepts_christian_prayer_ending():
    r=christian_ministry_gate('奉主耶穌基督的名禱告，阿們。',task='prayer')
    assert r.allowed


def test_comparative_religion_bypasses_devotional_admission():
    r=christian_ministry_gate('This passage compares two religious traditions historically.',task='bible_teaching',comparative_context=True)
    assert r.allowed


def test_generation_instruction_is_explicit_but_abstract():
    s=christian_ministry_instruction('prayer')
    assert 'CHRISTIAN MINISTRY AUTHORITY' in s
    assert 'other religions' in s
    assert 'Jesus Christ' in s
    assert 'blacklist' not in s.lower()
