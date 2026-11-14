#!/usr/bin/env python3
"""Produce 04 right-side Mount of Olives contour artwork from real terrain data.

Source: AWS Open Data / Mapzen Terrain Tiles (Terrarium, SRTM global source).
Bounds include Olivet ridge and the Kidron Valley, not invented waveforms.
Static build-time process: no network requests, raster or contour math in browser.
Line topology follows measured DEM; drawing stroke/style stays in Design OS.
Data documentation: https://registry.opendata.aws/terrain-tiles/
Rendering style reference only: Metaphor of The Times (Golden Pin).
"""
import io
import math
import pathlib
import urllib.request
import numpy as np
from PIL import Image
from contourpy import contour_generator

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'static/images/p2-realms/v15/04-olive-mount-terrain-contours-v1.svg'
Z=13
WEST,EAST,SOUTH,NORTH=35.236,35.253,31.772,31.790
W,H=900,960

def xyz(lon,lat):
    n=2**Z
    return ((lon+180)/360*n, (1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n)

ax,ay=xyz(WEST,NORTH)
bx,by=xyz(EAST,SOUTH)
x0,x1=math.floor(ax),math.floor(bx)
y0,y1=math.floor(ay),math.floor(by)
mosaic=np.zeros(((y1-y0+1)*256,(x1-x0+1)*256),dtype=np.float32)
for y in range(y0,y1+1):
    for x in range(x0,x1+1):
        url=f'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{Z}/{x}/{y}.png'
        req=urllib.request.Request(url,headers={'User-Agent':'WestsideWatch-P2-OpenTerrain-Builder/1.0'})
        with urllib.request.urlopen(req,timeout=35) as resp:
            tile=np.asarray(Image.open(io.BytesIO(resp.read())).convert('RGB'),dtype=np.float32)
        elevation=tile[:,:,0]*256+tile[:,:,1]+tile[:,:,2]/256-32768
        mosaic[(y-y0)*256:(y-y0+1)*256,(x-x0)*256:(x-x0+1)*256]=elevation
# Bilinear resampling to the displayed geographic envelope.
# Pixel rows increase north->south, so the SVG maintains map north at top.
ix=np.linspace((ax-x0)*256,(bx-x0)*256,W)
iy=np.linspace((ay-y0)*256,(by-y0)*256,H)
xx,yy=np.meshgrid(ix,iy)
xlo=np.floor(xx).astype(int); ylo=np.floor(yy).astype(int)
xhi=np.minimum(xlo+1,mosaic.shape[1]-1)
yhi=np.minimum(ylo+1,mosaic.shape[0]-1)
fx=xx-xlo; fy=yy-ylo
z=(mosaic[ylo,xlo]*(1-fx)*(1-fy)
   +mosaic[ylo,xhi]*fx*(1-fy)
   +mosaic[yhi,xlo]*(1-fx)*fy
   +mosaic[yhi,xhi]*fx*fy)
# Smooth the DEM by a very small kernel before drawing editorial contours:
# topographic levels stay true, while raster quantization is suppressed.
for _ in range(2):
    p=np.pad(z,1,mode='edge')
    z=(p[1:-1,1:-1]*4+p[:-2,1:-1]+p[2:,1:-1]+p[1:-1,:-2]+p[1:-1,2:])/8
cg=contour_generator(z=z,line_type='Separate',corner_mask=True)
minlevel=int(math.ceil(np.percentile(z,5)/7.5)*7.5)
maxlevel=int(math.floor(np.percentile(z,98)/7.5)*7.5)
paths=[]
for level in np.arange(minlevel,maxlevel+0.01,7.5):
    for line in cg.lines(float(level)):
        if len(line)<24:continue
        # Downsample the contour, never redraw the terrain by formula.
        step=max(1,int(len(line)/290))
        pts=line[::step]
        if np.linalg.norm(pts[-1]-line[-1])>2:pts=np.vstack((pts,line[-1]))
        if len(pts)<8:continue
        d='M'+' L'.join(f'{p[0]:.1f},{p[1]:.1f}' for p in pts)
        major=abs(level/30-round(level/30))<.001
        paths.append(f'<path d="{d}" stroke-width="{1.2 if major else 0.65}" opacity="{0.76 if major else 0.50}"/>')
if len(paths)<12:raise RuntimeError(f'Insufficient real terrain contours: {len(paths)}')
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 960" width="900" height="960" fill="none" stroke="white" stroke-linecap="round" stroke-linejoin="round">
<title>Mount of Olives — measured terrain contour plate</title>
<desc>Georeferenced 7.5-meter contours derived at build time from Mapzen / AWS Open Data Terrarium DEM, western Kidron Valley and Mount of Olives ridge. Editorial line-weight system inspired by Metaphor of The Times; no third-party print artwork copied. Terrain © Mapzen contributors, AWS Open Data; see repository asset notes.</desc>
<g id="olivet-true-topography">
'''+''.join(paths)+'''</g></svg>
'''
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(svg,encoding='utf-8')
print(f'Generated {OUT} from real DEM, {len(paths)} contour paths, {len(svg)} bytes, elevation {float(z.min()):.1f}-{float(z.max()):.1f} m')
