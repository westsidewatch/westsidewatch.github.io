#!/usr/bin/env python3
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parents[2]
resource=json.loads((ROOT/'cinema/data/video-resource.v0.json').read_text())
items={item['canonicalId']:item for item in resource['items']}

jesus=items['cinema:video:jesus-film:jesus']['providerSources'][0]
pawson=items['cinema:video:david-pawson:unlocking-matthew-1']['providerSources'][0]
waiting=items['cinema:video:goodtv:waiting-on-god-no-minute-wasted']['providerSources'][0]
goodtv=items['cinema:video:goodtv:holy-spirit-power-workplace-testimony']['providerSources'][0]

assert jesus['preview']['mode']=='official-poster'
assert jesus['preview']['posterUrl'].startswith('https://image.mux.com/')
assert jesus['preview']['hoverPreview'] is False
for source in (pawson,waiting):
    assert source['provider']=='youtube'
    assert source['preview']['mode']=='muted-hover'
    assert source['preview']['hoverPreview'] is True
    assert source['preview']['posterUrl'].startswith('https://i.ytimg.com/vi/')
assert goodtv['preview']['mode']=='handoff-only'
assert goodtv['preview']['hoverPreview'] is False

index=(ROOT/'cinema/index.html').read_text()
controller=(ROOT/'cinema/preview-controller.js').read_text()
style=(ROOT/'cinema/preview-layer.css').read_text()
assert 'preview-layer.css' in index
assert 'preview-controller.js' in index
assert index.index('cinema.js') < index.index('preview-controller.js')
assert 'youtube-nocookie.com' in controller
assert "url.searchParams.set('mute','1')" in controller
assert "url.searchParams.set('autoplay','1')" in controller
assert 'HOVER_DELAY=420' in controller
assert "poster.querySelector('.living-poster__play-mark')?.remove()" in controller
assert '.resource-preview.is-previewing iframe' in style
assert '.living-poster__poster[data-preview-ready="true"]' in style
print('Holy Light Cinema preview layer acceptance: PASS')
