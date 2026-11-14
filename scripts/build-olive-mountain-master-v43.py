#!/usr/bin/env python3
"""Reproducible historical intaglio native-SVG artmaster for P2 Olive 04.
Crops and vectorizes one verified 1881-84 STEEL ENGRAVING. This does NOT draw
algorithmic olive foliage or pretend to have manually redrawn the original.
Output is a clean-path, no-raster, no-font, no-JavaScript SVG.
"""
from __future__ import annotations
import hashlib
from io import BytesIO
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.request
import xml.etree.ElementTree as ET

from PIL import Image, ImageOps, ImageEnhance, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"static/images/p2-realms/v15"
URL=("https://upload.wikimedia.org/wikipedia/commons/0/06/"
     "Jerusalem_from_the_Mount_of_Olives_%28NYPL_b10607452-80257%29.jpg")
SOURCE_SHA1="8097a8aa1e5c1ee4ef0bcd126578b73d89229f04"
LICENSE=("Woodward, John Douglas (1846–1924), original art; Cousen, Charles "
" (1819–1889), steel engraver; 1881–1884, Picturesque Palestine, "
"Sinai and Egypt. NYPL Image ID 80257; Wikimedia Commons: "
"Jerusalem from the Mount of Olives (NYPL b10607452-80257).jpg. "
"Original public-domain artwork; mechanically scanned public-domain reproduction.")
PLATES={
 "desktop":dict(crop=(102,378,3820,2470),width=1500,thresholds=(116,165),fade=(.37,.66)),
 "mobile":dict(crop=(610,444,3290,2520),width=920,thresholds=(113,161),fade=(.42,.70)),
}

def get_source() -> Image.Image:
    """Hash check avoids substituting a different version without art review."""
    local=Path("/tmp/olive-woodward-master-verified.jpg")
    if local.exists(): data=local.read_bytes()
    else:
        req=urllib.request.Request(URL,headers={"User-Agent":"WestsideWatch-Artmaster/1.0 (public domain source research)"})
        with urllib.request.urlopen(req,timeout=90) as response: data=response.read()
        local.write_bytes(data)
    digest=hashlib.sha1(data).hexdigest()
    if digest != SOURCE_SHA1: raise ValueError(f"Source file SHA1 mismatch: {digest}; expected {SOURCE_SHA1}")
    img=Image.open(BytesIO(data)).convert("L")
    if img.size!=(3928,2703): raise ValueError(f"Unexpected source dimensions: {img.size}")
    return img

def run_potrace(image: Image.Image, threshold:int, tmp:Path, index:int) -> str:
    # PBM is 1 bit; no raster data are left in the final SVG.
    pbm=tmp/f"ink-{index}.pbm"
    output=tmp/f"ink-{index}.svg"
    image.point(lambda val:0 if val<threshold else 255,mode="1").save(pbm)
    subprocess.run(["potrace","--svg","--tight","-t","2","-a","0.85",
        "-O","0.8","-o",str(output),str(pbm)],check=True,capture_output=True,text=True)
    svg=output.read_text()
    m=re.search(r"(<g\b[\s\S]*</g>)\s*</svg>",svg)
    if not m: raise ValueError(f"Cannot recover original trace group: {index}")
    return m.group(1).replace('fill="#000000"','fill="#ffffff"').replace('fill="black"','fill="#ffffff"')

def master(img:Image.Image,kind:str,config:dict):
    c=img.crop(config["crop"])
    target_w=config["width"]
    h=round(c.height*target_w/c.width)
    c=ImageOps.autocontrast(c,cutoff=(1,1)).resize((target_w,h),Image.Resampling.LANCZOS)
    c=ImageEnhance.Contrast(c).enhance(1.08)
    c=c.filter(ImageFilter.UnsharpMask(radius=.75,percent=110,threshold=2))
    with tempfile.TemporaryDirectory(prefix="olive-plate-") as d:
        tmp=Path(d)
        fine=run_potrace(c,config["thresholds"][1],tmp,1)
        deep=run_potrace(c,config["thresholds"][0],tmp,2)
    # Use two real engraving-threshold traces; this is NOT two copies of a
    # generated tree. Gentle layer contrast remains OS-driven via a CSS mask.
    title="The Mount of Olives — Woodward/Cousen historical steel-engraving artmaster"
    desc=("Full native-path vector tracing from the verified public-domain "
          "1881-84 Jerusalem from the Mount of Olives steel engraving. "
          "Ancient olive trees, Kidron valley slopes, stone walls and Jerusalem skyline "
          "are all from the actual engraved image, not procedural substitute silhouettes. "
          f"Independent editorial crop for {kind}.")
    # Potrace groups have fixed 0.1 transforms and no raster payload.
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{target_w}" '
         f'height="{h}" viewBox="0 0 {target_w} {h}" role="img" aria-labelledby="title desc">\n'
         f'<title id="title">{title}</title>\n<desc id="desc">{desc}</desc>\n'
         f'<metadata>{LICENSE} Sha1: {SOURCE_SHA1}. Digitally traced to SVG via '
         f'Pillow monochrome thresholds and Potrace. Source URL: {URL}</metadata>\n'
         '<g id="historical-steel-engraving" fill="#ffffff" fill-rule="evenodd" stroke="none">\n'
         f'<g id="burin-fine" opacity="{config["fade"][0]}">{fine}</g>\n'
         f'<g id="burin-deep" opacity="{config["fade"][1]}">{deep}</g>\n'
         '</g>\n</svg>\n')
    if '<image' in svg or 'data:image' in svg or '<script' in svg: raise ValueError("Not native SVG")
    ET.fromstring(svg)
    name=f"04-olive-woodward-cousen-{kind}-intaglio-v43.svg"
    target=OUT/name
    target.write_text(svg)
    print(f"{name}: {target_w}×{h}, {len(svg):,} bytes, verified true engraved vector geometry")
    return target

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    img=get_source()
    for kind,config in PLATES.items(): master(img,kind,config)

if __name__=="__main__":main()
