#!/usr/bin/env python3
"""Doré Engraving Lab: dependency-free, deterministic SVG engraving renderer.
Usage: python3 scripts/dore_engraving.py --subject architecture --style wood --output /tmp/engraving.svg
Synthetic motifs are original geometry; no portraits, downloads, paid APIs or external models.
"""
import argparse, math, html
from pathlib import Path

INK="#174B35"
PAPER="#FFFFFF"
W,H=900,1200
def line(x1,y1,x2,y2,width=1.2):
    return f'<path d="M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}" stroke-width="{width:.2f}"/>'
def hatch_polygon(points,angle=35,spacing=10,width=1.1):
    # Scanline clipping in rotated coordinates; strokes remain inside silhouette.
    t=math.radians(angle);ux,uy=math.cos(t),math.sin(t);vx,vy=-uy,ux
    q=[(x*ux+y*uy,-x*uy+y*ux) for x,y in points]
    lo,hi=min(y for x,y in q),max(y for x,y in q)
    out=[]
    k=math.floor(lo/spacing)
    while k*spacing<=hi:
        yy=k*spacing;xs=[]
        for (ax,ay),(bx,by) in zip(q,q[1:]+q[:1]):
            if (ay<=yy<by) or (by<=yy<ay):
                xs.append(ax+(yy-ay)*(bx-ax)/(by-ay))
        xs.sort()
        for a,b in zip(xs[::2],xs[1::2]):
            if b-a<0.5:continue
            x1,y1=a*ux-yy*uy,a*uy+yy*ux
            x2,y2=b*ux-yy*uy,b*uy+yy*ux
            out.append(line(x1,y1,x2,y2,width))
        k+=1
    return ''.join(out)
def poly(points):
    return '<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+'"/>'
def scene(subject,style):
    parts=[]
    def fill(points,depth=1):
        parts.append(hatch_polygon(points,35,7 if style=="wood" else 11,1.6 if style=="wood" else 1.15))
        if style in ("cross","wood") and depth>0:
            parts.append(hatch_polygon(points,117,14 if style=="cross" else 10,0.9))
    if subject=="architecture":
        # Temple-like architectural study; no claims of archaeological accuracy.
        for x in range(120,760,128):
            fill([(x,420),(x+74,420),(x+74,970),(x,970)],1)
            parts.append(f'<rect x="{x}" y="420" width="74" height="550" fill="none" stroke-width="4"/>')
            for y in range(455,950,45):
                parts.append(line(x+5,y,x+68,y,0.6))
        fill([(90,360),(790,360),(730,420),(150,420)],2)
        fill([(85,970),(790,970),(820,1010),(55,1010)],1)
        for x in range(110,810,18):parts.append(line(x,1030,x-18,1110,0.65))
    elif subject=="sphere":
        # Variable chord lengths create engraved light/shadow with reserved highlight.
        cx,cy,r=450,640,290
        for y in range(cy-r,cy+r,7 if style=="wood" else 11):
            d=math.sqrt(max(0,r*r-(y-cy)**2))
            left,right=cx-d,cx+d
            cut=left+0.34*(right-left)
            if y<cy-60:cut=left+0.58*(right-left)
            parts.append(line(cut,y,right,y,1.3))
            if style in ("cross","wood") and y>cy-20:
                parts.append(line(left+0.58*(right-left),y-3,right,y+13,0.8))
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke-width="2"/>')
    elif subject=="landscape":
        for i in range(26):
            a=math.radians(-160+i*6)
            parts.append(line(455,390,455+730*math.cos(a),390+730*math.sin(a),0.55+i%3*0.35))
        for i in range(7):
            y=690+i*58
            points=[(35,y+20),(160,y-50-i*2),(320,y+30),(490,y-80+i*3),(700,y-10),(865,y+50),(865,1130),(35,1130)]
            fill(points,i%2)
    else:
        # Drapery: ribbon polygons with changing width and directional hatching.
        for i in range(8):
            x=145+i*80
            pts=[(x,280),(x+65,320),(x+95,510),(x+42,730),(x+85,1010),(x-10,1070),(x+5,780),(x-20,510)]
            fill(pts,i%2)
    return ''.join(parts)
def render(subject="architecture",style="wood",ink=INK,paper=PAPER):
    if subject not in ("architecture","sphere","landscape","drapery"):raise ValueError("unknown subject")
    if style not in ("parallel","cross","wood"):raise ValueError("unknown style")
    for color in (ink,paper):
        if len(color)!=7 or color[0]!="#" or any(c not in "0123456789abcdefABCDEF" for c in color[1:]):raise ValueError("invalid color")
    body=scene(subject,style)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{html.escape(subject)} engraving"><rect width="{W}" height="{H}" fill="{paper}"/><g fill="none" stroke="{ink}" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>\n'
def main():
    p=argparse.ArgumentParser();p.add_argument("--subject",choices=["architecture","sphere","landscape","drapery"],default="architecture")
    p.add_argument("--style",choices=["parallel","cross","wood"],default="wood")
    p.add_argument("--ink",default=INK);p.add_argument("--paper",default=PAPER)
    p.add_argument("--output",required=True);a=p.parse_args()
    path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(render(a.subject,a.style,a.ink,a.paper),encoding="utf-8")
    print(path)
if __name__=="__main__":main()
