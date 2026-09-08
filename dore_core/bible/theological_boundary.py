"""Hard theological boundary for Doré Christian ministry surfaces.

This is a deterministic output gate, not a model persona. Models may propose text;
Doré owns admission. Christian prayer/worship/blessing/devotional output must not
silently blend invocations, deities, mantras, or devotional formulas from another
religion. Comparative/research discussion remains allowed when explicitly requested.
"""
from __future__ import annotations
from dataclasses import dataclass
import re

CHRISTIAN_MINISTRY_TASKS=frozenset({'prayer','worship','blessing','devotional','sermon','bible_teaching'})
FOREIGN_DEVOTIONAL_FORMULAS=(
    ('amitabha', re.compile(r'阿[彌弥]陀佛|南無阿[彌弥]陀佛|南无阿[彌弥]陀佛',re.I)),
    ('buddhist_refuge', re.compile(r'皈依佛|皈依法|皈依僧',re.I)),
    ('islamic_invocation', re.compile(r'بسم الله|إن شاء الله',re.I)),
    ('hindu_invocation', re.compile(r'\bom\s+namah\b|ॐ',re.I)),
)

@dataclass(frozen=True)
class TheologyGateResult:
    allowed: bool
    code: str
    violations: tuple[str,...]=()


def christian_ministry_gate(text:str, *, task:str, comparative_context:bool=False)->TheologyGateResult:
    """Fail closed for devotional production; never rewrite a violation as if accepted."""
    if task not in CHRISTIAN_MINISTRY_TASKS or comparative_context:
        return TheologyGateResult(True,'not_applicable')
    violations=tuple(name for name,pattern in FOREIGN_DEVOTIONAL_FORMULAS if pattern.search(text or ''))
    if violations:
        return TheologyGateResult(False,'theological_boundary_violation',violations)
    return TheologyGateResult(True,'pass')


def christian_ministry_instruction(task:str)->str:
    """High-priority generation constraint supplied before model inference."""
    if task not in CHRISTIAN_MINISTRY_TASKS:return ''
    return (
      'DORÉ THEOLOGICAL BOUNDARY: This is Christian ministry content. '
      'Remain within historic Christian Scripture-centered language and the immediate biblical context. '
      'Do not blend prayers, invocations, mantras, deity names, devotional endings, or worship formulas from other religions. '
      'For prayer, address God in Christian terms appropriate to the request and ordinarily conclude in the name of Jesus Christ, Amen. '
      'Do not claim that Doré or AI has divine authority, revelation, inspiration, or the power to give spiritual life. '
      'If the request is comparative religion, describe other traditions as objects of study rather than adopting their devotional voice.'
    )
