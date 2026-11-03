// Authored opening/parapet profiles within existing metre envelopes, not surveyed facades.
export function towerShellParts(width,height){
 const parts=[],top=height-1,t=1.2,slab=.2,sill=height*.58,windowH=1.4,opening=.7,positions=[-width*.25,0,width*.25];
 const add=(id,x,y,z,w,h,d)=>parts.push({id,x,y,z,w,h,d});
 add('floor',0,slab/2,0,width,slab,width);
 for(const axis of['x','z'])for(const side of[-1,1]){
  const wall=(id,u,y,span,h)=>add(`${axis}-${side}-${id}`,axis==='x'?u:side*(width-t)/2,y,axis==='x'?side*(width-t)/2:u,axis==='x'?span:t,h,axis==='x'?t:span);
  const span=axis==='x'?width:width-2*t;
  wall('base',0,(sill+slab)/2,span,sill-slab);wall('head',0,(sill+windowH+top)/2,span,top-sill-windowH);
  let cursor=-span/2;for(const [i,p]of positions.entries()){wall(`pier-${i}`,(cursor+p-opening/2)/2,sill+windowH/2,p-opening/2-cursor,windowH);cursor=p+opening/2;}wall('pier-end',(cursor+span/2)/2,sill+windowH/2,span/2-cursor,windowH);
 }
 // Recessed roof terrace and low crenellated edge stay within inherited24m cap and total tower-height budget.
 const cap=width+2;add('roof',0,top+.1,0,cap,.2,cap);
 for(const axis of['x','z'])for(const side of[-1,1]){
  add(`parapet-${axis}-${side}`,axis==='x'?0:side*(cap-.5)/2,top+.5,axis==='x'?side*(cap-.5)/2:0,axis==='x'?cap:.5,.6,axis==='x'?.5:cap-1);
  for(let i=0;i<7;i++){const inset=axis==='x'?1:2,u=-cap/2+inset+i*(cap-2*inset)/6;add(`merlon-${axis}-${side}-${i}`,axis==='x'?u:side*(cap-.5)/2,top+1.4,axis==='x'?side*(cap-.5)/2:u,axis==='x'?1.2:.5,1.2,axis==='x'?.5:1.2);}
 }
 return parts;
}
