import * as THREE from 'three';

function yAt(terrain,x,z){const y=terrain?.heightAtWorld?.(x,z);return Number.isFinite(y)?y:0}
function box(group,meshes,material,terrain,x,z,w,d,h,stage,start,lift=0){const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);const ground=yAt(terrain,x,z)+lift;mesh.position.set(x,ground+h/2+1.5,z);mesh.receiveShadow=true;mesh.castShadow=true;mesh.userData.phase2={stage,start,baseHeight:h,groundY:ground};group.add(mesh);meshes.push(mesh);return mesh}
function line(group,meshes,material,terrain,a,b,width,stage,start,lift=0){const dx=b[0]-a[0],dz=b[1]-a[1],len=Math.hypot(dx,dz),mesh=box(group,meshes,material,terrain,(a[0]+b[0])/2,(a[1]+b[1])/2,len,width,2.1,stage,start,lift);mesh.rotation.y=-Math.atan2(dz,dx);return mesh}
function steppedBath(group,meshes,material,terrain,x,z,start,lift=0){box(group,meshes,material,terrain,x,z,18,14,3,'mikveh-basin',start,lift-4);for(let i=0;i<4;i++)box(group,meshes,material,terrain,x,z+5-i*2.7,12,2.2,1.3,'mikveh-step',start+.012+i*.006,lift-2.8+i*.65)}
function marketRow(group,meshes,material,terrain,x,z,count,start){for(let i=0;i<count;i++){const px=x+i*22;box(group,meshes,material,terrain,px,z,18,16,13+(i%3)*2,'market-shop',start+i*.008);box(group,meshes,material,terrain,px,z-9,18,3,2.2,'market-awning',start+.04+i*.008,7)}}

export function buildHerodianRitualCommerceLayer(group,materials,terrain,{cx=-15,cz=55,w=760,d=700}={}){
 const meshes=[],stone=materials.reconstructed,observed=materials.observed||stone,inferred=materials.inferred||stone;
 const tx=cx+w*.19,tz=cz-d*.28,s=.34;
 // Southern Temple approach: purification clusters before ascent.
 for(const [dx,dz,lift] of [[-118,128,4],[-88,137,5],[-56,132,6],[-24,142,7],[14,136,8],[48,129,9]])steppedBath(group,meshes,observed,terrain,tx+dx,tz+dz,s+(dx+120)*.00025,lift);
 // Commercial frontage beside the pilgrimage stream, kept outside the sanctuary core.
 marketRow(group,meshes,inferred,terrain,tx-126,tz+112,6,s+.07);
 marketRow(group,meshes,inferred,terrain,tx-116,tz+88,5,s+.10);
 // Exchange / animal-market courts as spatial envelopes rather than literal historical labels.
 box(group,meshes,inferred,terrain,tx-54,tz+105,72,34,3,'pilgrim-market-court',s+.12,8);
 box(group,meshes,inferred,terrain,tx+48,tz+108,62,32,3,'pilgrim-market-court',s+.135,9);
 // Narrow connectors weave purification, commerce and ascent into the existing southern approach.
 line(group,meshes,observed,terrain,[tx-132,tz+150],[tx-72,tz+104],5,'ritual-connector',s+.15,5);
 line(group,meshes,observed,terrain,[tx-72,tz+104],[tx-18,tz+94],5,'ritual-connector',s+.17,7);
 line(group,meshes,observed,terrain,[tx-18,tz+94],[tx+62,tz+88],5,'ritual-connector',s+.19,9);
 return {meshes,grammar:'herodian-pilgrimage-purification-commerce',status:'phase2-herodian-ritual-commerce'};
}

export function setHerodianRitualCommerceProgress(runtime,progress=1,{ruined=false}={}){
 if(!runtime?.meshes)return;const p=Math.max(0,Math.min(1,progress));
 for(const mesh of runtime.meshes){const meta=mesh.userData.phase2;if(!meta)continue;const duration=meta.stage.includes('mikveh')?.14:meta.stage.includes('market')?.18:.16;const local=Math.max(0,Math.min(1,(p-meta.start)/duration));mesh.visible=local>0;if(!mesh.visible)continue;const eased=local*local*(3-2*local),ruinScale=ruined?.22:1,scaleY=Math.max(.015,eased)*ruinScale;mesh.scale.y=scaleY;mesh.position.y=meta.groundY+(meta.baseHeight*scaleY)/2+1.5;mesh.material.opacity=Math.max(.18,.32+.68*eased)*(ruined?.58:1);mesh.material.transparent=local<.999||ruined}
}
