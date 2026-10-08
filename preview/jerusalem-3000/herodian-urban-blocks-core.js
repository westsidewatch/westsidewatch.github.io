const EPS=1e-6;
function centroid(poly){return{x:poly.reduce((s,p)=>s+p.x,0)/poly.length,z:poly.reduce((s,p)=>s+p.z,0)/poly.length}}
function inside(p,poly){let c=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if(((a.z>p.z)!==(b.z>p.z))&&(p.x<(b.x-a.x)*(p.z-a.z)/(b.z-a.z+EPS)+a.x))c=!c}return c}
function area(poly){let a=0;for(let i=0;i<poly.length;i++){const p=poly[i],q=poly[(i+1)%poly.length];a+=p.x*q.z-q.x*p.z}return a/2}
function key(p,tol=1.5){return`${Math.round(p.x/tol)}:${Math.round(p.z/tol)}`}
function dist(a,b){return Math.hypot(b.x-a.x,b.z-a.z)}
function lerp(a,b,t){return{x:a.x+(b.x-a.x)*t,z:a.z+(b.z-a.z)*t}}
function shrink(poly,f){const c=centroid(poly);return poly.map(p=>({x:c.x+(p.x-c.x)*f,z:c.z+(p.z-c.z)*f}))}
function segmentIntersection(a,b,c,d){const r={x:b.x-a.x,z:b.z-a.z},s={x:d.x-c.x,z:d.z-c.z},den=r.x*s.z-r.z*s.x;if(Math.abs(den)<EPS)return null;const q={x:c.x-a.x,z:c.z-a.z},t=(q.x*s.z-q.z*s.x)/den,u=(q.x*r.z-q.z*r.x)/den;if(t>EPS&&t<1-EPS&&u>EPS&&u<1-EPS)return{x:a.x+t*r.x,z:a.z+t*r.z,t,u};return null}
function roadSegments(roads){const out=[];for(const road of roads){const pts=road.geometry?.points||[];for(let i=0;i<pts.length-1;i++)if(dist(pts[i],pts[i+1])>EPS)out.push({a:pts[i],b:pts[i+1],roadId:road.id})}return out}
function envelopeSegments(boundary){return boundary.map((a,i)=>({a,b:boundary[(i+1)%boundary.length],roadId:'__envelope__',boundary:true}))}
function splitAtIntersections(segments){const cuts=segments.map(()=>[0,1]);
 // A road ending on another segment is a topological junction even without a proper crossing.
 for(let i=0;i<segments.length;i++)for(let j=0;j<segments.length;j++){
  if(i===j)continue;
  const s=segments[i],t=segments[j],dx=t.b.x-t.a.x,dz=t.b.z-t.a.z,len2=dx*dx+dz*dz;
  if(len2<EPS)continue;
  for(const p of [s.a,s.b]){
   const u=((p.x-t.a.x)*dx+(p.z-t.a.z)*dz)/len2;
   if(u>EPS&&u<1-EPS&&Math.hypot(p.x-(t.a.x+u*dx),p.z-(t.a.z+u*dz))<.05)cuts[j].push(u);
  }
 }
for(let i=0;i<segments.length;i++)for(let j=i+1;j<segments.length;j++){const hit=segmentIntersection(segments[i].a,segments[i].b,segments[j].a,segments[j].b);if(hit){cuts[i].push(hit.t);cuts[j].push(hit.u)}}const out=[];for(let i=0;i<segments.length;i++){const ts=[...new Set(cuts[i].map(v=>Math.round(v*1e6)/1e6))].sort((a,b)=>a-b);for(let j=0;j<ts.length-1;j++){const a=lerp(segments[i].a,segments[i].b,ts[j]),b=lerp(segments[i].a,segments[i].b,ts[j+1]);if(dist(a,b)>1)out.push({...segments[i],a,b})}}return out}
function graphFromSegments(segments){const nodes=new Map(),edges=[];function node(p){const k=key(p);if(!nodes.has(k))nodes.set(k,{id:k,x:p.x,z:p.z,out:[]});return nodes.get(k)}for(const s of segments){const a=node(s.a),b=node(s.b),e={a,b,roadId:s.roadId,boundary:!!s.boundary};edges.push(e);a.out.push({to:b,edge:e});b.out.push({to:a,edge:e})}return{nodes,edges}}
function angle(from,to){return Math.atan2(to.z-from.z,to.x-from.x)}
function traceFaces(graph){const used=new Set(),faces=[];for(const node of graph.nodes.values())for(const first of node.out){const start=`${node.id}>${first.to.id}`;if(used.has(start))continue;let prev=node,cur=first.to,face=[{x:node.x,z:node.z}],guard=0;used.add(start);while(guard++<2048){face.push({x:cur.x,z:cur.z});if(cur.id===node.id)break;const incoming=angle(cur,prev),choices=cur.out.filter(o=>o.to.id!==prev.id||cur.out.length===1).map(o=>{let turn=angle(cur,o.to)-incoming;while(turn<=0)turn+=Math.PI*2;return{o,turn}}).sort((a,b)=>a.turn-b.turn);if(!choices.length){face=[];break}const next=choices[0].o,directed=`${cur.id}>${next.to.id}`;if(used.has(directed)&&next.to.id!==node.id){face=[];break}used.add(directed);prev=cur;cur=next.to}if(face.length>=4&&face[face.length-1].x===face[0].x&&face[face.length-1].z===face[0].z){face.pop();const a=area(face);if(Math.abs(a)>25)faces.push({polygon:face,signedArea:a})}}return faces}
function normalizeFace(poly){return area(poly)<0?[...poly].reverse():poly}
function polygonize(boundary,roads){const split=splitAtIntersections([...roadSegments(roads),...envelopeSegments(boundary)]),graph=graphFromSegments(split),raw=traceFaces(graph),faces=[];for(const f of raw){const poly=normalizeFace(f.polygon),c=centroid(poly),a=Math.abs(area(poly));if(!inside(c,boundary)||a<180||a>180000)continue;faces.push({polygon:poly,area:a})}faces.sort((a,b)=>b.area-a.area);if(faces.length>1&&faces[0].area>faces.slice(1).reduce((s,f)=>s+f.area,0)*.65)faces.shift();return{faces,graphNodes:graph.nodes.size,graphEdges:graph.edges.length}}
function rectAt(center,tx,tz,w,d){const nx=-tz,nz=tx,hw=w/2,hd=d/2;return[[-hw,-hd],[hw,-hd],[hw,hd],[-hw,hd]].map(([u,v])=>({x:center.x+tx*u+nx*v,z:center.z+tz*u+nz*v}))}
function onSegment(p,a,b){return Math.abs(orient(a,b,p))<EPS&&p.x>=Math.min(a.x,b.x)-EPS&&p.x<=Math.max(a.x,b.x)+EPS&&p.z>=Math.min(a.z,b.z)-EPS&&p.z<=Math.max(a.z,b.z)+EPS}
function inOrOn(p,poly){return inside(p,poly)||poly.some((a,i)=>onSegment(p,a,poly[(i+1)%poly.length]))}
function polyInside(poly,boundary){
 if(!poly.every(p=>inOrOn(p,boundary)))return false;
 for(let i=0;i<poly.length;i++)for(let j=0;j<boundary.length;j++)if(strictCross(poly[i],poly[(i+1)%poly.length],boundary[j],boundary[(j+1)%boundary.length]))return false;
 // A concave block may contain all four parcel corners while the connecting
 // parcel edges still cross a re-entrant notch.
 for(let i=0;i<poly.length;i++){
  const a=poly[i],b=poly[(i+1)%poly.length];
  if(!inOrOn(lerp(a,b,.25),boundary)||!inOrOn(lerp(a,b,.5),boundary)||!inOrOn(lerp(a,b,.75),boundary))return false;
 }
 return true;
}
function orient(a,b,c){return(b.x-a.x)*(c.z-a.z)-(b.z-a.z)*(c.x-a.x)}
function strictCross(a,b,c,d){const ab1=orient(a,b,c),ab2=orient(a,b,d),cd1=orient(c,d,a),cd2=orient(c,d,b);return ab1*ab2 < -EPS && cd1*cd2 < -EPS}
function polygonEdges(poly){return poly.map((a,i)=>[a,poly[(i+1)%poly.length]])}
function boundaryIntersections(a,b){return polygonEdges(a).some(([p,q])=>polygonEdges(b).some(([r,s])=>strictCross(p,q,r,s)))}
function polygonsOverlap(a,b){
  // Detect crossings and proper containment, including coincident centroids.
  for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++)if(strictCross(a[i],a[(i+1)%a.length],b[j],b[(j+1)%b.length]))return true;
  if(a.some(p=>inside(p,b))||b.some(p=>inside(p,a)))return true;
  const ca=centroid(a),cb=centroid(b);
  return inside(ca,b)||inside(cb,a);
}
function parcelOverlap(poly,parcels){return parcels.some(p=>polygonsOverlap(poly,p.geometry.polygon))}
function edgeClearance(a,b,other){const v={x:b.x-a.x,z:b.z-a.z},length=Math.hypot(v.x,v.z);if(length<EPS)return 0;const dx=v.x/length,dz=v.z/length;const project=p=>(p.x-a.x)*dx+(p.z-a.z)*dz;const lo=Math.max(0,Math.min(...other.map(project))),hi=Math.min(length,Math.max(...other.map(project)));return Math.max(0,hi-lo)}
function sharedStreetFrontage(poly,parcels){const edgeA=poly[0],edgeB=poly[1];return parcels.filter(p=>p.metadata?.frontage&&p.geometry?.polygon?.length===4).map(p=>{const q=p.geometry.polygon;return {parcelId:p.id,sharedLength:edgeClearance(edgeA,edgeB,q.slice(0,2)),collinear:Math.abs(orient(edgeA,edgeB,q[0]))<.05&&Math.abs(orient(edgeA,edgeB,q[1]))<.05}}).filter(x=>x.collinear&&x.sharedLength>EPS)}
function dominantAxis(poly){let best={length:0,tx:1,tz:0};for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length],L=dist(a,b);if(L>best.length)best={length:L,tx:(b.x-a.x)/L,tz:(b.z-a.z)/L}}return best}
function buildInteriorMorphology(block,parcels,{minFrontage=9,maxFrontage=18}={}){const poly=block.geometry.polygon,A=Math.abs(area(poly));if(A<1600)return{parcels,alleys:[],courtyards:[]};const c=centroid(poly),axis=dominantAxis(poly),tx=axis.tx,tz=axis.tz,nx=-tz,nz=tx,core=shrink(poly,A>9000?.72:.64),alleys=[],courtyards=[];if(!polyInside(core,poly))return{parcels,alleys,courtyards};const alleyWidth=A>8000?3.2:2.4,span=Math.sqrt(A)*.58,mainA={x:c.x-tx*span*.5,z:c.z-tz*span*.5},mainB={x:c.x+tx*span*.5,z:c.z+tz*span*.5};if(inside(mainA,poly)&&inside(mainB,poly))alleys.push({a:mainA,b:mainB,width:alleyWidth,kind:'internal-alley'});if(A>5200){const cross=.34+((block.id.length%5)*.05),cc={x:c.x+tx*span*(cross-.5),z:c.z+tz*span*(cross-.5)},crossSpan=Math.sqrt(A)*.38,a={x:cc.x-nx*crossSpan*.5,z:cc.z-nz*crossSpan*.5},b={x:cc.x+nx*crossSpan*.5,z:cc.z+nz*crossSpan*.5};if(inside(a,poly)&&inside(b,poly))alleys.push({a,b,width:2.2,kind:'secondary-alley'})}
const courtCount=A>10000?3:A>5000?2:1;for(let i=0;i<courtCount;i++){const along=(i-(courtCount-1)/2)*Math.min(28,Math.sqrt(A)*.18),side=i%2===0?1:-1,cc={x:c.x+tx*along+nx*side*Math.sqrt(A)*.09,z:c.z+tz*along+nz*side*Math.sqrt(A)*.09},cw=Math.min(16,Math.max(8,Math.sqrt(A)*.1)),cd=cw*(.72+((i*17)%20)/100),court=rectAt(cc,tx,tz,cw,cd);if(polyInside(court,core))courtyards.push(court)}
const rowSpacing=Math.max(12,Math.min(18,maxFrontage)),depth=Math.max(10,Math.min(18,Math.sqrt(A)*.12)),frontage=Math.max(minFrontage,Math.min(maxFrontage,12.5)),half=Math.sqrt(A)*.34;for(const side of[-1,1])for(let row=0;row<2;row++){const offset=side*(depth*.65+row*rowSpacing),count=Math.max(2,Math.floor((half*2)/frontage));for(let i=0;i<count;i++){const u=-half+(i+.5)*(half*2/count),jitter=(((i+row*7+(side>0?3:0))*37)%9-4)*.45,pc={x:c.x+tx*(u+jitter)+nx*offset,z:c.z+tz*(u+jitter)+nz*offset},w=(half*2/count)*.84,d=depth*(.76+((i*13+row*5)%19)/100),parcelPoly=rectAt(pc,tx,tz,w,d);if(!polyInside(parcelPoly,core))continue;if(courtyards.some(q=>inside(pc,q)))continue;if(alleys.some(a=>distanceToSegment(pc,a.a,a.b)<a.width*1.8))continue;if(parcelOverlap(parcelPoly,parcels))continue;parcels.push({id:`${block.id}:parcel:${String(parcels.length+1).padStart(3,'0')}`,type:'parcel',districtId:block.districtId,blockId:block.id,confidence:'inferred',geometry:{primitive:'polygon',polygon:parcelPoly,terrainFollowing:true},orientation:{source:'block-interior-morphology',tangent:{x:tx,z:tz}},typologyPool:['courtyard-house','street-house','workshop-house'],metadata:{generator:'block-interior-morphology-v1',interiorFabric:true,gridGenerated:false,semanticBox:false}})}}return{parcels,alleys,courtyards}}
function distanceToSegment(p,a,b){const dx=b.x-a.x,dz=b.z-a.z,l2=dx*dx+dz*dz;if(!l2)return dist(p,a);const t=Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.z-a.z)*dz)/l2));return dist(p,{x:a.x+t*dx,z:a.z+t*dz})}
export function validateParcelGeometry(parcels,blockPolygon){
 const errors=[];
 for(let i=0;i<parcels.length;i++){
  const p=parcels[i],poly=p.geometry?.polygon;
  if(!poly||poly.length<3||Math.abs(area(poly))<EPS){errors.push({kind:'invalid-area',parcelId:p.id});continue}
  if(!polyInside(poly,blockPolygon))errors.push({kind:'outside-block',parcelId:p.id});
  for(let j=0;j<i;j++){
   const q=parcels[j],other=q.geometry?.polygon;
   if(other&&polygonsOverlap(poly,other))errors.push({kind:'overlapping-parcels',parcelId:p.id,otherId:q.id});
  }
 }
 return {valid:errors.length===0,errors,parcelCount:parcels.length};
}
export function generateUrbanBlocks({district,roads=[]}={}){const boundary=district?.geometry?.polygon;if(!boundary?.length)return{blocks:[],withheld:true,reason:'district-envelope-withheld'};if(!roads.length)return{blocks:[],withheld:true,reason:'street-graph-withheld'};const result=polygonize(boundary,roads),blocks=result.faces.map((face,i)=>({id:`${district.id}:block:${String(i+1).padStart(3,'0')}`,type:'block',districtId:district.id,confidence:'inferred',geometry:{primitive:'polygon',polygon:face.polygon,terrainFollowing:true},metadata:{generator:'street-graph-polygonizer-v1',area:face.area,closedFace:true,roadBounded:true,gridPopulation:false,semanticBox:false}}));return{blocks,withheld:false,count:blocks.length,policy:'city-envelope + street-graph → planar faces → closed urban blocks',generator:'street-graph-polygonizer-v1',graphNodes:result.graphNodes,graphEdges:result.graphEdges}}
export function subdivideBlockToParcels(block,{minFrontage=9,maxFrontage=18,depthInset=2.4}={}){const poly=block.geometry?.polygon;if(!poly?.length)return[];const c=centroid(poly),es=poly.map((a,i)=>({a,b:poly[(i+1)%poly.length],length:dist(a,poly[(i+1)%poly.length])})).filter(e=>e.length>=minFrontage*1.4),parcels=[];for(let ei=0;ei<es.length;ei++){const edge=es[ei],dx=edge.b.x-edge.a.x,dz=edge.b.z-edge.a.z,L=edge.length,tx=dx/L,tz=dz/L,nx=-tz,nz=tx,side=((c.x-(edge.a.x+edge.b.x)/2)*nx+(c.z-(edge.a.z+edge.b.z)/2)*nz)>=0?1:-1,count=Math.max(1,Math.round(L/Math.max(minFrontage,Math.min(maxFrontage,13.5))));for(let i=0;i<count;i++){const t0=(i+.004)/count,t1=(i+.996)/count,frontA=lerp(edge.a,edge.b,t0),frontB=lerp(edge.a,edge.b,t1),depth=Math.min(24,Math.max(10,Math.sqrt(Math.abs(area(poly)))*.16)),p1={x:frontA.x+nx*depthInset*side,z:frontA.z+nz*depthInset*side},p2={x:frontB.x+nx*depthInset*side,z:frontB.z+nz*depthInset*side},p3={x:frontB.x+nx*depth*side,z:frontB.z+nz*depth*side},p4={x:frontA.x+nx*depth*side,z:frontA.z+nz*depth*side},parcelPoly=[p1,p2,p3,p4];if(!polyInside(parcelPoly,poly))continue;const pc=centroid(parcelPoly);if(parcelOverlap(parcelPoly,parcels))continue;const streetNeighbors=sharedStreetFrontage(parcelPoly,parcels);parcels.push({id:`${block.id}:parcel:${String(parcels.length+1).padStart(3,'0')}`,type:'parcel',districtId:block.districtId,blockId:block.id,confidence:'inferred',geometry:{primitive:'polygon',polygon:parcelPoly,terrainFollowing:true},orientation:{source:'street-bounded-block-edge',tangent:{x:tx,z:tz}},typologyPool:['courtyard-house','street-house','workshop-house'],metadata:{generator:'closed-block-edge-subdivision-v4',blockFace:true,perimeterFabric:true,frontage:{a:frontA,b:frontB,edgeIndex:ei},streetNeighbors,gridGenerated:false,semanticBox:false}})}}const morphology=buildInteriorMorphology(block,parcels,{minFrontage,maxFrontage});
const geometryAudit=validateParcelGeometry(morphology.parcels,poly);
if(!geometryAudit.valid){
 block.metadata.geometryAudit={valid:false,errors:geometryAudit.errors.slice(0,30),errorCount:geometryAudit.errors.length};
 // Fail closed: malformed inferred parcels must never enter the city core.
 return [];
}
block.metadata.geometryAudit={valid:true,parcelCount:morphology.parcels.length};block.metadata.interiorMorphology={generator:'block-interior-morphology-v1',alleys:morphology.alleys,courtyards:morphology.courtyards,parcelCount:morphology.parcels.length};// Build a symmetric frontage adjacency index after every perimeter parcel exists.
const perimeter=morphology.parcels.filter(p=>p.metadata?.perimeterFabric);
for(const parcel of perimeter){
  const neighbors=sharedStreetFrontage(parcel.geometry.polygon,perimeter.filter(p=>p.id!==parcel.id));
  parcel.metadata.streetNeighbors=neighbors;
}
return morphology.parcels}
