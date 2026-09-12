"""Explicitly withdrawn resources/providers: never re-ingest or publish them.

Wikisource is isolated as a single forbidden source. This boundary must not
change admission behavior for any other provider.
"""
import json
from urllib.parse import unquote

TITLES = (
    '巴勒斯坦、阿拉伯人民反击以色列侵略',
    '巴勒斯坦游击队不断袭击以色列侵略军',
    '巴勒斯坦、阿拉伯人民反擊以色列侵略',
    '巴勒斯坦游擊隊不斷襲擊以色列侵略軍',
)
IDS = ('zh-wikisource-b4099fc5e7d8', 'zh-wikisource-6837d67baf5e')
BLOCKED_SOURCE_MARKERS = (
    'wikisource.org',
    'zh.wikisource.org',
    'wikisource',
    '維基文庫',
    '维基文库',
)

def excluded(item):
    text = unquote(json.dumps(item, ensure_ascii=False))
    folded = text.casefold()
    return (
        any(value in text for value in TITLES + IDS)
        or any(value.casefold() in folded for value in BLOCKED_SOURCE_MARKERS)
    )
