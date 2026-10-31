// Middot4:3–7 nominal cubit plan, not a surveyed position or unique reconstruction.
export function herodianSanctuaryPlan(c=.525){
 const segments=[['rear-wall',5],['rear-cell',6],['sanctuary-west-wall',6],['holy-of-holies',20],['partition',1],['holy-place',40],['entry-wall',6],['porch',11],['facade-wall',5]];
 let x=0;const longitudinal=segments.map(([id,length])=>{const item={id,start:x*c,length:length*c};x+=length;return item;});
 return {cubit:c,longitudinal,length:x*c,coreHalfWidth:16*c,outerHalfWidth:35*c,frontHalfWidth:50*c,
  chamberStorey:6*c,chamberStoreyAuthority:'authored-height-not-specified-by-Middot4:3',geometryVerified:false};
}
export function buildHerodianSanctuary({builder,west,y,z,c,surface,emit}){
 const plan=herodianSanctuaryPlan(c),b=(size,p,phase='superstructure',shade=1)=>emit(builder,size,p,surface,phase,shade);
 const at=(x,h,zz=0)=>[west+x*c,y+h*c,z+zz*c];
 const cub=(sx,sy,sz,x,yy,zz=0,phase='superstructure',shade=1)=>b([sx*c,sy*c,sz*c],at(x,yy,zz),phase,shade);
 // Existing100×100cubit podium and roof envelope; narrow core, low side rooms.
 cub(100,6,100,50,3,0,'foundation',.98);
 // Holy Place/Most Holy are real volumes, not a solid body or black door panel.
 for(const side of[-1,1]){
  cub(73,40,6,47.5,26,side*13);
  cub(73,40,6,47.5,71,side*13);
 }
 cub(6,85,32,14,48.5);
 // Central partition: plain opening is an interpretive representation of the boundary.
 for(const side of[-1,1])cub(1,40,8,37.5,26,side*6);
 cub(1,20,4,37.5,36);
 //10×20cubit main door through the6cubit front wall.
 for(const side of[-1,1])cub(6,40,11,81,26,side*10.5);
 cub(6,20,10,81,36);
 // Four main-door leaves in an authored open pose; the outer porch stays doorless.
 for(const xx of[75.5,86.5])for(const side of[-1,1])cub(5,20,.15,xx,16,side*4.925,'superstructure',.9);
 cub(73,5,32,47.5,48.5,0,'roof',.94);
 cub(73,5,32,47.5,93.5,0,'roof',.97);
 // Roof parapets enclose a recessed upper roof; total stays100cubits.
 for(const side of[-1,1])cub(73,3,1,47.5,97.5,side*15.5,'roof',1);
 for(const x of[11.5,83.5])cub(1,3,30,x,97.5,0,'roof',1);
 // Spike count/profile is schematic, not an asserted ancient count.
 for(const x of[12,26,40,54,68,83])for(const side of[-1,1])cub(.3,1,.3,x,99.5,side*15.5,'roof',.95);
 // Front porch has100cubit width,11cubit clear depth and5cubit facade wall.
 // Wings are hollow service envelopes rather than full-height solid jamb blocks.
 for(const side of[-1,1]){
  cub(16,94,2,92,53,side*49);
  cub(2,94,34,85,53,side*33);
  cub(5,94,40,97.5,53,side*30);
 }
 cub(11,1,100,89.5,99.5,0,'roof',1);
 cub(5,54,20,97.5,73);
 // Five progressively longer beams above the20×40cubit porch aperture (Middot3:7).
 for(let i=0;i<5;i++)cub(.7,.5,22+2*i,100-.35,46.25+i,0,'roof',.9);
 //38 actual side/rear cell envelopes:15north,15south,8west.
 for(let tier=0;tier<3;tier++){
  const floor=6+tier*6,inner=17-tier,outer=22,roomWidth=outer-inner;
  for(const side of[-1,1])cub(84,.3,3,42,floor+.15,side*28.5,'foundation',.94);
  for(const side of[-1,1])for(let i=0;i<5;i++){
   const span=73/5,cx=11+(i+.5)*span,zc=side*(inner+roomWidth/2);
   cub(span,.3,roomWidth,cx,floor+.15,zc,'foundation',.94);
   cub(span,.3,roomWidth+5,cx,floor+5.85,side*(inner+(roomWidth+5)/2),'roof',.95);
   for(const end of[-1,1])cub(.4,5.7,roomWidth,cx+end*(span-.4)/2,floor+3.15,zc);
   // Door from each room towards the outside service band.
   for(const end of[-1,1])cub((span-2)/2,5.7,5,cx+end*(2/2+(span-2)/4),floor+3.15,side*24.5);
   cub(2,2.7,5,cx,floor+4.65,side*24.5);
  }
  const n=tier===2?2:3,span=32/n;
  for(let i=0;i<n;i++){
   const zz=-16+(i+.5)*span;
   cub(6,.3,span,8,floor+.15,zz,'foundation',.94);
   cub(11,.3,span,5.5,floor+5.85,zz,'roof',.95);
   for(const end of[-1,1])cub(6,5.7,.4,8,floor+3.15,zz+end*(span-.4)/2);
   for(const end of[-1,1])cub(5,5.7,(span-2)/2,2.5,floor+3.15,zz+end*(1+(span-2)/4));
   cub(5,2.7,2,2.5,floor+4.65,zz);
  }
 }
 // Outer service bands/water-descent envelopes at the70cubit body boundary.
 for(const side of[-1,1]){
  cub(84,18,5,42,15,side*32.5);
  cub(84,.4,8,42,24.2,side*31,'roof',.92);
 }
 return plan;
}
