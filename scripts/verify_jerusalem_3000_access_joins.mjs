import assert from 'node:assert/strict';import * as THREE from 'three';
import {accessRibbonSections,ribbonFraction} from '../preview/jerusalem-3000/access-ribbon-plan.js';
import {sanctuaryAccessVertices} from '../preview/jerusalem-3000/sanctuary-access-geometry.js';
const points=[[0,0],[20,0],[20,20]],width=4,sections=accessRibbonSections(points,width);
assert.deepEqual(points,[[0,0],[20,0],[20,20]],'engineering join must retain centreline and metre dimensions');
assert.deepEqual(sections[1],{left:[18,2],right:[22,-2]});
const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(sanctuaryAccessVertices(points,width,()=>0,()=>.16),3));g.computeVertexNormals();const mesh=new THREE.Mesh(g,new THREE.MeshBasicMaterial()),topTriangles=[],p=g.attributes.position;
for(let i=0;i<p.count;i+=3){const a=new THREE.Vector3().fromBufferAttribute(p,i),b=new THREE.Vector3().fromBufferAttribute(p,i+1),c=new THREE.Vector3().fromBufferAttribute(p,i+2);if(new THREE.Vector3().subVectors(b,a).cross(new THREE.Vector3().subVectors(c,a)).y>1e-8)topTriangles.push([a,b,c]);}
// The legacy independent rectangles overlap at the inside of this bend and
// omit the outer corner. Dense actual-ray coverage rejects both defects.
let samples=0;
for(let x=.137;x<22;x+=.317)for(let z=-1.853;z<20;z+=.329){
 const inside=x>0&&x<22&&z> -2&&z<20&&(x>18||z<2);
 const hits=new THREE.Raycaster(new THREE.Vector3(x,2,z),new THREE.Vector3(0,-1,0)).intersectObject(mesh);
 assert.equal(hits.length,inside?1:0,`bend paving must cover once, ${x},${z}`);samples++;
}
for(const side of['left','right']){
 const q=sections[1][side];assert.ok(Math.abs(ribbonFraction(...q,sections[0].left,sections[1].left,sections[0].right,sections[1].right)-1)<1e-8);assert.ok(ribbonFraction(...q,sections[1].left,sections[2].left,sections[1].right,sections[2].right)<1e-8);
}
assert.throws(()=>accessRibbonSections([[0,0],[20,0],[0,0]],4),/landing/,'a hairpin cannot silently fold into a fake walkable route');
assert.throws(()=>accessRibbonSections([[0,0],[0,0]],4),/Zero-length/);
assert.throws(()=>accessRibbonSections([[0,0],[1,0],[1,1]],4),/landing/,'close bends must not invert a paving strip');
for(let i=1;i<sections.length;i++)for(const f of[0,.2,.6,1])for(const s of[0,.3,.8,1]){const a=sections[i-1].left,b=sections[i].left,c=sections[i-1].right,d=sections[i].right,q=[0,1].map(k=>(1-f)*(1-s)*a[k]+f*(1-s)*b[k]+(1-f)*s*c[k]+f*s*d[k]);assert.ok(Math.abs(ribbonFraction(...q,a,b,c,d)-f)<1e-8,'sloped endpoint height parameter must survive the bend');}
g.dispose();mesh.material.dispose();console.log(JSON.stringify({ok:true,samples,topTriangles:topTriangles.length,originalCentrelinePreserved:true,historicalGeometryAccepted:false}));
