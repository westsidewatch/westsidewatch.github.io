# 多雷製片手冊 · Doré Production Handbook

> 工程狀態：Canonical working doctrine
> 建立：2026-09-12
> 適用：Doré Static Cinema / AW Camera Core / Golden Camera Spine

## 1. 製片基本原則

多雷不是把靜態原作「動畫化」，而是把原作當作一個等待攝影機進入的世界。

**Source Before Synthesis. Camera Before Animation. Depth Before Hallucination.**

1. 原作是 canonical world，也是可見像素的最高 authority。
2. 16:9 是 Static Cinema 的 master camera viewfinder；8:5 可作網站與 editorial surface。
3. Golden Line 的底層含義是 **Golden Camera Spine**：先設計導演意圖，再由 renderer 執行。
4. Depth / geometry / parallax 的目的不是讓所有物體動起來，而是讓攝影機能夠進入原作的空間。
5. AI generation 只處理攝影機真正揭露、而原作與可靠幾何都不能提供的 hidden surface。
6. 不生成已經存在的世界；不動畫化不需要運動的東西。
7. 最大限度使用確定世界，最小限度生成不確定世界。

## 2. Golden Camera Spine

Golden Camera Spine 是攝影系統的導演意圖表示，也是 Camera Core 的調度入口。

Spine segment 可包含：

- X / Y / Z camera position
- velocity / acceleration / easing
- hold / pause
- look target
- FOV / FOV delta
- depth emphasis
- narrative beat

Golden Line 的視覺外顯與 Camera Spine 必須分離：

- 運鏡不好 → 修改 Camera Spine。
- 金線不好看 → 修改 Golden Line Renderer。
- 視覺修飾不得反向改寫 camera trajectory。

## 3. Camera-conditioned Rendering Policy

不同鏡頭軌跡應調用不同能力。多雷不設一條永遠全開的固定 pipeline，而是根據每個 Camera Spine segment 的狀態選擇最低成本、最高原作保真、足以完成該鏡頭的能力組合。

Camera State Vector 至少包括：

- ΔX / ΔY / ΔZ
- camera velocity / acceleration
- FOV change
- depth gradient
- occlusion density / expected disocclusion
- geometry confidence
- source coverage
- residual / provenance confidence

## 4. Doré Cinematography Capability Registry

所有成熟攝影、幾何、NVS、hidden-surface 與修復技術應作為 capability 註冊，而不是硬編進單一路徑。

初始能力類型：

- `projection.source-reprojection`
- `geometry.moge`
- `geometry.depth-crosscheck`
- `hidden.ldi`
- `hidden.layered-gaussian`
- `repair.warp`
- `repair.inpaint`
- `nvs.generative-fallback`

每個 Capability Profile 必須記錄：

- 適用 Camera State 範圍
- input / output contract
- source fidelity
- geometry confidence requirement
- computational cost
- hallucination risk
- temporal / view consistency
- expected generation budget
- 禁止或不應調用的條件

多雷探索發現新技術時，不先問「能不能取代現有方案」，而問：

1. 它解決哪一種 Camera Spine 狀態？
2. 它在哪個區間比現有能力更輕、更穩、更保真？
3. 什麼情況絕對不應調用它？

## 5. Minimum Sufficient Capability Router

Camera Core 採用 **Minimum Sufficient Capability Router** 原則。

它借鑑 Registry、Mixture-of-Experts sparse routing 與 modular rendering pipeline，但多雷的目標不是選擇「最強 expert」，而是找到**完成當前鏡頭所需的最小充分能力集合**。

概念評分：

`Score_i = Need_i × Confidence_i × Fidelity_i - Cost_i - HallucinationRisk_i`

全局優化方向：

`min(Generation)`

subject to:

`CameraIntentSatisfied = true`

執行採 sparse / top-k 思路，但還要遵循逐級停止：

1. Source reprojection 足夠 → 停止，不啟動 hidden/generative 能力。
2. Reprojection + geometry 足夠 → 停止。
3. 只有出現真實 disocclusion 才啟動 LDI / layered representation。
4. geometry / hidden representation 仍不足才啟動局部 repair。
5. full generative NVS 永遠是最後 fallback，不是常駐 renderer。

**能力增加，不等於每幀成本增加。多雷越熟悉技術，就越知道什麼時候不用它。**

## 6. Generation Budget 與 Pixel Provenance

Renderer 應逐步讓每個輸出像素保留 provenance：

- original source pixel
- geometry-reprojected source pixel
- canonical hidden-surface pixel
- locally repaired pixel
- generatively synthesized pixel

Generation Budget 應成為 shot / segment / frame 的可測量指標。核心方向不是追求生成比例，而是追求在滿足 Camera Intent 前提下的最低生成比例。

## 7. 多雷探索與 Core 的邊界

多雷探索負責：

- 發現成熟開源與新研究；
- 理解其能力邊界；
- 建立或更新 Capability Profile；
- 用固定 Camera Spine 做 controlled bakeoff；
- 把驗證結果回寫 Registry 的 cost / confidence / suitability。

Camera Core 負責：

- 讀取 Golden Camera Spine；
- 建立 Camera State Vector；
- 使用確定、可解釋的 Router 選擇 capability；
- 執行 rendering graph；
- 記錄 provenance、generation budget 與結果。

LLM 可以協助探索、理解、分類與 profile 建立；**正式逐幀 Camera Router 不依賴 LLM 臨場猜測。** Router 必須可重現、可測試、可解釋。

## 8. 可借鑑的成熟工程模式

工程實現優先借鑑，而非重造：

- MMEngine-style Registry：能力註冊、配置、分層 registry。
- Sparse Mixture-of-Experts routing：按狀態只啟動 top-k experts。
- Nerfstudio-style plugin / method pipeline：renderer 與方法可插拔，不污染 Core。
- Warp-first NVS：先幾何重投影與 confidence/provenance mask，再允許生成。

借鑑的是成熟架構與 contract；避免為了借用框架而把大型依賴整體拖入 Doré Core。

## 9. Static Cinema 的判斷準則

一個鏡頭成功，不以「畫面裡有多少東西動了」判斷，而以：

- 原作是否保持 authority；
- camera movement 是否表達導演意圖；
- depth / parallax 是否只提供必要空間感；
- disocclusion 是否穩定；
- 是否沒有為了炫技而增加 object motion；
- 是否以最低 generation budget 完成鏡頭。

Canonical question：

> 如果這是一個真實存在的世界，攝影機應該怎樣觀看它？

而不是：

> 怎樣讓這張圖片動起來？

## 10. 當前工程驗證線

AW-011 已把探索從 extended outside-canvas world 收斂到：

`Original Doré World → 16:9 Viewfinder → Golden Camera Spine → Geometry / Depth → Internal Disocclusion → Minimal Completion`

V10 已證明 outside-canvas generation 可以退出主路徑。V11 起清理 residual，並區分 raster crack 與真正 structural disocclusion。

後續每加入一種技術，都應以同一 Camera Spine / source authority / viewport 做 controlled comparison，只有在某類 Camera State 上帶來真實收益，才進入 Capability Registry。

---

### 核心製片法則

> **技術不決定鏡頭；鏡頭決定技術。**
>
> **技術越多，單一鏡頭真正需要啟動的技術應該越少。**
>
> **原作本來就已經是一部等待攝影機進入的電影。**
