import * as THREE from 'three';

const CALIBRATION={
  'david-solomon':{cx:-260,cz:210,sx:.70,sz:.82,rows:3,cols:5,block:72,lane:22,courtyard:.34,wall:true},
  'herodian-jesus':{cx:80,cz:0,sx:1.25,sz:1.15,rows:6,cols:8,block:82,lane:28,courtyard:.28,wall:true},
  'crusader':{cx:0,cz:-20,sx:.96,sz:.94,rows:5,cols:7,block:76,lane:20,courtyard:.24,wall:true}
};
const HERODIAN_SEQUENCE={road:.08,wall:.18,block:.28,monument:.48};
function terrainY(terrain,x,z){const y=terrain?.heightAtWorld?.(x,z);return Number.isFinite(y)?y:0}
function addBox(group,meshes,material,terrain,x,z,w,d,h,rotation=0,stage='block',start=0){const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);mesh.position.set(x,terrainY(terrain,x,z)+h/2+4,z);mesh.rotation.y=rotation;mesh.receiveShadow=true;mesh.userData.phase2={stage,start,baseHeight:h};group.add(mesh);meshes.push(mesh);return mesh}
function courtyardBlock(group,meshes,material,terrain,x,z,w,d,h,ratio,rotation,start){const gapW=w*ratio,gapD=d*ratio,wingW=(w-gapW)/2,wingD=(d-gapD)/2;addBox(group,meshes,material,terrain,x-(w-wingW)/2,z,wingW,d,h,rotation,'block',start);addBox(group,meshes,material,terrain,x+(w-wingW)/2,z,wingW,d,h*.86,rotation,'block',start+.018);addBox(group,meshes,material,terrain,x,z-(d-wingD)/2,gapW,wingD,h*.92,rotation,'block',start+.036);addBox(group,meshes,material,terrain,x,z+(d-wingD)/2,gapW,wingD,h*.78,rotation,'block',start+.054)}
function street(group,meshes,material,terrain,x,z,w,d,start=0){addBox(group,meshes,material,terrain,x,z,w,d,3.5,0,'road',start)}
function wallCircuit(group,meshes,material,terrain,c,start=0){const width=(c.cols*c.block+(c.cols-1)*c.lane)*c.sx+90,depth=(c.rows*c.block+(c.rows-1)*c.lane)*c.sz+90,t=15,h=42;addBox(group,meshes,material,terrain,c.cx,c.cz-depth/2,width,t,h,0,'wall',start);addBox(group,meshes,material,terrain,c.cx,c.cz+depth/2,width,t,h,0,'wall',start+.025);addBox(group,meshes,material,terrain,c.cx-width/2,c.cz,t,depth,h,0,'wall',start+.05);addBox(group,meshes,material,terrain,c.cx+width/2,c.cz,t,depth,h,0,'wall',start+.075);let n=0;for(const[x,z]of[[c.cx-width/2,c.cz-depth/2],[c.cx+width/2,c.cz-depth/2],[c.cx-width/2,c.cz+depth/2],[c.cx+width/2,c.cz+depth/2]])addBox(group,meshes,material,terrain,x,z,34,34,62,0,'wall',start+.10+n++*.018)}
function applyConstruction(meshes,progress,ruined){for(const mesh of meshes){const meta=mesh.userData.phase2;if(!meta)continue;const local=Math.max(0,Math.min(1,(progress-meta.start)/.16));mesh.visible=local>0;const ruinScale=ruined?.22:1;mesh.scale.y=Math.max(.02,local)*ruinScale;mesh.material.opacity=Math.max(.16,local);mesh.material.transparent=local<.999||mesh.material.opacity<1}}
export function setPhase2MorphologyProgress(runtime,progress=1,{ruined=false}={}){if(!runtime?.meshes)return;runtime.progress=Math.max(0,Math.min(1,progress));runtime.ruined=ruined;applyConstruction(runtime.meshes,runtime.progress,ruined)}
export function buildPhase2UrbanMorphology(group,phaseId,materials,terrain,{ruined=false,progress=1}={}){
  const c=CALIBRATION[phaseId];if(!c)return null;
  const meshes=[],building=materials.reconstructed,road=materials.observed||materials.reconstructed,wall=materials.reconstructed;
  const pitchX=(c.block+c.lane)*c.sx,pitchZ=(c.block+c.lane)*c.sz,herodian=phaseId==='herodian-jesus';
  for(let r=0;r<c.rows;r++)for(let col=0;col<c.cols;col++){
    const x=c.cx+(col-(c.cols-1)/2)*pitchX,z=c.cz+(r-(c.rows-1)/2)*pitchZ,seed=(r+1)*37+(col+1)*19,h=ruined?10+(seed%8):28+(seed%44),rot=((seed%7)-3)*.012,start=herodian?HERODIAN_SEQUENCE.block+(r*c.cols+col)/(c.rows*c.cols)*.34:0;
    courtyardBlock(group,meshes,building,terrain,x,z,c.block*c.sx,c.block*c.sz,h,c.courtyard,rot,start);
  }
  for(let col=0;col<c.cols-1;col++){const x=c.cx+(col-(c.cols-2)/2)*pitchX+pitchX/2;street(group,meshes,road,terrain,x,c.cz,c.lane*.42,c.rows*pitchZ,herodian?HERODIAN_SEQUENCE.road+col*.018:0)}
  for(let r=0;r<c.rows-1;r++){const z=c.cz+(r-(c.rows-2)/2)*pitchZ+pitchZ/2;street(group,meshes,road,terrain,c.cx,z,c.cols*pitchX,c.lane*.42,herodian?HERODIAN_SEQUENCE.road+r*.018:0)}
  if(c.wall)wallCircuit(group,meshes,wall,terrain,c,herodian?HERODIAN_SEQUENCE.wall:0);
  const runtime={phaseId,meshes,blocks:c.rows*c.cols,grammar:'courtyard-block-street-wall',status:'phase2-calibration',progress:1,ruined};setPhase2MorphologyProgress(runtime,herodian?progress:1,{ruined});return runtime;
}
