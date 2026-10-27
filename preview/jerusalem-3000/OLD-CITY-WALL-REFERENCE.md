# 後期城牆、城門與舊城約束

2026-10-26。承接整體工程的城界／城門缺口，將現代可定位輪廓、舊城住宅約束及城門動線一起接入。這不是把現代城牆回推為所有時代的城界。

## 資料與年代

本包取自[OpenStreetMap官方API](https://api.openstreetmap.org/api/0.6/map?bbox=35.222,31.770,35.242,31.785)，保存七條外牆way的216個來源點、版本和時間戳；另保留雅法門node與大馬士革門way。原始子集約41KB、衍生JSON約37KB。整個12MB檢索範圍沒有進入網站；網站僅一次載入衍生JSON，不在切期時查詢外部API。授權與歸屬為© OpenStreetMap contributors、ODbL。

年代語境：[Jerusalem Foundation](https://jerusalemfoundation.org/old-project/old-city-walls/)與[IAA Mount Zion發掘報告](https://hadashot.iaa.org.il/Report_Detail_Eng.aspx?id=25008&mag_id=124)將目前舊城城牆的重建置於蘇萊曼時期。這只支持年代與構造語境；現代OSM線位不是1535–1542年的測繪復原，歷代修補、城門改建與開口不能默認相同。

外牆選取排除了聖殿山內部及南側擋土線，避免把所有city_wall標記拼成假城界。七條來源線保留一個約13.082米的現代開口，不繪製補線。為約束住宅而閉合的包絡只是規劃範圍，不能當作新增牆段或行政邊界。

`ingest_jerusalem_3000_wall_reference.py`以凍結XML離線重製JSON，記錄原始子集SHA256。CI要求重製資料完全相同；不在測試中下載會變動的地圖。

## 同一整體場景

- 僅在鄂圖曼、城外擴張、現代三個階段顯示，三期使用同一批城牆網格和原有wall/gate物件ID；現有生命週期事件不改寫。這是選定後期參照，不能代表1517起每一年的精確外觀。
- 城牆表示高度10米、厚度2.5米純屬模型設計，並非來源測量。每8米內分段貼合共同現代DEM，避免長段被中途山坡遮沒；未改動地形、也沒有由此復原古地表。
- 兩個城門只作地圖位置標記：雅法門用來源node，大馬士革門用來源建築輪廓頂點平均位置。沒有將門點假作城門建築測繪，也未添加新門等其他城門的年代模型。
- 舊城住宅依參照包絡裁切；城內示意道路不在包絡外繼續顯示。城外擴張地區保持獨立，鄂圖曼→城外擴張→現代的共同舊城裁切結果必須完全一致。
- 加入兩個城門至既有主街的設計連接，城外西向／西南連接改從雅法門參照點出發。連接線未測繪，不能稱為歷史街道原線；它們是共同城市骨架的示意動線。
- 共同骨架圖新增多段線表示，一個wall物件仍只計一次。來源七條線分開繪製，不能連接空隙。住宅、地圖來源與模型表示的數量不能當作歷史人口或構件數量。

幾何表示以inferred篩選；保留原本歷史存在證據為observed的來源欄位。geometryVerified=false，古代幾何與個別構件存續仍未核定。先前幾何缺口中這三項現在有現代參照，但考古／歷史測繪需求並未因此結案。

## 驗證與剩餘工作

單元測試要求凍結來源可重製、七段外牆與原始開口完整、211個穩定顯示組件、前15個階段不出現此牆、三期正反向使用同一模型、證據篩選往返、生命週期完全不變；住宅與城內道路落在參照包絡、兩條城門連接起點正確，三期共同舊城一致；資料失配失敗不得留下場景殘件。

18期／手機瀏覽器核對三期可見城牆、三個綁定水防物件、無前代洩漏或無登記組件；缺口矩陣可重新產生。

其他時代城界、完整城門與主街網、宗教核心—街區關係，以及固定方格住宅替換仍需按全線清單繼續處理。本包不是全18期城防或歷史城市延續性驗收；foundationAccepted保持false。

### Religious core positions and approaches

The late three phases also use modern OSM building-bounds centres for the Holy Sepulchre (way 1022672085 v14) and Dome of the Rock (way 4709536 v102). The frozen source is `data/urban/sources/old-city-cores.osm.xml`; `scripts/ingest_jerusalem_3000_core_reference.py` reproduces `core-location-reference.js` offline, using Decimal bounds midpoints rounded to seven decimal places. © OpenStreetMap contributors, ODbL. Source API and raw SHA-256 are embedded in the generated reference.

Only the position of the existing illustrative mass changes. Dimensions, orientation and profile remain authored, and a modern bounds centre is not an ancient footprint survey. Two authored approaches join existing illustrative axes to the edge of these masses; they are not traced historical streets. Housing exclusions and persistent phase generation consume the same positions. Earlier periods retain their prior contextual positions pending separate evidence; no modern footprint is back-projected. The southern sanctuary/precinct and complete historical street network remain unresolved.
