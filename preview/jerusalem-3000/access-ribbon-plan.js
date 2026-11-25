// Engineering joins for an existing metre-scale centreline, not new ancient roads.
export function accessRibbonSections(points,width){
 if(!Array.isArray(points)||points.length<2||!Number.isFinite(width)||width<=0||points.some(p=>p.length!==2||!p.every(Number.isFinite)))throw new Error('Invalid access ribbon');
 const directions=points.slice(1).map((b,i)=>{const a=points[i],dx=b[0]-a[0],dz=b[1]-a[1],len=Math.hypot(dx,dz);if(len<1e-6)throw new Error('Zero-length access segment');return[dx/len,dz/len];});
 const sections=points.map((p,i)=>{
  const before=directions[Math.max(0,i-1)],after=directions[Math.min(i,directions.length-1)],dot=before[0]*after[0]+before[1]*after[1];
  if(dot<-.95)throw new Error('Access hairpin requires an explicit landing');
  const denominator=1+dot,nx=(-before[1]-after[1])/denominator*width/2,nz=(before[0]+after[0])/denominator*width/2;
  return {left:[p[0]+nx,p[1]+nz],right:[p[0]-nx,p[1]-nz]};
 });
 for(let i=1;i<sections.length;i++){const q=[sections[i-1].left,sections[i].left,sections[i].right,sections[i-1].right],turns=q.map((a,j)=>{const b=q[(j+1)%4],c=q[(j+2)%4];return(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]);});if(turns.some(v=>v>=-1e-8))throw new Error('Access bend spacing requires an explicit landing');}
 return sections;
}
// Invert a convex bilinear strip: the same join has f=1 on its incoming
// segment and f=0 on its outgoing segment, including the two outside corners.
export function ribbonFraction(x,z,a,b,c,d){
 const ux=b[0]-a[0],uz=b[1]-a[1],vx=c[0]-a[0],vz=c[1]-a[1],wx=d[0]-b[0]-c[0]+a[0],wz=d[1]-b[1]-c[1]+a[1];
 let f=.5,s=.5;
 for(let k=0;k<8;k++){
  const ex=a[0]+f*ux+s*vx+f*s*wx-x,ez=a[1]+f*uz+s*vz+f*s*wz-z,fx=ux+s*wx,fz=uz+s*wz,sx=vx+f*wx,sz=vz+f*wz,det=fx*sz-fz*sx;
  if(Math.abs(det)<1e-10)throw new Error('Folded access ribbon');
  const df=(ex*sz-ez*sx)/det,ds=(fx*ez-fz*ex)/det;f-=df;s-=ds;if(Math.abs(df)+Math.abs(ds)<1e-9)break;
 }
 return Math.max(0,Math.min(1,f));
}
