import * as THREE from 'three';
// Presentation only: never change DEM positions, datum, sampling or vertical scale.
export function createTerrainPresentation(mesh,{datum=0,interval=20}={}){
 if(!(interval>0)||!Number.isFinite(datum))throw new Error('Invalid terrain presentation settings');
 const geometry=mesh.geometry,p=geometry.attributes.position,index=geometry.index;
 if(!p||!index)throw new Error('Indexed DEM mesh required');
 let min=Infinity,max=-Infinity;for(let i=0;i<p.count;i++){min=Math.min(min,p.getY(i));max=Math.max(max,p.getY(i));}
 // Elevation tint alone was washed out by the material tint and broad lighting.
 // Bake directional relief into vertex colours; geometry and ground authority stay exact.
 const normals=geometry.attributes.normal,sun=new THREE.Vector3(-.8,.55,.35).normalize();
 const colors=new Float32Array(p.count*3),low=new THREE.Color(0x536c5d),high=new THREE.Color(0xdfcba3),color=new THREE.Color();
 let shadeMin=1,shadeMax=0;
 for(let i=0;i<p.count;i++){
  const illumination=Math.max(0,normals.getX(i)*sun.x+normals.getY(i)*sun.y+normals.getZ(i)*sun.z),shade=.30+.70*illumination;
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
 const material=new THREE.LineBasicMaterial({color:0x534f3c,transparent:true,opacity:.28,depthWrite:false});
 const contours=new THREE.LineSegments(lineGeometry,material);contours.name='modern-dem-20m-contours';contours.visible=true;mesh.add(contours);
 return {contours,diagnostics:{verticalScale:1,hillshade:true,reliefLighting:'baked-directional-without-double-scene-lighting',nominalPaletteMetres:[630,840],hillshadeRange:[shadeMin,shadeMax],contoursDefaultVisible:true,contourIntervalMetres:interval,contourSegments:lines.length/6,elevationRangeMetres:[min+datum,max+datum],authority:'modern-dem-not-ancient-surface'},
  dispose(){contours.removeFromParent();lineGeometry.dispose();material.dispose();if(previousColor)geometry.setAttribute('color',previousColor);else geometry.deleteAttribute('color');mesh.material=previousMaterial;reliefMaterial.dispose();}};
}
