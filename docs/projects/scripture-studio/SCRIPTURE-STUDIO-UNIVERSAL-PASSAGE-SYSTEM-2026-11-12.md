# Scripture Studio — 通用經文印章設計系統（V45，2026-11-12）

## 項目定位

系統不是《以賽亞書》62:6 的一張海報；它必須適用於首頁主經文、各版塊主題經文、one／其他查經工具中的經文。**任何特定經文的中文字數、英文詞數、出處高度、行數、框線比例、字帶位置，都不能變成全案預設。** Isaiah 62:6 只是第一個實驗 fixture。

## 必須固定的 OS／工程語法

- 保留中文與 KJV 的原文、章節出處；單一中英出處只寫一次章節數
- 中文 Chiron Hei HK WS、英文 Bodoni Moda 系列（英文斜體需載入及核驗真 Italic 字型，不能 browser synthetic italic 當完成）
- 90° 反轉對應同一母版；不能用兩套分別排好的印面冒充可逆
- 自然斷句優先：USFM 原文／V18 語義保護、詞界候選、人工批准分開；不得把 `Intl.Segmenter` 分詞直接當合法印章字帶
- 沒有貼片底色；結構線不能愈疊愈多，框線數量取決於畫面必要性
- 優先讀性、雙向可讀與防碰撞；充滿方塊是柔性光學目標，不能硬定「90% 以上」
- 英文與中文共享一套真正可度量且可回溯的設計文法，非固定 3–4 中文柱、7 柱或固定頂右位置

## 通用輸入資料結構（已完成）

共用模組：`static/experiments/scripture-studio-passage-model.js`

```js
const profile=ScriptureStudioPassageModel.passage({
  id:'section-topic-01',
  kind:'section', // 'home' | 'section' | 'tool'
  zh:'<中文經文原文>',
  en:'<English KJV exact text>',
  reference:{zh:'<書卷中文>',en:'<Book>',chapterVerse:'<chapter:verse>'},
  segments:{zh:null,en:null}, // V18 審核結果；null=只可用分詞候選試驗
  hardSpans:{zh:[],en:[]},
  breakReview:'unreviewed' // 經編輯確核後才能標 approved
});
```

模組功能：
- `passage`：嚴格檢查語言、出處、語義單元是否完整還原原文
- `referenceLabel`：中英文書卷＋一組章節號
- `tokenBoundaries` 與 `legalBreaks`：針對不同長度經文從字詞界生成 *候選* 可換行點，保護專名／受保護詞組，不能假稱審核成功
- `designParameters`：按內容長度提供類型與視覺密度建議，**不預設行數／硬填滿率**，不綁定某個固定出處位置
- `audit`：語義資料仍未經編輯審核時禁止標記出版準備完成

## 目前程式接入範圍（已完成）

`static/experiments/scripture-studio-motherform-live.html` 現有《以賽亞書》62:6 樣章已接入通用模組；正反面出處的書卷中英文名稱及 `62:6` 由 `scripturePassage.reference` 生成，不再從渲染與引用驗收函式內手工寫死；頁面保留 V43–V44 的語義斷句實驗、真字形排序。通用 QA 已接入 debug 資料。

## 仍未完成的關鍵整合

**目前母版仍以 Isaiah 62:6 的 `zhLines/enLines`、已硬編 V18 軟斷點和那段經文的 Chiron 字型子集做渲染。** 所以本輪完成的是跨經文的資料契約與母版引用橋接，**不是**已經完成更換經文後能正常出版的通用渲染器。

下一施工階段必須：
1. 把 `createFillCandidates()/evaluate()/build()` 完全改用選中 `profile` 的原文與 `legalBreaks`，不再參考 Isaiah-only 全域常數。
2. 建立各經卷字體覆蓋方案；現有 Chiron 12 子集只覆蓋現行樣章，不得用 fallback 字型假裝 OS 正確。
3. 查核所需真正 Bodoni Italic 字型文件、license 與瀏覽器渲染，再決定英文正文 italic 的適用字重和 optical size。
4. 至少以短（單節）、中（版塊）、長（多節）三組**有核對來源**的 CUV/KJV 進行桌面、390px 與印刷的雙向檢查。
5. 將邊框由逐頁固定數量，改成可在「無框／單框／少量必要刻線」之間按閱讀動線選擇；不可讓多餘框線淹沒文字。

