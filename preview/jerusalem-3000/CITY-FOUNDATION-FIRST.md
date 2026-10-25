# Jerusalem 3000：先完成全線基礎，再深化建築

2026-10-22 修訂。此文件取代「下一包繼續住宅入口／屋頂細化」的工作順序；現有模型保留為可重用成果。基準為 118f92c4b，PR #1271 尚未合併。

## 判斷與現況

最近的低層住宅、材質和坡地修正解決了局部問題，但已提前進入建築深化。全線共同變遷基礎尚未完成，此時繼續細化容易在後續整合時重做。

18 個時代能顯示、瀏覽器測試通過，代表程式可以切換，不能代表 18 個時代已構成同一座城市的連續歷史。共同地形與座標已有基礎；共同物件帳本、生成發布及毀壞回放只覆蓋部分對象和時段。

| 範圍 | 已有基礎 | 仍需統一 |
| --- | --- | --- |
| 最早聚落、迦南、晚青銅、大衛—所羅門 | 各期早期景觀；部分王城、水防物件共用身分 | 全住區、道路及相鄰期去向 |
| 第一聖殿晚期—巴比倫—波斯 | 獨立示意住區、共同住宅發布、毀壞與保留遺跡；波斯有獨立重建 | 所有道路、水防、公共區域的命運與前後銜接 |
| 希臘化—哈斯蒙尼 | 共享生成器的暫定骨架 | 不依賴縮放參考城的時代骨架；與波斯、希律銜接 |
| 希律—羅馬毀城 | 共同城核心與毀壞投影；目前最完整的局部 | 向前接希臘化，向後接 Aelia；全域變遷驗收 |
| Aelia—拜占庭—早期伊斯蘭—十字軍—阿尤布／馬穆魯克 | 可見的各期形態與地標 | 共同核心所有權、各層骨架及相鄰期存續／替換 |
| 奧斯曼—城外擴張—現代 | 各期形態與城市擴張示意 | 同一帳本中的保留舊城、擴張區與道路變遷 |

以上是程式工程盤點，不是歷史範圍的考古認證。每一期六類城市骨架的正式基礎驗收均尚未完成。

## 地貌先決條件（2026-10-23補充）

統一基礎首先要讓共同山地可讀。沿用同一DEM與原始垂直比例，呈現山脊／谷地、聚落落地與道路高低關係，再整合各期骨架。見 MOUNTAIN-LANDSCAPE-FOUNDATION.md。現代地表不等於古代地表；展示地形與復原古地形必須分清。

## 統一基礎應做到什麼

每一期都使用同一套六類結構：住區範圍、主要路徑、水與防禦、聖域與公共核心、聚居量體、生命週期。先以輪廓、帶狀道路和簡單量體表達；屋門、柱式、牆紋與屋頂小構件不在此階段。

資料不足時允許明確標示「未知／暫不繪製」，不必為了鋪滿畫面捏造城牆或道路。可驗收的是留白決策、表示方式、共同身分與時段規則，而不是把未知變成歷史確定性。此處的「統一」是共同資料與變遷契約；不同時代仍需各自的範圍和城市結構，不複製希律城當作全時代模板。

17 段相鄰變遷逐段交代：哪些對象保留、哪些新增、哪些毀壞、哪些退場、哪些去向未知。存續者保持 ID；重建者使用新 ID，只有證據支持時才加重用關係。未有證據的繼承不以位置接近代替。現代地形上的建模適配不算古代台地證據。

## 接下來的順序與交付

1. **F1 全線盤點與契約（本包）**：把 18 期、17 段接續、六類骨架與缺口列入同一份機讀清單。CI 檢查漏期、錯序、漏類及無證據的驗收標記。輸出是規劃與驗收依據，本包沒有新增可見城市模型。
2. **F2 共同骨架接入**：先建立所有時代一致的骨架輸出、核心發布／清除與診斷介面，再逐期接入現有生成器。重用模型；拆開「歷史對象」和「當期顯示網格」。優先處理跨生成器斷點：波斯→希臘化→希律、羅馬毀城→Aelia，再向後接至現代、向前接至最早聚落。每一包都跑全線回歸。
3. **F3 全程變遷**：在相同骨架上完成 17 段存續／新增／毀壞／退場／未知規則與反向重建。處理路網、住區、公共核心和水防的整體關係；先補輪廓與量體，暫不雕刻單棟住宅。
4. **F4 全線基礎驗收**：固定同一地圖視角，產生 18 期總覽與 17 段前後對照；檢查身分、證據篩選、往返時間、無重複層、資源釋放及桌面／直向顯示。全部六類與17段均有可查的驗收記錄，才解除細化暫停。
5. **D1 分級深化**：先深化能改變城市辨識的大地標、城界、道路與住區密度，再做代表街區，最後才是入口、屋頂與材質。細化應替換對象的表示層，不能再改寫整個時代的座標或物件身分。

