#!/usr/bin/env python3
import design2_snap_guides

def test_augment_contract():
    html='<html><head></head><body><div class="canvas"><div data-id="x"></div></div></body></html>'
    out=design2_snap_guides.augment(html)
    assert 'd2-snap-guides-js' in out
    assert 'd2-guide v' in out
    assert 'd2-multi-selected' in out
    assert 'SNAP=6' in out
    assert 'e.shiftKey' in out
    assert "saveAll" in out

if __name__=='__main__':
    test_augment_contract();print('PASS')
