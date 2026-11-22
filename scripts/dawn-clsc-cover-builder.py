#!/usr/bin/env python3
"""Render source-identical Chinese book title/cover pages from Yale CLSC PDFs.

No invented jackets: every image has an exact Yale PDF filename + source-page
provenance. This is an edition documentary scan preview, not an original trade
jacket. Rebuilds only matched Work IDs. Python 3 + requests + pymupdf + Pillow.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import time

import fitz
from PIL import Image, ImageStat
import requests

BASE = Path(__file__).resolve().parents[1]
COLLECTION = BASE / "static/dawn-library/chinese-collection.json"
OUT_DIR = BASE / "static/dawn-library/chinese-facsimile-covers"
YALE_INDEX = "https://adhoc.yalepages.org/Collections/HKBU/CLSC/clsc_list.js"
YALE_PDF = "https://divinity-adhoc.library.yale.edu/HKBU/CLSC/"
CATALOGUE = "https://adhoc.yalepages.org/Collections/HKBU/CLSC/index.html"
SOURCE_PATTERN = re.compile(
    r'\{\s*title:\s*"(?P<title>(?:\\.|[^"])*)"\s*,'
    r'\s*author:\s*"(?P<author>(?:\\.|[^"])*)"\s*,'
    r'\s*year:\s*"(?P<year>(?:\\.|[^"])*)"\s*,'
    r'\s*filename:\s*"(?P<filename>[0-9A-Za-z_-]+\.pdf)"\s*\}'
)

def sha256(buf):
    return hashlib.sha256(buf).hexdigest()

def get_limited(url, max_bytes=150 * 1024 * 1024, timeout=90):
    with requests.get(url, stream=True, timeout=timeout,
                      headers={"User-Agent": "WestsideWatch-Dawn-Library/1.0 (source identification)"}) as r:
        r.raise_for_status()
        content_length = int(r.headers.get("content-length", 0))
        if content_length > max_bytes:
            raise ValueError(f"PDF exceeds source acquisition cap: {content_length} B")
        buffer = io.BytesIO()
        for chunk in r.iter_content(131072):
            if not chunk:
                continue
            buffer.write(chunk)
            if buffer.tell() > max_bytes:
                raise ValueError(f"Download exceeds cap: {buffer.tell()} B")
        return buffer.getvalue()

def cover_image_from_pdf(pdf_bytes):
    doc=fitz.open(stream=pdf_bytes, filetype="pdf")
    if doc.page_count < 1:
        raise ValueError("PDF has zero pages")
    # A scanned title page is not necessarily the very first page.
    candidates=[]
    for i in range(min(doc.page_count,4)):
        page=doc.load_page(i)
        if page.rect.width<=0 or page.rect.height<=0:
            continue
        max_side=max(page.rect.width,page.rect.height)
        scale=min(1.6,740/max_side)
        pix=page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False,colorspace=fitz.csRGB)
        img=Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
        grayscale=img.convert("L")
        grayscale.thumbnail((130,170))
        hist=grayscale.histogram()
        pixel_count=sum(hist)
        coverage=sum(hist[:210])/pixel_count if pixel_count else 0
        contrast=ImageStat.Stat(grayscale).stddev[0]
        # Choose earliest reasonably nonblank source page; not a fabricated cover.
        candidates.append((i,img,coverage,contrast))
        if coverage>=.005 and contrast>=9:
            break
    if not candidates: raise ValueError("No renderable source pages")
    chosen=next((c for c in candidates if c[2]>=.005 and c[3]>=9),
                max(candidates,key=lambda c:c[2]))
    i,img,cov,contrast=chosen
    stream=io.BytesIO()
    img.save(stream,"WEBP",quality=82,method=5)
    result=stream.getvalue()
    if len(result)<1400:
        raise ValueError("Cover render unexpectedly small")
    return result, {"sourcePage":i+1,"inkRatio":round(cov,4),
                    "contrast":round(contrast,2),"width":img.width,"height":img.height,
                    "pageCount":doc.page_count}
def slug_id(value):
    return re.sub(r'[^A-Za-z0-9-]','-',value).strip("-")[:120]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--limit",type=int,default=0)
    parser.add_argument("--write-collection",action="store_true")
    parser.add_argument("--strict",action="store_true")
    args=parser.parse_args()
    collection=json.loads(COLLECTION.read_text(encoding="utf-8"))
    works=[x for x in collection["works"] if x.get("source",{}).get("provider")=="Christian Literature Society for China Collection"]
    raw=get_limited(YALE_INDEX,max_bytes=3*1024*1024).decode("utf-8-sig")
    records=[]
    for m in SOURCE_PATTERN.finditer(raw):
        d=m.groupdict()
        records.append(d)
    by_title={}
    for d in records: by_title.setdefault(d["title"].strip(),[]).append(d)
    audit={"schema":"dawn.clsc.facsimile-provenance.v1",
        "source":YALE_INDEX,"catalogue":CATALOGUE,
        "entriesInYaleIndex":len(records),"expected":len(works),
        "rendered":[],"failed":[],"unmatched":[],"ambiguous":[],"notProcessed":[]}
    OUT_DIR.mkdir(parents=True,exist_ok=True)
    by_id={}
    for k,work in enumerate(works):
        title=work["work"]["title"]
        identity=work["workId"]
        if args.limit and k>=args.limit:
            audit["notProcessed"].append(identity)
            continue
        matches=by_title.get(title,[])
        if len(matches)!=1:
            audit["unmatched" if not matches else "ambiguous"].append({"workId":identity,"title":title,
              "candidateCount":len(matches)})
            continue
        record=matches[0]
        year=int(work.get("edition",{}).get("year") or 0)
        if record["year"].isdigit() and len(record["year"])==4 and abs(int(record["year"])-year)>1:
            audit["ambiguous"].append({"workId":identity,"title":title,"reason":"source year mismatch",
                                      "sourceYear":record["year"],"catalogueYear":year})
            continue
        filename=record["filename"]
        url=YALE_PDF+filename
        destination=OUT_DIR/(slug_id(identity)+".webp")
        try:
            pdf=get_limited(url)
            if not pdf.startswith(b"%PDF"):
                raise ValueError("File is not a PDF")
            page_data,stats=cover_image_from_pdf(pdf)
            destination.write_bytes(page_data)
            entry={"workId":identity,"title":title,"sourceTitle":record["title"],
                   "sourceYear":record["year"],"sourceAuthor":record["author"],
                   "pdf":url,"pdfSha256":sha256(pdf),"pdfBytes":len(pdf),
                   "localCover":"/dawn-library/chinese-facsimile-covers/"+destination.name,
                   "imageSha256":sha256(page_data),"imageBytes":len(page_data),
                   **stats}
            audit["rendered"].append(entry)
            by_id[identity]=entry
            print("COVER_OK",identity,title,filename,stats["sourcePage"],len(page_data),flush=True)
        except Exception as ex:
            entry={"workId":identity,"title":title,"pdf":url,"error":str(ex)}
            audit["failed"].append(entry)
            print("COVER_FAILED",identity,title,str(ex),flush=True)
    out_report=BASE/"artifacts/dawn-clsc/facsimile-provenance.json"
    out_report.parent.mkdir(parents=True,exist_ok=True)
    out_report.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if args.write_collection:
        for work in collection["works"]:
            info=by_id.get(work["workId"])
            if not info:continue
            work["cover"]={
              "mode":"source-facsimile-title-page",
              "url":info["localCover"],
              "title":work["work"]["title"],
              "creator":work["work"]["creator"],
              "pointer":"dawn://cover/"+work["workId"],
              "provenance":{"provider":"Yale Divinity Library / CLSC collection",
                "sourcePdf":info["pdf"],
                "sourcePage":info["sourcePage"],
                "sourceTitle":info["sourceTitle"],
                "year":info["sourceYear"],
                "imageSha256":info["imageSha256"],
                "imageKind":"scanned original title or opening page, not modern jacket"}}
        COLLECTION.write_text(json.dumps(collection,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:(len(v) if isinstance(v,list) else v) for k,v in audit.items()
                     if k in ["entriesInYaleIndex","expected","rendered","failed","unmatched","ambiguous","notProcessed"]},
                     ensure_ascii=False),flush=True)
    if args.strict and (audit["failed"] or audit["unmatched"] or audit["ambiguous"]):sys.exit(1)

if __name__=="__main__":
    main()
