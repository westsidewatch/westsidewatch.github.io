#!/usr/bin/env python3
import json
import os
import pathlib
import urllib.request

ROOT=pathlib.Path(__file__).resolve().parents[2]
resource=json.loads((ROOT/'cinema/data/video-resource.v0.json').read_text())
items={item['canonicalId']:item for item in resource['items']}
jesus=items['cinema:video:jesus-film:jesus']
source=jesus['providerSources'][0]
assert jesus['sourcePointer']=='https://www.jesusfilm.org/watch/jesus.html'
assert jesus['rights']['rehost'] is False
assert source['official'] is True
assert source['embed'] is True
assert source['access']=='embedded-playback'
assert source['embedUrl'].startswith('https://api.arclight.org/videoPlayerUrl?')
assert 'refId=1_529-jf-0-0' in source['embedUrl']
assert source['embedPermissionUrl']=='https://www.jesusfilm.org/about/faq/'

index=(ROOT/'cinema/index.html').read_text()
adapter=(ROOT/'cinema/provider-adapters.js').read_text()
script=(ROOT/'cinema/cinema.js').read_text()
style=(ROOT/'cinema/inline-player.css').read_text()
assert 'provider-adapters.js' in index and index.index('provider-adapters.js') < index.index('cinema.js')
assert 'HolyLightProviders' in adapter and 'iframe' in adapter
assert 'mountInlinePlayer' in script and "dataset.cinemaPlayback='inline'" in script
assert '.living-poster.is-playing' in style

if os.getenv('CINEMA_PROVIDER_PROBE')=='1':
    request=urllib.request.Request(source['embedUrl'],headers={'User-Agent':'Mozilla/5.0 HolyLightCinemaAcceptance/1.0'})
    with urllib.request.urlopen(request,timeout=20) as response:
        assert 200 <= response.status < 400, response.status
        body=response.read(65536).decode('utf-8','ignore').lower()
        assert '<html' in body or '<iframe' in body or '<video' in body or 'brightcove' in body or 'player' in body

print('Holy Light Cinema inline player acceptance: PASS')
