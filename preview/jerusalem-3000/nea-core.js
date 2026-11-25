import {appendAisledHall,appendHalfApse} from './aisled-hall-shell.js';
const PLAN='https://www.biblicalarchaeology.org/daily/biblical-sites-places/jerusalem/found-after-1400-years-the-magnificent-nea/';
const HISTORY='https://jerusalemfoundation.org/old-project/nea-church/';
const FORM='https://jewishvirtuallibrary.org/jsource/Archaeology/Nea.html';
const LITERARY='https://dig.corps-cmhl.huji.ac.il/literary_sources/jerusalem-old-city-new-church-theotokos-nea-church-4';
// Selected post-543 context, not every point in the fourth–seventh centuries.
export function neaCore(phase){
 if(phase!=='byzantine')return null;
 const x=-320,z=490,length=105,width=57,forecourt=26;
 return {id:'j3k:byzantine:independent:monument:nea-context',type:'monument',confidence:'inferred',geometry:{frame:'canonical-dem-enu',status:'relative-site-context-not-surveyed-footprint',primitive:'polygon',polygon:[{x:x-length/2-forecourt,z:z-width/2},{x:x+length/2+10,z:z-width/2},{x:x+length/2+10,z:z+width/2},{x:x-length/2-forecourt,z:z+width/2}]},source:{urls:[PLAN,HISTORY,FORM,LITERARY],authority:'published basilica dimensions and historical context; authored massing and relative placement',limitations:['採用Ben-Dov建議復原的三通廊與三入口關係；內寬、屋高及門寬仍是示意，並非定論。','本期選取543年後的Nea語境，不表示四世紀已有這座教堂。','115×57公尺為外交部考古概述之轉載參照；前院、屋高、內部分配及位置為示意，非轉錄發掘平面。','後續使用及受損分期未在此模型核定；退出展示不是宣告614年或某個確定年份全部毀滅。']},metadata:{name:'Nea 新聖母教堂（543年後三通廊建議方案）',planInterpretation:{source:PLAN,author:'Meir Ben-Dov',publicationYear:1977,form:'suggested-three-aisle-reconstruction',internalWidthsMetres:[17,23,17],widthsAuthority:'authored-distribution-within-existing57m-envelope',excavatedInteriorPlanVerified:false},coreProfile:'nea-three-aisle-proposal',landmarkChronology:{projection:'landmark-specific-display-offset-not-city-year-clock',years:[324,638],sources:[LITERARY,HISTORY],stages:[{year:543,offset:(543-324)/(638-324),state:'build',profile:'nea-three-aisle-proposal',label:'543年後Nea（三通廊建議方案）',authority:'source-dated-dedication; shape unverified'}]},modelAnchor:{x,z},approachAxis:'western',mainChurchMetres:{length:115,width:57,authority:'published-excavation-overview-reference-not-digitized-plan'},referencePeriod:'selected post-543 Byzantine context; subsequent use and damage unresolved',wholePhaseSimultaneity:false,geometryVerified:false,ancientGroundVerified:false,placeId:'j3k:place:nea-site',placeRelation:'selected-building-context-not-verified-cross-era-fabric',siteRegistration:{policy:'relative-southern-cardo-context-not-surveyed',historicalPositionVerified:false,historicalFootprintVerified:false},terrainFit:'level-upper-mass-modern-dem-footings-not-ancient-podium'}};
}
export function appendNeaGeometry(record,{box,append,THREE},cx,cz){
 const length=105,widths=[17,23,17],heights=[14,20,14];
 appendAisledHall({append,THREE},{cx,cz,length,widths,heights,axis:'x',rearOpen:[1],doorWidths:[2.5,4,2.5]});
 const roof=new THREE.BufferGeometry(),positions=[],w=11.5,n=cz-w,s=cz+w,a=cx-length/2,b=cx+length/2;
 const tri=(...points)=>points.forEach(p=>positions.push(...p));
 tri([a,20,n],[a,20,s],[a,23,cz]);tri([b,20,n],[b,23,cz],[b,20,s]);
 tri([a,20,n],[a,23,cz],[b,20,n]);tri([a,23,cz],[b,23,cz],[b,20,n]);
 tri([a,20,s],[b,20,s],[a,23,cz]);tri([a,23,cz],[b,20,s],[b,23,cz]);
 roof.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));roof.computeVertexNormals();append(roof,0,0);
 // Three east-facing half-apses; only the small side-apse diameter is described
 // in the source. Central radius and all heights are illustrative.
 for(const [offset,radius,height]of [[0,10,18],[-20,2.5,11],[20,2.5,11]])appendHalfApse({append,THREE},{x:b,z:cz+offset,radius,height});
 const west=a-26;
 box((west+a)/2,cz-27.9,26,1.2,3);box((west+a)/2,cz+27.9,26,1.2,3);
 for(const side of [-1,1])box(west+.6,cz+side*18,1.2,21,3);
}
