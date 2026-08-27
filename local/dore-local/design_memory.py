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
    if any(k in s for k in ALWAYS_IN_SCOPE):
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
    by_id = {x.evidence_id: x for x in rows}
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
