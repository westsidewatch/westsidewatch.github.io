# 雙聖殿及周邊完整建造盤點（2026-10-30）

範圍基線：68 個工作項，第一聖殿 22 項、希律聖殿及周邊 46 項。這是可追蹤的整體範圍，不宣稱所有古代設施均已獲考古定位。部分工作項包含多間房或整列構件，不等於建築數量。

## 結論與現況

現有兩座聖殿仍是量體及入口階段，尚未形成完整院落系統。已有主殿、前廊、部分側室、平台、院面與南柱廊示意；不能因為院名或物件ID已存在，就把院區列為完成。此次不改網站模型，預覽仍為 81aadade。

唯一候選權威沿用 `data/landmark-building-programme.v1.json`，本盤點是其中 templePrecinctProgramme；不另建可執行生命週期。王宮、安東尼堡、道路等沿用既有候選，清單項目是分解工作，不重複建立建築。

## 不再逐點補丁的施工方式

### A — 雙時期完整配準總平面、肘制對照、院區剖面與尺寸收支；與全城道路地形銜接

每項有位置依據或明確不確定區；不得用500肘方域覆寫擴建平台；無未知高度冒充考古值

### B — 雙時期院牆、院門、臺階、柱廊、主殿及主要祭儀量體整組完成

總覽可辨完整分區、路徑可通、門洞真實、公共院區保持開敞；兩時期一起驗收

### C — 服務房間、水系、池群、地下通路與城市接口統一落地

每項入帳：已建、合併展示、證據不足暫緩附原因；不得靜默遺漏

### D — 全構件分期建造、毀壞及後續同址變化

David／Solomon、第一聖殿後期、流亡、歸回、哈斯摩尼、希律、70年及後世逐段審核；同址不是原物存續

### E — 材質、器物、柱頭、門扇與選看內部；效能及全18期回歸

近景可讀、遠景不超預算；無穿模、懸空、閃爍、標註遮擋與外部模型下載依賴

先凍結整體總平面與分層尺寸預算，再按整組交付。發現新證據可修訂，但需同步標記受影響的院落、道路、高程與分期，不在局部任意放大。未知項列出暫緩原因；「做滿」不等於用假建築填滿空地。

## 全量清單

現況：partial＝部分已有；placeholder＝示意替身；missing＝未有可對應的完整構件。所有項目的歷史幾何准入均未通過。

### 第一聖殿：殿體與圍護

| 項目 | 現況 | 缺口／約束 | 來源鍵 |
|---|---|---|---|
| 主殿與聖所 | partial | 既有27×9×13.5米量體；重核牆厚、內外尺寸及肘制 | kings6-full |
| 前廊與門洞 | partial | 已有門洞；高度與開口為示意，不能當文獻定值 | kings6-full |
| 至聖所及隔斷 | missing | 20肘內部空間與主殿40肘分段，先確認內外尺寸 | kings6-full |
| 三層側室及西側房間 | partial | 六個側向量體不等於完整房間群；補西側與分室 | kings6-full |
| 側室出入口與樓梯 | missing | 核對入口方位、樓層連通及譯文分歧 | kings6-full |
| 屋頂、窗與檐部 | missing | 先完成牆屋交接，後做可見窗與木構 | kings6-full |
| 雅斤、波阿斯及柱頭 | placeholder | 現有方柱，需核對圓柱、柱頭、網飾及高度分段 | kings7-full |
| 內院與大院邊界 | missing | 文獻院牆構造不等於已定位院區平面 | kings6-full, kings7-full |
| 院門、通路與殿前高差 | missing | 無依據不借用第二聖殿院落與門名 | kings6-full, chronicles4 |
### 第一聖殿：祭儀與器物

