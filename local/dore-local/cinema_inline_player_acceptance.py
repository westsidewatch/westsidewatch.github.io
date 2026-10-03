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
assert source['access']=='official-hls-playback'
assert source['streamUrl'].startswith('https://stream.mux.com/') and source['streamUrl'].endswith('.m3u8')
assert source['embedPermissionUrl']=='https://www.jesusfilm.org/about/faq/'
tracks=source['subtitleTracks']
assert tracks[0]['srclang']=='zh-Hant' and tracks[0]['label']=='中文（繁體）' and tracks[0]['default'] is True
assert any(track['srclang']=='zh-Hans' for track in tracks)

index=(ROOT/'cinema/index.html').read_text()
adapter=(ROOT/'cinema/provider-adapters.js').read_text()
script=(ROOT/'cinema/cinema.js').read_text()
style=(ROOT/'cinema/inline-player.css').read_text()
play_control=(ROOT/'cinema/play-control.js').read_text()
assert 'vendor/hls.min.js' in index and index.index('vendor/hls.min.js') < index.index('provider-adapters.js') < index.index('cinema.js')
assert 'play-control.js' in index and index.index('cinema.js') < index.index('play-control.js')
assert 'HolyLightProviders' in adapter and "kind:'hls'" in adapter and 'window.Hls' in adapter and 'video.controls=true' in adapter
assert "['embed','hls']" in script and 'cinema-feature__play' in script and 'HolyLightProviders?.mount' in script
assert '.living-poster.is-playing' in style

if os.getenv('CINEMA_PROVIDER_PROBE')=='1':
    request=urllib.request.Request(source['streamUrl'],headers={'User-Agent':'Mozilla/5.0 HolyLightCinemaAcceptance/1.0'})
    with urllib.request.urlopen(request,timeout=20) as response:
        assert 200 <= response.status < 400, response.status
        body=response.read(65536).decode('utf-8','ignore')
        assert '#EXTM3U' in body

print('Holy Light Cinema inline HLS player acceptance: PASS')
