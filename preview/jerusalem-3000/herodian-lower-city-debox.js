import {irregularHouse,ribbon} from './herodian-stone-geometry.js';

export function deboxHerodianLowerCity(group,runtime,materials,terrain){
 if(!runtime?.meshes)return runtime;
 const stone=materials.reconstructed,road=materials.observed||stone;
 const removed=[];
 for(const mesh of [...runtime.meshes]){
  const stage=mesh.userData?.phase2?.stage;
  const {x,z}=mesh.position;
  const lowerCity=stage==='block'&&z>55&&x<190;
  const gridRoad=stage==='road'&&z>15;
  if(lowerCity||gridRoad){group.remove(mesh);mesh.geometry?.dispose?.();removed.push(mesh)}
 }
 runtime.meshes=runtime.meshes.filter(mesh=>!removed.includes(mesh));
 const houses=[];
 for(let i=0;i<20;i++){
  const row=Math.floor(i/5),col=i%5;
  const x=-120+col*58+(row%2?19:-7)+((i*17)%13-6);
  const z=95+row*48+((i*23)%17-8);
  const w=34+(i%4)*7,d=31+(i%3)*8,h=22+(i%5)*6,lift=row*3.2+(col%2)*1.1;
  houses.push(irregularHouse(group,runtime.meshes,stone,terrain,x,z,w,d,h,'lower-city-polygon',.32+i*.009,{lift,variant:i}));
 }
 const lanes=[
  [[-155,82,0],[-92,112,2],[-28,126,4],[38,151,7],[106,166,9]],
  [[-128,205,7],[-73,174,6],[-15,153,5],[49,132,4],[118,108,2]],
  [[-66,72,0],[-55,116,3],[-42,165,6],[-28,220,10]],
  [[58,80,1],[48,121,3],[64,168,6],[86,214,9]]
 ];
 lanes.forEach((points,i)=>ribbon(group,runtime.meshes,road,terrain,points,5.5-(i%2)*.7,'lower-city-lane',.24+i*.025));
 runtime.grammar='herodian-lower-city-polygon-ribbon';
 runtime.deboxed={zone:'lower-city',removedBoxes:removed.length,polygonHouses:houses.length,lanes:lanes.length};
 return runtime;
}
