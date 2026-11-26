"""Obtain only explicitly listed SVGs; fail closed and retain hashes. No generators."""
from pathlib import Path
import json, urllib.request, urllib.parse, hashlib, re, xml.etree.ElementTree as ET
root=Path("static/experiments/material-atlas-r123")
items=json.loads((root/"candidates.json").read_text())["options"]
out=root/"assets";out.mkdir(exist_ok=True)
results=[]; seen=set()
def inspect(raw):
    if len(raw)>2500000: raise ValueError("oversized")
    if re.search(rb"<!DOCTYPE|<!ENTITY|<\?xml-stylesheet",raw,re.I): raise ValueError("active XML declaration")
    doc=ET.fromstring(raw)
    tag=lambda x:x.rsplit("}",1)[-1]
    if tag(doc.tag)!="svg": raise ValueError("not SVG")
    n=0
    for el in doc.iter():
        k=tag(el.tag)
        if k in {"script","foreignObject","image","feImage","iframe","audio","video","animate","animateTransform","set"}: raise ValueError("unsupported element "+k)
        if k in {"path","rect","circle","ellipse","line","polyline","polygon","use","pattern"}: n+=1
        for a,v in el.attrib.items():
            name=tag(a)
            if name.lower().startswith("on"): raise ValueError("event attribute")
            if name=="href" and k in {"use","a","linearGradient","radialGradient","pattern","textPath","mpath","filter"} and not v.startswith("#"): raise ValueError("external href")
            if re.search(r"url\(\s*['\"]?(?!#)[^)'\"]",v,re.I): raise ValueError("external CSS URL")
        if k=="style" and re.search(r"@import|url\(\s*['\"]?(?!#)[^)'\"]",el.text or "",re.I): raise ValueError("external style")
    if not n: raise ValueError("no vector geometry")
    if not (doc.get("viewBox") or (doc.get("width") and doc.get("height"))): raise ValueError("missing viewport")
    return n,doc.get("viewBox") or [doc.get("width"),doc.get("height")]
for a in items:
    result={"id":a["id"],"realm":a["realm"],"source":a["page"],"ok":False}
    try:
        local=out/(a["id"]+".svg")
        if local.exists():
            raw=local.read_bytes()
        else:
            req=urllib.request.Request(a["download"],headers={"User-Agent":"WestsideWatch material research / SVG asset verification","Accept":"image/svg+xml"})
            with urllib.request.urlopen(req,timeout=15) as r:
                if urllib.parse.urlsplit(r.geturl()).hostname not in {"openclipart.org","www.openclipart.org","freesvg.org","www.freesvg.org","cdn.freesvg.org"}: raise ValueError("unexpected download host")
                raw=r.read(2500001)
        n,view=inspect(raw); digest=hashlib.sha256(raw).hexdigest()
        if digest in seen: raise ValueError("duplicate digest")
        seen.add(digest)
        (out/(a["id"]+".svg")).write_bytes(raw)
        result.update(ok=True,bytes=len(raw),sha256=digest,vectorElements=n,viewport=view,license=a["license"],licenseUrl=a["licenseUrl"])
    except Exception as e:
        result["error"]=str(e)[:160]
        (out/(a["id"]+".svg")).unlink(missing_ok=True)
    results.append(result)
report={"results":results,"successful":sum(x["ok"] for x in results),"realms":sorted({x["realm"] for x in results if x["ok"]}),"state":"technical acquisition only; art and individual provenance acceptance pending"}
(out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(report,ensure_ascii=False,indent=2))
if not report["successful"]: raise SystemExit("No usable source files")
