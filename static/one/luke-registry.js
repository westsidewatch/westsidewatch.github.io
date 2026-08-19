/* 路加福音 ONE：開卷註冊與入口保護
 * 必須在所有 Luke 章資料載入完成後、one-map-catalog / one-app 之前執行。
 * 章封面由後續 one-cover-policy.js 統一分配；本註冊檔不得動態載入插圖腳本。
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const luke=D?.luke;
  if(!D||!luke)return;

  /* Mark has no dedicated registry file yet; by the time Luke's registry runs, all Mark
   * chapter files are already loaded and Book 41 is registered. Add only missing chronology
   * here as a compatibility bridge, without changing Mark content or cover ownership.
   */
  const mark=D.studyBooks?.[41]||D.mark;
  const markStudies=mark?.chapterStudies||{};
  const markChronology=number=>{
    let range,phase,note;
    if(number===1){range="福音起頭 · 馬可福音 1";phase="施洗約翰、耶穌受洗、受試探與加利利事奉開始";note="馬可直接從公開事奉起頭，不提供降生敘事；時序以敘事階段為主。";}
    else if(number<=8){range="加利利事奉 · 馬可福音 2–8";phase="權柄、比喻、神蹟與門徒逐步認識耶穌身份";note="主要舞台在加利利及周邊；第8章彼得認信形成重要轉折。";}
    else if(number<=10){range="往耶路撒冷的門徒道路 · 馬可福音 9–10";phase="三次受難預告背景下學習捨己、服事與跟從";note="敘事逐步由北方轉向耶路撒冷，重點是十字架式門徒訓練。";}
    else if(number<=13){range="進入耶路撒冷與聖殿 · 馬可福音 11–13";phase="進城、潔淨聖殿、爭辯與橄欖山講論";note="本段集中於耶路撒冷最後一週前半，經文次序比推測精確日期更可靠。";}
    else if(number<=15){range="受難敘事 · 馬可福音 14–15";phase="最後晚餐、客西馬尼、審判、十字架與安葬";note="敘事集中於逾越節背景下耶穌受難的最後時段。";}
    else{range="空墳墓與復活宣告 · 馬可福音 16";phase="婦女到墳墓、耶穌已經復活的宣告與福音使命";note="第16章位於復活敘事；ONE 不用 chronology 模塊處理馬可結尾的文本批判問題。";}
    const study=markStudies[String(number)];
    return{title:"馬可福音事奉時序",range,note,events:[[range,`馬可福音 ${number}`,study?.title||phase],["全卷位置",phase,"按馬可敘事與地理轉折定位，不製造不必要的日期精確度。"]],url:"https://bibleeveryone.com/bible-timeline.php"};
  };
  for(let number=1;number<=16;number+=1){
    const study=markStudies[String(number)];
    if(study&&(!study.timeline||!Array.isArray(study.timeline.events)||!study.timeline.events.length))study.timeline=markChronology(number);
  }

  const expected=D.books?.find(book=>book[0]===42)?.[3]||24;
  const studies=luke.chapterStudies||{};

  /* Luke chronology follows the Gospel's own narrative geography and ministry phases.
   * Absolute dates are kept broad where chronology is debated; the stable anchors are
   * infancy, preparation, Galilean ministry, the Jerusalem journey, Passion and Resurrection.
   */
  const lukeChronology=number=>{
    let range,phase,note;
    if(number<=2){range="耶穌降生與童年 · 路加福音 1–2";phase="施洗約翰與耶穌的降生、聖殿與拿撒勒";note="本段置於希律與羅馬帝國背景；對人口登記等細節不製造超出經文與史料共識的精確日期。";}
    else if(number<=4){range="預備與事奉起點 · 路加福音 3–4";phase="施洗約翰、受洗、家譜、試探與拿撒勒宣告";note="耶穌公開事奉開始；以路加敘事順序為主，不把每一事件鎖定到單一月份。";}
    else if(number<=9){range="加利利事奉 · 路加福音 5–9";phase="呼召、教導、醫治、神蹟與門徒身份逐步顯明";note="本段主要位於加利利；路9:51是全卷重要轉折。";}
    else if(number<=19){range="上耶路撒冷的旅程 · 路加福音 9:51–19";phase="耶穌定意往耶路撒冷去，在路上集中教導門徒";note="路加以長篇旅程框架組織大量獨有材料；地理次序不應被過度強行重建。";}
    else if(number<=23){range="耶路撒冷與受難週 · 路加福音 20–23";phase="聖殿教導、最後晚餐、客西馬尼、審判與十字架";note="敘事集中於耶路撒冷最後數日，與四福音受難敘事互相對照。";}
    else{range="復活日與升天前夕 · 路加福音 24";phase="空墳墓、以馬忤斯、向門徒顯現與差遣";note="第24章在復活日展開，並把路加福音直接引向使徒行傳的見證使命。";}
    const study=studies[String(number)];
    return{title:"路加福音事奉時序",range,note,events:[[range,`路加福音 ${number}`,study?.title||phase],["全卷位置",phase,"以福音書敘事階段定位，不製造不必要的日期精確度。"]],url:"https://bibleeveryone.com/bible-timeline.php"};
  };
  for(let number=1;number<=expected;number+=1){
    const study=studies[String(number)];
    if(study&&(!study.timeline||!Array.isArray(study.timeline.events)||!study.timeline.events.length))study.timeline=lukeChronology(number);
  }

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
  luke.summary=luke.summary||"路加按次序見證耶穌是為萬民而來的救主；祂在聖靈中尋找失喪的人，定意走向耶路撒冷，並從復活開啟向萬邦的使命。";
  luke.meta=luke.meta||[["位置","新約第三卷 · 第42卷"],["文體","福音書 · 歷史敘事與旅程教導"],["章數","24章"],["核心線索","救恩 · 聖靈 · 禱告 · 失喪者 · 耶路撒冷 · 萬邦"]];

  D.studyBooks={...(D.studyBooks||{}),42:luke};

  const allReady=Array.from({length:expected},(_,index)=>Boolean(studies[String(index+1)])).every(Boolean);
  document.documentElement.dataset.lukeReady=allReady?"true":"partial";

  /* Legacy document.write loader removed.
   * ONE-RUNTIME-LOAD-ORDER-MASTER requires explicit book-data registration before the
   * canonical cover policy. one-cover-policy.js is the sole runtime illustration writer,
   * so loading mark-luke-illustrations.js here was both redundant and cache-sensitive.
   */

  document.addEventListener("DOMContentLoaded",()=>{
    const item=document.querySelector('.cover-book[data-book="42"]');
    if(!item)return;
    item.classList.remove("forthcoming");
    item.classList.add("has-study");
    item.setAttribute("aria-label","第 42 卷，路加福音，可開始查考");
    item.addEventListener("click",()=>{
      if(!item.classList.contains("rail-current"))return;
      requestAnimationFrame(()=>{
        const dialog=document.getElementById("book-dialog");
        if(dialog&&!dialog.hidden)return;
        const url=new URL(location.href);
        url.searchParams.set("book","42");
        url.searchParams.set("chapter","1");
        location.assign(url.toString());
      });
    });
  });
})();
