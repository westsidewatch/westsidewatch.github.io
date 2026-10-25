# Jerusalem 3000：18期／17段空間缺口矩陣

渲染基準：`e5da00d04`。此表是工程盤點；整體歷史基礎尚未驗收，建築細雕暫停。

數字 `登記／地圖` 表示帳本登記數／當前有效且可定位的骨架圖對象。帳本可能含前期留下的未明去向記錄，並受逐期生成順序影響，不能當作城市規模。地圖為零不代表建築不存在；公共核心欄只盤點目前 monument 分類，不能涵蓋所有建築語義。

共同地圖窗口：X[-2000,1100]、Z[-1300,1300] 公尺；使用現代DEM，非古地表。

## 18期空間矩陣

| 時期 | 分區 | 路徑 | 水防 | 公共核心 | 佔用可見綁定 | 未明事件 | 主動對象缺少幾何 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 最早聚落 | 0／0 | 6／6 | 0／0 | 0／0 | 14 | 0 | 0 |
| 迦南城市 | 0／0 | 12／6 | 4／3 | 0／0 | 24 | 21 | 0 |
| 晚青銅—鐵器早期 | 0／0 | 12／6 | 2／0 | 0／0 | 24 | 32 | 0 |
| 大衛—所羅門 | 3／2 | 19／13 | 8／6 | 4／3 | 24 | 32 | 2 |
| 第一聖殿晚期 | 7／4 | 19／6 | 9／2 | 4／3 | 1104 | 46 | 2 |
| 巴比倫毀城 | 5／4 | 6／6 | 4／1 | 4／3 | 1104 | 4 | 1 |
| 波斯—尼希米 | 9／3 | 10／4 | 4／2 | 5／1 | 189 | 1172 | 3 |
| 希臘化—哈斯蒙尼 | 5／1 | 12／8 | 3／0 | 1／0 | 1534 | 2660 | 2 |
| 大希律—耶穌 | 6／0 | 20／10 | 3／0 | 5／3 | 1067 | 3235 | 3 |
| 羅馬毀城 | 1／0 | 10／10 | 0／0 | 5／3 | 1067 | 0 | 2 |
| Aelia Capitolina | 3／2 | 13／3 | 0／0 | 4／0 | 32 | 2300 | 0 |
| 拜占庭 | 6／4 | 6／3 | 0／0 | 0／0 | 53 | 37 | 0 |
| 早期伊斯蘭 | 8／4 | 6／3 | 0／0 | 0／0 | 56 | 60 | 0 |
| 十字軍 | 8／4 | 8／5 | 0／0 | 0／0 | 40 | 63 | 0 |
| 阿尤布—馬穆魯克 | 9／5 | 9／4 | 0／0 | 0／0 | 45 | 49 | 0 |
| 奧斯曼 | 12／6 | 9／5 | 3／0 | 0／0 | 53 | 54 | 4 |
| 城外擴張 | 17／9 | 14／8 | 3／0 | 0／0 | 97 | 64 | 5 |
| 現代耶路撒冷 | 23／11 | 18／9 | 3／0 | 0／0 | 142 | 114 | 7 |

佔用可見綁定是已登記 block／parcel／building 的模型數，不是歷史住宅數。事件未明是現有事件投影狀態，不等同於未綁定或資料錯誤。完整對象ID、分類與幾何缺口見 JSON。每期六域的審核狀態保留自計劃，數量不自動提升驗收。

## 優先順序與交付門檻

1. **既有對象定位與分類**（existing-spatial-bindings）— 先核對已登記分區、道路、水防及核心的幾何與分類；明確暫緩定位的對象保持缺口，避免重建已有模型。 驗收門檻：每項具備適用來源的可用幾何，或明確暫緩決定；驗證場景／地圖身分與篩選恢復。
2. **早期四期分區基礎**（early-period-districts）— 統一最早聚落至大衛—所羅門四期的分區、路徑與佔用範圍，各期保留獨立年代與地形關係。 驗收門檻：零登記不等於歷史不存在；範圍、年代和未知邊界均需明示。
3. **希臘化獨立骨架**（hellenistic-independent-foundation）— 以獨立來源約束分區、入口及公共核心，替換希臘化時期的參考城衍生骨架。 驗收門檻：不能把縮放希律城或複製圍牆作為本期依據。
4. **後期六期水防與公共核心**（later-water-civic-foundations）— 成組規劃Aelia至鄂圖曼六期的防禦、水系與公共核心，再進入建築深化。 驗收門檻：預留空區不算完成核心；城牆年代及座標依據必須明確。
5. **現代覆蓋範圍**（modern-coverage）— 成對補足城外擴張／現代的東部及遠端地區與交通脈絡，明示各層年代範圍。 驗收門檻：西側局部窗口不算完整城市，也不代表政治邊界。
6. **17段接續驗收**（adjacent-transition-acceptance）— 逐段審核17段接續的保留、新建、毀壞、退出與未知去向，驗證反向還原。 驗收門檻：共同ID、外觀相似、原型保留百分比或切換測試均不能證明歷史存續。

既有區位核對已完成，來源要求暫緩的對象仍保留缺口。下一包：**early-period-districts**，早期四期分區／路徑／佔用基礎。

## 17段相鄰接續

下面只比較四類骨架圖對象ID的出現。共同ID不等於已證明存續，僅前期／僅後期不等於拆除／新建；不含全部佔用或不可定位對象。所有接續歷史驗收仍為 false。