| 項目 | 現況 | 缺口／約束 | 來源鍵 |
|---|---|---|---|
| 銅祭壇與接近空間 | placeholder | 現有4×4×2.5米為示意，與歷代志20×20×10肘候選比較 | chronicles4 |
| 銅海、十二牛與基座 | missing | 核對10肘口徑、5肘高及東南側相對關係 | kings7-full |
| 十個盆座與十盆 | missing | 兩側各五組，需保留通行與器物尺度 | kings7-full |
| 橄欖木門與柏木門 | missing | 區分內外門、門框與折扇，不能將整殿做成實心 | kings6-full |
| 至聖所兩基路伯 | missing | 內部展示層，不在遠景堆疊金色物件 | kings6-full |
| 香壇、陳設餅桌、燈臺與器具 | missing | 器物清單與數量逐項校核，近景載入 | kings7-full |
| 石材、香柏木、金飾與雕刻 | missing | 最後材質層，不能代替空間建設 | kings6-full |
### 第一聖殿：王室與山城聯繫

| 項目 | 現況 | 缺口／約束 | 來源鍵 |
|---|---|---|---|
| 所羅門居所及王室院落 | placeholder | 沿用既有solomon-palace候選，不能把通用院落當已復原宮殿 | kings7 |
| 利巴嫩林宮 | missing | 沿用lebanon-house；100×50×30肘候選須與殿區共同配置 | kings7 |
| 柱子廊 | missing | 沿用pillars-hall，50×30肘平面，高度未定 | kings7 |
| 寶座廊與審判廊 | missing | 沿用judgement-hall，不虛構確定獨立位置 | kings7 |
| 法老女兒宮殿 | missing | 沿用既有候選，與外邦祭祀高處分開 | kings7 |
| 大衛城—王室—殿山通路及高程 | partial | 現代DEM展示基準不能宣稱古代庭院標高 | cod-guide |
### 希律聖殿：外院與平台

| 項目 | 現況 | 缺口／約束 | 來源鍵 |
|---|---|---|---|
| 擴建平台、擋土牆及角部 | partial | 300×480米矩形參考不等於實測四邊形，先核對邊界 | josephus |
| 外邦人院／外院開放空間 | partial | 不能把主殿以外全部空白都命名外邦人院 | josephus, middot2 |
| 所羅門廊／東廊 | missing | 東側連續柱廊、端部及通行；名稱不證明所羅門原構存續 | john-temple, josephus |
| 北廊與西廊 | missing | 各側柱列、屋蓋與城門間關係 | josephus |
| 南側皇家柱廊 | partial | 既有稀疏柱列與屋蓋，需重核柱網及中側廊高度 | royal-portico-study, josephus |
| Soreg界欄與警告標識 | missing | 邊界層級、通行口及短欄，不能做成城牆 | middot2 |
| Hel環帶及十二級階梯 | missing | 10肘帶寬；此十二級與殿前十二級不同 | middot2 |
| 外院環行與朝聖集散 | missing | 建立各入口到院區路線，不用滿鋪建築填公共空間 | middot2 |
### 希律聖殿：內院、門與高程

| 項目 | 現況 | 缺口／約束 | 來源鍵 |
|---|---|---|---|
| 婦女院 | partial | 現有135×135肘院面，補真正邊界與高程 | middot2 |
| 婦女院四角用房 | missing | 離俗者、木、潔淨與油酒用房；西南用途傳承分歧保留 | middot2 |
| 婦女院周邊看臺 | missing | 文獻後增構件，不能無分期從頭出現 | middot2 |
| 十五級半圓階與利未人位置 | missing | 與殿前12級分開；不能在同一標高貼階梯 | middot2 |
| 尼迦挪門及兩側用房 | placeholder | 現有通用門洞不等於具名門；補衣服與餅房關係 | middot1, middot2 |
| 以色列院 | missing | 11肘帶寬、與祭司院邊界及分歧標高 | middot2, middot5 |
| 祭司院及利未人臺 | partial | 現有整塊內院未作11肘區帶和儀式界線 | middot2, middot5 |
| 內院南北諸門與西側門問題 | missing | 七門與十三門傳承先列表比較，不強行合成一套 | middot1, middot2 |
| 院下樂器用房 | missing | 開向婦女院，須與15級階及樓板共用剖面 | middot2 |
### 希律聖殿：祭壇與服務設施

