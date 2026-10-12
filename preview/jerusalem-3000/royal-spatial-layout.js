// Topology is shared by geometry, gateways and verification. Coordinates remain
// illustrative spring-relative ENU metres, not an archaeological road survey.
export function compileRoyalSpatialLayout(data){
 const raw=data.royalCity.spatial;if(raw.schema!=='j3k.royal-spatial-layout.v1')throw new Error('Unsupported royal spatial schema');if(raw.frame!=='spring-relative-east-x-south-z-metres')throw new Error('Unsupported royal spatial frame');
 if(!Number.isFinite(raw.roadWidth)||raw.roadWidth<=0)throw new Error('Invalid royal road width');
 const validStage=s=>['david','solomon'].includes(s);
 const gates=new Map(),nodes=new Map(),edges=[];
 const point=p=>Array.isArray(p)&&p.length===2&&p.every(Number.isFinite);
 for(const g of raw.gates){
  const line=g.wall==='david-wall'?data.royalCity.davidWall:g.wall==='north-wall'?data.royalCity.northernWall:null;
  const a=line?.[g.segment-1],b=line?.[g.segment];
  if(!Number.isInteger(g.segment)||!validStage(g.stage)||gates.has(g.id)||!point(a)||!point(b)||!(g.t>0&&g.t<1)||!(g.width>0))throw new Error('Invalid royal gate');
  const length=Math.hypot(b[0]-a[0],b[1]-a[1]);if(length<=g.width||g.t*length<g.width/2||(1-g.t)*length<g.width/2)throw new Error('Gate exceeds wall segment');
  gates.set(g.id,{...g,offset:[a[0]+(b[0]-a[0])*g.t,a[1]+(b[1]-a[1])*g.t],unit:[(b[0]-a[0])/length,(b[1]-a[1])/length],angle:-Math.atan2(b[1]-a[1],b[0]-a[0])});
 }
 for(const g of gates.values())for(const other of gates.values())if(g.id!==other.id&&g.wall===other.wall&&g.segment===other.segment&&Math.hypot(g.offset[0]-other.offset[0],g.offset[1]-other.offset[1])<(g.width+other.width)/2)throw new Error('Overlapping royal gates');
 for(const n of raw.nodes){const court=data.royalCity.courtyards.find(c=>c.id===n.courtId),temple=data.royalCity.temple;const offset=n.gateId?gates.get(n.gateId)?.offset:n.courtId?(court?[court.offset[0],court.offset[1]+(n.courtPoint==='entry'?16:5)]:null):n.templePoint?[temple.offset[0]+temple.lengthCubits*temple.cubitMetres/2+10*temple.cubitMetres+.2,temple.offset[1]]:n.offset;if((n.gateId&&gates.get(n.gateId)?.stage!==n.stage)||(n.courtId&&(court?.stage!==n.stage||!['entry','inner'].includes(n.courtPoint)))||(n.templePoint&&(n.templePoint!=='entry'||n.stage!=='solomon')))throw new Error('Spatial node stage or entrance mismatch');if(!validStage(n.stage)||nodes.has(n.id)||!point(offset))throw new Error('Invalid royal spatial node');nodes.set(n.id,{...n,offset});}
 const regions=raw.regions.map(region=>{if(!validStage(region.stage))throw new Error('Invalid royal region stage');const polygon=region.boundary==='david-wall'?data.royalCity.davidWall:region.boundary==='north-wall'?data.royalCity.northernWall:null;if(!polygon||polygon.some(p=>!point(p)))throw new Error('Invalid royal region boundary');return {...region,polygon};});
 const seen=new Set();
 for(const e of raw.edges){
  if(seen.has(e.id)||!nodes.has(e.from)||!nodes.has(e.to)||!['david','solomon'].includes(e.stage))throw new Error('Invalid royal spatial edge');seen.add(e.id);if(e.stage==='david'&&[e.from,e.to].some(id=>nodes.get(id).stage==='solomon'))throw new Error('Road precedes its destination');
  const points=[nodes.get(e.from).offset,...(e.via||[]),nodes.get(e.to).offset];if(points.some(p=>!point(p)))throw new Error('Invalid royal road coordinates');
  for(let i=1;i<points.length;i++)if(Math.hypot(points[i][0]-points[i-1][0],points[i][1]-points[i-1][1])===0)throw new Error('Zero length royal road');
  edges.push({...e,points});
 }
 const reach=stage=>{const found=new Set(['spring']);let changed=true;while(changed){changed=false;for(const e of edges.filter(e=>stage==='solomon'||e.stage==='david')){if(found.has(e.from)&&!found.has(e.to)){found.add(e.to);changed=true;}if(found.has(e.to)&&!found.has(e.from)){found.add(e.from);changed=true;}}}return found;};
 for(const stage of ['david','solomon'])for(const id of raw.requiredDestinations[stage])if(!reach(stage).has(id))throw new Error(`Disconnected royal destination ${id}`);
 return {roadWidth:raw.roadWidth,regions,gates:[...gates.values()],nodes:[...nodes.values()],edges,reachable:stage=>[...reach(stage)],authority:raw.authority};
}
