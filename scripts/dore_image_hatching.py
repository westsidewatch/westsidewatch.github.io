#!/usr/bin/env python3
"""Deterministic image-to-hatching SVG renderer (PGM P2/P5, zero dependencies).
Accepts REAL grayscale raster input; each hatch is clipped to local tonal mask.
No paid API. No third-party dependency. This is a baseline, not historical engraving.
"""
import argparse, math, hashlib
from pathlib import Path

def read_pgm(path):
    data=Path(path).read_bytes()
    i=0
    def token():
        nonlocal i
        while i<len(data):
            if data[i] in b' \t\r\n':i+=1;continue
            if data[i]==35:
                while i<len(data) and data[i]!=10:i+=1
                continue
            break
        start=i
        while i<len(data) and data[i] not in b' \t\r\n#':i+=1
        if start==i:raise ValueError('truncated PGM header')
        return data[start:i]
    magic=token();w=int(token());h=int(token());maxval=int(token())
    if magic not in (b'P2',b'P5') or not 0<w<=5000 or not 0<h<=5000 or not 0<maxval<=255:raise ValueError('unsupported PGM')
    if magic==b'P2':values=[int(token()) for _ in range(w*h)]
    else:
        if i>=len(data) or data[i] not in b' \t\r\n':raise ValueError('PGM separator missing')
        i+=1;values=list(data[i:i+w*h])
    if len(values)!=w*h or any(not 0<=v<=maxval for v in values):raise ValueError('invalid PGM pixel data')
    return w,h,[v/maxval for v in values]
def engrave(w,h,pixels,style='cross',spacing=5,ink='#174B35',paper='#FFFFFF'):
    if style not in ('parallel','cross','wood'):raise ValueError('unsupported style')
    if not 2<=spacing<=40:raise ValueError('spacing out of range')
    for color in (ink,paper):
        if len(color)!=7 or color[0]!='#' or any(c not in '0123456789abcdefABCDEF' for c in color[1:]):raise ValueError('invalid color')
    paths=[]
    # Multi-direction line screens; threshold on local pixel luminance, not arbitrary decoration.
    angles=[(0,0.78)]
    if style in ('cross','wood'):angles.append((90,0.56))
    if style=='wood':angles.append((45,0.32))
    for angle,threshold in angles:
        theta=math.radians(angle);dx,dy=math.cos(theta),math.sin(theta)
        nx,ny=-dy,dx
        extent=math.hypot(w,h)
        n=int(extent/spacing)+2
        for k in range(-n,n+1):
            off=k*spacing
            run=None;prev=None
            for j in range(-n*spacing,n*spacing+1,2):
                x=w/2+nx*off+dx*j;y=h/2+ny*off+dy*j
                ix=int(x);iy=int(y)
                inside=0<=ix<w and 0<=iy<h
                dark=inside and pixels[iy*w+ix]<threshold
                if dark:
                    if run is None:run=(x,y)
                    prev=(x,y)
                elif run is not None:
                    if prev and math.dist(run,prev)>=3:
                        paths.append(f'M{run[0]:.1f},{run[1]:.1f}L{prev[0]:.1f},{prev[1]:.1f}')
                    run=None;prev=None
            if run and prev and math.dist(run,prev)>=3:paths.append(f'M{run[0]:.1f},{run[1]:.1f}L{prev[0]:.1f},{prev[1]:.1f}')
    if len(paths)>200000:raise ValueError('excessive path count')
    path=''.join(f'<path d="{p}"/>' for p in paths)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="{paper}"/><g fill="none" stroke="{ink}" stroke-width=".85" stroke-linecap="round">{path}</g></svg>\n'
def main():
    p=argparse.ArgumentParser()
    p.add_argument('input',help='PGM P2 or P5 raster')
    p.add_argument('--output',required=True)
    p.add_argument('--style',choices=['parallel','cross','wood'],default='cross')
    p.add_argument('--spacing',type=int,default=5)
    a=p.parse_args();w,h,pixels=read_pgm(a.input)
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    svg=engrave(w,h,pixels,a.style,a.spacing);out.write_text(svg,encoding='utf-8')
    print(f'{out} sha256={hashlib.sha256(svg.encode()).hexdigest()}')
if __name__=='__main__':main()