## 本輪技術驗證

- 通用 JS 模組語法 PASS
- 主母版內嵌 JS 語法 PASS
- 短／中／長度不同的測試 fixture 參考標籤和動態候選字詞界正常；測試文字是架構 fixture，**不是**由 USFM 審核的聖經原文資料
- 新模組對 `breakReview='unreviewed'` 不會給出出版完成狀態

**總結：** 通用設計系統的標準是「固定法則，可變構圖」，不是讓其他經文配合 Isaiah 62:6 排版模版。

## V46 視覺修正：回應 V45 預覽「畫面沒有改變」

V45 本來只完成資料模型與出處橋接，並沒有執行前一輪要求的英文斜體與減框；用戶提供的 V45 截圖清楚顯示仍有正體英文、重複框線、過大的出處軌。這不能作為已完成的視覺設計。

V46 **實際修改母版** `static/experiments/scripture-studio-motherform-live.html`：
- 將 `applyEngravedStructure()` 從「外框、內框、定位脊、端線」改成僅一個精細方形 SVG 框；移除全部嵌套次框與定位梁。不增加貼片底色。
- 經文英文 `.piece.en` 改用**確實存在的 Georgia Italic 系統斜體路線**，而非仍沿用 Bodoni Moda SC 正體；這是本次的可見字型試驗，**不宣稱已接入正式 Bodoni Moda Italic**。後續找到已授權並驗證的 Bodoni Italic，才可取代測試字體。中文 Chiron 保持。
- 中文＋英文＋章節號保持同一組 citation，縮小字級並收短出處軌（由經文字高和 em 自適應，不固定 Isaiah 62:6 的具體像素）。
- 新版維持首頁／版塊／工具的 passage model 契約，保留 V18 候選及印刷未核准狀態。

**驗證**：主頁內嵌 JS 語法 PASS、共用 passage model JS 語法 PASS；原稿僅存在一個 `applyEngravedStructure`，已確認無 nested-frame 生成程式；英文 italic CSS 存在。**尚缺 V46 真實瀏覽器截圖及字型碰撞驗證**，不能宣稱視覺已驗收。

提交：`cb64fc8d5f8188f311f46d83c768195fcea55f55`。

## V50｜跨經文交錯語法施工（2026-11-12）

此輪改動針對 V49 的實質缺口：多數字帶仍是機械 `ZH–EN` 配對，H4「過半字帶至少兩次語言轉換」不足。**無框、中文 Chiron Heavy/ExtraLight、英文 Bodoni Moda SC 正文、僅出處斜體，以及母版 90° 轉向一律保留**。不增刻線、不改動既有經文內容。

- 共用模型 `static/experiments/scripture-studio-passage-model.js` 新增 `runSignatures(zhUnits,enUnits)` 和 `verifyMixedRuns()`，以有來源的語義單元而非單字數作輸入，生成不同帶數、真正 `Z–E–Z`／`E–Z–E` 及以上的連續交錯字帶。每語原文順序保留，H4 不合格方案不輸出；沒有合法單元就不強造雙語帶。
- 現有 `scripture-studio-motherform-live.html` 排字求解器已改為呼叫**同一個通用模型**；刪除專屬於主頁的重複分配函式，仍使用 V18 以賽亞書 62:6 的語義候選作第一輪實際構圖。
- `evaluate()` 和 `candidateVisualScore()` 的排序把真實雙向碰撞與 H4／H6 放在方形比例之前，光學平衡只在語義與交錯成立後參與排序。
- 輸出診斷現在報告真實多次語言轉換的字帶數，不再把任意「三個片段」錯認為兩次切換。

### 回歸

新的 `static/experiments/scripture-studio-v50-regression.js` 以**合成測試文字（不是聖經原文）**驗證三種長度：短文 2 個構圖候選、中等長度 28 個、長文 57 個。全部來源精確、H4、每帶中英、未批准不得出版 PASS。

