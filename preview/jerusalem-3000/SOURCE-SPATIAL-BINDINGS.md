# 既有核心、水防與分區定位核對

本包核對上一份18期矩陣的19個不同「當期有效但沒有可畫幾何」ID。現有希律來源包的 spatial 欄原本沒有傳入共同帳本，因此概略區位雖已存在，骨架圖仍缺表示。本包保留來源欄並接回五個推定區位點，沒有新增模型、建築、城牆線或歷史存續事件。

## 五個接回的來源區位

來源：[objects/herodian-30ce.json](data/objects/herodian-30ce.json)。平台包絡、皇家柱廊、安東尼亞共三個公共核心點；南側進路、西側街道共兩個路徑區位點。兩個路徑點不構成道路走線，三個核心點不構成建築輪廓。它們不是從現行3D網格推算的測量結果。

轉接時校驗既有 local ENU 與地理錨點在固定 canonical 原點的一致性（容許來源四捨五入誤差1m），並驗證位於同一DEM內。這是座標內部一致性檢查，不是歷史定位達到1m精度。高度仍取現代DEM，不補古地表。

原始幾何狀態、來源信心、物件ID、事件與分類保持原值；只有地圖區位表示一律降為 inferred。實證篩選不顯示這些點，全部／推定可顯示。只有來源本身的希律與羅馬毀城有效事件可畫；Aelia未明去向不能沿用。內殿雖有平台共同錨點，其 registration 明列 withheld-exact-placement，因此不畫點；東側入口也繼續暫緩定位。

## 其餘14項的處置

| ID（省略 j3k:object: 前綴） | 決定與需要的依據 |
| --- | --- |
| j3k:district:western-lower-city | 原始範圍要求歷史街區重建；不借用生成住宅包絡冒充來源分區 |
| southeastern-ridge-iron-age | 保留來源要求的暫緩範圍，不借用王城示意區包絡 |
| persian-settlement-envelope | 保留來源要求的暫緩範圍，不把波斯示意生成區當考古邊界 |
| royal-monumental-zone-10c | 保留爭議與暫緩定位，不借王室模型中心確認候選遺址 |
| inner-temple | 精確位置暫緩，不以聖殿山中心代替內殿位置 |
| siloam-water-tunnel | 保留尚待來源線圖配準的缺口，不使用無關平面或猜測地下走線 |
| nehemiah-wall | 需要分段年代與變體，不能直接連成確定城界 |
| ottoman-wall | 等待測繪線圖；不恢復舊規則矩形圍牆 |
| damascus-gate-ottoman、jaffa-gate-ottoman | 等待來源測繪足跡／定位，不以示意街端當城門中心 |
| old-city-fabric-ottoman | 需要歷史地圖配準；六個設計分區僅是模型背景 |
| modern-old-city-preserved | 需要現行調查範圍；不把保留背景等同每棟實物存續 |
| modern-metropolitan-envelope、modern-road-fabric | 需要現行地理資料；西側局部窗口不代表完整城市與道路網 |

依據為 [anchor-era-packs.json](data/anchor-era-packs.json)、[希律城市來源](data/urban/herodian-30ce.city.json)、[水防登記](data/urban/water-defense.registration.v1.json) 與希律物件包內的明確幾何要求。這些是工程處置，不提升任何考古認證或基礎驗收狀態。

## 驗證與後續

測試以真實來源包核對五點、共同原點與地理／ENU差異、DEM邊界、內殿及東側入口暫緩、希律／羅馬／Aelia事件，以及推定篩選的精確恢復。全18期瀏覽器檢查同樣要求僅希律和羅馬出現五個來源點。網站沿用已快取來源包，沒有新增資料請求。

下一包按矩陣進入早期四期的分區／路徑／佔用基礎：先完成範圍和山地關係，再深化地標。真實水防走線、來源分區邊界與公共建築輪廓仍按上述資料門檻逐項推進；建築細雕暫停，整體歷史基礎仍未驗收。
