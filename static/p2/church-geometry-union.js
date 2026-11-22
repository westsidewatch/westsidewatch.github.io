import {B as BufferGeometry,M as Mesh,p as Vector3} from "../p2-maquette/assets/GLTFLoader-j388d5bW.js";

/**
 * R34: consolidate actual intersecting, axis-aligned opaque GLB cuboids.
 * Emit only exposed union faces, never internal overlapped triangles.
 * Preserve the volume, footprints, architectural openings and paint.
 * Original GLB sources remain in the scene graph for rollback, hidden
 * only AFTER a conservative watertight exterior has been verified.
 */
export function consolidateIntersectingOpaqueCuboids(building,{whiteArchitecture,whiteFloor,modelName,meshWorldBox}){
  const audit={sourceBoxCount:0,componentCount:0,mergedSourceCount:0,
    originalOverlappingPairs:0,exteriorQuads:0,physicalUnion:true,
    materialOffsets:false,groups:[]};
  const key=n=>Math.round(n*10000)/10000;
  const movingDoor=name=>/^(?:sanctuary staff door|sanctuary main public door|tall single white pivot door|d south court inner glass vestibule door|c east chapel large sliding glass door|a north court double-wide glass door)\b/i.test(modelName(name));
  function solidBox(mesh){
    if(!mesh.isMesh||!mesh.visible||!mesh.geometry||
      (mesh.material!==whiteArchitecture&&mesh.material!==whiteFloor))return null;
    const name=modelName(mesh.name);
    if(movingDoor(name)||/^v26 (?:route 03|continuous upper stair|upper ascent fitted)/.test(name)
      ||/\broof\b|ghost cutaway|cross|maple|tree|foliage|handle|hardware|mullion|railing|handrail|glass/i.test(name))return null;
    const attr=mesh.geometry.attributes?.position;
    if(!attr||(mesh.geometry.index?.count??attr.count)/3!==12)return null;
    const b=meshWorldBox(mesh);if(!b)return null;
    const lo=[b.min.x,b.min.y,b.min.z],hi=[b.max.x,b.max.y,b.max.z];
    if(lo.some((v,i)=>hi[i]-v<.015))return null;
    const vertex=new Vector3();
    for(let i=0;i<attr.count;i++){
      vertex.set(attr.getX(i),attr.getY(i),attr.getZ(i)).applyMatrix4(mesh.matrixWorld);
      for(let j=0;j<3;j++)if(Math.min(
        Math.abs(vertex.getComponent(j)-lo[j]),
        Math.abs(vertex.getComponent(j)-hi[j]))>.0015)return null;
    }
    return {mesh,lo,hi,material:mesh.material};
  }

  building.updateMatrixWorld(true);
  const solids=[];
  building.traverse(mesh=>{const box=solidBox(mesh);if(box)solids.push(box);});
  audit.sourceBoxCount=solids.length;
  const parent=solids.map((_,i)=>i);
  function root(i){while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i];}return i;}
  const unite=(a,b)=>{const ra=root(a),rb=root(b);if(ra!==rb)parent[rb]=ra;};
  for(let i=0;i<solids.length;i++)for(let j=i+1;j<solids.length;j++){
    const a=solids[i],b=solids[j];
    if(a.material!==b.material)continue;
    const dx=Math.min(a.hi[0],b.hi[0])-Math.max(a.lo[0],b.lo[0]);
    const dy=Math.min(a.hi[1],b.hi[1])-Math.max(a.lo[1],b.lo[1]);
    const dz=Math.min(a.hi[2],b.hi[2])-Math.max(a.lo[2],b.lo[2]);
    if(Math.min(dx,dy,dz)<.001||dx*dy*dz<.00002)continue;
    audit.originalOverlappingPairs++;
    unite(i,j);
  }

  const components=new Map();
  for(let i=0;i<solids.length;i++){
    const id=root(i);
    if(!components.has(id))components.set(id,[]);
    components.get(id).push(solids[i]);
  }
  for(const group of components.values()){
    if(group.length<2)continue;
    const coords=[0,1,2].map(k=>Array.from(new Set(
      group.flatMap(s=>[key(s.lo[k]),key(s.hi[k])]))).sort((a,b)=>a-b));
    const [nx,ny,nz]=coords.map(c=>c.length-1),n=nx*ny*nz;
    if(n<=0||n>180000)throw Error("Architectural boolean grid is invalid: "+n);
    const index=(i,j,k)=>(i*ny+j)*nz+k;
    const occupied=new Uint8Array(n),maps=coords.map(c=>new Map(c.map((v,i)=>[v,i])));
    for(const b of group){
      const low=b.lo.map((v,k)=>maps[k].get(key(v)));
      const high=b.hi.map((v,k)=>maps[k].get(key(v)));
      if(low.some(v=>v===undefined)||high.some(v=>v===undefined))
        throw Error("Architectural boolean coordinate mapping failed");
      for(let x=low[0];x<high[0];x++)
        for(let y=low[1];y<high[1];y++)
          for(let z=low[2];z<high[2];z++)occupied[index(x,y,z)]=1;
    }
    const voxel=(x,y,z)=>x<0||y<0||z<0||x>=nx||y>=ny||z>=nz
      ?0:occupied[index(x,y,z)];
    let filledVolume=0;
    for(let x=0;x<nx;x++)for(let y=0;y<ny;y++)for(let z=0;z<nz;z++)
      if(occupied[index(x,y,z)])filledVolume+=
        (coords[0][x+1]-coords[0][x])*
        (coords[1][y+1]-coords[1][y])*
        (coords[2][z+1]-coords[2][z]);
    const positions=[];let quads=0;
    const emit=(axis,p,u0,u1,v0,v1,sign)=>{
      const point=(u,v)=>axis===0?[p,u,v]:axis===1?[u,p,v]:[u,v,p];
      const corners=[point(u0,v0),point(u1,v0),point(u1,v1),point(u0,v1)];
      const outward=(axis===1?-1:1)*sign;
      const triangles=outward>0?[0,1,2,0,2,3]:[0,2,1,0,3,2];
      for(const i of triangles){
        const vertex=building.worldToLocal(new Vector3(...corners[i]));
        positions.push(vertex.x,vertex.y,vertex.z);
      }
      quads++;
    };
    for(let axis=0;axis<3;axis++){
      const [ua,va]=[0,1,2].filter(k=>k!==axis);
      const U=coords[ua].length-1,V=coords[va].length-1,N=coords[axis].length-1;
      for(let p=0;p<=N;p++){
        const face=new Int8Array(U*V);
        const side=(plane,u,v)=>{
          const q=[0,0,0];q[axis]=plane;q[ua]=u;q[va]=v;
          return voxel(q[0],q[1],q[2]);
        };
        for(let u=0;u<U;u++)for(let v=0;v<V;v++){
          const behind=side(p-1,u,v),ahead=side(p,u,v);
          if(behind!==ahead)face[u*V+v]=behind?1:-1;
        }
        for(let u=0;u<U;u++)for(let v=0;v<V;v++){
          const sign=face[u*V+v];if(!sign)continue;
          let width=1,height=1;
          while(v+width<V&&face[u*V+v+width]===sign)width++;
          scan:while(u+height<U){
            for(let k=0;k<width;k++)if(face[(u+height)*V+v+k]!==sign)break scan;
            height++;
          }
          for(let du=0;du<height;du++)for(let dv=0;dv<width;dv++)
            face[(u+du)*V+v+dv]=0;
          emit(axis,coords[axis][p],coords[ua][u],coords[ua][u+height],
            coords[va][v],coords[va][v+width],sign);
        }
      }
    }
    if(positions.length<36)throw Error("Architectural union generated empty shell");
    let surfaceVolume=0;
    for(let i=0;i<positions.length;i+=9){
      const ax=positions[i],ay=positions[i+1],az=positions[i+2],
        bx=positions[i+3],by=positions[i+4],bz=positions[i+5],
        cx=positions[i+6],cy=positions[i+7],cz=positions[i+8];
      surfaceVolume+=(ax*(by*cz-bz*cy)+ay*(bz*cx-bx*cz)+az*(bx*cy-by*cx))/6;
    }
    if(Math.abs(surfaceVolume-filledVolume)>Math.max(.0005,filledVolume*.0001))
      throw Error("Architectural volume changed during union: "+
        surfaceVolume.toFixed(4)+" vs "+filledVolume.toFixed(4));
    const geometry=new BufferGeometry();
    const Attr=group[0].mesh.geometry.attributes.position.constructor;
    geometry.setAttribute("position",new Attr(new Float32Array(positions),3));
    geometry.computeVertexNormals();
    geometry.computeBoundingBox();
    geometry.computeBoundingSphere();
    const combined=new Mesh(geometry,group[0].material);
    combined.name="P2 physically unified wall floor shell "+audit.componentCount;
    combined.castShadow=true;
    combined.receiveShadow=true;
    building.add(combined);
    for(const s of group){
      s.mesh.visible=false;
      s.mesh.castShadow=false;
      s.mesh.userData.physicalUnionSource=true;
    }
    audit.componentCount++;
    audit.mergedSourceCount+=group.length;
    audit.exteriorQuads+=quads;
    audit.groups.push({sources:group.length,quads,volume:+filledVolume.toFixed(3),
      names:group.map(s=>s.mesh.name)});
  }
  return audit;
}
