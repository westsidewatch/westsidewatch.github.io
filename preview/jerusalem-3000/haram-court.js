import {foundationContactGeometry} from './foundation-contact.js';
import * as THREE from 'three';
import {geographicToENU} from './terrain-runtime.js';
import {clipBlockToEnvelope} from './district-infill.js';
import {haramCourtReference as R} from './haram-court-reference.js';
export const HARAM_PHASES=new Set(['early-islamic','crusader','ayyubid-mamluk','ottoman','outside-walls','modern']);
const origin={lat:31.778,lon:35.235},convert=([lat,lon])=>{const q=geographicToENU(lat,lon,origin);return{x:q.east,z:-q.north};};
export const haramFootprint=R.footprint.map(convert),haramPodium=R.podium.map(convert),chainPoint=convert(R.chainPoint);
export const haramFloor=terrain=>terrain.heightAtWorld(0,0)+.8;
export function haramCourt(phase){const former=['aelia','byzantine'].includes(phase);return HARAM_PHASES.has(phase)||former?{id:`j3k:${phase}:independent:monument:${former?'eastern-site-context':'haram-court-context'}`,type:'monument',confidence:'inferred',geometry:{frame:'canonical-dem-enu',status:'modern-outline-with-selected-era-court-context',primitive:'polygon',polygon:haramFootprint},source:{urls:former?[R.source.url,'https://publications.iaa.org.il/atiqot/vol56/iss1/14/']:[R.source.url,'https://www.archnet.org/sites/2814','https://www.islamicarchitecturalheritage.com/listings/dome-of-the-chain-qubbat-al-silsila','https://archives.iaa.org.il/zoom/zoom.aspx?folder_id=40&id=5121'],authority:former?'modern site outline only; internal Roman/Byzantine land use unresolved':'modern mapped outer and upper courts; architectural types sourced, heights/stair/arcade layout schematic'},metadata:{name:former?'舊聖域遺址語境（內部建築未核定）':'聖域庭院、台階與附屬建築（示意）',coreProfile:former?'post-temple-site-context':'haram-court-ensemble',terrainFollowingSite:former,precinctContext:true,siteRegistration:{historicalFootprintVerified:false,policy:'modern-map-context-not-ancient-survey'},wholePhaseSimultaneity:false,geometryVerified:false,ancientGroundVerified:false,referencePeriod:'selected phase context; modern outline does not certify ancient paving or fabric'}}:null;}
export function haramCourtGeometry(record,terrain){
 if(record.metadata.terrainFollowingSite)return formerPrecinctGeometry(terrain);
 const floor=haramFloor(terrain),positions=[],colours=[],stone=new THREE.Color(0xd2c4a5),dark=new THREE.Color(0xb9a27b);
 const add=(g,c=stone)=>{const p=g.attributes.position,idx=g.index?.array||Array.from({length:p.count},(_,i)=>i);for(const i of idx){positions.push(p.getX(i),p.getY(i),p.getZ(i));colours.push(c.r,c.g,c.b);}g.dispose();};
 const box=(x,y,z,w,h,d,c)=>{const g=new THREE.BoxGeometry(w,h,d);g.translate(x,y+h/2,z);add(g,c);};
 const surface=(poly,y,skirt=false)=>{const tris=THREE.ShapeUtils.triangulateShape(poly.map(p=>new THREE.Vector2(p.x,p.z)),[]),p=[];for(const tri of tris){const a=poly[tri[0]],b=poly[tri[1]],c=poly[tri[2]],up=(b.z-a.z)*(c.x-a.x)-(b.x-a.x)*(c.z-a.z)>0;for(const i of up?tri:[...tri].reverse())p.push(poly[i].x,y,poly[i].z);}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));g.computeVertexNormals();add(g);if(skirt)add(foundationContactGeometry(poly.map((a,i)=>[a,poly[(i+1)%poly.length]]),terrain,y),dark);};
 surface(haramFootprint,floor,true);surface(haramPodium,floor+3,true);
 // A separate upper court, four authored stair approaches and late arcade
 // context make circulation legible without filling an open sanctuary with houses.
 const xs=haramPodium.map(p=>p.x),zs=haramPodium.map(p=>p.z),cx=(Math.min(...xs)+Math.max(...xs))/2,cz=(Math.min(...zs)+Math.max(...zs))/2;
 const late=['ayyubid-mamluk','ottoman','outside-walls','modern'].includes(record.id.split(':')[1]);
 for(const [x,z,axis,sign]of [[cx,Math.min(...zs),0,-1],[cx,Math.max(...zs),0,1],[Math.min(...xs),cz,1,-1],[Math.max(...xs),cz,1,1]]){
  for(let i=0;i<6;i++)box(x+(axis?sign*(11-i*2):0),floor+i*.5,z+(!axis?sign*(11-i*2):0),axis?2:16,.5,axis?16:2,dark);
  if(late){for(const t of [-6,0,6])box(x+(axis?0:t),floor+3,z+(axis?t:0),1,5,1,dark);for(const t of [-3,3]){const shape=new THREE.Shape();for(let i=0;i<=16;i++){const a=i*Math.PI/16;const px=3.3*Math.cos(a),py=3.3*Math.sin(a);i?shape.lineTo(px,py):shape.moveTo(px,py);}for(let i=16;i>=0;i--){const a=i*Math.PI/16;shape.lineTo(2.8*Math.cos(a),2.8*Math.sin(a));}shape.closePath();const g=new THREE.ExtrudeGeometry(shape,{depth:.8,bevelEnabled:false});g.translate(0,0,-.4);if(axis)g.rotateY(Math.PI/2);g.translate(x+(axis?0:t),floor+8,z+(axis?t:0));add(g,dark);}}
 }
 // Open domed kiosk: mapped Chain location, illustrative dimensions/columns.
 for(let i=0;i<12;i++){const a=i*Math.PI*2/12;box(chainPoint.x+5.5*Math.cos(a),floor+3,chainPoint.z+5.5*Math.sin(a),.65,5,.65,dark);}
 const roof=new THREE.CylinderGeometry(7,7,.5,12);roof.translate(chainPoint.x,floor+8.2,chainPoint.z);add(roof,dark);const dome=new THREE.SphereGeometry(5,16,8,0,Math.PI*2,0,Math.PI/2);dome.translate(chainPoint.x,floor+8.5,chainPoint.z);add(dome,dark);
 // A few broad stone bands distinguish open courts from unbuilt terrain; no
 // invented residential blocks, exact paving or detailed school reconstructions.
 for(const z of [85,115,145])box(0,floor+.015,z,120,.04,2,dark);
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setAttribute('color',new THREE.Float32BufferAttribute(colours,3));g.computeVertexNormals();return g;
}

