import {subtractPlanarZones,clipBlockToEnvelope} from './district-infill.js';
import {terrainRibbonTop} from './terrain-ribbon-top.js';
import * as THREE from 'three';
// The road linework is the same provisional registration used to subdivide blocks.
export function buildHerodianRoadGeometry(group,roads,materials,terrain,{exclusions=[],envelope=null}={}){
  const meshes=[];
  for(const road of roads){
    const points=road.geometry?.points||[];
    for(let i=0;i<points.length-1;i++){
      const a=points[i],b=points[i+1],dx=b.x-a.x,dz=b.z-a.z,length=Math.hypot(dx,dz);
      const steps=Math.ceil(length/12);
      for(let j=0;j<steps;j++){
        const t0=j/steps,t1=(j+1)/steps,x0=a.x+dx*t0,z0=a.z+dz*t0,x1=a.x+dx*t1,z1=a.z+dz*t1;
        const y0=terrain.heightAtWorld(x0,z0)+.35,y1=terrain.heightAtWorld(x1,z1)+.35;
        const halfWidth=(road.geometry.widthMetres??5)/2;if(!(halfWidth>0&&halfWidth<=10))throw new Error('Invalid road width');const nx=-dz/length*halfWidth,nz=dx/length*halfWidth;
        const polygon=[{x:x0+nx,z:z0+nz},{x:x1+nx,z:z1+nz},{x:x1-nx,z:z1-nz},{x:x0-nx,z:z0-nz}];
        // Clip the actual paving at courts/circuits, rather than dropping a
        // whole12m cell merely because one corner crosses a boundary.
        let pieces=envelope?clipBlockToEnvelope(polygon,envelope,{minArea:.001}):[polygon];
        if(exclusions.length)pieces=subtractPlanarZones(pieces,exclusions.map(z=>z.polygon));
        if(!pieces.length)continue;
        const vertices=[];
        for(const piece of pieces){
          if(terrain.mesh&&terrain.grid)vertices.push(...terrainRibbonTop(piece.map(p=>[p.x,p.z]),terrain,{x:0,z:0},(x,z)=>terrain.heightAtWorld(x,z)+.35));
          else for(let k=1;k<piece.length-1;k++){
            const a=piece[0],b=piece[k],c=piece[k+1],signed=(b.x-a.x)*(c.z-a.z)-(b.z-a.z)*(c.x-a.x);
            for(const p of signed>0?[a,c,b]:[a,b,c])vertices.push(p.x,terrain.heightAtWorld(p.x,p.z)+.35,p.z);
          }
        }
        if(!vertices.length)continue;
        const geometry=new THREE.BufferGeometry();
        geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));geometry.computeVertexNormals();
        geometry.userData.roadSurface={terrainFit:'rendered-dem-triangle-partition',offsetMetres:.35,planWidthMetres:halfWidth*2,exactCourtAndCircuitClipping:true,ancientStreetLevelVerified:false};
        const mesh=new THREE.Mesh(geometry,materials[road.confidence]||materials.inferred);
        mesh.receiveShadow=true;
        mesh.userData.cityObject={objectId:road.id,confidence:road.confidence,infrastructure:true,terrainGround:(y0+y1)/2};
        group.add(mesh);meshes.push(mesh);
      }
    }
  }
  return meshes;
}
