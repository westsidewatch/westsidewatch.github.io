(()=>{"use strict";
const CORPUS={
 id:"fsn-seal-metadata-v1",
 source:"Fu Ssu-Nien Library Seal Database",
 sourceUrl:"https://dap.ihp.sinica.edu.tw/database/2/",
 policy:"metadata-only; source seal images are not copied",
 records:[
  {id:"11111501.002",text:"蕉林藏書",h:2,w:2,shape:"square",carving:"yang",script:"small-seal"},
  {id:"11080001.001",text:"畢氏珍藏",h:1.55,w:1.6,shape:"rectangle",carving:"yang",script:"small-seal"},
  {id:"13110001.001",text:"謙牧堂藏書記",h:2.55,w:2.65,shape:"rectangle",carving:"yin",script:"small-seal"},
  {id:"04181101.003",text:"掃塵齋積書記",h:2.9,w:2.9,shape:"square",carving:"yang",script:"small-seal"},
  {id:"06181201.002",text:"梅會里朱氏潛釆堂藏書",h:4.3,w:2.15,shape:"rectangle",carving:"yang",script:"small-seal"},
  {id:"11100901.002",text:"皖南張師亮筱漁氏校書於篤素堂",h:5.57,w:3.64,shape:"rectangle",carving:"yang",script:"small-seal"},
  {id:"08040901.003",text:"摛藻堂",h:2.65,w:2.65,shape:"square",carving:"yin",script:"small-seal"}
 ]
};
function stats(records=CORPUS.records){const usable=records.filter(r=>r.h>0&&r.w>0),ratios=usable.map(r=>r.w/r.h),mean=ratios.reduce((a,v)=>a+v,0)/(ratios.length||1),square=ratios.filter(v=>v>=.9&&v<=1.1).length/(ratios.length||1);return{n:usable.length,meanAspect:mean,squareShare:square,aspectRatios:ratios}}
window.SEAL_CORPUS={...CORPUS,stats:stats()};
})();