// An archaeological-context surface on the original DEM, not an empty-city or
// complete ruin reconstruction. No Islamic platform/kiosk is copied backwards.
function formerPrecinctGeometry(terrain){
 const positions=[],colors=[],colour=new THREE.Color(0xb9ac91),mesh=terrain.mesh,p=mesh?.geometry.attributes.position,index=mesh?.geometry.index;
 const add=(poly)=>{for(let i=1;i+1<poly.length;i++){const tri=[poly[0],poly[i],poly[i+1]],a=tri[0],b=tri[1],c=tri[2];if((b.z-a.z)*(c.x-a.x)-(b.x-a.x)*(c.z-a.z)<0)tri.reverse();for(const q of tri){positions.push(q.x,terrain.heightAtWorld(q.x,q.z)+.12,q.z);colors.push(colour.r,colour.g,colour.b);}}};
 if(p&&index){for(let i=0;i<index.count;i+=3){const tri=[0,1,2].map(k=>{const j=index.getX(i+k);return{x:p.getX(j)+mesh.position.x,z:p.getZ(j)+mesh.position.z};});if(Math.max(...tri.map(q=>q.x))< -124||Math.min(...tri.map(q=>q.x))>243||Math.max(...tri.map(q=>q.z))< -257||Math.min(...tri.map(q=>q.z))>261)continue;for(const part of clipBlockToEnvelope(tri,haramFootprint,{minArea:1e-8}))add(part);}}
 else{const triangles=THREE.ShapeUtils.triangulateShape(haramFootprint.map(p=>new THREE.Vector2(p.x,p.z)),[]);for(const t of triangles)add(t.map(i=>haramFootprint[i]));}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));g.computeVertexNormals();return g;
}
