#!/usr/bin/env python3
import living_water_candidate as c
html=c.render(edit=True)
assert c.PAGE_ID=='living-water-candidate-01'
assert 'Scripture Cinema' in html
assert '守望' in html and 'Daylight' in html and 'Watch Prayer' in html and '黎明書局' in html
assert '三更報導' not in html
assert 'river-progress' in html and 'view-timeline' in html
assert 'prefers-reduced-motion' in html
assert '8:5' in html
print('living-water-candidate-01: PASS')
