/* Complete Isaiah connection coverage. Existing curated connections are preserved; only empty chapters are filled. */
(() => {
  "use strict";
  const D=window.ONE_DATA,I=D?.isaiah;if(!D||!I)return;
  const S=I.chapterStudies||{};
  const V={
    justice:["以賽亞書 1:17","學習行善與公平","學習行善，尋求公平，解救受欺壓的；給孤兒伸冤，為寡婦辨屈。"],
    holy:["以賽亞書 6:3","耶和華的聖潔","聖哉！聖哉！聖哉！萬軍之耶和華；他的榮光充滿全地！"],
    immanuel:["以賽亞書 7:14","以馬內利","必有童女懷孕生子，給他起名叫以馬內利。"],
    child:["以賽亞書 9:6","和平之君","因有一嬰孩為我們而生；有一子賜給我們。政權必擔在他的肩頭上。"],
    branch:["以賽亞書 11:1–2","耶西的枝子","從耶西的本必發一條；從他根生的枝子必結果實。耶和華的靈必住在他身上。"],
    death:["以賽亞書 25:8","吞滅死亡","他已經吞滅死亡直到永遠；主耶和華必擦去各人臉上的眼淚。"],
    peace:["以賽亞書 26:3–4","倚靠耶和華得平安","堅心倚賴你的，你必保守他十分平安，因為他倚靠你。你們當倚靠耶和華直到永遠。"],
    desert:["以賽亞書 35:1–2","曠野歡喜","曠野和乾旱之地必然歡喜；沙漠也必快樂，又像玫瑰開花。"],
    wait:["以賽亞書 40:31","等候耶和華","但那等候耶和華的必重新得力。他們必如鷹展翅上騰。"],
    servant:["以賽亞書 42:1","我的僕人","看哪，我的僕人－我所扶持所揀選、心裏所喜悅的！我已將我的靈賜給他。"],
    redeem:["以賽亞書 43:1","我已救贖你","你不要害怕！因為我救贖了你。我曾提你的名召你，你是屬我的。"],
    suffering:["以賽亞書 53:5–6","受苦僕人擔當罪孽","哪知他為我們的過犯受害，為我們的罪孽壓傷。因他受的刑罰，我們得平安；因他受的鞭傷，我們得醫治。"],
    water:["以賽亞書 55:1","白白得水","你們一切乾渴的都當就近水來；沒有銀錢的也可以來。"],
    fast:["以賽亞書 58:6","真正的禁食","我所揀選的禁食不是要鬆開兇惡的繩，解下軛上的索，使被欺壓的得自由，折斷一切的軛嗎？"],
    light:["以賽亞書 60:1","興起發光","興起，發光！因為你的光已經來到！耶和華的榮耀發現照耀你。"],
    spirit:["以賽亞書 61:1","主的靈在我身上","主耶和華的靈在我身上；因為耶和華用膏膏我，叫我傳好信息給謙卑的人。"],
    newcreation:["以賽亞書 65:17","新天新地","看哪！我造新天新地；從前的事不再被記念，也不再追想。"]
  };
  const map={3:"justice",4:"branch",10:"holy",12:"water",13:"holy",14:"holy",15:"justice",16:"branch",17:"redeem",18:"light",19:"holy",20:"peace",21:"wait",23:"holy",24:"death",26:"peace",27:"redeem",30:"peace",31:"peace",32:"spirit",33:"peace",34:"holy",36:"peace",37:"holy",38:"redeem",39:"redeem",41:"wait",43:"redeem",44:"holy",45:"redeem",46:"holy",47:"holy",48:"redeem",50:"servant",51:"redeem",57:"peace",58:"fast",60:"light",62:"light",63:"redeem",64:"holy"};
  Object.entries(map).forEach(([n,key])=>{const c=S[n];if(c&&(!Array.isArray(c.connections)||c.connections.length===0))c.connections=[V[key]];});
  // Every chapter must now have at least one real Scripture connection. If a future edit leaves one empty, use a thematically broad, actual Scripture anchor rather than prose.
  Object.keys(S).forEach(n=>{const c=S[n];if(!Array.isArray(c.connections)||c.connections.length===0)c.connections=[V.holy];});
})();