import * as THREE from 'three';
import {geographicToENU} from './terrain-runtime.js';
import {createSharedPlaceView} from './shared-place-view.js';
export function compileRegionalLandforms(data,terrain){
 if(data.schema!=='j3k.regional-landforms.v1'||data.origin.lat!==terrain.grid.origin.lat||data.origin.lon!==terrain.grid.origin.lon)throw new Error('Regional landform origin mismatch');
 const point=p=>{const enu=geographicToENU(p.lat,p.lon,data.origin),x=enu.east,z=-enu.north,y=terrain.heightAtWorld(x,z);if(!Number.isFinite(y))throw new Error('Landform outside canonical DEM');return{x,y,z,elevation:y+terrain.grid.verticalDatumOffsetMetres};};
 const anchors=data.anchors.map(a=>({...a,...point(a),label:a.label,semanticCityObject:false,ancientGroundVerified:false}));
 const traces=data.traces.map(t=>({...t,points:t.points.map(point)}));
 const east=anchors.find(a=>a.role==='east-ridge'),kidron=anchors.find(a=>a.role==='intermittent-valley-context'),zion=anchors.find(a=>a.role==='city-hill'),hinnom=anchors.find(a=>a.role==='valley-context');
 return{anchors,traces,window:{...data.window},source:data.attribution,sourceSnapshot:data.sourceSnapshot,limitations:[...data.limitations],verticalScale:1,modernSurface:true,ancientGroundVerified:false,comparisons:{olivesAboveKidron:east.y-kidron.y,zionAboveHinnom:zion.y-hinnom.y}};
}
export function createRegionalLandforms(parent,mount,data,terrain){
 const model=compileRegionalLandforms(data,terrain),group=new THREE.Group();group.name='modern-regional-landform-references';group.visible=false;parent.add(group);
 const material=new THREE.LineBasicMaterial({color:0x355c56,transparent:true,opacity:.85,depthWrite:false}),geometries=[];
 for(const trace of model.traces){const points=[];for(let i=1;i<trace.points.length;i++){const a=trace.points[i-1],b=trace.points[i],steps=Math.ceil(Math.hypot(b.x-a.x,b.z-a.z)/8);for(let j=i===1?0:1;j<=steps;j++){const t=j/steps,x=a.x+(b.x-a.x)*t,z=a.z+(b.z-a.z)*t;points.push(new THREE.Vector3(x,terrain.heightAtWorld(x,z)+.7,z));}}const geometry=new THREE.BufferGeometry().setFromPoints(points);geometries.push(geometry);const line=new THREE.Line(geometry,material);line.name=`modern-map-valley-context:${trace.id}`;group.add(line);}
 const priority=['east-ridge','intermittent-valley-context','valley-context','north-ridge-context','city-hill','southwest-hill'];
 const view=createSharedPlaceView(mount,{anchors:()=>[...model.anchors].sort((a,b)=>priority.indexOf(a.role)-priority.indexOf(b.role)).map(a=>({...a,label:a.label,description:`${a.description?`${a.description} `:''}現代 GLO-30 地表取樣約${Math.round(a.elevation)}m；不是峰頂測量或古代高程。`}))},{credit:false});
 mount.lastElementChild.classList.add('j3k-landform-references');let enabled=false;
 return{setVisible(v){enabled=!!v;group.visible=enabled;view.setVisible(enabled);},project:(camera,occupied=[])=>view.project(camera,occupied),diagnostics:()=>({enabled,anchorIds:model.anchors.map(a=>a.id),terrainSurfaceId:terrain.mesh.uuid,verticalScale:1,ancientGroundVerified:false}),snapshot:()=>({...structuredClone(model),enabled,terrainSurfaceId:terrain.mesh.uuid,semanticCityObjects:false}),dispose(){view.dispose();for(const g of geometries)g.dispose();material.dispose();group.removeFromParent();}};
}
