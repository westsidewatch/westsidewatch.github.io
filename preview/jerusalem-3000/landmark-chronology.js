// Source dates are mapped to offsets ONLY for these named landmarks. These
// display intervals do not turn the entire city timeline into a uniform year clock.
export const HOLY_SEPULCHRE_HISTORY='https://www.custodia.org/en/sanctuaries/basilica-of-the-holy-sepulchre/';
const DEDICATION='https://cmc-terrasanta.org/en/media/news/17899/basilica-of-the-holy-sepulcher%2C-the-feast-of-dedication';
export function holySepulchreChronology(phase){
 const presets={
  byzantine:{years:[324,638],stages:[{year:335,state:'build',profile:'constantinian-rotunda-east-basilica',label:'聖墓：335年後建築群'}]},
  'early-islamic':{years:[638,1099],stages:[{year:638,state:'transform',profile:'constantinian-rotunda-east-basilica',label:'聖墓：1009年前建築群'},{year:1009,state:'ruin',profile:'sepulchre-1009-fragments',label:'聖墓：1009年毀壞遺構'},{year:1048,state:'rebuild',profile:'sepulchre-1048-rotunda',label:'聖墓：1048年後圓堂'}]},
  crusader:{years:[1099,1187],stages:[{year:1099,state:'transform',profile:'sepulchre-1048-rotunda',label:'聖墓：十字軍改建前圓堂'},{year:1149,state:'transform',profile:'medieval-rotunda-church',label:'聖墓：1149年後整合堂體'}]}
 };
 const plan=presets[phase];if(!plan)return null;
 return {projection:'landmark-specific-display-offset-not-city-year-clock',years:plan.years,sources:[HOLY_SEPULCHRE_HISTORY,...(phase==='crusader'?[DEDICATION]:[])],stages:plan.stages.map(s=>({...s,offset:(s.year-plan.years[0])/(plan.years[1]-plan.years[0]),authority:'source-dated-event; shapes and physical survival unverified'})),limitations:['展示座標與尺寸為既有示意，不是分期發掘平面。','1009年殘存高度及1048年附屬小堂外形未測繪；不能從模型推定原構件存續。','614年受損與修復、後期火災／修復等仍未逐事件建模。']};
}
export function coreStageAt(record,offset){
 const plan=record.metadata?.landmarkChronology;if(!plan)return null;
 // Once published, read dates/profile choices from the live shared events.
 // Source declarations only compile geometry; they cannot override ledger edits.
 const stages=record.lifecycle?(record.lifecycle.events||[]).filter(e=>e.phase===record.metadata.generationPhase&&e.representationProfile).map(e=>({year:e.year??null,offset:e.offset??0,state:e.state,profile:e.representationProfile,label:e.representationLabel,authority:e.authority})):plan.stages;
 return [...stages].sort((a,b)=>b.offset-a.offset).find(s=>s.offset<=offset)||{profile:null,state:'absent',label:'尚未到來源記載的落成階段',year:null,offset:0};
}
export function coreGeometryVariants(record){
 const plan=record.metadata?.landmarkChronology;
 return plan?[...new Set(plan.stages.map(s=>s.profile))]:[record.metadata?.coreProfile];
}
export function coreStageVisible(record,profile,offset){const stage=coreStageAt(record,offset);return stage?stage.profile===profile:true;}
