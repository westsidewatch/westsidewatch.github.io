# 城防／取水來源與空間缺口

M2 第六批是來源／定位契約，未完成城防或地下水道幾何。從已合併 #1251 主線開始，不另做城市或 Gateway。

原始 `gihon-system-iron-age` 把自然泉、塔、水道彙總為同一高信心構件，並在毀城期統一 ruin。改為待按构件核對的彙總，新增四個獨立 ID：自然基訓泉、泉防禦塔、西丘寬牆、地下水道。自然水源不設定人造 build／統一 ruin；特定塔／牆／水道的後續去向未知時保留 unresolved。沒有把城市毀壞等同每段水工消失。

來源與幾何分開：

- [寬牆遺址說明](https://timeline.cityofdavid.org.il/event/the-broad-wall-an-archaeological-revolution/)支持遺構與晚期背景，未提供本工程可配準的完整牆線。
- [2017 泉防禦塔定年研究](https://weizmann.elsevierpure.com/en/publications/absolute-dating-of-the-gihon-spring-fortifications-jerusalem/)討論中青銅／鐵器時代方案；不直接延用中青銅草模為後代原物件。
- [官方導覽](https://cityofdavid.org.il/wp-content/uploads/2023/03/Traveler_COD_Eng_2022_lowrez.pdf)提供取水與地下水道背景，並非已配準地下中心線／高程。
- [2024 鐵器時代定年研究](https://pubmed.ncbi.nlm.nih.gov/38683984/)列入後續東側牆段及城市擴張定年核對；不將所有城防都歸給單一君王。

`water-defense.registration.v1.json` 統一 ID、來源、年代／去向、geometryStatus 與下一步缺口。兩個現代 OSM 近似地圖點（基訓泉、西丘寬牆）轉入 canonical DEM ENU，僅作 reference point，標明 ODbL attribution。不得擴成牆段、塔基或水道曲線，也不能據此刪除周邊示意住宅。編譯器拒絕未審核 footprint／linework、無來源或無效座標。

Core 與時代資料皆由同一配置衍生，消費者共用一次資料請求。Evidence「城防／取水 · 定位與缺口」呈現同座標來源的兩點參考圖、四個獨立資料狀態、來源及缺口；沒有在3D場景放假牆線或直線水渠。這張圖不是古城平面，未知亦不表示遺構不存在。

驗收：分構件事件、自然泉不隨毀城消失、特定水道去向未知、現代點轉換、未核定線面拒絕、來源／座標失敗、來源去重、帳本重複 ID 拒絕、18期桌面／手機視窗回歸。既有住宅、兩聖殿、近看、毀城與倒退沒有重建。

下一包把既有中青銅水防草模接入共同的年代版本／構件帳本，再依可配準的考古平面建立局部幾何；地下中心線、高程、古取水口與完整城防路線仍待來源核定。M2、全歷史時間軸保持未完成；沒有 Jev／token／硬體效能的新結論。