| 項目 | 現況 | 缺口／約束 | 來源鍵 |
|---|---|---|---|
| 燔祭壇、角、退臺與紅線 | missing | 32肘平面及分層；不能複製第一聖殿小祭壇 | middot3, middot5 |
| 祭壇南側坡道 | missing | 32×16肘候選，與南側通路及祭壇合排 | middot3, middot5 |
| 洗濯盆 | missing | 殿廊與祭壇之間略偏南，保留22肘間距 | middot3 |
| 北側宰牲區、環、柱與桌 | missing | 數量與北側服務帶統一佈置，環列有異說 | middot3, middot5 |
| 排水溝與汲倫方向聯繫 | missing | 只能據證據表示系統；不虛構地下精確管線 | middot3 |
| 鹽、Parvah、洗滌、木／祭司長、汲水、鑿石室 | missing | 六室分項及屋頂浴池；方位須對照版本，不直接照單一英譯定案 | middot5 |
| 火房及四個內室 | missing | 羊、餅、舊壇石及浴池通道分開；非四棟外加住宅 | middot1 |
| 火花門樓與守衛層 | missing | 上層祭司、下層利未人及通向Hel的門 | middot1 |
| 守衛、香料與帷幔等用房 | missing | 逐項研究識別；非每個名稱都有確定平面 | middot1 |
| 水井、浴池、供水與服務通道 | missing | 地上地下分層；隱藏空間選看，不能無證據開挖地形 | middot1, middot5 |
### 希律聖殿：主殿完整建築

| 項目 | 現況 | 缺口／約束 | 來源鍵 |
|---|---|---|---|
| 前廊、門洞及上部梁 | partial | 已有20×40肘洞口，補梁與構造，厚度仍需核對 | middot3 |
| 殿前十二級與平臺 | partial | 已有12級；原文中間平臺及最上層異說尚未落地 | middot3 |
| 聖所、至聖所與分隔 | placeholder | 現有實心主殿不能算內部完成，需40與20肘空間 | middot4 |
| 主殿門扇與兩側小門 | missing | 10×20肘入口、門厚、北通路與封閉南門 | middot4 |
| 三十八側室與西側八室 | missing | 北15、南15、西8；不以六個外殼量體代替 | middot4 |
| 環繞上升通道及上室入口 | missing | 東北到北、西、南的路徑，連接屋頂 | middot4 |
| 上室、女兒牆、排水及屋頂分層 | missing | 總高100肘各層預算，避免只向上疊加而超高 | middot4 |
| 前廊兩翼藏刀空間 | missing | 與100肘前寬、70肘後寬關係統一 | middot4 |
| 燈臺、陳設餅桌、香壇與帷幔 | missing | 不能放第一聖殿約櫃模型進第二聖殿至聖所 | josephus |
| 金葡萄藤、柱式、門材與石砌 | missing | 最後近景層，依來源與可見距離控制密度 | middot3, middot4, josephus |
### 希律聖殿：入口、街道與周邊

| 項目 | 現況 | 缺口／約束 | 來源鍵 |
|---|---|---|---|
| 南側戶勒大門、階梯與地下通道 | partial | 既有接近示意需核對雙／三門各期與人流，現狀不整套回投 | middot1, southern-miqweh |
| 西側出入口、橋與階梯系統 | partial | Wilson／Robinson等考古命名與古代門名分開核實，不自動一一配對 | josephus |
| Taddi、東門及橄欖山方向 | missing | 北門不使用、東側視線與儀式聯繫；不是現存金門直接回投 | middot1, middot2 |
| 安東尼堡與聖域接口 | partial | 沿用antonia；重核角部、地勢、通道與足跡爭議 | josephus |
| 畢士大池及五廊 | missing | 獨立於聖殿院區；池壩、周廊、羅馬及教堂各期分開 | john-temple, bethesda-site |
| 南／西側潔淨池與服務群 | missing | 採已發掘樣本定點；不生成無來源均勻池群 | southern-miqweh |
| 南西側鋪石街、商業接口與排水 | partial | 接既有街道權威資料，商店數量與年代另核 | josephus, southern-miqweh |
| 汲倫谷坡、東側擋土及橄欖山關係 | partial | 保持原始地形比例，不為平台擴大而移山 | josephus, middot2 |
| 與希律宮、上城及朝聖路的聯繫 | partial | 沿用全城既有候選，不將所有宮殿塞進聖殿圍區 | upper-city, josephus |

