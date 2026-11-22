// Architectural GLB geometry ledger (read-only). All measurements in metres.
// Parses shipped split gzip GLB and computes true scene-node world AABBs.
import {readFileSync} from 'node:fs';
import {gunzipSync} from 'node:zlib';
import {join} from 'node:path';

const root=join(process.cwd(),'static/p2-maquette');
const compressed=Buffer.concat([0,1,2].map(i=>readFileSync(join(root,`model-v34.${i}.part`))));
const bin=gunzipSync(compressed);
if(bin.toString('utf8',0,4)!=='glTF')throw Error('Invalid GLB magic');
const jsonLength=bin.readUInt32LE(12);
const json=JSON.parse(bin.toString('utf8',20,20+jsonLength));
const identity=()=>[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1];
function multiply(a,b){const r=new Array(16).fill(0);for(let c=0;c<4;c++)for(let row=0;row<4;row++)for(let k=0;k<4;k++)r[c*4+row]+=a[k*4+row]*b[c*4+k];return r;}
function localMatrix(n){
 if(n.matrix)return n.matrix;
 const [x,y,z,w]=n.rotation??[0,0,0,1], [sx,sy,sz]=n.scale??[1,1,1],
       [tx,ty,tz]=n.translation??[0,0,0];
 return [
 (1-2*y*y-2*z*z)*sx,(2*x*y+2*z*w)*sx,(2*x*z-2*y*w)*sx,0,
 (2*x*y-2*z*w)*sy,(1-2*x*x-2*z*z)*sy,(2*y*z+2*x*w)*sy,0,
 (2*x*z+2*y*w)*sz,(2*y*z-2*x*w)*sz,(1-2*x*x-2*y*y)*sz,0,
 tx,ty,tz,1];
}
function transform(m,p){const [x,y,z]=p;return [m[0]*x+m[4]*y+m[8]*z+m[12],m[1]*x+m[5]*y+m[9]*z+m[13],m[2]*x+m[6]*y+m[10]*z+m[14]];}
function nodeBox(node,matrix){
 const mesh=json.meshes[node.mesh];if(!mesh)return null;
 const outMin=[Infinity,Infinity,Infinity],outMax=[-Infinity,-Infinity,-Infinity];
 for(const prim of mesh.primitives){const a=json.accessors[prim.attributes.POSITION];if(!a.min||!a.max)continue;
   for(const x of[a.min[0],a.max[0]])for(const y of[a.min[1],a.max[1]])for(const z of[a.min[2],a.max[2]]){
     const p=transform(matrix,[x,y,z]);for(let j=0;j<3;j++){outMin[j]=Math.min(outMin[j],p[j]);outMax[j]=Math.max(outMax[j],p[j]);}
   }
 }
 return outMin.every(Number.isFinite)?{min:outMin,max:outMax}:null;
}
const ledger=[];
function visit(id,parent){const n=json.nodes[id],m=multiply(parent,localMatrix(n));
 if(n.mesh!==undefined){ledger.push({id,name:n.name||json.meshes[n.mesh]?.name||('mesh_'+id),box:nodeBox(n,m)});}
 for(const child of n.children||[])visit(child,m);
}
for(const rootNode of json.scenes[json.scene||0].nodes)visit(rootNode,identity());
const fmt=(v)=>v.map(n=>+n.toFixed(2));
const print=(tag,query,limit=30)=>{
 const items=ledger.filter(o=>query.test(o.name));
 console.log('##',tag,'count',items.length);
 for(const item of items.slice(0,limit))console.log(JSON.stringify({id:item.id,name:item.name,min:fmt(item.box.min),max:fmt(item.box.max)}));
};
console.log('GLB mesh nodes:',ledger.length,'JSON nodes:',json.nodes.length,'Model bytes:',bin.length);
print('South entrance / doors',/door|entrance|south.*lintel|south entry/i,45);
print('Courtyard entrances',/courtyard.*glass|court.*glass|sliding|chapel west/i,45);
print('Roof / ceiling',/roof|ceiling/i,18);
print('Cross',/cross/i,12);
console.log('## Route point solid intersection audit');
const samples=[
 ['south arrival',[9,1.76,3.15]],
 ['south doorway',[9,1.76,.23]],
 ['foyer',[9,1.76,-2.15]],
 ['south glass',[9,1.76,-6]],
 ['courtyard',[9,1.81,-8.9]],
 ['east glass',[12,1.81,-9.1]],
 ['sanctuary',[15.4,1.8,-10.7]],
 ['west forum',[5.9,1.82,-11.7]]
];
for (const [name,p] of samples){
 const collisions=ledger.filter(a=>a.box && /wall|glass|door|partition|column|support|screen|cross|roof|slab/i.test(a.name) &&
 p.every((v,j)=>v>=a.box.min[j]-.16&&v<=a.box.max[j]+.16)).map(a=>a.name);
 console.log(JSON.stringify({name,point:p,collisions:collisions.slice(0,12),count:collisions.length}));
}

console.log('## CC0 maple material and hierarchy audit');
for(let id=0;id<json.nodes.length;id++){
 const n=json.nodes[id];
 const name=n.name||'';
 if(/maple|leaves|foliage|trunk|branch|tree|twig|stem|bark/i.test(name)){
 const m=n.mesh===undefined?null:json.meshes[n.mesh];
 console.log(JSON.stringify({id,name,children:n.children?.length||0,mesh:n.mesh,
 mats:m?.primitives?.map(p=>({material:p.material,name:json.materials?.[p.material]?.name,base:json.materials?.[p.material]?.pbrMetallicRoughness?.baseColorFactor}))}));
 }
}
console.log('## Relevant route geometry for west/south interior, terraces and upper floors');
for(const item of ledger.filter(x=>/V19 INDOOR|V19 NORTH|V05|V26 ROUTE|STAIR|terrace|landing|cafe|forum|SOUTH-TO-WEST|south foyer|WEST MID/i.test(x.name)).slice(0,115)){
 console.log(JSON.stringify({name:item.name,min:fmt(item.box.min),max:fmt(item.box.max)}));
}

console.log('## R30 upper-gallery floor support survey (north side, y=3.3..5.1)');
for(const item of ledger.filter(o=>o.box && o.box.max[0]>5.3 && o.box.min[0]<12.1 &&
    o.box.max[2]>-18.1 && o.box.min[2]<-11.5 &&
    o.box.max[1]>=3.3 && o.box.min[1]<=5.1)){
 console.log(JSON.stringify({name:item.name,min:fmt(item.box.min),max:fmt(item.box.max)}));
}
