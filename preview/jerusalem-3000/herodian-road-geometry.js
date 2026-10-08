import * as THREE from 'three';
// The road linework is the same provisional registration used to subdivide blocks.
export function buildHerodianRoadGeometry(group,roads,materials,terrain){
  const meshes=[];
  for(const road of roads){
    const points=road.geometry?.points||[];
    for(let i=0;i<points.length-1;i++){
      const a=points[i],b=points[i+1],dx=b.x-a.x,dz=b.z-a.z,length=Math.hypot(dx,dz);
      const steps=Math.ceil(length/12);
      for(let j=0;j<steps;j++){
        const t0=j/steps,t1=(j+1)/steps,x0=a.x+dx*t0,z0=a.z+dz*t0,x1=a.x+dx*t1,z1=a.z+dz*t1;
        const y0=terrain.heightAtWorld(x0,z0)+.35,y1=terrain.heightAtWorld(x1,z1)+.35;
        const nx=-dz/length*2.5,nz=dx/length*2.5;
        const geometry=new THREE.BufferGeometry();
        geometry.setAttribute('position',new THREE.Float32BufferAttribute([x0+nx,y0,z0+nz,x0-nx,y0,z0-nz,x1+nx,y1,z1+nz,x1-nx,y1,z1-nz],3));
        geometry.setIndex([0,2,1,1,2,3]);geometry.computeVertexNormals();
        const mesh=new THREE.Mesh(geometry,materials[road.confidence]||materials.inferred);
        mesh.receiveShadow=true;
        mesh.userData.cityObject={objectId:road.id,confidence:road.confidence,infrastructure:true,terrainGround:(y0+y1)/2};
        group.add(mesh);meshes.push(mesh);
      }
    }
  }
  return meshes;
}
