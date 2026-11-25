from pathlib import Path
from shapely.geometry import Polygon, box, LineString
from shapely.ops import unary_union
from shapely.affinity import translate, scale, rotate
import json
out=Path(__file__).resolve().parent
P={'water':[1,2,1,3,1,2],'olive':[3,2,1,2,3],'library':[2,3,3,2,1],'cinema':[1,1,2,3,3]}
F=box(0,0,300,300)
def step(ds,x,y,w,u,bottom):
    p=[(x,bottom),(x,y+ds[0]*u)]
    for i,d in enumerate(ds):
        if i:p.append((x+i*w/len(ds),y+d*u))
        p.append((x+(i+1)*w/len(ds),y+d*u))
    p.append((x+w,bottom));return Polygon(p)
def path(p):
    if p.is_empty:return ''
    if p.geom_type!='Polygon':return ' '.join(path(q) for q in p.geoms if q.geom_type in ['Polygon','MultiPolygon'])
    def ring(r):return 'M'+' L'.join(f'{x:.3f} {y:.3f}' for x,y in list(r.coords)[:-1])+'Z'
    return ' '.join([ring(p.exterior)]+[ring(r) for r in p.interiors])
def svgpath(g):return f'<path d="{path(g)}" fill="currentColor" fill-rule="evenodd"/>'
def curve(points):
    a,b,c,d=points;return LineString([tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k] for k in [0,1]) for t in [i/120 for i in range(121)]])
bank=step(P['water'],-18,41,336,20,330).intersection(F)
river=curve([(-30,255),(99,300),(118,34),(333,67)])
solid=bank.difference(river.buffer(19,cap_style=2,join_style=1))
cuts=[]
for delta,width in [(-31,1.3),(-37,1.5),(-45,2.1),(-55,3.1),(30,1.4),(37,1.8),(46,2.5),(59,3.4),(77,4.2)]:
    cuts.append(translate(river,yoff=delta).buffer(width/2,cap_style=2))
water=solid.difference(unary_union(cuts))
water=water.union(translate(river,yoff=-31).buffer(.85,cap_style=2).intersection(F).difference(bank))
water=unary_union([g for g in water.geoms if g.area>=14]) if water.geom_type=='MultiPolygon' else water
peak=step(P['olive'],-103,10,375,44,330)
contours=[]
for offset,weight in [(0,5),(10,2.8),(23,2.1),(40,1.8),(61,1.5),(86,1.3)]:
    contours.append(peak.buffer(offset,join_style=2).boundary.buffer(weight/2,join_style=2).intersection(F))
ridge=peak.intersection(box(-120,0,350,96)).intersection(F)
olive=unary_union(contours+[ridge]).intersection(F)
base=step(P['library'],0,0,250,11,83)
left=translate(rotate(base,-90,origin=(0,0)),xoff=5,yoff=280).intersection(F)
right=step(P['library'],111,17,211,14,300).intersection(F).difference(box(111,92,236,292)).difference(box(111,283,236,310))
rules=unary_union([box(129,y,129+w,y+1.5) for y,w in [(122,70),(131,81),(140,64),(160,80),(169,75),(178,54),(201,70),(210,78)]])
library=unary_union([left,right,rules]).intersection(F)
top=step(P['cinema'],-30,-6,360,17,113).intersection(F)
bottom=scale(step(P['cinema'],-30,-6,360,17,132),1,-1,origin=(150,150)).intersection(F)
screen=box(12,82,268,226)
cinema=unary_union([top.difference(screen),bottom.difference(screen)]).difference(box(268,82,300,226)).intersection(F)
cinema=cinema.difference(unary_union([box(0,62,300,63.5),box(0,252,300,253.5)]))
arts={k:g.simplify(.12,preserve_topology=True) for k,g in {'water':water,'olive':olive,'library':library,'cinema':cinema}.items()}
for k,g in arts.items():assert g.is_valid and F.covers(g),k
symbols=''.join(f'<symbol id="original-{k}" viewBox="0 0 {len(ds)*8} 8">{svgpath(step(ds,0,0,len(ds)*8,1,8))}</symbol>' for k,ds in P.items())+''.join(f'<symbol id="art-{k}" viewBox="0 0 300 300">{svgpath(g)}</symbol>' for k,g in arts.items())
(out/'watch-rhythm-assets.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg">{symbols}</svg>')
report={k:{'valid':g.is_valid,'ink_fraction':round(g.area/F.area,4),'components':len(g.geoms) if g.geom_type=='MultiPolygon' else 1,'source_depths':P[k]} for k,g in arts.items()}
(out/'report.json').write_text(json.dumps(report,indent=2));print(report)