F2/F3 可按相鄰時段分包，但每包都服從完整清單並驗證全線，不另開平行城市系統。若發現有確切來源的基礎幾何缺口，優先修正，不把整座城市進度綁在單一建築的精度上。

## 省用量與驗收界線

保留既有模型、帳本及資料快取；未改動的資產不重新生成，不下載重複來源圖。日常修改先跑契約／受影響投影測試，實際改動顯示或變遷時再做全線瀏覽器驗證。一次全線對照定位問題後再集中修正，避免反覆進入同一住宅。

本包的清單只供工程／CI 使用，沒有新增網站執行時請求。這不是已量測的 token、GPU 或下載流量節省。Hermes + JevSkills 的既有入口在目前會話仍不可調用，不能聲稱本包已經走 Jev。

機讀清單：data/city-foundation-plan.v1.json。檢查器：scripts/verify_jerusalem_3000_foundation_plan.mjs。清單通過表示盤點結構完整；不表示城市基礎、歷史認證或整體工程已完成。細化暫停是工作順序約束，目前不會攔截所有程式修改。

2026-10-23 F2第一包已接入共同地表取樣、18期入口與六類只讀檢查，並修正後期進度錯接；見 FOUNDATION-RUNTIME-INTERFACE.md。這不等於所有模型已發布至共同帳本，18期與17段驗收狀態仍未完成。下一步依缺口接入穩定物件身分與未知去向，繼續暫停建築細化。

2026-10-24 步驟1進度：共用物件包／事件載入、修復期別替換索引，並對齊六個希律來源模型的毀城期別。見 PHASE-REGISTRATION-FOUNDATION.md。這是共同規則與已知錯配的修正；早期／希臘化／後期未登記生成層仍需批次接入，不能視為步驟1全部完成。

## Hellenistic shared registration (2026-10-24)

Existing generated districts, roads and residences now publish atomically into the common ledger. All 32,754 visible components bind to stable IDs; later fate is unresolved. This is a reference-derived scaffold, not a surveyed historical layout. See HELLENISTIC-LEDGER-FOUNDATION.md. Step 1 and overall foundation acceptance remain incomplete.

## Early settlement batch registration (2026-10-24)

The four early-era dwelling/footpath batches now share canonical object IDs and lifecycle events. Later fate is explicitly unresolved; source defense adapters retain ownership and disputed/location symbols remain outside this publication. No new geometry or invented district/parcel parentage. See EARLY-SETTLEMENT-LEDGER-FOUNDATION.md. Full foundation acceptance and step 1 remain incomplete.

## Crusader/Ottoman batch registration (2026-10-24)

Both later morphology generators now publish stable phase-scoped scaffold identities and unknown next-era fates. Renderer rebuilds rebind the same definitions and preserve ledger event edits. Anonymous masses remain blocks rather than semantic buildings; inherited layers are still provisional. See LATER-MORPHOLOGY-LEDGER-FOUNDATION.md. Step 1 and whole-foundation acceptance remain incomplete.

## Remaining footprint batch registration (2026-10-24)

Six later-era footprint batches now publish 234 inferred block masses through the shared publisher. Existing generator definitions are extracted for direct tests, preserving geometry. Static event/evidence visibility restores on filter return; provisional inheritance remains unbound. See LEGACY-FOOTPRINT-LEDGER-FOUNDATION.md. Full adjacent-era transformations and foundation acceptance remain incomplete.

## Legacy inheritance transition audit (2026-10-24)

The 17 legacy display transitions now expose adjacent vs source phases, generator gaps and unverified retention policy. Every displayed overlay component has a separate trace ID; it remains provisional/unbound, with no fabricated source-object lineage. Scene notes disclose the illustration. See INHERITANCE-TRANSITION-AUDIT.md. This audit does not replace shared object events or certify historical transitions.

## Evidence and annotation consistency (2026-10-24)

Legacy inherited overlays now obey the common evidence policy as inferred content, including filter return and phase suppression. The 21 remaining early display components have explicit annotation roles and remain outside semantic city registration. Foundation counts disclose those annotations separately. See EVIDENCE-ANNOTATION-FOUNDATION.md. Historical geometry and whole-timeline acceptance remain incomplete.

## Canonical generated event registration (2026-10-24)

The Herodian generated batch now declares shared build/schematic ruin-or-transform/unknown-fate events and registers its eight provisional road IDs. Parent references are normalized; source-anchor events remain untouched. Finished meshes read shared event visibility. Foundation inspection lists remaining missing-event IDs rather than concealing gaps. See CANONICAL-GENERATED-EVENTS.md. Full foundation acceptance remains incomplete.

## Source scopes and registration accounting (2026-10-24)

Seven source relations/withheld entries now explicitly declare why no physical events belong to them. Live anchor context remains separate from their own history. All-era accounting distinguishes these declarations from unclassified event gaps and distinguishes annotated/provisional display components from unexplained unbound scope. See SOURCE-SCOPE-ACCOUNTING.md. This is an engineering checkpoint, not historical foundation acceptance.
