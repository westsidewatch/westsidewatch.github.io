/* 創世記 ONE：開卷註冊與完整性保護
 * 必須在 genesis-core 與所有分章資料載入完成後、one-map-catalog / one-app 之前執行。
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const genesis=D?.genesis;
  if(!D||!genesis)return;

  const expected=D.books?.find(book=>book[0]===1)?.[3]||50;
  const studies=genesis.chapterStudies||{};
  const chapters=Array.from({length:expected},(_,index)=>{
    const number=index+1;
    return studies[String(number)]?.title||`第 ${number} 章`;
  });

  genesis.number=1;
  genesis.code="GEN";
  genesis.zhCode="GEN";
  genesis.enCode="GEN";
  genesis.name="創世記";
  genesis.nameEn="Genesis";
  genesis.chapters=chapters;
  genesis.summary=genesis.summary||"創世記從創造、墮落與洪水，進入亞伯拉罕、以撒、雅各與約瑟的故事；神以後裔、土地、祝福與約展開救贖歷史的起點。";
  genesis.meta=genesis.meta||[["位置","舊約第一卷 · 第01卷"],["文體","律法書 · 起源與族長敘事"],["章數","50章"],["核心線索","創造 · 後裔 · 土地 · 祝福 · 約 · 神的護理"]];
  genesis.nowCards=genesis.nowCards||[["主線","創造 · 墮落 · 應許 · 族長 · 約瑟"],["辨別","後裔 · 土地 · 祝福 · 約 · 神同在"]];

  D.studyBooks={...(D.studyBooks||{}),1:genesis};

  const missing=[];
  for(let number=1;number<=expected;number+=1){
    if(!studies[String(number)])missing.push(number);
  }
  const allReady=missing.length===0;
  document.documentElement.dataset.genesisReady=allReady?"true":"partial";
  document.documentElement.dataset.genesisChapterCount=String(Object.keys(studies).filter(key=>/^\d+$/.test(key)).length);
  if(!allReady){
    console.error(`[ONE Genesis] missing chapter studies: ${missing.join(", ")}`);
  }

  document.addEventListener("DOMContentLoaded",()=>{
    const item=document.querySelector('.cover-book[data-book="1"]');
    if(!item)return;
    item.classList.toggle("has-study",allReady);
    item.classList.toggle("forthcoming",!allReady);
    item.setAttribute("aria-label",allReady?"第 1 卷，創世記，可開始查考":`第 1 卷，創世記，資料尚未完整載入：缺少 ${missing.join("、")} 章`);
  });
})();
