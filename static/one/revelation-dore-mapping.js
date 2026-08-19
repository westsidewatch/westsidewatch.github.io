/* Revelation chronology + Acts/Revelation Doré canonical mapping.
 * Doré section is DATA ONLY: this file never writes study.illustration;
 * ONE_COVER_POLICY remains the sole runtime illustration writer.
 */
(() => {
  "use strict";
  const D = window.ONE_DATA;
  const R = window.ONE_DORE_COVER_REGISTRY;
  if (!R) return;

  /* Revelation's chronology is the literary sequence of John's received visions,
   * not a prediction calendar. Symbolic scenes are placed in the order the book gives
   * them; ONE does not assign modern dates or force one millennial scheme onto the text.
   */
  const revelation=D?.studyBooks?.[66];
  const revStudies=revelation?.chapterStudies||{};
  const revChronology=number=>{
    let range,phase,note;
    if(number===1){range="拔摩海島的啟示起點 · 啟示錄 1";phase="約翰領受耶穌基督的啟示，看見復活榮耀的人子";}
    else if(number<=3){range="七教會書信 · 啟示錄 2–3";phase="向亞細亞七教會的責備、鼓勵、警告與得勝應許";}
    else if(number<=5){range="天上寶座與羔羊 · 啟示錄 4–5";phase="創造主受敬拜，惟有被殺的羔羊配展開書卷";}
    else if(number<=7){range="七印異象 · 啟示錄 6–7";phase="印被揭開、地上震動與神僕受印的中段安慰";}
    else if(number<=11){range="七號異象 · 啟示錄 8–11";phase="號筒審判、苦味小書卷、兩個見證人與第七號";}
    else if(number<=14){range="龍、獸與羔羊 · 啟示錄 12–14";phase="屬天爭戰、逼迫權勢與錫安羔羊形成對照";}
    else if(number<=16){range="七碗異象 · 啟示錄 15–16";phase="末後災殃與神公義審判的杯";}
    else if(number<=18){range="巴比倫受審 · 啟示錄 17–18";phase="大淫婦與巴比倫體系被揭露並傾倒";}
    else if(number<=20){range="羔羊得勝與最後審判 · 啟示錄 19–20";phase="婚筵、騎白馬者、終局爭戰、復活與白色大寶座";}
    else{range="新天新地 · 啟示錄 21–22";phase="新耶路撒冷、生命河、神與人同住及主必快來的結語";}
    note="這條時序表示約翰異象在書卷中的展開順序，不把象徵段落換算成未經文本確證的現代年份。";
    const study=revStudies[String(number)];
    return{title:"啟示錄異象時序",range,note,events:[[range,`啟示錄 ${number}`,study?.title||phase],["異象序列",phase,"按書卷呈現次序定位；不同末世詮釋不被偽裝成單一精確年表。"]],url:"https://bibleeveryone.com/bible-timeline.php"};
  };
  for(let number=1;number<=22;number+=1){
    const study=revStudies[String(number)];
    if(study&&(!study.timeline||!Array.isArray(study.timeline.events)||!study.timeline.events.length))study.timeline=revChronology(number);
  }

  R.titles = R.titles || {};
  R.titles[224] = "The Descent of the Spirit";
  R.titles[225] = "The Apostles Preaching the Gospel";
  R.titles[226] = "St. Peter and St. John at the Beautiful Gate";
  R.titles[227] = "The Death of Ananias";
  R.titles[228] = "The Death of Stephen";
  R.titles[229] = "The Conversion of Saul";
  R.titles[230] = "St. Peter at the House of Cornelius";
  R.titles[231] = "St. Peter Delivered from Prison";
  R.titles[232] = "St. Paul at Ephesus";
  R.titles[233] = "St. Paul Rescued from the Multitude";
  R.titles[234] = "St. Paul Shipwrecked";
  R.titles[236] = "John at Patmos";
  R.titles[237] = R.titles[237] || "The Vision of Death";
  R.titles[238] = "The Crowned Virgin: A Vision of John";
  R.titles[239] = "Babylon Fallen";
  R.titles[240] = R.titles[240] || "The Last Judgment";
  R.titles[241] = R.titles[241] || "The New Jerusalem";

  R.maps = R.maps || {};
  R.maps[44] = "2:224,3:226,5:227,7:228,9:229,10:230,12:231,19:232,21:233,27:234";
  R.maps[66] = "1:236,6:237,12:238,18:239,20:240,21:241";

  R.actsOriginalLocked = Object.freeze({2:224,3:226,5:227,7:228,9:229,10:230,12:231,19:232,21:233,27:234});
  R.actsAdditionalOriginals = Object.freeze({2:Object.freeze([225])});
  R.actsMappingBasis = "P1_ORIGINAL_LOCKED_WIKIMEDIA_DORE_GALLERY";
  R.actsMappedChapters = 10;
  R.actsCanonicalOriginalPlates = 11;
  R.actsUnmappedChapters = 18;

  R.revelationOriginalLocked = Object.freeze({1:236,6:237,12:238,18:239,20:240,21:241});
  R.revelationMappingBasis = "P1_ORIGINAL_LOCKED_WIKIMEDIA_DORE_GALLERY";
  R.revelationMappedChapters = 6;
  R.revelationUnmappedChapters = 16;

  document.documentElement.dataset.actsDore = "10-chapters-11-originals-locked";
  document.documentElement.dataset.revelationDore = "6-original-locked";
})();