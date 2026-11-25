#!/usr/bin/env python3
"""Reproduce the local 096 shape-grammar geometry proof, no production dependency."""
from shapely.geometry import Polygon, box
from shapely.affinity import scale, translate
from shapely.ops import unary_union
from pathlib import Path
import cairosvg, json
OUT=Path(__file__).resolve().parent
profiles={'Living Water':[1,2,1,3,1,2],'Olive Mountain':[3,2,1,2,3],'Dawn Library':[2,3,3,2,1],'Paradise Cinema':[1,1,2,3,3]}
def mark(d):
    pts=[(0,8),(0,d[0])]
    for i,v in enumerate(d):
        if i: pts.append((i*8,v))
        pts.append(((i+1)*8,v))
    pts.append((len(d)*8,8))
    return Polygon(pts)
def path(p):
    if p.is_empty: return ''
    if p.geom_type!='Polygon': return ' '.join(path(x) for x in p.geoms)
    def ring(r): return 'M'+' L'.join(f'{x:.4f} {y:.4f}' for x,y in r.coords[:-1])+' Z'
    return ' '.join([ring(p.exterior)]+[ring(r) for r in p.interiors])
W,H=240,120
field=box(0,0,W,H)
ink='#252525'; paper='#faf9f5'; muted='#d9d7cf'
shifts=[(25,22,76,76),(95,19,63,63),(154,19,47,75.2),(32,10,176,99)]
records=[];svg=[]
def add(s): svg.append(s)
def geom(p,c): return f'<path fill="{c}" fill-rule="evenodd" d="{path(p)}"/>'
def txt(x,y,s,size=16,weight=400,fill=ink): return f'<text x="{x}" y="{y}" font-family="Georgia,serif" font-size="{size}" font-weight="{weight}" fill="{fill}">{s}</text>'
add('<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="860" viewBox="0 0 1320 860">')
add(f'<rect width="1320" height="860" fill="{paper}"/>')
add(txt(55,64,'Watch Rhythm.',46));add(txt(56,92,'WESTSIDE WATCH     /     OPTICAL STUDY     /     096',12))
add('<path d="M55 115H1265" stroke="#252525" stroke-width="1"/>')
for i,(name,d) in enumerate(profiles.items()):
    x=55+i*309; y=145
    original=mark(d)
    source=translate(scale(original,1.6,1.6,origin=(0,0)),xoff=x,yoff=y+16)
    add(txt(x,y,name,22));add(geom(source,ink))
    lower=translate(scale(original,W/(8*len(d)),18,origin=(0,0)),yoff=30).intersection(field)
    upper=field.difference(lower)
    ax,ay,aw,ah=shifts[i]; opening=box(ax,ay,ax+aw,ay+ah)
    assert field.covers(opening)
    assert lower.intersection(upper).area < 1e-8
    assert abs(unary_union([lower,upper]).area-field.area)<1e-8
    result=lower.symmetric_difference(opening)
    inverse=field.difference(result)
    assert result.is_valid and inverse.is_valid
    assert result.intersection(inverse).area < 1e-8
    assert abs(result.area+inverse.area-field.area)<1e-8
    records.append(dict(name=name,source_width=8*len(d),source_depths=d,opening=[aw,ah],seam_complement_error=round(abs(lower.area+upper.area-field.area),9),xor_complement_error=round(abs(result.area+inverse.area-field.area),9),ink_coverage=round(result.area/field.area,4)))
    for j,(label,p) in enumerate([('01  /  Shared edge',lower),('02  /  Figure–ground exchange',result),('03  /  Reverse proof',inverse)]):
        yy=218+j*178
        add(txt(x,yy-10,label,12))
        add(f'<g transform="translate({x} {yy})">')
        add(f'<rect x="0" y="0" width="240" height="120" fill="{paper}" stroke="{muted}" stroke-width="0.75"/>')
        add(geom(p,ink));add('</g>')
    add(txt(x,778,'Micro',11))
    for j,s in enumerate([0.5,0.8,1.1]):
        add(geom(translate(scale(original,s,s,origin=(0,0)),xoff=x+62+j*57,yoff=767),ink))
    add(f'<rect x="{x}" y="799" width="240" height="30" fill="{ink}"/>')
    add(geom(translate(scale(original,.8,.8,origin=(0,0)),xoff=x+12,yoff=810),paper))
add('</svg>')
svg=''.join(svg)
(OUT/'watch-rhythm-optical-study.svg').write_text(svg)
cairosvg.svg2png(bytestring=svg.encode(),write_to=str(OUT/'watch-rhythm-optical-study.png'))
(OUT/'optical-study-report.json').write_text(json.dumps(records,indent=2))
print(json.dumps(records,indent=2))
