"""Explicitly withdrawn resources: never re-ingest or publish them."""
import json
from urllib.parse import unquote

TITLES = (
    '巴勒斯坦、阿拉伯人民反击以色列侵略',
    '巴勒斯坦游击队不断袭击以色列侵略军',
    '巴勒斯坦、阿拉伯人民反擊以色列侵略',
    '巴勒斯坦游擊隊不斷襲擊以色列侵略軍',
)
IDS = ('zh-wikisource-b4099fc5e7d8', 'zh-wikisource-6837d67baf5e')

def excluded(item):
    text = unquote(json.dumps(item, ensure_ascii=False))
    return any(value in text for value in TITLES + IDS)
