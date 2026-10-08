#!/usr/bin/env python3
"""Build a real, local image+HTML/CSS preview and objective raster measurements.

Uses Python stdlib only; JPEG/PNG/SVG are shown by browser, while image dimension
inspection supports PNG and JPEG. No face recognition or subjective visual grading.
"""
import argparse,html,json,struct
from pathlib import Path
from urllib.parse import quote

BREAKPOINTS=(320,375,768,1440)
def dimensions(path):
 data=Path(path).read_bytes()
 if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data)>=24:
  return struct.unpack('>II',data[16:24])
 if data[:2]==b'\xff\xd8':
  i=2
  while i<len(data)-9:
   if data[i]!=255:i+=1;continue
   marker=data[i+1];i+=2
   if marker in (0xD8,0xD9) or 0xD0<=marker<=0xD7:continue
   if i+2>len(data):break
   size=int.from_bytes(data[i:i+2],'big')
   if size<2:break
   if marker in (0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF):
    return (int.from_bytes(data[i+3:i+5],'big'),int.from_bytes(data[i+5:i+7],'big'))
   i+=size
 return None
def build(spec,image_name,title,subtitle):
 from dore_editorial_scenarios import SLOTS
 from dore_editorial_palettes import PALETTES
 slot=spec.get('slot','cover');ratio=SLOTS[slot]['ratio']
 palette=PALETTES[spec['palette']]
 recipe=spec['composition']
 tb=recipe['type_box'];sb=recipe['subject_box']
 def css_box(a):
  return f'left:{a[0]}%;top:{a[1]}%;width:{a[2]-a[0]}%;height:{a[3]-a[1]}%;'
 paper=palette['paper'];ink=palette['type_ink']
 safe_title=html.escape(title);safe_sub=html.escape(subtitle)
 image_src=quote(image_name)
 sections=[]
 for width in BREAKPOINTS:
  sections.append(f'''<section class="proof"><h2>{width}px viewport</h2>
 <div class="frame" style="width:{width}px">
 <div class="art" role="img" aria-label="Editorial art proof">
 <img src="{image_src}" alt="">
 <div class="type" style="{css_box(tb)}"><span class="eyebrow">{safe_sub}</span><strong>{safe_title}</strong></div>
 </div></div></section>''')
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
 <meta name="viewport" content="width=device-width,initial-scale=1">
 <title>Doré visual proof</title>
 <style>
 *{{box-sizing:border-box}}body{{margin:0;padding:24px;background:#e8e8e8;color:#252525;font-family:system-ui,sans-serif}}
 .proof{{margin:0 0 36px}}.proof h2{{font:14px system-ui;margin:0 0 12px}}
 .frame{{max-width:100%;outline:1px solid #aaa;background:{paper}}}
 .art{{position:relative;aspect-ratio:{ratio.replace(':',' / ')};overflow:hidden;background:{paper}}}
 .art>img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
 .type{{position:absolute;display:flex;flex-direction:column;justify-content:center;z-index:2;color:{ink};overflow-wrap:anywhere;pointer-events:none}}
 .type strong{{font-family:"Bodoni Moda",Georgia,serif;font-size:clamp(20px,5.5vw,88px);font-weight:400;line-height:.9}}
 .eyebrow{{font-size:clamp(10px,1.3vw,17px);letter-spacing:.09em;margin-bottom:.75em}}
 .frame::after{{content:"";display:block}}
 @media(max-width:600px){{.type strong{{font-size:clamp(18px,7vw,36px)}}}}
 </style></head><body><h1>Doré image + live type visual proof</h1>
 <p>Preview only. Text remains HTML; responsive crop, likeness, color and legibility require human review.</p>
 {''.join(sections)}</body></html>'''
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--spec',required=True)
 p.add_argument('--image',required=True)
 p.add_argument('--title',default='EDITORIAL')
 p.add_argument('--subtitle',default='WESTSIDE WATCH')
 p.add_argument('--out',default='local/dore-editorial-preview')
 a=p.parse_args()
 spec=json.loads(Path(a.spec).read_text(encoding='utf-8'))
 img=Path(a.image).resolve()
 if not img.is_file():p.error('image not found')
 if img.suffix.lower() not in ('.png','.jpg','.jpeg','.webp','.svg'):p.error('unsupported image format')
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 import shutil
 target=out/('asset'+img.suffix.lower())
 shutil.copyfile(img,target)
 size=dimensions(target)
 report={'image':target.name,'dimensions':list(size) if size else None,
         'breakpoints':list(BREAKPOINTS),'has_image':True,
         'image_format':img.suffix.lower(),'image_metrics_verified':size is not None,
         'visual_qa_status':'pending_human_review','publication_approved':False}
 (out/'preview.html').write_text(build(spec,target.name,a.title,a.subtitle),encoding='utf-8')
 (out/'preview-manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(out/'preview.html')
if __name__=='__main__':main()
