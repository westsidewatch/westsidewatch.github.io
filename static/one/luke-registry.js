/* 路加福音 ONE：開卷註冊
 * 必須在所有 Luke 章資料載入完成後、one-map-catalog / one-app 之前執行。
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const luke=D?.luke;
  if(!D||!luke)return;

  const expected=24;
  const studies=luke.chapterStudies||{};
  const chapters=Array.from({length:expected},(_,index)=>{
    const number=index+1;
    return studies[String(number)]?.title||`第 ${number} 章`;
  });

  luke.number=42;
  luke.code="LUK";
  luke.zhCode="LUK";
  luke.enCode="LUK";
  luke.name="路加福音";
  luke.nameEn="Luke";
  luke.chapters=chapters;

  D.studyBooks={...(D.studyBooks||{}),42:luke};
})();
