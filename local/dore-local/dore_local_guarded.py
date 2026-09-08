#!/usr/bin/env python3
"""Production Doré Local entrypoint with Christian ministry admission rails.

This wrapper keeps the existing local server intact and patches only the model proposal
boundary. Candidate text is never returned to the HTTP/chat layer until admission passes.
The Core stores positive Christian authority rules, not adversarial devotional watchwords.
"""
from __future__ import annotations
import os
import re
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0,str(REPO))
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))

import dore_local as runtime
from dore_core.bible.theological_boundary import christian_ministry_gate, christian_ministry_instruction

_RAW_OLLAMA=runtime.ollama
_MAX_RETRIES=max(0,min(2,int(os.environ.get('DORE_THEOLOGY_RETRIES','1'))))

_TASK_PATTERNS=(
    ('prayer', re.compile(r'(?:禱告|祷告|代禱|代祷|pray(?:er)?|intercession)',re.I)),
    ('worship', re.compile(r'(?:敬拜|讚美|赞美|worship)',re.I)),
    ('blessing', re.compile(r'(?:祝福|blessing)',re.I)),
    ('devotional', re.compile(r'(?:靈修|灵修|devotional)',re.I)),
    ('sermon', re.compile(r'(?:講道|讲道|sermon|homily)',re.I)),
    ('bible_teaching', re.compile(r'(?:查經|查经|聖經教導|圣经教导|Bible\s+(?:study|teaching))',re.I)),
)
_COMPARATIVE=re.compile(r'(?:比較|比较|對比|对比|歷史|历史|研究|介紹|介绍|compare|comparative|history|historical|research|describe)',re.I)
_CJK=re.compile(r'[\u3400-\u9fff]')


def classify_ministry_task(text:str)->tuple[str|None,bool]:
    source=text or ''
    comparative=bool(_COMPARATIVE.search(source))
    for task,pattern in _TASK_PATTERNS:
        if pattern.search(source):
            return task,comparative
    return None,comparative


def _current_request(messages)->str:
    for item in reversed(messages or []):
        if item.get('role')!='user':
            continue
        text=str(item.get('content') or '')
        marker='Current user message:\n'
        if marker in text:
            return text.rsplit(marker,1)[-1].strip()
        return text.strip()
    return ''


def _with_authority(messages, instruction:str):
    out=[dict(x) for x in (messages or [])]
    if not instruction:
        return out
    if out and out[0].get('role')=='system':
        out[0]['content']=str(out[0].get('content') or '')+'\n\n'+instruction
    else:
        out.insert(0,{'role':'system','content':instruction})
    return out


def _safe_prayer_fallback(request:str)->str:
    """Return a small positive-authority prayer without reusing rejected model text.

    The fallback is intentionally fixed and contamination-free. User text is used only to
    select language and is never interpolated into the devotional body.
    """
    if _CJK.search(request or ''):
        return (
            '天父，我們感謝祢賜下祢的話語。求祢使我們存謙卑受教的心，'
            '在今天的查考與彼此分享中得著真理、智慧與愛，也使我們所學的能活在日常生活中。'
            '奉主耶穌基督的名禱告，阿們。'
        )
    return (
        'Heavenly Father, thank You for giving us Your Word. Give us humble and teachable hearts, '
        'grant us truth, wisdom, and love as we study and share together, and help us live what we learn. '
        'We pray in the name of Jesus Christ. Amen.'
    )


def guarded_ollama(messages):
    request=_current_request(messages)
    task,comparative=classify_ministry_task(request)
    if not task or comparative:
        return _RAW_OLLAMA(messages)

    instruction=christian_ministry_instruction(task)
    prepared=_with_authority(messages,instruction)
    candidate=_RAW_OLLAMA(prepared)
    gate=christian_ministry_gate(candidate,task=task,comparative_context=False)
    attempts=0
    while not gate.allowed and attempts<_MAX_RETRIES:
        attempts+=1
        repair=(
            'The previous candidate did not pass Doré Christian ministry admission. '
            'Regenerate the answer from the original user request. Preserve the requested meaning, '
            'remain explicitly Christian and Scripture-centered, and satisfy the Christian ministry '
            'authority instruction. Do not discuss the failed candidate or the admission process.'
        )
        candidate=_RAW_OLLAMA(_with_authority(prepared,repair))
        gate=christian_ministry_gate(candidate,task=task,comparative_context=False)
    if gate.allowed:
        return candidate

    # Fail closed. No rejected candidate is returned, saved, or displayed.
    # Prayer has a deterministic positive-authority fallback so the product remains usable
    # even when the model repeatedly misses the admission contract.
    if task=='prayer':
        fallback=_safe_prayer_fallback(request)
        fallback_gate=christian_ministry_gate(fallback,task='prayer',comparative_context=False)
        if fallback_gate.allowed:
            return fallback
    return '這個候選內容沒有通過基督教事工內容的權威邊界，因此沒有交付。'


runtime.ollama=guarded_ollama

if __name__=='__main__':
    runtime.main()
