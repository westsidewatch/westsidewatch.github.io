function cross(a,b,c){return(b.x-a.x)*(c.z-a.z)-(b.z-a.z)*(c.x-a.x)}
function onSegment(p,a,b){return Math.abs(cross(a,b,p))<1e-6&&p.x>=Math.min(a.x,b.x)-1e-6&&p.x<=Math.max(a.x,b.x)+1e-6&&p.z>=Math.min(a.z,b.z)-1e-6&&p.z<=Math.max(a.z,b.z)+1e-6}
function inside(p,poly){let hit=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[j],b=poly[i];if(onSegment(p,a,b))return true;if((a.z>p.z)!==(b.z>p.z)&&p.x<(b.x-a.x)*(p.z-a.z)/(b.z-a.z)+a.x)hit=!hit;}return hit}
export function polygonsOverlap(a,b){
  if(a.some(p=>inside(p,b))||b.some(p=>inside(p,a)))return true;
  for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++){
    const p=a[i],q=a[(i+1)%a.length],r=b[j],s=b[(j+1)%b.length];
    if(cross(p,q,r)*cross(p,q,s)<0&&cross(r,s,p)*cross(r,s,q)<0)return true;
  }
  return false;
}
