"""Hebrew lexical resolver foundation for Doré."""
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class HebrewLexicalResolution:
    raw_value: str
    prefixes: tuple[str, ...]
    lexical_id: str
    lexeme: Optional[str]
    transliteration: Optional[str]
    source: str
    snapshot: str
    status: str

SEED = {
    "539": ("אמן", "amn"),
    "3068": ("יהוה", "YHWH"),
    "2803": ("חשב", "hshb"),
    "6666": ("צדקה", "tsdqah"),
}

def parse_oshb_lexical_value(raw_value: str):
    if not raw_value:
        raise ValueError("empty lexical value")
    parts = tuple(p for p in raw_value.split("/") if p)
    return parts[:-1], parts[-1]


def resolve_oshb_lexeme(raw_value: str, snapshot: str) -> HebrewLexicalResolution:
    prefixes, lexical_id = parse_oshb_lexical_value(raw_value)
    entry = SEED.get(lexical_id)
    if entry is None:
        return HebrewLexicalResolution(raw_value, prefixes, lexical_id, None, None, "dore.seed.hebrew.v0.1", snapshot, "unresolved")
    lexeme, transliteration = entry
    return HebrewLexicalResolution(raw_value, prefixes, lexical_id, lexeme, transliteration, "dore.seed.hebrew.v0.1", snapshot, "resolved")
