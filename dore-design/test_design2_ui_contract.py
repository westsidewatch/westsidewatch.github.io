#!/usr/bin/env python3
import design2_ui

def test_contract():
    out=design2_ui.install('<html><head></head><body>DORÉ DESIGN 1.9 · PROMOTION PIPELINE</body></html>')
    for marker in ['DORÉ · SAME ARTIFACT','id="d2-command"','data-tool="select"','data-tool="frame"','data-tool="text"','data-tool="asset"','id="d2-zoom"','Search Design commands','multiwrite-home','⌘K']:
        assert marker in out, marker

if __name__=='__main__':
    test_contract();print('DESIGN2_UI_CONTRACT_PASS')