## 來源與衝突審核

本輪已透過 Sefaria 官方 API 讀取 Middot 1–5 全章；文獻為後期編纂的聖殿描述，不能當作希律期實測圖。其餘為既有工程來源或本輪檢索的研究／遺址上下文，精確位置與尺寸仍需逐項原文及圖版核對。Kings、Chronicles、Josephus、Middot 不混成一份無分歧的「標準答案」。

- `bethesda-site`：https://ste-anne-jerusalem.org/en/bethesda/
- `chronicles4`：https://www.biblegateway.com/passage/?search=2+Chronicles+3-4&version=WEB
- `cod-guide`：https://cityofdavid.org.il/wp-content/uploads/2023/03/Traveler_COD_Eng_2022_lowrez.pdf
- `john-temple`：https://www.biblegateway.com/passage/?search=John+5%3A1-9%3BJohn+10%3A23&version=WEB
- `josephus`：https://penelope.uchicago.edu/josephus/war-5.html
- `kings6-full`：https://classic.biblegateway.com/passage/?search=1+Kings+6&version=WEB
- `kings7`：https://www.biblegateway.com/passage/?search=1+Kings+7%3A1-12&version=KJV
- `kings7-full`：https://www.biblegateway.com/passage/?search=1+Kings+7&version=WEB
- `middot1`：https://www.sefaria.org/Mishnah_Middot.1
- `middot2`：https://www.sefaria.org/Mishnah_Middot.2
- `middot3`：https://www.sefaria.org/Mishnah_Middot.3
- `middot4`：https://www.sefaria.org/Mishnah_Middot.4
- `middot5`：https://www.sefaria.org/Mishnah_Middot.5
- `royal-portico-study`：https://publications.iaa.org.il/cornerstone/vol10/iss1/9/
- `southern-miqweh`：https://publications.iaa.org.il/atiqot/vol85/iss1/9/
- `upper-city`：https://www.gov.il/en/pages/jerusalem-the-upper-city-during-the-second-temple-period

須先裁決：

- 0.45m-first-temple-vs-0.525m-second-temple-cubit-conventions
- internal-vs-external-sanctuary-dimensions
- 500-cubit-sacred-square-vs-expanded-platform
- seven-vs-thirteen-court-gate-traditions
- Middot-service-chamber-direction-translation-comparison
- porch-stair-landings-and-alternative-upper-landing
- source-temple-levels-vs-modern-DEM-display-datum
- first-temple-altar-Kings-vs-Chronicles-and-current-placeholder
- Bethesda-pool-porticoes-vs-later-Roman-and-Christian-fabric

## 分期與交付驗收

第一聖殿不得在大衛階段提前出現；所羅門初建與後期改建區分；巴比倫毀壞不把整套內部默認保存至歸回。歸回與哈斯摩尼階段不能直接複製希律擴建。70年毀壞後，保留、拆除、埋藏與未知逐項有據；同一場所不代表同一構件。畢士大後世建築另有分期，不能將教堂或羅馬設施回投耶穌時期。

每個清單項最終必有「已建／合併呈現／有理由暫緩」處置。檢查實際網格接地、院門淨空、臺階銜接、殿區邊界、排水與通路；近景與移動端可讀，標註留在城市外。18期與17轉場回歸不能替代歷史來源驗收。

效能：遠景合併／實例化重複柱列，內部與微小器具按近景需求建立；固定資料隨網站本地發佈，不在每次載入時查經文API或下載大型外部模型。先量測再定幾何與載入預算，不承諾尚未測得的節省比例。

