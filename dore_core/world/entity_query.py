"""Natural-language intent routing for BW-1 entity questions."""
from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class EntityQuestion:
    kind: str
    mention: str
    entity_type: str | None = None
    scope: str = 'canon'

_COUNT_PATTERNS=(
    re.compile(r'^(?:聖經|圣经)(?:中|裡|里)?(?:一共|總共|总共)?有(?:幾|几|多少)(?:位|個|个)?(.+?)[？?]?$'),
    re.compile(r'^(?:聖經|圣经)(?:中|裡|里)?(.+?)(?:一共|總共|总共)?有(?:幾|几|多少)(?:位|個|个)?[？?]?$'),
)

def parse_entity_question(text:str)->EntityQuestion|None:
    q=re.sub(r'\s+','',text or '')
    for p in _COUNT_PATTERNS:
        m=p.match(q)
        if m:
            mention=m.group(1).strip('？?，,。')
            if mention:return EntityQuestion('entity_count',mention,'person','canon')
    return None
