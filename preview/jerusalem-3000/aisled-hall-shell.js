// Shared engineering shell. Aisle/height budgets supplied independently by each period core.
// Door counts, column grid and clerestory profiles are authored, not excavated plans.
export function appendAisledHall({append,THREE},{cx,cz,length,widths,heights,axis,rearOpen=[],frontEnd=-1}){
 const total=widths.reduce((a,b)=>a+b,0),wall=.6,roof=.25;
 const emit=(u,v,along,across,h,bottom=0)=>append(new THREE.BoxGeometry(axis==='x'?along:across,h,axis==='x'?across:along),axis==='x'?cx+u:cx+v,axis==='x'?cz+v:cz+u,bottom+h/2);
 emit(0,0,length,total,.12);
 let cursor=-total/2;
 for(let i=0;i<widths.length;i++){
  const width=widths[i],height=heights[i],mid=cursor+width/2,door=Math.min(3,width*.5),doorH=4;
  emit(0,mid,length,width,roof,height-roof);
  for(const end of[-1,1]){
   const u=end*(length-wall)/2;
   if(end===frontEnd||rearOpen.includes(i)){
    for(const side of[-1,1])emit(u,mid+side*(door/2+(width-door)/4),wall,(width-door)/2,height-roof-.12,.12);
    emit(u,mid,wall,door,height-roof-doorH,doorH);
   }else emit(u,mid,wall,width,height-roof-.12,.12);
  }
  if(i===0||i===widths.length-1)emit(0,cursor+(i===0?wall/2:width-wall/2),length-2*wall,wall,height-roof-.12,.12);
  if(i<widths.length-1){
   const boundary=cursor+width,low=Math.min(height,heights[i+1]),high=Math.max(height,heights[i+1]),n=Math.ceil((length-2)/8);
   emit(0,boundary,length-2*wall,.5,.4,low-roof-.4);
   for(let k=0;k<=n;k++){
    const u=-length/2+1+(length-2)*k/n;emit(u,boundary,.45,.45,low-roof-.52,.12);

   }
   if(high>low){
    const span=length-2*wall,gap=high-low-roof,wh=Math.min(1.8,gap*.6),sill=low+(gap-wh)/2,ww=1.3,windows=Math.ceil(span/8);
    emit(0,boundary,span,.45,sill-low,low);emit(0,boundary,span,.45,high-roof-sill-wh,sill+wh);
    let edge=-span/2;for(let k=0;k<windows;k++){const u=-span/2+(k+.5)*span/windows;emit((edge+u-ww/2)/2,boundary,u-ww/2-edge,.45,wh,sill);edge=u+ww/2;}emit((edge+span/2)/2,boundary,span/2-edge,.45,wh,sill);
   }
  }
  cursor+=width;
 }
}
export function appendHalfApse({append,THREE},{x,z,radius,height}){
 const t=.5,n=24,vertices=[],tri=(a,b,c)=>vertices.push(...a,...b,...c),quad=(a,b,c,d)=>{tri(a,b,c);tri(c,b,d);tri(c,b,a);tri(d,b,c);},point=(r,a,y)=>[x+r*Math.cos(a),y,z+r*Math.sin(a)];
 for(let i=0;i<n;i++){
  const a=-Math.PI/2+i*Math.PI/n,b=a+Math.PI/n;
  quad(point(radius,a,0),point(radius,a,height),point(radius,b,0),point(radius,b,height));
  quad(point(radius-t,a,0),point(radius-t,a,height),point(radius-t,b,0),point(radius-t,b,height));
  tri([x,height,z],point(radius,b,height),point(radius,a,height));tri([x,0,z],point(radius,b,0),point(radius,a,0));
 }
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.computeVertexNormals();append(g,0,0);
}
