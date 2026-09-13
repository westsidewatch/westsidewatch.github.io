#!/usr/bin/env python3
from urllib.request import Request, urlopen

TRACKS = {
    'en': 'https://api-media-core.jesusfilm.org/1_jf-0-0/editions/ot/subtitles/1_jf-0-0_ot_529.vtt',
    'zh-Hant': 'https://api-media-core.jesusfilm.org/1_jf-0-0/editions/ot/subtitles/1_jf-0-0_ot_21753.vtt',
}
TARGET = 'Love your enemies'
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/140.0 Safari/537.36',
    'Accept':'text/vtt,text/plain,*/*',
    'Referer':'https://api.arclight.org/',
    'Origin':'https://api.arclight.org',
}

for lang, url in TRACKS.items():
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=30) as response:
        text = response.read().decode('utf-8', errors='replace')
    print(f'{lang}_STATUS={getattr(response, "status", 200)}')
    print(f'{lang}_WEBVTT={text.startswith("WEBVTT")}')
    if lang == 'en':
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if TARGET.lower() in line.lower():
                lo = max(0, i-3)
                hi = min(len(lines), i+5)
                print('MATCH_BEGIN')
                print('\n'.join(lines[lo:hi]))
                print('MATCH_END')
                break
        else:
            raise SystemExit('target English cue not found')
