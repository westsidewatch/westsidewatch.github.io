#!/usr/bin/env python3
"""Deterministic Design Working Memory primitives for Doré Local.

No model/API dependency. Raw evidence remains authoritative; this module adds
scope inheritance, truth-state metadata, and current-state consolidation.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable

TRUTH_STATES = (
    'observation','reference','proposal','attempt','evidence','decision',
    'rejected','corrected','final','verified'
)

WESTSIDE_PROJECT_HINTS = {
    'westside watch','西望','one','dore','多雷','dawn library','黎明書局',
    'westside stories','join','journal','西區的夜晚'
}
ALWAYS_IN_SCOPE = {'scripture','bible','聖經','圣经','church','教會','教会','theology','神學','神学'}
BIBLE_BOOK_HINTS = {
    '創世記','创世记','出埃及記','出埃及记','利未記','利未记','民數記','民数记','申命記','申命记',
    '約書亞記','约书亚记','士師記','士师记','路得記','路得记','撒母耳記','撒母耳记','列王紀','列王纪',
    '歷代志','历代志','以斯拉記','以斯拉记','尼希米記','尼希米记','以斯帖記','以斯帖记','約伯記','约伯记',
    '詩篇','诗篇','箴言','傳道書','传道书','雅歌','以賽亞書','以赛亚书','耶利米書','耶利米书','耶利米哀歌',
    '以西結書','以西结书','但以理書','但以理书','何西阿書','何西阿书','約珥書','约珥书','阿摩司書','阿摩司书',
    '俄巴底亞書','俄巴底亚书','約拿書','约拿书','彌迦書','弥迦书','那鴻書','那鸿书','哈巴谷書','哈巴谷书',
    '西番雅書','西番雅书','哈該書','哈该书','撒迦利亞書','撒迦利亚书','瑪拉基書','玛拉基书',
    '馬太福音','马太福音','馬可福音','马可福音','路加福音','約翰福音','约翰福音','使徒行傳','使徒行传',
    '羅馬書','罗马书','哥林多前書','哥林多前书','哥林多後書','哥林多后书','加拉太書','加拉太书','以弗所書','以弗所书',
    '腓立比書','腓立比书','歌羅西書','歌罗西书','帖撒羅尼迦前書','帖撒罗尼迦前书','帖撒羅尼迦後書','帖撒罗尼迦后书',
    '提摩太前書','提摩太前书','提摩太後書','提摩太后书','提多書','提多书','腓利門書','腓利门书','希伯來書','希伯来书',
    '雅各書','雅各书','彼得前書','彼得前书','彼得後書','彼得后书','約翰一書','约翰一书','約翰二書','约翰二书',
    '約翰三書','约翰三书','猶大書','犹大书','啟示錄','启示录','福音','經文','经文','耶穌','耶稣','耶和華','耶和华'
}

@dataclass(frozen=True)
class DesignEvidence:
    evidence_id: str
    content: str
    truth_state: str = 'observation'
    project_id: str = 'dore-global'
    scope: str = 'candidate'
    source_ref: str | None = None
    created_at: str | None = None
    supersedes: str | None = None

    def validate(self):
        if self.truth_state not in TRUTH_STATES:
            raise ValueError(f'unsupported truth_state: {self.truth_state}')
        return self

    def json(self):
        self.validate()
        return asdict(self)


def classify_scope(text: str, inherited_scope: str | None = None) -> str:
    """Conservative deterministic first pass; model enrichment may run later."""
    if inherited_scope in {'westside_brand','scripture_church_theology'}:
        return inherited_scope
    s = (text or '').lower()
    if any(k in s for k in ALWAYS_IN_SCOPE) or any(k.lower() in s for k in BIBLE_BOOK_HINTS):
        return 'scripture_church_theology'
    if any(k in s for k in WESTSIDE_PROJECT_HINTS):
        return 'westside_brand'
    return 'candidate'


def consolidate(items: Iterable[DesignEvidence]):
    """Build a current view without deleting rejected/corrected/raw evidence.

    Explicit supersedes wins. Otherwise later final/verified evidence can become
    current, while proposals/attempts never silently override a final rule.
    """
    rows = [x.validate() for x in items]
    superseded = {x.supersedes for x in rows if x.supersedes}
    active = [x for x in rows if x.evidence_id not in superseded]
    current = [x for x in active if x.truth_state in {'decision','final','verified'}]
    exploration = [x for x in active if x.truth_state in {'proposal','attempt'}]
    references = [x for x in active if x.truth_state in {'observation','reference','evidence'}]
    historical = [x for x in rows if x.truth_state in {'rejected','corrected'} or x.evidence_id in superseded]
    return {
        'current': [x.json() for x in current],
        'exploration': [x.json() for x in exploration],
        'references': [x.json() for x in references],
        'historical': [x.json() for x in historical],
        'unresolved': [x.json() for x in exploration],
        'evidence_count': len(rows),
    }