| 接續 | 共同地圖ID | 僅前期 | 僅後期 | 審核狀態 |
| --- | ---: | ---: | ---: | --- |
| chalcolithic-early-bronze → middle-bronze | 0 | 6 | 9 | unresolved |
| middle-bronze → late-bronze-iron1 | 0 | 9 | 6 | unresolved |
| late-bronze-iron1 → david-solomon | 0 | 6 | 24 | unresolved |
| david-solomon → late-first-temple | 4 | 20 | 11 | partial |
| late-first-temple → babylonian-destruction | 14 | 1 | 0 | partial |
| babylonian-destruction → persian-nehemiah | 1 | 13 | 9 | partial |
| persian-nehemiah → hellenistic-hasmonean | 0 | 10 | 9 | unresolved |
| hellenistic-hasmonean → herodian-jesus | 0 | 9 | 13 | unresolved |
| herodian-jesus → roman-destruction | 13 | 0 | 0 | partial |
| roman-destruction → aelia | 0 | 13 | 5 | unresolved |
| aelia → byzantine | 0 | 5 | 7 | unresolved |
| byzantine → early-islamic | 0 | 7 | 7 | unresolved |
| early-islamic → crusader | 0 | 7 | 9 | unresolved |
| crusader → ayyubid-mamluk | 0 | 9 | 9 | unresolved |
| ayyubid-mamluk → ottoman | 0 | 9 | 11 | unresolved |
| ottoman → outside-walls | 0 | 11 | 17 | unresolved |
| outside-walls → modern | 0 | 17 | 20 | unresolved |

17段都需檢查有年代的來源、具體對象去向、地形／幾何適用期和正反向投影；既有17條舊繼承規則與局部反向測試不能代替這項驗收。

## 各期範圍與缺口

- **最早聚落**：Illustrative early dwellings and footpaths share atomic object/event registration; later fate remains unresolved. Selected royal/water IDs have separate adapters. District foundations, disputed support and marker registration remain incomplete.
- **迦南城市**：Illustrative early dwellings and footpaths share atomic object/event registration; later fate remains unresolved. Selected royal/water IDs have separate adapters. District foundations, disputed support and marker registration remain incomplete.
- **晚青銅—鐵器早期**：Illustrative early dwellings and footpaths share atomic object/event registration; later fate remains unresolved. Selected royal/water IDs have separate adapters. District foundations, disputed support and marker registration remain incomplete.
- **大衛—所羅門**：Illustrative early dwellings and footpaths share atomic object/event registration; later fate remains unresolved. Selected royal/water IDs have separate adapters. District foundations, disputed support and marker registration remain incomplete.
- **第一聖殿晚期**：Independent inferred districts and residential publication exist; routes, defenses and all predecessor/successor fates are incomplete.
- **巴比倫毀城**：Independent inferred districts and residential publication exist; routes, defenses and all predecessor/successor fates are incomplete.
- **波斯—尼希米**：Independent inferred districts and residential publication exist; routes, defenses and all predecessor/successor fates are incomplete.
- **希臘化—哈斯蒙尼**：Layout derives from a reference footprint; independent period baseline and predecessor mapping missing.
- **大希律—耶穌**：Canonical city and destruction projection exist; incoming Hellenistic and outgoing Aelia changes are incomplete.
- **羅馬毀城**：Canonical city and destruction projection exist; incoming Hellenistic and outgoing Aelia changes are incomplete.
- **Aelia Capitolina**：Independent authored district/path skeleton and terrain-following coarse occupied cells replace the old mass grid. Geometry remains inferred, not archaeological survey; city limits, water/defense, dated subphases and public-building footprints remain incomplete.
- **拜占庭**：Independent authored district/path skeleton and terrain-following coarse occupied cells replace the old mass grid. Geometry remains inferred, not archaeological survey; city limits, water/defense, dated subphases and public-building footprints remain incomplete.
- **早期伊斯蘭**：Independent authored district/path skeleton and terrain-following coarse occupied cells replace the old mass grid. Geometry remains inferred, not archaeological survey; city limits, water/defense, dated subphases and public-building footprints remain incomplete.
- **十字軍**：Independently authored district/path envelopes, DEM-following coarse cells and reserved cores now share scene, ledger and comparison map. Geometry remains illustrative/composite, not surveyed; actual wall/water networks, public buildings and adjacent survival are unverified.
- **阿尤布—馬穆魯克**：Independently authored district/path envelopes, DEM-following coarse cells and reserved cores now share scene, ledger and comparison map. Geometry remains illustrative/composite, not surveyed; actual wall/water networks, public buildings and adjacent survival are unverified.
- **奧斯曼**：Independently authored district/path envelopes, DEM-following coarse cells and reserved cores now share scene, ledger and comparison map. Geometry remains illustrative/composite, not surveyed; actual wall/water networks, public buildings and adjacent survival are unverified.
- **城外擴張**：Paired inferred old-city background, extra-mural districts and connectors share DEM, ledger and comparison. Coverage is a local western-environs window, not the complete modern city; exact walls, public cores, eastern/distant districts and historical adjacent survival remain unresolved.
- **現代耶路撒冷**：Paired inferred old-city background, extra-mural districts and connectors share DEM, ledger and comparison. Coverage is a local western-environs window, not the complete modern city; exact walls, public cores, eastern/distant districts and historical adjacent survival remain unresolved.

## 重製

先執行全18期瀏覽器檢查，再以報告生成矩陣：

```sh
node scripts/audit_jerusalem_3000_foundation_gaps.mjs --report work/j3k-validation/phase-report.json --render-commit <captured-render-commit> --out work/j3k-validation/foundation-gap-audit
```

輸入報告與計劃的 SHA-256 記錄於 JSON；這是固定基準快照，不是假定永遠最新的即時狀態。CI 會從當次瀏覽器報告產出新矩陣，不額外載入網站資料或生成場景。
