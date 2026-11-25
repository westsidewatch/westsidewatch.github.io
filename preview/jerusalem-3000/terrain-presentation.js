import * as THREE from 'three';
// Average positive horizon angles in eight directions. This is display shading,
// not erosion, vegetation, water, or a reconstruction of an ancient surface.
export function terrainHorizonOcclusion(geometry,{radii=[90,180,360]}={}){
 const p=geometry.attributes.position,w=geometry.parameters?.widthSegments+1,h=geometry.parameters?.heightSegments+1;
 const result=new Float32Array(p.count);
 if(!Number.isInteger(w)||!Number.isInteger(h)||w*h!==p.count)return result;
 const dx=Math.abs(p.getX(1)-p.getX(0)),dz=Math.abs(p.getZ(w)-p.getZ(0));
 if(!(dx>0&&dz>0))return result;
 for(let row=0;row<h;row++)for(let col=0;col<w;col++){
  const i=row*w+col;let sum=0,directions=0;
  for(const [ux,uz]of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]){
   let horizon=0,available=false;
   for(const radius of radii){
    const norm=Math.hypot(ux,uz),x=col+Math.round(ux*radius/(norm*dx)),z=row+Math.round(uz*radius/(norm*dz));
    if(x<0||z<0||x>=w||z>=h)continue;
    const j=z*w+x,distance=Math.hypot(p.getX(j)-p.getX(i),p.getZ(j)-p.getZ(i));if(!distance)continue;
    available=true;horizon=Math.max(horizon,Math.atan2(p.getY(j)-p.getY(i),distance));
   }
   if(available){sum+=horizon;directions++;}
  }
  result[i]=directions?Math.min(1,sum/directions/(Math.PI/4)):0;
 }
 return result;
}
// Presentation only: never change DEM positions, datum, sampling or vertical scale.
export function createTerrainPresentation(mesh,{datum=0,interval=20}={}){
 if(!(interval>0)||!Number.isFinite(datum))throw new Error('Invalid terrain presentation settings');
 const geometry=mesh.geometry,p=geometry.attributes.position,index=geometry.index;
 if(!p||!index)throw new Error('Indexed DEM mesh required');
 let min=Infinity,max=-Infinity;for(let i=0;i<p.count;i++){min=Math.min(min,p.getY(i));max=Math.max(max,p.getY(i));}
 // Elevation tint alone was washed out by the material tint and broad lighting.
 // Bake directional relief into vertex colours; geometry and ground authority stay exact.
 const normals=geometry.attributes.normal,sun=new THREE.Vector3(-.8,.55,.35).normalize();
 const colors=new Float32Array(p.count*3),low=new THREE.Color(0x77756a),high=new THREE.Color(0xbdb6a2),color=new THREE.Color();
 const horizon=terrainHorizonOcclusion(geometry);
 let shadeMin=1,shadeMax=0,occlusionMax=0;
 for(let i=0;i<p.count;i++){
  const illumination=Math.max(0,normals.getX(i)*sun.x+normals.getY(i)*sun.y+normals.getZ(i)*sun.z),shade=(.48+.52*illumination)*(1-.55*horizon[i]);
  occlusionMax=Math.max(occlusionMax,horizon[i]);
  shadeMin=Math.min(shadeMin,shade);shadeMax=Math.max(shadeMax,shade);
  color.copy(low).lerp(high,THREE.MathUtils.clamp((p.getY(i)+datum-630)/210,0,1)).multiplyScalar(shade);color.toArray(colors,i*3);
 }
 const previousColor=geometry.getAttribute('color'),previousMaterial=mesh.material;
 const reliefMaterial=new THREE.MeshBasicMaterial({color:0xffffff,vertexColors:true});mesh.material=reliefMaterial;
 geometry.setAttribute('color',new THREE.BufferAttribute(colors,3));mesh.material.color.setHex(0xffffff);mesh.material.needsUpdate=true;
 const lines=[];
 for(let i=0;i<index.count;i+=3){
  const ids=[index.getX(i),index.getX(i+1),index.getX(i+2)],ys=ids.map(j=>p.getY(j));
  for(let elevation=Math.ceil((Math.min(...ys)+datum)/interval)*interval;elevation<Math.max(...ys)+datum;elevation+=interval){
   const level=elevation-datum,hits=[];
   for(let e=0;e<3;e++){
    const a=ids[e],b=ids[(e+1)%3],ya=p.getY(a),yb=p.getY(b);
    if((ya<=level&&yb>level)||(yb<=level&&ya>level)){
     const t=(level-ya)/(yb-ya);hits.push([p.getX(a)+(p.getX(b)-p.getX(a))*t,level+.35,p.getZ(a)+(p.getZ(b)-p.getZ(a))*t]);
    }
   }
   if(hits.length===2)lines.push(...hits[0],...hits[1]);
  }
 }
 const lineGeometry=new THREE.BufferGeometry();lineGeometry.setAttribute('position',new THREE.Float32BufferAttribute(lines,3));
 const material=new THREE.LineBasicMaterial({color:0x534f3c,transparent:true,opacity:.13,depthWrite:false});
 const contours=new THREE.LineSegments(lineGeometry,material);contours.name='modern-dem-20m-contours';contours.visible=true;mesh.add(contours);
 return {contours,diagnostics:{verticalScale:1,hillshade:true,reliefLighting:'baked-directional-without-double-scene-lighting',palette:"muted-earth-separated-from-building-stone-no-water-encoding",horizonOcclusion:{directions:8,radiiMetres:[90,180,360],strength:.55,max:occlusionMax,computedOnce:true},nominalPaletteMetres:[630,840],hillshadeRange:[shadeMin,shadeMax],contoursDefaultVisible:true,contourIntervalMetres:interval,contourSegments:lines.length/6,elevationRangeMetres:[min+datum,max+datum],authority:'modern-dem-not-ancient-surface'},
  dispose(){contours.removeFromParent();lineGeometry.dispose();material.dispose();if(previousColor)geometry.setAttribute('color',previousColor);else geometry.deleteAttribute('color');mesh.material=previousMaterial;reliefMaterial.dispose();}};
}
