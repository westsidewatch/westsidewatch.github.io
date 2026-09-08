from dore_core.bible.theological_boundary import christian_ministry_gate, christian_ministry_instruction


def test_rejects_amitabha_in_christian_prayer():
    r=christian_ministry_gate('求主帶領我們。阿彌陀佛。',task='prayer')
    assert not r.allowed
    assert 'amitabha' in r.violations


def test_accepts_christian_prayer_ending():
    r=christian_ministry_gate('奉主耶穌基督的名禱告，阿們。',task='prayer')
    assert r.allowed


def test_comparative_religion_can_quote_foreign_formula():
    r=christian_ministry_gate('佛教徒可能念阿彌陀佛。',task='bible_teaching',comparative_context=True)
    assert r.allowed


def test_generation_instruction_is_explicit():
    s=christian_ministry_instruction('prayer')
    assert 'Christian ministry content' in s
    assert 'other religions' in s
    assert 'Jesus Christ' in s
