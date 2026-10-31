// Display precinct context, not an ancient survey. All coordinates stay in metres.
export function firstTempleOuterCourt(data,spatial){
 const {bounds,gateWidth}=data.royalCity.temple.outerCourt,[xmin,zmin,xmax,zmax]=bounds;
 const sides=[{axis:'x',fixed:zmin,start:xmin,end:xmax},{axis:'x',fixed:zmax,start:xmin,end:xmax},{axis:'z',fixed:xmin,start:zmin,end:zmax},{axis:'z',fixed:xmax,start:zmin,end:zmax}];
 return sides.flatMap((s,index)=>{
  const cuts=[];
  for(const edge of spatial.edges)for(let i=1;i<edge.points.length;i++){
   const a=edge.points[i-1],b=edge.points[i],ac=s.axis==='x'?a[1]:a[0],bc=s.axis==='x'?b[1]:b[0];if(ac===bc)continue;
   const f=(s.fixed-ac)/(bc-ac);if(f<0||f>1)continue;
   const u=(s.axis==='x'?a[0]:a[1])+f*((s.axis==='x'?b[0]:b[1])-(s.axis==='x'?a[0]:a[1]));
   if(u>s.start&&u<s.end)cuts.push([u-gateWidth/2,u+gateWidth/2]);
  }
  cuts.sort((a,b)=>a[0]-b[0]);let cursor=s.start;const intervals=[];
  for(const [a,b]of cuts){if(a>cursor)intervals.push([cursor,a]);cursor=Math.max(cursor,b);}if(cursor<s.end)intervals.push([cursor,s.end]);
  return intervals.flatMap(([a,b])=>{const n=Math.ceil((b-a)/5);return Array.from({length:n},(_,i)=>({...s,id:`outer-${index}-${a}-${i}`,start:a+(b-a)*i/n,end:a+(b-a)*(i+1)/n}));});
 });
}
export function earlyCourtPorticoes(bounds){
 const [xmin,zmin,xmax,zmax]=bounds,inset=2,depth=4;
 return [{id:'west',axis:'z',fixed:xmin+inset+depth/2,start:zmin+inset+depth,end:zmax-inset},
 {id:'east',axis:'z',fixed:xmax-inset-depth/2,start:zmin+inset+depth,end:zmax-inset},
 {id:'north',axis:'x',fixed:zmin+inset+depth/2,start:xmin+inset,end:xmax-inset}].map(s=>({...s,depth,height:3.8,columnWidth:.35,bay:6}));
}
