// Literary budgets and explicit uncertain display positions; never excavated footprints.
export function royalPrecinctHallLayouts(data){
 const c=data.royalCity.temple.cubitMetres;
 return data.royalCity.precinctHalls.map(h=>({...h,length:h.lengthCubits*c,width:h.widthCubits*c,height:h.heightCubits?h.heightCubits*c:h.authoredHeightMetres}));
}
export function buildRoyalPrecinctHalls(data,{emit,datum,stone,timber}){
 for(const hall of royalPrecinctHallLayouts(data)){
  const [x,z]=hall.offset,L=hall.length,W=hall.width,H=hall.height,ground=datum([x-L/2,z-W/2,x+L/2,z+W/2]);
  const part=(suffix,px,pz,w,d,h,material,lift=0)=>{const mesh=emit(`precinct-${hall.id}-${suffix}`,px,pz,w,d,h,material,lift,ground);mesh.userData.cityObject.reservationCluster=`j3k:royal-context:${hall.id}`;mesh.userData.cityObject.landmarkProgrammeId=hall.id;return mesh;};
  const floor=part('floor',x,z,L,W,.2,stone);floor.userData.cityObject.role='walkable-floor';
  const roof=part('roof',x,z,L,W,.3,timber,H-.3);
  if(hall.id==='lebanon-house'){roof.userData.landmarkFocus={x:0,y:.15,z:0};roof.userData.landmarkRepresentation={label:'所羅門王室建築群：利巴嫩林宮／柱子廊（位置推定）'};}
  for(let row=0;row<hall.rows;row++){
   const zz=z-W/2+.8+row*(W-1.6)/(hall.rows-1);
   part(`beam-${row}`,x,zz,L,.6,.4,timber,H-.7);
   for(let i=0;i<hall.columnsPerRow;i++){
    const xx=x-L/2+.8+i*(L-1.6)/(hall.columnsPerRow-1);
    part(`column-${row}-${i}`,xx,zz,.5,.5,H-.9,timber,.2);
   }
  }
 }
}
