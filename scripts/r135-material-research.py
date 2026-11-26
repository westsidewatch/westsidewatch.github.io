"""Acquire originals into CI artifacts only. No automatic publication or selection."""
import hashlib,json,re,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlparse
root=Path("artifacts/r124/r135-originals");root.mkdir(parents=True,exist_ok=True)
items=json.loads(Path("static/experiments/seven-realm-r124/materials/r135-discovery.json").read_text())
prior=json.loads(Path("static/experiments/seven-realm-r124/materials/provenance.json").read_text())
seen={x["sha256"] for x in prior["verifiedAcquisition"]}
for version in ("r127","r128","r129"):
 for row in json.loads(Path("static/experiments/seven-realm-r124/materials/"+version+"/report.json").read_text()):
  if row.get("sha256"):seen.add(row["sha256"])
class Links(HTMLParser):
 def __init__(self): super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=="a":
   h=dict(attrs).get("href","")
   if h:self.links.append(h)
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"WestsideWatch material research/1.0"}),timeout=20) as r:
  if urlparse(r.url).hostname not in ("openclipart.org","www.openclipart.org"):raise ValueError("redirect outside source provider")
  data=r.read(4_000_001)
  if len(data)>4_000_000:raise ValueError("file size")
  return data,r.url
report=[]
for item in items:
 row=dict(item)
 try:
  page,_=get(item["source"]);html=page.decode("utf-8","replace")
  if re.search(r'>(pd_issue|need-review|needs-review)<',html,re.I):raise ValueError("rights review flag")
  p=Links();p.feed(html);urls=[urljoin(item["source"],x) for x in p.links if re.search(r'/download/'+item["id"]+r'(?:/|$|\?)',x)]
  urls += ["https://openclipart.org/download/"+item["id"]]
  errors=[]
  for u in dict.fromkeys(urls):
   try:
    raw,final=get(u)
    if re.search(br'<!DOCTYPE|<!ENTITY',raw,re.I):raise ValueError("DTD")
    xml=ET.fromstring(raw)
    if xml.tag.split("}")[-1]!="svg":raise ValueError("not SVG")
    count=0
    for el in xml.iter():
     tag=el.tag.split("}")[-1].lower()
     if tag in ("script","image","foreignobject","iframe","animate","set"):raise ValueError("unsafe or raster SVG: "+tag)
     if tag in ("path","line","polyline","polygon","rect","circle","ellipse"):count+=1
     for k,v in el.attrib.items():
      k=k.split("}")[-1].lower()
      if k.startswith("on") or (k=="href" and not v.startswith("#")) or re.search(r'url\(\s*["\']?(?:https?:|//|data:)',v,re.I):raise ValueError("external reference")
     if tag=="style" and re.search(r'@import|url\(\s*["\']?(?:https?:|//|data:)',el.text or "",re.I):raise ValueError("external style")
    if not count:raise ValueError("no native vector")
    digest=hashlib.sha256(raw).hexdigest()
    if digest in seen:raise ValueError("duplicate original")
    seen.add(digest);(root/(item["id"]+".svg")).write_bytes(raw)
    row.update(state="native_original_acquired_pending_visual_and_rights_review",sha256=digest,bytes=len(raw),vectorElements=count,viewport=xml.get("viewBox"),download=final)
    break
   except Exception as e:errors.append(str(e))
  else:raise ValueError("; ".join(errors))
 except Exception as e:row.update(state="acquisition_failed",error=str(e))
 report.append(row)
(root/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
