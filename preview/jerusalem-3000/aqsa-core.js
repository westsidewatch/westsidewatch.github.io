// A selected late-Fatimid-or-later schematic form, not the early Umayyad mosque.
export const AQSA_SOURCE='https://islamicart.museumwnf.org/database_item.php?id=monument%3Bisl%3Bpa%3Bmon01%3B3%3Ben';
const PHASES=['early-islamic','crusader','ayyubid-mamluk','ottoman','outside-walls','modern'];
export function aqsaCore(phase){
 if(!PHASES.includes(phase))return null;
 const x=35,z=220,recess=phase!=='early-islamic',west=x-25,east=x+(recess?31:25);
 return {id:`j3k:${phase}:independent:monument:aqsa-context`,type:'monument',confidence:'inferred',geometry:{frame:'canonical-dem-enu',status:'relative-site-context-not-surveyed-footprint',primitive:'polygon',polygon:[{x:west,z:z-40},{x:east,z:z-40},{x:east,z:z+40},{x:west,z:z+40}]},source:{urls:[AQSA_SOURCE],authority:'present main-hall dimensions and described forms; relative position and heights authored',limitations:['50×80公尺引用現存主廳，不是伍麥葉時期測繪平面。','早期伊斯蘭概覽選取較晚法蒂瑪形態，不表示七世紀起一直如此。','東側增建的位置與形體為示意；高程適配使用現代DEM，同址不等於原構件保存。']},metadata:{name:phase==='early-islamic'?'阿克薩南部禮拜堂（晚期形態）':phase==='crusader'?'阿克薩南部禮拜堂／十字軍改用':'阿克薩南部禮拜堂',coreProfile:'aqsa-seven-aisle-context',modelAnchor:{x,z},mainHallMetres:{width:50,length:80,authority:'present-main-hall-reference-not-phase-survey'},eastRecess:recess,referencePeriod:phase==='early-islamic'?'selected late-Fatimid context after eleventh-century rebuilding':phase==='crusader'?'Crusader use and illustrative eastern addition':'later repaired and altered mosque; specific fabric unresolved',wholePhaseSimultaneity:false,geometryVerified:false,ancientGroundVerified:false,placeId:'j3k:place:southern-haram',placeRelation:'same-site-not-verified-original-fabric',siteRegistration:{policy:'relative-southern-site-context-not-surveyed',historicalPositionVerified:false,historicalFootprintVerified:false},terrainFit:'level-upper-mass-modern-dem-footings-not-ancient-platform'}};
}
// Append one recognizable assembly through the existing core renderer.
export function appendAqsaGeometry(record,{box,dome,append,THREE},cx,cz){
 const widths=[20/3,20/3,20/3,10,20/3,20/3,20/3];let left=cx-25;
 for(const [i,width]of widths.entries()){
  const x=left+width/2,height=i===3?16:11;box(x,cz,width,80,height);
  // Only the central raised roof receives a pitched silhouette; side covering
  // remains schematic rather than inventing seven separate basilica roofs.
  if(i!==3){left+=width;continue;}
  const g=new THREE.BufferGeometry(),positions=[],a=x-width/2,b=x+width/2,n=cz-40,s=cz+40;
  const tri=(...points)=>points.reverse().forEach(p=>positions.push(...p));
  tri([a,height,n],[x,height+2,n],[a,height,s]);tri([x,height+2,n],[x,height+2,s],[a,height,s]);
  tri([b,height,n],[b,height,s],[x,height+2,n]);tri([x,height+2,n],[b,height,s],[x,height+2,s]);
  tri([a,height,n],[b,height,n],[x,height+2,n]);tri([a,height,s],[x,height+2,s],[b,height,s]);
  g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.computeVertexNormals();append(g,0,0);left+=width;
 }
 dome(cx,cz+24,9,18);
 if(record.metadata.eastRecess)box(cx+25,cz+14,12,16,11);
}