以 Isaiah 62:6 目前 V18 研究候選進行純程式碼測試：236 組可供排版測量的交錯構圖，每組中英來源還原正確，H4 結構檢查通過；使用*近似而非真實字型*的字寬模型，200 組達 H6，這不等於真正的字型驗收。

**未完成**：真實瀏覽器兩面截圖及肉眼光學驗收、Chiron 跨經文完整字庫、正式經文分詞編輯核准、Bodoni Moda 真正斜體字型，以及其他主題經文的完整印面渲染。新的模組可用於其他輸入，但目前 live 頁仍展示 Isaiah 樣章，不能聲稱七版塊已自動套版或作品達得獎標準。

工程：`cf7c8abdf109e602fe515a67de7afdff2fe9658a`、`c5f0ebb02c31018db8e4e98819af28163119370f`、`97e0dc8769b6129a4082b4f21d00bb0a088d135a`、`2ca980c4545a970a20cc28e360e0a71b8ad73426`、`467a64416bf794c15322115afa87b9e50587092f`。

## V51｜現代聖經出版編輯構圖（2026-11-12）

**設計參照**：Byble Matthew／Genesis 的字形重心與比例、Magnify Magazine Tokyo 的雙文字方向秩序、She Reads Truth 的經文正文／出處層次。這些參照並不是現成的雙向 90° 中文英文合版印刷演算法；不複製其攝影、色塊或裝飾。

**本輪實際修改的工程**：`static/experiments/scripture-studio-motherform-live.html`

1. 新增「Editorial／經文主導」和「V49／飽滿母版」的實際可操作版面切換，並把 V49 的候選池、36 組初選、字體、經文片段與來源順序原樣保留。
2. `editorialSelect()` 在既有 V49 **真實瀏覽器 DOM 字形雙面覆蓋率**測量基準上選構圖。新增強制安全閘：中文、英文任一面的可見文字框覆蓋均不得低於 V49 最佳候選的 97%；選出的方案不能增加 V49 的 DOM 碰撞計數；原本的候選 `fillEstimate` 也不得低於基準 97%。未找到更好的合法方案就退回 V49，不再進入 V50「為增加 H4 切換而把方塊變成狹長字群」的路徑。
3. 只有在上述閘成立後，才評估多次交錯、非平均文字量、疏密節奏與兩面光學平衡。這並非讓 H4/H6 變成可忽略的通過條件：若無通過 H4/H6 的合法候選，仍要保留研究樣章／不可匯出的狀態。
4. 刪去三個實際無效的「構造線 A/B/C」UI 選項，固定無框印面；英文**正文**保留 Bodoni Moda SC、中文 Chiron Heavy 900／ExtraLight 200；**只有英文書卷出處和章節號**為 400 italic，未把正文誤改斜體。
5. 版面診斷新增 V49 雙向填充保護 PASS/FAIL，`window.__scriptureCandidateQA` 保存兩面基準覆蓋與本輪挑選的覆蓋數值，以供後續實際瀏覽器截圖驗收。

**已測**：內嵌 JS 和共用經文模型語法 PASS；V18 原文候選仍有 259 組、全數中英完整復原、無孤字，字帶搜尋 1–9。**未測**：因本次環境無法連接預覽網域取得真實字型與 Chromium 畫面，不能聲稱 V51 比 V49 更美、更飽滿或已通過 V14。**如編輯模式不能在不破壞 97% 基準的情況下選出更好方案，應回退 V49，不能強行破壞既有成果**。

本輪是實際母版排版算法改動，不是對七個版塊的跨經文完整渲染。跨經文排字仍須繼續接入字庫及核准斷點。

提交：`29435efa6f62310d06574291dc6461f53f2ddb47`、`19e2fd9cc57b4334bf2fbee000057fcebca2a030`、`11fc5ee6f912006e9b49d24bef619c08541fa8e9`、`3ad2296b50d2fbee6fb239392490aa7f67ea3ad6`。
