"""Offline, reproducible extraction from a frozen OSM API subset; no network."""
import argparse, hashlib, json, math
from pathlib import Path
import xml.etree.ElementTree as ET
WALLS=[137726904,391433919,391433915,511655207,391433911,1080613976,391433907]
JAFFA=561157424
DAMASCUS=616186088
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args()
raw=Path(a.source).read_bytes();root=ET.fromstring(raw)
nodes={int(n.attrib['id']):n for n in root.findall('node')};ways={int(w.attrib['id']):w for w in root.findall('way')}
def tags(e):return {t.attrib['k']:t.attrib['v'] for t in e.findall('tag')}
def point(n):return {'lat':float(n.attrib['lat']),'lon':float(n.attrib['lon'])}
def refs(w):return [int(n.attrib['ref']) for n in w.findall('nd')]
def line(wid):
 w=ways[wid];assert tags(w).get('barrier')=='city_wall';ids=refs(w);return {'osmWay':wid,'version':int(w.attrib['version']),'timestamp':w.attrib['timestamp'],'nodeIds':ids,'points':[point(nodes[n]) for n in ids]}
lines=[line(i) for i in WALLS];gaps=[];envelope=[]
for i,line in enumerate(lines):
 previous=lines[i-1];start=line['nodeIds'][0];end=previous['nodeIds'][-1]
 if start!=end:
  aa,bb=previous['points'][-1],line['points'][0];distance=math.hypot((aa['lat']-bb['lat'])*111319.49,(aa['lon']-bb['lon'])*111319.49*math.cos(math.radians(31.778)))
  gaps.append({'fromNode':end,'toNode':start,'distanceMetres':round(distance,3),'wallGapNotFilled':True})
 envelope.extend(line['points'] if start!=end else line['points'][1:])
if envelope[-1]==envelope[0]:envelope.pop()
jaffa=nodes[JAFFA];assert tags(jaffa).get('historic')=='city_gate' and tags(jaffa).get('name:en')=='Jaffa Gate'
damascus=ways[DAMASCUS];assert tags(damascus).get('historic')=='city_gate' and tags(damascus).get('name:en')=='Damascus Gate'
dpoints=[point(nodes[n]) for n in refs(damascus)[:-1]]
result={'schema':'j3k.modern-wall-reference.v1','origin':{'lat':31.778,'lon':35.235},'source':{'url':'https://api.openstreetmap.org/api/0.6/map?bbox=35.222,31.770,35.242,31.785','snapshotDate':'2026-10-26','rawSubset':'sources/old-city-wall.osm.xml','rawSubsetSha256':hashlib.sha256(raw).hexdigest(),'license':'ODbL','attribution':'© OpenStreetMap contributors','historicalContext':['https://jerusalemfoundation.org/old-project/old-city-walls/','https://hadashot.iaa.org.il/Report_Detail_Eng.aspx?id=25008&mag_id=124']},'lines':lines,'gaps':gaps,'occupationEnvelope':envelope,'envelopeRule':'planning-constraint-only; closes mapped openings, never rendered as additional wall','gates':[{'objectId':'j3k:object:jaffa-gate-ottoman','label':'雅法門','osmType':'node','osmId':JAFFA,'version':int(jaffa.attrib['version']),'point':point(jaffa),'positionAuthority':'modern-map-node-not-surveyed-gate-footprint'},{'objectId':'j3k:object:damascus-gate-ottoman','label':'大馬士革門','osmType':'way','osmId':DAMASCUS,'version':int(damascus.attrib['version']),'point':{'lat':sum(p['lat'] for p in dpoints)/len(dpoints),'lon':sum(p['lon'] for p in dpoints)/len(dpoints)},'positionAuthority':'modern-map-footprint-vertex-average-not-surveyed-entrance'}],'display':{'heightMetres':10,'widthMetres':2.5,'dimensionsAuthority':'illustrative-display-not-measured-wall-height-or-thickness'},'geometryVerified':False,'limitations':['Modern OSM linework is not a survey of the wall as built in 1535–1542.','Only selected outer-wall lines are drawn; Temple Mount internal retaining lines are excluded.','Mapped gaps remain open; the closed occupation envelope is only a modelling constraint.','Gate markers locate modern map references; they do not reconstruct historical gate architecture.','This reference is not applied before the Ottoman phase; exact late-Ottoman alterations remain unresolved.','Modern DEM is not ancient ground.']}
Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'ways':len(lines),'points':sum(len(l['points']) for l in lines),'gaps':gaps,'rawSha256':result['source']['rawSubsetSha256']}))
