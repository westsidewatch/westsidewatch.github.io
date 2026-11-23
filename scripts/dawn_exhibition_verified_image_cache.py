#!/usr/bin/env python3
"""Cache exactly matched exhibition images from institution/public-domain records."""
from pathlib import Path
import io
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps
OUT=Path("static/dawn-library/reading-room/assets")
OUT.mkdir(parents=True,exist_ok=True)
SOURCES=[
 ("salzmann-jerusalem",["https://collectionapi.metmuseum.org/api/collection/v1/iiif/287019/603191/main-image"]),
 ("frith-sinai-palestine",["https://collectionapi.metmuseum.org/api/collection/v1/iiif/271102/600009/main-image"]),
 ("conder-city",["https://www.gutenberg.org/files/70537/70537-h/images/i_001.jpg","https://www.gutenberg.org/cache/epub/70537/images/i_001.jpg"]),
 ("besant-herod-saladin",["https://www.gutenberg.org/files/60319/60319-h/images/frontis.jpg","https://www.gutenberg.org/cache/epub/60319/images/frontis.jpg"]),
 ("manning-holy-fields",["https://www.gutenberg.org/files/51452/51452-h/images/i_093.jpg","https://www.gutenberg.org/cache/epub/51452/images/i_093.jpg"])
]
session=requests.Session();session.headers.update({"User-Agent":"Mozilla/5.0 (Dawn Library historical editorial illustration check)","Accept":"image/avif,image/webp,image/jpeg,image/png,image/*;q=0.8,*/*;q=0.2"})
def fetch_img(url):
    try:
        r=session.get(url,timeout=14,headers={"Referer":"https://www.gutenberg.org/"})
        ct=r.headers.get("Content-Type","")
        print("GET",r.status_code,ct,len(r.content),url,flush=True)
        if r.status_code!=200: return None
        with Image.open(io.BytesIO(r.content)) as im:
            if min(im.size)<180: return None
            im.verify()
        with Image.open(io.BytesIO(r.content)) as im:
            return ImageOps.exif_transpose(im).convert("RGB")
    except Exception as e:
        print("FETCH_FAILED",type(e).__name__,str(e)[:160],url,flush=True)
        return None
found=[]
for name,candidates in SOURCES:
    image=None;origin=None
    for url in candidates:
        image=fetch_img(url)
        if image is not None:
            origin=url;break
    if image is None:
        print("UNRESOLVED",name,flush=True)
        continue
    original_size=image.size
    image.thumbnail((960,820),Image.Resampling.LANCZOS)
    target=OUT/("historic-"+name+".jpg")
    image.save(target,format="JPEG",quality=80,optimize=True,progressive=True)
    print("CACHED",name,original_size,image.size,target.stat().st_size,str(target),"ORIGIN",origin,flush=True)
    found.append(name)
print("FINAL",len(found),"/",len(SOURCES),"IDs",",".join(found),flush=True)
