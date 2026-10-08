#!/usr/bin/env python3
"""Fail-closed image quality gate for Olive Mountain generated speaker backgrounds.
This is a mechanical preflight, NOT a portrait detector or aesthetic approval.
"""
import argparse,json
from pathlib import Path
def validate(path):
 from PIL import Image,ImageFilter,ImageStat
 im=Image.open(path).convert('RGB')
 if min(im.size)<512:return ['image resolution below 512px']
 im.thumbnail((512,512))
 pixels=list(im.getdata())
 n=len(pixels)
 # Olive palette: white/light neutrals or green, not orange/brown/blue/gold.
 def allowed(r,g,b):
  near_white=min(r,g,b)>=225 and max(r,g,b)-min(r,g,b)<=20
  olive_green=(g>=r*0.92 and g>=b*0.96 and r<=160 and b<=150 and g<=180 and (g>r*1.08 or g>b*1.08))
  dark_green=(r<=65 and g<=100 and b<=85 and g>=r*0.9)
  return near_white or olive_green or dark_green
 bad=sum(not allowed(*p) for p in pixels)/n
 gray=im.convert('L')
 edges=gray.filter(ImageFilter.FIND_EDGES)
 edge_stat=ImageStat.Stat(edges)
 mean_edge=edge_stat.mean[0]
 reasons=[]
 if bad>0.08:reasons.append(f'palette violation: {bad:.1%} pixels outside olive/white tolerance')
 if mean_edge<8:reasons.append(f'insufficient edge detail: {mean_edge:.1f}')
 if ImageStat.Stat(gray).stddev[0]<25:reasons.append('insufficient tonal contrast')
 return reasons
def main():
 p=argparse.ArgumentParser();p.add_argument('image');a=p.parse_args()
 reasons=validate(a.image)
 print(json.dumps({'passed':not reasons,'reasons':reasons},ensure_ascii=False))
 if reasons:raise SystemExit(1)
if __name__=='__main__':main()
