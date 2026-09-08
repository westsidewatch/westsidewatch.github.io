"""Christian ministry authority boundary for Doré.

The Core stores abstract authority rules only. It must not embed adversarial devotional
phrases, foreign-religion watchwords, or incident text as blacklist knowledge.
Models propose candidate text; Doré decides whether the candidate may be admitted.
"""
from __future__ import annotations
from dataclasses import dataclass
import re

CHRISTIAN_MINISTRY_TASKS=frozenset({'prayer','worship','blessing','devotional','sermon','bible_teaching'})

@dataclass(frozen=True)
class TheologyGateResult:
    allowed: bool
    code: str
    violations: tuple[str,...]=()


def christian_ministry_instruction(task:str)->str:
    """High-authority instruction supplied before inference.

    This rule is intentionally abstract. The Core does not carry a blacklist of
    adversarial religious expressions.
    """
    if task not in CHRISTIAN_MINISTRY_TASKS:
        return ''
    return (
      'DORÉ CHRISTIAN MINISTRY AUTHORITY: This output belongs to an explicitly Christian, '
      'Scripture-centered ministry context. Keep devotional voice, prayer, worship, blessing, '
      'and theological claims within that authority. Material about other religions may be '
      'described for comparison or history, but must never be adopted as devotional voice, '
      'invocation, worship, blessing, mantra, deity-address, or closing formula. '
      'For prayer, address the God confessed in Christian Scripture and ordinarily conclude '
      'in the name of Jesus Christ, Amen, with nothing devotional appended after Amen. '
      'Doré and its models have no divine authority, revelation, inspiration, or power to give spiritual life.'
    )


def _prayer_has_christian_close(text:str)->bool:
    """Positive admission test: require an explicitly Christian prayer close.

    Positive validation avoids storing a contamination vocabulary in Core.
    """
    t=(text or '').strip()
    if not t:
        return False
    close=t[-180:]
    has_christ=(
        bool(re.search(r'耶[穌稣].{0,10}基督',close,re.I))
        or bool(re.search(r'Jesus\s+Christ',close,re.I))
        or bool(re.search(r'in\s+(?:the\s+)?name\s+of\s+Jesus',close,re.I))
    )
    has_amen=bool(re.search(r'(?:阿們|阿们|Amen)[。.!！\s]*$',t,re.I))
    return has_christ and has_amen


def christian_ministry_gate(text:str, *, task:str, comparative_context:bool=False)->TheologyGateResult:
    """Fail closed on positive Christian ministry admission rules.

    Comparative/research discussion is outside devotional production and remains allowed.
    The gate contains no incident phrase or foreign-devotional blacklist.
    """
    if task not in CHRISTIAN_MINISTRY_TASKS or comparative_context:
        return TheologyGateResult(True,'not_applicable')
    if not (text or '').strip():
        return TheologyGateResult(False,'empty_candidate',('empty_candidate',))
    if task=='prayer' and not _prayer_has_christian_close(text):
        return TheologyGateResult(False,'christian_close_required',('christian_close_required',))
    return TheologyGateResult(True,'pass')
