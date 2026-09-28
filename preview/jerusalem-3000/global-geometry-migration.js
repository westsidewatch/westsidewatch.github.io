import * as THREE from 'three';

const KEEP_RECTANGULAR=new Set(['pool','pool-wall','siloam-pool','bethesda-pool','reservoir','temple-platform','temple-inner-court']);
const ROAD_WORDS=['road','street','lane','valley','channel','connector'];
function stageOf(mesh){return String(mesh.userData?.phase2?.stage||'').toLowerCase()}
function isRoad(stage){return ROAD_WORDS.some(word=>stage.includes(word))}
function polygonPrism(w,d,h,seed=0){
 const sx=w/2,sz=d/2,k=.08+((seed%5)*.012);
 const pts=[[-sx,-sz*.84],[-sx*.34,-sz],[sx*.52,-sz*(.92-k)],[sx, -sz*.22],[sx*(.88-k),sz*.68],[sx*.30,sz],[-sx*.56,sz*(.91-k)],[-sx,sz*.28]];
 const shape=new THREE.Shape();pts.forEach(([x,z],i)=>i?shape.lineTo(x,z):shape.moveTo(x,z));shape.closePath();
 const g=new THREE.ExtrudeGeometry(shape,{depth:h,bevelEnabled:false,steps:1});g.rotateX(-Math.PI/2);g.translate(0,-h/2,0);g.computeVertexNormals();return g;
}
function wallPrism(w,d,h,seed=0){
 const alongX=w>=d,L=(alongX?w:d)/2,T=(alongX?d:w)/2,j=Math.min(T*.34,1.8+(seed%3));
 const p=[[-L,-T],[-L*.36,-T+j],[L*.22,-T],[L,-T+j*.45],[L,T-j*.25],[L*.31,T],[-L*.44,T-j*.55],[-L,T]];
 const pts=alongX?p:p.map(([a,b])=>[b,a]);const shape=new THREE.Shape();pts.forEach(([x,z],i)=>i?shape.lineTo(x,z):shape.moveTo(x,z));shape.closePath();
 const g=new THREE.ExtrudeGeometry(shape,{depth:h,bevelEnabled:false,steps:1});g.rotateX(-Math.PI/2);g.translate(0,-h/2,0);g.computeVertexNormals();return g;
}
function roadRibbonFromBox(w,d,seed=0){
 const alongX=w>=d,L=(alongX?w:d)/2,T=(alongX?d:w)/2,bend=Math.min(L*.10,5+(seed%7));
 const pts=alongX?[[-L,-T],[-L*.18,-T*.72],[L*.30,-T],[L,T*.05],[L,T], [L*.25,T*.72],[-L*.22,T],[-L,-T*.05]]:[[-T,-L],[-T*.72,-L*.18],[-T,L*.30],[T*.05,L],[T,L],[T*.72,L*.25],[T,-L*.22],[-T*.05,-L]];
 const shape=new THREE.Shape();pts.forEach(([x,z],i)=>i?shape.lineTo(x,z):shape.moveTo(x,z));shape.closePath();const g=new THREE.ShapeGeometry(shape);g.rotateX(-Math.PI/2);g.translate(alongX?0:bend*.02,0,alongX?bend*.02:0);g.computeVertexNormals();return g;
}
function migrateMesh(mesh,index){
 if(mesh.geometry?.type!=='BoxGeometry')return false;const stage=stageOf(mesh);if(KEEP_RECTANGULAR.has(stage))return false;
 const p=mesh.geometry.parameters||{},w=p.width||1,h=p.height||1,d=p.depth||1;let next;
 if(isRoad(stage))next=roadRibbonFromBox(w,d,index);
 else if(stage.includes('wall')||stage.includes('retaining')||stage.includes('front'))next=wallPrism(w,d,h,index);
 else next=polygonPrism(w,d,h,index);
 mesh.geometry.dispose();mesh.geometry=next;mesh.userData.geometryMigration={from:'BoxGeometry',to:isRoad(stage)?'terrain-ribbon':'irregular-stone-prism',global:true};return true;
}
export function migrateRuntimeGeometry(runtime){
 if(!runtime?.meshes)return runtime;let migrated=0;runtime.meshes.forEach((mesh,index)=>{if(migrateMesh(mesh,index))migrated++});
 runtime.geometryMigration={version:'global-debox-v1',migrated,total:runtime.meshes.length};runtime.grammar=`${runtime.grammar||'urban'}-global-debox`;return runtime;
}
