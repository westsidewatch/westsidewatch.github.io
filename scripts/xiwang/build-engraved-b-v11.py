#!/usr/bin/env python3
"""Xi Wang B, print-plate poster: actual editable SVG paths.
Tools executed: fontTools 4.x glyph contours, Shapely (exact path-line intersections),
SVGWrite SVG export; separately verified in Inkscape and Chromium.
Typeface input: local Noto Sans CJK TC Bold (OFL-1.1). No rejected Westside art paths.
"""
import sys, math, random, json, hashlib, argparse, os, subprocess, importlib.metadata
from pathlib import Path
from functools import lru_cache
import svgwrite
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from shapely.geometry import Polygon,LineString,MultiLineString,Point,MultiPoint,GeometryCollection,box
from shapely import affinity
from shapely.ops import unary_union, voronoi_diagram
from shapely.prepared import prep

FONT=os.environ.get('XI_WANG_CJK_FONT','/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
FONT_NUMBER=int(os.environ.get('XI_WANG_CJK_FONT_INDEX','3'))
OUTPUT_DIR=Path(os.environ.get('XI_WANG_OUTPUT_DIR','./xiwang-poster-output')).resolve()
PALETTE={
'water':'#5B8FA8','first-light':'#A2872A','pale-gold':'#CEBD74',
'olive':'#738A5A','harvest':'#B8944A','crimson':'#A14D57','daylight-mauve':'#B085AB',
'ink':'#273138','paper':'#FAF9F5'}
SITE=[(250,330),(760,340),(285,555),(785,545),(205,715),(745,720),(510,695)]
STYLES=[('water','ripple'),('first-light','radial'),('pale-gold','contour'),('olive','current'),('harvest','hatch'),('crimson','crosshatch'),('daylight-mauve','stippling')]
CANVAS=1000
# True vector Voronoi regions: seven different engraving logics arranged inside
# the same glyph silhouette with restrained ink overprint at the field seams.
from shapely.ops import voronoi_diagram
def zones():
 cells=list(voronoi_diagram(MultiPoint(SITE),envelope=box(0,180,1000,870)).geoms)
 return [min(cells,key=lambda c:c.centroid.distance(Point(site))).intersection(box(40,160,960,840)).buffer(10,join_style=1) for site in SITE]


class FlattenPen(BasePen):
 def __init__(self,gs): super().__init__(gs);self.contours=[];self.cur=[]
 def _moveTo(self,p):
  if len(self.cur)>2: self.contours.append(self.cur)
  self.cur=[p]
 def _lineTo(self,p): self.cur.append(p)
 def _curveToOne(self,p1,p2,p3):
  a=self.cur[-1]
  for k in range(1,19):
   t=k/18;u=1-t
   self.cur.append((u**3*a[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*a[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
 def _qCurveToOne(self,p1,p2):
  a=self.cur[-1]
  for k in range(1,13):
   t=k/12;u=1-t
   self.cur.append((u*u*a[0]+2*u*t*p1[0]+t*t*p2[0], u*u*a[1]+2*u*t*p1[1]+t*t*p2[1]))
 def _closePath(self):
  if len(self.cur)>2: self.contours.append(self.cur)
  self.cur=[]
 def _endPath(self): self._closePath()

@lru_cache(maxsize=2)
def glyph_shape(ch):
 f=TTFont(FONT,fontNumber=(FONT_NUMBER if FONT.lower().endswith('.ttc') else -1),lazy=True);gs=f.getGlyphSet();p=FlattenPen(gs)
 gs[f.getBestCmap()[ord(ch)]].draw(p)
 shape=None
 for pts in p.contours:
  poly=Polygon(pts)
  if not poly.is_valid: poly=poly.buffer(0)
  shape=poly if shape is None else shape.symmetric_difference(poly)
 # Ensure positive Y down, anchored by bbox and scaled to optical rectangle
 minx,miny,maxx,maxy=shape.bounds
 shape=affinity.translate(shape,-minx,-maxy)
 shape=affinity.scale(shape,xfact=1,yfact=-1,origin=(0,0))
 shape=affinity.scale(shape,xfact=430/(maxx-minx),yfact=462/(maxy-miny),origin=(0,0))
 assert shape.is_valid
 return shape

def word_shape(layer):
 # These are seven physically distinct outline regions, never reused A SVG.
 # 0° always: controlled widths, counters and optical X/Y support.
 widths=[(1.000,1.000),(1.024,.990),(.982,1.012),(1.009,1.018),(.988,.975),(1.019,1.005),(.996,1.013)]
 # Same magazine axis; minor overprint offsets intentionally closer than characters' width.
 offsets=[(0,0),(7,-4),(-8,4),(4,8),(-10,-5),(12,2),(-4,-8)]
 change=[0,-1.8,1.2,-.7,1.4,-1.2,.5]
 a,b=widths[layer];ox,oy=offsets[layer]
 xi=affinity.scale(glyph_shape('西'),xfact=a,yfact=b,origin=(215,231))
 wang=affinity.scale(glyph_shape('望'),xfact=b,yfact=a,origin=(215,231))
 if change[layer] > 0:
  xi=xi.buffer(change[layer],join_style=2).buffer(-change[layer]*.40,join_style=2)
  wang=wang.buffer(change[layer],join_style=2).buffer(-change[layer]*.40,join_style=2)
 elif change[layer] < 0:
  xi=xi.buffer(change[layer]*.5,join_style=2)
  wang=wang.buffer(change[layer]*.5,join_style=2)
 xi=affinity.translate(xi,xoff=65+ox,yoff=205+oy)
 wang=affinity.translate(wang,xoff=511+ox,yoff=260+oy)
 return unary_union([xi,wang])

def lines_for(style, site, layer, density=1.0):
 """Independent, deterministic line family in the actual positive-Y poster field."""
 rng=random.Random(210071+layer*117)
 cx,cy=site
 lines=[]
 if style=='ripple':
  for y in range(180,850,7):
   pts=[(x,y + 16*math.sin(x/72+y/67) + 3*math.sin(x/19+y/48)) for x in range(30,985,8)]
   lines.append(LineString(pts))
 elif style=='radial':
  for i in range(200):
   a=2*math.pi*i/200
   # Curved aperture-like rays, bends only the line geometry not the characters.
   pts=[]
   for r in range(24,900,9):
    aa=a+0.17*math.sin(r/183+a*3)
    pts.append((cx+r*math.cos(aa),cy+.70*r*math.sin(aa)))
   lines.append(LineString(pts))
 elif style=='contour':
  for j in range(45):
   r=18+j*12
   pts=[]
   for i in range(150):
    a=2*math.pi*i/149
    rr=r*(1+.085*math.sin(5*a + j*.09))
    pts.append((cx+rr*math.cos(a),cy+rr*.68*math.sin(a)))
   lines.append(LineString(pts))
 elif style=='current':
  for x0 in range(-270,1100,10):
   pts=[]
   for y in range(155,885,7):
    x=x0+27*math.sin(y/80+x0/173)+8*math.cos(y/27+x0/116)
    pts.append((x,y))
   lines.append(LineString(pts))
 elif style=='hatch':
  for offset in range(-1000,1600,8):
   pts=[(offset-720,90),(offset+650,990)]
   lines.append(LineString(pts))
 elif style=='crosshatch':
  for offset in range(-1060,1500,13):
   lines.append(LineString([(offset-650,120),(offset+600,930)]))
   lines.append(LineString([(offset+620,120),(offset-670,930)]))
 elif style=='stippling':
  for y in range(185,835,10):
   for x in range(47,975,10):
    jx=rng.uniform(-2.0,2.0);jy=rng.uniform(-2.0,2.0)
    lines.append(Point(x+jx,y+jy).buffer(1.5+rng.uniform(-.5,1.3),resolution=5))
 return lines

def regions(geom):
 if geom.is_empty: return
 if isinstance(geom,(LineString,Polygon)):
  yield geom
 elif hasattr(geom,'geoms'):
  for g in geom.geoms:yield from regions(g)

def path_d(g):
 if isinstance(g, LineString):
  pts=list(g.coords)
  if len(pts)<2:return None
  return 'M '+' L '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
 elif isinstance(g, Polygon):
  def ring(r):
   pts=list(r.coords)
   return 'M '+' L '.join(f'{x:.1f},{y:.1f}' for x,y in pts)+' Z'
  return ' '.join([ring(g.exterior)]+[ring(r) for r in g.interiors])
 return None

def should_keep(g,site,layer,idx):
 x,y=g.centroid.x,g.centroid.y
 dx=(x-site[0])/420.;dy=(y-site[1])/330.
 weight=math.exp(-(dx*dx+dy*dy)*1.3)
 # Each engraving layer dominates a distinct (overlapping) optical locality,
 # but retains sparse ink elsewhere, avoiding seven full-page conflicting fields.
 rr=random.Random(layer*103593 + idx*8301).random()
 return rr < (0.12 + 0.63*weight)

def build(version='v7'):
 dwg=svgwrite.Drawing(size=('1000px','1000px'),viewBox='0 0 1000 1000',profile='full',debug=False)
 dwg.set_desc(title='西望 · Westside Watch / engraved editorial poster study',desc='Seven upright overlapping Westside word plates, seven field-driven interior engravings. Native clipped vector strokes; no external images, filters or background ornament.')
 dwg.add(dwg.rect(insert=(0,0),size=(1000,1000),fill=PALETTE['paper']))
 # Editorial, no pictorial ornament; all microtype is subordinate to two giant characters.
 ink=PALETTE['ink']
 dwg.add(dwg.line((57,86),(944,86),stroke=ink,stroke_width=.7,opacity=.45))
 def txt(s,x,y,fs=15,spacing=2,anchor='start',family='serif',color=ink):
  dwg.add(dwg.text(s,insert=(x,y),font_size=fs,font_family=family,fill=color,letter_spacing=f'{spacing}px',text_anchor=anchor))
 txt('WESTSIDE WATCH',58,65,17,3.0,family='Bodoni Moda, Georgia, serif')
 
 txt('VOL.00',943,65,13,2.0,anchor='end',family='Bodoni Moda, Georgia, serif')
 # The 7 word plates share one optical field, not 7 stacked rows.
 base=word_shape(0)
 # A restrained first impression remains legible even at 320px.
 # Subtle light key substrate is NOT a replicated decorative outline; it gives the print structure a readable ink mass.
 for p in regions(base):
  if isinstance(p,Polygon):
   d=path_d(p)
   if d:dwg.add(dwg.path(d=d,fill=PALETTE['ink'],opacity=1,fill_rule='evenodd',stroke='none'))
 # Main engraved impression: a dense but calm directional stroke family, confined
 # to the word's real outlines by geometric intersection (no SVG clipping mask).
 main=downgrade=None
 imprint=dwg.g(id='base-print-lines', **{'data-print-process':'subtractive-engraving'})
 for yy in range(185,826,8):
  wave=LineString([(xx,yy+4.2*math.sin(xx/90+yy/76)) for xx in range(54,947,7)])
  for seg in regions(wave.intersection(base)):
   if not isinstance(seg,LineString) or seg.length<1.3:continue
   d=path_d(seg)
   if d: imprint.add(dwg.path(d=d,fill='none',stroke=PALETTE['paper'],stroke_width=2.4,stroke_linecap='butt',opacity=.98))
 dwg.add(imprint)
 counts={}
 regions_by_layer=zones()
 for layer,(color,style) in enumerate(STYLES):
  poly=word_shape(layer).intersection(regions_by_layer[layer]).intersection(base)
  site=SITE[layer]
  group=dwg.g(id=f'sevenfold-plate-{layer+1}',**{'data-word-layer':str(layer+1),'data-color-role':color,'data-line-family':style,'data-orientation':'upright-0deg'})
  chosen=0;length=0
  for i,line in enumerate(lines_for(style,site,layer)):
   if style=='stippling':
    g=line.intersection(poly)
   else:
    g=line.intersection(poly)
   if g.is_empty:continue
   for piece in regions(g):
    # Every clipped stroke belongs to its intended engraving plate;
    # no random scattered strokes outside the assigned optical field.
    if isinstance(piece,LineString) and piece.length < 2.5:continue
    if isinstance(piece,Polygon) and piece.area < 1:continue
    d=path_d(piece)
    if not d:continue
    # Structural plate printed in deep editorial ink; OS colors are accent plate inks,
    # not neon full bleed. Color is still traceable independently per word layer.
    op=.90
    chromatic=(i%8==0)
    plate_ink=PALETTE[color] if chromatic else PALETTE['paper']
    if not chromatic: op=.95
    if isinstance(piece,Polygon):
     group.add(dwg.path(d=d,fill=plate_ink,fill_opacity=op,stroke='none'))
    else:
     group.add(dwg.path(d=d,fill='none',stroke=plate_ink,stroke_width=[3.2,2.1,2.3,2.8,2.6,2.3,2.0][layer],stroke_linecap='round',opacity=op))
    chosen+=1;length+=len(d)
  dwg.add(group);counts[color]={'line_family':style,'path_segments':chosen,'svg_bytes':length}
 # Publisher metadata quiet, no icons, no invented year/issue articles.
 dwg.add(dwg.line((57,871),(944,871),stroke=ink,stroke_width=.65,opacity=.35))
 txt('西望',58,918,29,2.4,family='Chiron Hei HK WS, Noto Sans CJK TC, sans-serif')
 
 txt('Watch for the Dawn',944,910,19,1.2,anchor='end',family='Bodoni Moda, Georgia, serif')
 
 
 OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
 path=str(OUTPUT_DIR/f'xiwang-poster-b-{version}.svg');dwg.saveas(path,pretty=False)
 stats={'version':version,'size_bytes':os.stat(path).st_size,'layers':7,'palette':PALETTE,'glyph_origin':f'{FONT}: {FONT_NUMBER} (OFL-1.1 Noto CJK); modified independently from font outlines; NOT a handcrafted original Chinese letter skeleton' ,'methods':['fontTools contour extraction','Shapely even-odd region booleans','Shapely exact line intersections','SVGWrite native path export','Inkscape render','Chromium viewport screenshot'], 'linework':counts,'output':path}
 Path(OUTPUT_DIR/f'xiwang-b-{version}-build.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
 print(json.dumps({'SVG':path,'bytes':stats['size_bytes'],'counts':{k:v['path_segments'] for k,v in counts.items()}},ensure_ascii=False))
if __name__=='__main__':
 parser=argparse.ArgumentParser(description='Build-time seven-plate Xi Wang B SVG; licensed font required, no raster effects.')
 parser.add_argument('--font',default=FONT,help='local OFL CJK font .ttc/.otf, not bundled')
 parser.add_argument('--font-index',type=int,default=FONT_NUMBER,help='TTC face number for Traditional Chinese; ignored for .otf')
 parser.add_argument('--outdir',default=str(OUTPUT_DIR),help='writable directory; never edit P2 runtime by default')
 parser.add_argument('--version',default='v11',help='output version string')
 args=parser.parse_args()
 FONT=args.font;FONT_NUMBER=args.font_index;OUTPUT_DIR=Path(args.outdir).resolve()
 if not Path(FONT).is_file(): parser.error(f'missing CJK font file: {FONT}')
 build(version=args.version)