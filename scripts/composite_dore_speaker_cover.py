#!/usr/bin/env python3
"""Composite locally generated background and deterministic speaker text.
Requires Pillow, installed on Mac with: python3 -m pip install Pillow
Never invents portraits. Background is external locally generated PNG.
"""
import argparse,json
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--job',required=True)
 p.add_argument('--font',help='Optional local Chinese font file path')
 a=p.parse_args()
 try:
  from PIL import Image,ImageDraw,ImageFont
 except ImportError:raise SystemExit('Pillow required: python3 -m pip install Pillow')
 job=Path(a.job);spec=json.loads((job/'design-spec.json').read_text())
 if spec.get('portraitAllowed') or spec['section']!='olive':raise SystemExit('Invalid cover policy')
 source=job/'generated-background.png'
 if not source.exists():raise SystemExit(f'Missing local image: {source}. Render the prompt first.')
 im=Image.open(source).convert('RGB').resize((720,960),Image.Resampling.LANCZOS)
 # Force generated image into the illustration field; text region is deterministic white.
 im.paste('#FFFFFF',(0,700,720,960))
 draw=ImageDraw.Draw(im)
 ink='#174B35'
 draw.line((48,735,672,735),fill=ink,width=2)
 draw.line((48,885,672,885),fill=ink,width=2)
 if a.font:
  font=ImageFont.truetype(a.font,74)
 else:
  candidates=['/System/Library/Fonts/Supplemental/Songti.ttc',
              '/System/Library/Fonts/PingFang.ttc']
  match=next((x for x in candidates if Path(x).exists()),None)
  if not match:raise SystemExit('Chinese font not found; supply --font')
  font=ImageFont.truetype(match,74)
 small=ImageFont.truetype(a.font,22) if a.font else ImageFont.truetype(match,22)
 draw.text((48,752),spec['displayName'],font=font,fill=ink)
 draw.text((48,830),spec['subtitle'],font=small,fill=ink)
 draw.text((48,900),'OLIVE MOUNTAIN / SERMONS',fill=ink)
 dest=job/'final-cover.png';im.save(dest,optimize=True)
 print('COMPOSITE:',dest)
if __name__=='__main__':main()
