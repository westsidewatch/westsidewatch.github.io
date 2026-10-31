// Shared metre budgets for paired precinct construction. Relative layouts are
// interpretive: literary dimensions do not establish surveyed coordinates.
export function herodianRitualLayout(c=.525){
 const court=187*c,women=135*c;
 return {court,women,westMargin:11*c,sanctuary:100*c,porchAltarGap:22*c,
  altar:{size:32*c,centreFromWest:(11+100+22+16)*c,height:10*c},
  ramp:{width:16*c,length:32*c,altarJoinOffset:14*c},womenRoom:{size:40*c,height:3,wall:.5,inset:2},
  dimensionClosure:(11+100+22+32+11+11)*c,
  geometryVerified:false};
}
export function firstTempleWaterLayout(c=.45){
 return {sea:{diameter:10*c,height:5*c,eastFromBodyEnd:18,southFromAxis:8},
  stands:{count:10,size:4*c,height:3*c,sideOffset:8,eastOffsets:[-10,-5,0,5,10]},
  geometryVerified:false,placement:'authored-relative-zones-not-survey',
  supports:'schematic-pedestal-not-twelve-oxen-reconstruction'};
}
