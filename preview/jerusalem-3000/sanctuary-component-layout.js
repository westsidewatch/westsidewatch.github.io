// Shared construction grammar; each era supplies its own explicit, unverified profile.
export function compileSanctuaryComponents(phase,{phaseId,gateId,accessId,approachId,approachObjectId,reservationId}) {
  const s=phase.sanctuary;
  const finitePoint=p=>Array.isArray(p)&&p.length===2&&p.every(Number.isFinite);
  const positive=(...values)=>values.every(v=>Number.isFinite(v)&&v>0);
  const {hall:h,porch:p,court:c,altar:a,access}=s;
  if(!h||!p||!c||!a||!access||!finitePoint(h.offset)||!finitePoint(a.offset)||!positive(h.length,h.width,h.height,h.wallThickness,h.doorWidth,h.doorHeight,p.depth,p.height,c.wallHeight,c.wallThickness,c.gateWidth,a.width,a.depth,a.height,access.width))throw new Error('Invalid sanctuary dimensions');
  if(h.wallThickness>=Math.min(h.length,h.width)/2||h.doorWidth>=h.width-2*h.wallThickness||h.doorHeight>=Math.min(h.height,p.height))throw new Error('Invalid sanctuary doorway');
  if(!Array.isArray(c.bounds)||c.bounds.length!==4||!c.bounds.every(Number.isFinite))throw new Error('Invalid sanctuary court');
  const [xmin,zmin,xmax,zmax]=c.bounds;
  if(xmin>=xmax||zmin>=zmax||!Number.isFinite(c.gateX)||c.gateX-c.gateWidth/2<=xmin+c.wallThickness||c.gateX+c.gateWidth/2>=xmax-c.wallThickness)throw new Error('Invalid sanctuary gate');
  const gate=[c.gateX,zmax],door=[h.offset[0]+h.length/2+p.depth,h.offset[1]];
  const approach=phase.roads.find(r=>r.id===approachId);
  if(!approach?.points?.length)throw new Error('Missing sanctuary approach');
  const start=approach.points.at(-1);
  if(!finitePoint(start)||Math.abs(start[0]-gate[0])>1e-6||start[1]<=gate[1])throw new Error('Sanctuary approach must meet gate from outside');
  const points=[start,gate,...access.waypoints,door];
  if(!points.every(finitePoint)||points.some((v,i)=>i&&Math.hypot(v[0]-points[i-1][0],v[1]-points[i-1][1])<.01))throw new Error('Invalid sanctuary access');
  const components=[];
  const box=(id,x,z,w,d,height,lift=0,role='wall')=>components.push({id,x,z,w,d,height,lift,role});
  const [hx,hz]=h.offset,t=h.wallThickness,L=h.length,W=h.width;
  box('hall-floor',hx,hz,L,W,.12,0,'floor');
  box('hall-west',hx-L/2+t/2,hz,t,W,h.height);
  for(const side of [-1,1])box(`hall-side-${side}`,hx,hz+side*(W/2-t/2),L-2*t,t,h.height);
  const jamb=(W-h.doorWidth)/2;
  for(const side of [-1,1])box(`hall-front-${side}`,hx+L/2-t/2,hz+side*(h.doorWidth/2+jamb/2),t,jamb,h.height);
  box('hall-door-lintel',hx+L/2-t/2,hz,t,h.doorWidth,h.height-h.doorHeight,h.doorHeight);
  // Open leaves are an authored viewing pose, not excavated Persian door details.
  for(const side of[-1,1])box(`hall-open-door-${side}`,hx+L/2-t-h.doorWidth/4,hz+side*(h.doorWidth/2-.06),h.doorWidth/2,.12,h.doorHeight-.12,.12,'door');
  box('hall-roof',hx,hz,L,W,.6,h.height,'roof');
  box('porch-floor',hx+L/2+p.depth/2,hz,p.depth,W,.12,0,'floor');
  for(const side of [-1,1])box(`porch-side-${side}`,hx+L/2+p.depth/2,hz+side*(W/2-t/2),p.depth,t,p.height);
  box('porch-roof',hx+L/2+p.depth/2,hz,p.depth,W,.5,p.height,'roof');
  // Existing era-specific display envelope retained; tier/rim profile is authored.
  box('altar',...a.offset,a.width,a.depth,a.height*.2,0,'altar');
  box('altar-body',...a.offset,a.width*.88,a.depth*.88,a.height*.5,a.height*.2,'altar');
  box('altar-hearth',...a.offset,a.width*.84,a.depth*.84,.06,a.height*.7,'hearth');
  const rim=.3;
  for(const side of[-1,1]){
    box(`altar-rim-x-${side}`,a.offset[0]+side*(a.width-rim)/2,a.offset[1],rim,a.depth,a.height*.3,a.height*.7,'altar');
    box(`altar-rim-z-${side}`,a.offset[0],a.offset[1]+side*(a.depth-rim)/2,a.width-2*rim,rim,a.height*.3,a.height*.7,'altar');
  }
  for(const side of [-1,1])box(`court-side-${side}`,side<0?xmin:xmax,(zmin+zmax)/2,c.wallThickness,zmax-zmin,c.wallHeight);
  box('court-north',(xmin+xmax)/2,zmin,xmax-xmin,c.wallThickness,c.wallHeight);
  const left=gate[0]-c.gateWidth/2,right=gate[0]+c.gateWidth/2;
  box('court-south-west',(xmin+left)/2,zmax,left-xmin,c.wallThickness,c.wallHeight);
  box('court-south-east',(right+xmax)/2,zmax,xmax-right,c.wallThickness,c.wallHeight);
  for(const side of [-1,1])box(`gate-post-${side}`,gate[0]+side*(c.gateWidth/2+.4),gate[1],.8,c.wallThickness,3.2,0,'gate');
  const margin=access.width/2;
  for(const component of components.filter(c=>!c.id.startsWith('court-')&&c.role!=='gate'))if(component.x-component.w/2<xmin+margin||component.x+component.w/2>xmax-margin||component.z-component.d/2<zmin+margin||component.z+component.d/2>zmax-margin)throw new Error('Sanctuary component outside court');
  // Validate the actual route footprint against all ground-level building components.
  for(let i=1;i<points.length;i++){
    const [ax,az]=points[i-1],[bx,bz]=points[i],length=Math.hypot(bx-ax,bz-az);
    for(let j=0;j<=Math.ceil(length/.25);j++){
      const f=j/Math.ceil(length/.25),x=ax+(bx-ax)*f,z=az+(bz-az)*f;
      for(const part of components.filter(c=>c.lift===0&&c.role!=='floor'))if(x+margin>part.x-part.w/2&&x-margin<part.x+part.w/2&&z+margin>part.z-part.d/2&&z-margin<part.z+part.d/2)throw new Error(`Sanctuary access crosses ${part.id}`);
    }
  }
  const reservation=phase.reservations.find(r=>r.id===reservationId);
  if(!reservation?.polygon?.length)throw new Error('Missing sanctuary reservation');
  const inside=(x,z)=>{let hit=false;const poly=reservation.polygon;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if((a[1]>z)!==(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])hit=!hit;}return hit;};
  for(const part of components)for(const sideX of [-1,1])for(const sideZ of [-1,1])if(!inside(part.x+sideX*part.w/2,part.z+sideZ*part.d/2))throw new Error('Sanctuary outside reserved precinct');
  return {...s,components,gate:{id:gateId,point:gate},access:{id:accessId,width:access.width,points,from:approachObjectId,to:s.objectId},door,phase:phaseId};
}
