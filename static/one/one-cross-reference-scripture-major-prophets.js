/* ONE — reviewed Scripture fill for explanation-only major prophets.
 * Exact-reference only. Existing verified Scripture may be reused; commentary never is.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks)return;
  const known={};
  Object.values(D.studyBooks).forEach(book=>Object.values(book?.chapterStudies||{}).forEach(study=>(Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{
    if(Array.isArray(row)&&String(row[0]||'').trim()&&String(row[3]||'').trim())known[String(row[0]).trim()]=String(row[3]).trim();
  })));
  const reviewed={
    '申命記 30:1–6':'我所陳明在你面前的這一切咒詛都臨到你身上；你在耶和華－你上帝追趕你到的萬國中必心裏追念祝福的話；你和你的子孫若盡心盡性歸向耶和華－你的上帝，照着我今日一切所吩咐的聽從他的話；那時，耶和華－你的上帝必憐恤你，救回你這被擄的子民；耶和華－你的上帝要回轉過來，從分散你到的萬民中將你招聚回來。你被趕散的人，就是在天涯的，耶和華－你的上帝也必從那裏將你招聚回來。耶和華－你的上帝必領你進入你列祖所得的地，使你可以得着；又必善待你，使你的人數比你列祖眾多。耶和華－你上帝必將你心裏和你後裔心裏的污穢除掉，好叫你盡心盡性愛耶和華－你的上帝，使你可以存活。',
    '希伯來書 8:8–12':'所以主指責他的百姓說：日子將到，我要與以色列家和猶大家另立新約，不像我拉着他們祖宗的手，領他們出埃及的時候，與他們所立的約。因為他們不恆心守我的約，我也不理他們。這是主說的。主又說：那些日子以後，我與以色列家所立的約乃是這樣：我要將我的律法放在他們裏面，寫在他們心上；我要作他們的上帝；他們要作我的子民。他們不用各人教導自己的鄉鄰和自己的弟兄，說：你該認識主；因為他們從最小的到至大的，都必認識我。我要寬恕他們的不義，不再記念他們的罪愆。',
    '哥林多後書 4:8–9':'我們四面受敵，卻不被困住；心裏作難，卻不至失望；遭逼迫，卻不被丟棄；打倒了，卻不至死亡。',
    '耶利米書 31:31–34':'耶和華說：「日子將到，我要與以色列家和猶大家另立新約，不像我拉着他們祖宗的手，領他們出埃及地的時候，與他們所立的約。我雖作他們的丈夫，他們卻背了我的約。」這是耶和華說的。耶和華說：「那些日子以後，我與以色列家所立的約乃是這樣：我要將我的律法放在他們裏面，寫在他們心上。我要作他們的上帝，他們要作我的子民。他們各人不再教導自己的鄰舍和自己的弟兄說：『你該認識耶和華』，因為他們從最小的到至大的都必認識我。我要赦免他們的罪孽，不再記念他們的罪惡。」這是耶和華說的。',
    '約翰福音 10:11':'我是好牧人；好牧人為羊捨命。',
    '耶利米書 25:11–12':'這全地必然荒涼，令人驚駭。這些國民要服事巴比倫王七十年。七十年滿了以後，我必刑罰巴比倫王和那國民，並迦勒底人之地，因他們的罪孽使那地永遠荒涼。這是耶和華說的。',
    '馬太福音 24:15':'你們看見先知但以理所說的「那行毀壞可憎的」站在聖地（讀這經的人須要會意）。'
  };
  Object.assign(known,reviewed);
  const books=[24,25,26,27];
  let filled=0;
  const missing={};
  for(const bookNo of books){
    missing[bookNo]=new Set();
    Object.values(D.studyBooks?.[bookNo]?.chapterStudies||{}).forEach(study=>{
      (Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{
        if(!Array.isArray(row)||String(row[3]||'').trim())return;
        const ref=String(row[0]||'').trim(),scripture=known[ref];
        if(scripture){row[3]=scripture;filled++;}else if(ref)missing[bookNo].add(ref);
      });
    });
    missing[bookNo]=[...missing[bookNo]];
  }
  window.ONE_MAJOR_PROPHETS_CROSS_REFERENCE_SCRIPTURE={filled,books,missing};
})();
