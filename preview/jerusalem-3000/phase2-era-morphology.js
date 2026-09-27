import * as THREE from 'three';

const ERA={
 'chalcolithic-early-bronze':{cx:-430,cz:360,w:250,d:310,n:8,wall:0,road:.10,build:.22,growth:.58},
 'middle-bronze':{cx:-360,cz:300,w:330,d:390,n:13,wall:.12,road:.20,build:.28,growth:.62},
 'late-bronze-iron1':{cx:-330,cz:270,w:370,d:420,n:16,wall:.12,road:.21,build:.29,growth:.64},
 'late-first-temple':{cx:-100,cz:120,w:650,d:610,n:34,wall:.08,road:.18,build:.26,growth:.58},
 'persian-nehemiah':{cx:-220,cz:170,w:440,d:480,n:22,wall:.10,road:.22,build:.32,growth:.66},
 'hellenistic-hasmonean':{cx:-40,cz:80,w:680,d:620,n:38,wall:.08,road:.18,build:.27,growth:.60},
 'aelia':{cx:40,cz:-40,w:680,d:620,n:34,wall:0,road:.12,build:.25,growth:.58,grid:true},
 'byzantine':{cx:20,cz:-30,w:760,d:690,n:44,wall:.08,road:.17,build:.25,growth:.57},
 'early-islamic':{cx:10,cz:-20,w:730,d:670,n:42,wall:.08,road:.18,build:.27,growth:.60},
 'ayyubid-mamluk':{cx:0,cz:-10,w:700,d:640,n:40,wall:.08,road:.18,build:.27,growth:.61},
 'outside-walls':{cx:55,cz:-35,w:980,d:850,n:58,wall:0,road:.10,build:.20,growth:.46,edge:true},
 'modern':{cx:120,cz:-80,w:1320,d:1080,n:78,wall:0,road:.08,build:.17,growth:.40,edge:true}
};
function yAt(t,x,z){const y=t?.heightAtWorld?.(x,z);return Number.isFinite(y)?y:0}
function box(g,a,m,t,x,z,w,d,h,stage,start,r=0){const q=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);q.position.set(x,yAt(t,x,z)+h/2+4,z);q.rotation.y=r;q.receiveShadow=true;q.userData.phase2={stage,start,baseHeight:h};g.add(q);a.push(q);return q}
function road(g,a,m,t,x,z,w,d,start,r=0){return box(g,a,m,t,x,z,w,d,3,'road',start,r)}
function walls(g,a,m,t,c){if(!c.wall)return;const h=34,tick=12,s=c.wall;box(g,a,m,t,c.cx,c.cz-c.d/2,c.w,tick,h,'wall',s);box(g,a,m,t,c.cx,c.cz+c.d/2,c.w,tick,h,'wall',s+.02);box(g,a,m,t,c.cx-c.w/2,c.cz,tick,c.d,h,'wall',s+.04);box(g,a,m,t,c.cx+c.w/2,c.cz,tick,c.d,h,'wall',s+.06);for(let i=0;i<6;i++){const x=c.cx-c.w*.38+i*c.w*.152;box(g,a,m,t,x,c.cz-c.d/2,25,25,46+(i%2)*6,'tower',s+.08+i*.012)}}
function streets(g,a,m,t,c){road(g,a,m,t,c.cx,c.cz,c.w*.82,9,c.road);road(g,a,m,t,c.cx,c.cz,9,c.d*.82,c.road+.035);if(c.grid){for(const o of[-.24,.24]){road(g,a,m,t,c.cx+o*c.w,c.cz,7,c.d*.72,c.road+.07);road(g,a,m,t,c.cx,c.cz+o*c.d,c.w*.72,7,c.road+.09)}}else{road(g,a,m,t,c.cx-c.w*.16,c.cz+c.d*.05,7,c.d*.56,c.road+.075,.05);road(g,a,m,t,c.cx+c.w*.10,c.cz-c.d*.18,c.w*.55,7,c.road+.10,-.035)}}
function fabric(g,a,m,t,c){for(let i=0;i<c.n;i++){const cols=Math.max(4,Math.round(Math.sqrt(c.n*1.3))),col=i%cols,row=Math.floor(i/cols),jx=((i*47)%31)-15,jz=((i*29)%27)-13,x=c.cx+(col-(cols-1)/2)*(c.w/(cols+1))+jx,z=c.cz+(row-2.2)*(c.d/6)+jz,w=24+(i%4)*7,d=23+(i%3)*8,h=19+(i%6)*6;box(g,a,m,t,x,z,w,d,h,'fabric',c.build+i*(.28/c.n),((i%5)-2)*.014)}}
function growth(g,a,m,t,c){const count=Math.max(8,Math.round(c.n*.38));for(let i=0;i<count;i++){const angle=(i/count)*Math.PI*2+(i%3)*.11,rad=(c.edge?.58:.39)+(i%4)*.035,x=c.cx+Math.cos(angle)*c.w*rad,z=c.cz+Math.sin(angle)*c.d*rad,w=22+(i%4)*7,d=22+(i%3)*6,h=18+(i%5)*6;box(g,a,m,t,x,z,w,d,h,'growth',c.growth+i*(.20/count),angle*.08)}}
function anchors(g,a,materials,t,c,id){const stone=materials.reconstructed,inferred=materials.inferred||stone,s=Math.min(.78,c.growth+.08);if(id==='late-first-temple'||id==='persian-nehemiah'||id==='hellenistic-hasmonean'){box(g,a,inferred,t,c.cx+c.w*.10,c.cz-c.d*.31,104,72,16,'sanctuary',s);box(g,a,inferred,t,c.cx+c.w*.10,c.cz-c.d*.31,58,42,48,'sanctuary',s+.05)}else if(id==='byzantine'){box(g,a,inferred,t,c.cx-c.w*.18,c.cz-c.d*.12,112,78,18,'church',s);box(g,a,inferred,t,c.cx-c.w*.18,c.cz-c.d*.12,66,44,55,'church',s+.05)}else if(id==='early-islamic'||id==='ayyubid-mamluk'){box(g,a,inferred,t,c.cx+c.w*.12,c.cz-c.d*.22,118,84,18,'religious',s);box(g,a,inferred,t,c.cx+c.w*.12,c.cz-c.d*.22,68,48,52,'religious',s+.05)}else if(id==='modern'){for(let i=0;i<7;i++)box(g,a,inferred,t,c.cx+c.w*.18+i*54,c.cz-c.d*.18,38,38,48+i*9,'modern-anchor',s+i*.018)}}
export function buildEraUrbanMorphology(group,phaseId,materials,terrain,{progress=1}={}){const c=ERA[phaseId];if(!c)return null;const meshes=[],stone=materials.reconstructed,observed=materials.observed||stone,inferred=materials.inferred||stone;walls(group,meshes,stone,terrain,c);streets(group,meshes,observed,terrain,c);fabric(group,meshes,stone,terrain,c);growth(group,meshes,inferred,terrain,c);anchors(group,meshes,materials,terrain,c,phaseId);const runtime={phaseId,meshes,grammar:`${phaseId}-continuous-morphology`,status:'phase2-propagation',progress:1,ruined:false};setEraMorphologyProgress(runtime,progress);return runtime}
export function setEraMorphologyProgress(runtime,progress=1,{ruined=false}={}){if(!runtime?.meshes)return;runtime.progress=Math.max(0,Math.min(1,progress));runtime.ruined=ruined;for(const mesh of runtime.meshes){const meta=mesh.userData.phase2;if(!meta)continue;const local=Math.max(0,Math.min(1,(runtime.progress-meta.start)/.15));mesh.visible=local>0;mesh.scale.y=Math.max(.02,local)*(ruined?.22:1);mesh.material.opacity=Math.max(.16,local);mesh.material.transparent=local<.999}}
