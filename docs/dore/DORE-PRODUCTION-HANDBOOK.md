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
8. **只要原作能完整提供下一幀，就禁止啟動 3D、hidden surface、repair 與 generation。**

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

## 3. Doré 長鏡頭時間語法

Static Cinema 的預設鏡頭語言不是快速技術展示，而是均勻、緩慢、平和的長鏡頭。速度本身屬於 Camera Compute Budget：鏡頭越快，相鄰視圖差異越大，越容易產生不必要的 disocclusion、repair 與畸變。

預設時間語法：

**Stillness → Awakening → Drift → Approach → Contemplation → Rest**  
**靜觀 → 起行 → 漂移 → 進入 → 凝視 → 歸靜**

規則：

- 長鏡頭預設從空鏡／原作靜幀開始，先停留，再起行。
- 起步與停止使用長而平緩的 acceleration / deceleration；中段近似恆速。
- 平移、推拉、行走都以真實攝影機可感知的緩慢速度進行，不以動畫速度追求刺激。
- 沒有敘事理由，不允許第一幀就啟動 3D。
- 重要人物、光線、十字架影子與敘事節點可以自然停留或接近靜止。
- **速度不是常數；平和才是常數。**

## 4. 2D Camera Pan 與 3D Activation Boundary

16:9 Viewfinder 在原作有效像素範圍內移動時，X/Y 運鏡首先被視為純 2D camera operation。對固定 Viewfinder 而言，這等價於原作在取景框後平移。

因此：

`2D Pan = source crop / translate / scale only`

在這個區間：

`Depth = OFF`  
`3D = OFF`  
`LDI = OFF`  
`Repair = OFF`  
`Generation = OFF`

例如由原作底部 16:9 緩慢上移至中部、再到上部，只要下一幀仍完全存在於原作中，就不存在需要補的世界。

只有當 Camera Spine 真正進入 Z 軸、產生前後景差速、遮擋關係改變或 source coverage 不足時，才跨越 **3D Activation Boundary**。

Canonical rule：

> **不是先做 3D 再想辦法修，而是先證明 2D 已經不夠，才允許 3D 發生。**

## 5. Script-to-Compute Compiler

腳本不是單純的敘事文件。腳本完成並被多雷讀取後，應立即被編譯為可執行的攝影與計算計畫。

Canonical chain：

`Script → Shot Grammar → Golden Camera Spine → Camera Dry Run → Visibility Forecast → Camera Compute Map → Capability Schedule → Render`

腳本編譯完成的瞬間，系統應能預先知道或計算：

- 每個 shot / segment 的開始與結束時間；
- camera X / Y / Z 位置與移動方向；
- velocity / acceleration / easing / hold；
- look target 與 FOV；
- 每個時間點的 source coverage；
- 哪些區段是純 2D；
- 哪些區段真正需要 depth deviation / 3D；
- 哪個方向可能出現 occlusion / disocclusion；
- 哪些局部 tile 可能需要 hidden surface 或 repair；
- 每種 capability 的預計啟動時間、區域與成本。

### Camera Dry Run

Camera Dry Run 是低成本 visibility/compiler pass，不是先完整渲染一次。它首先回答：

> **下一幀所需像素，原作是否已經全部存在？**

如果答案是「是」，Router 直接標記：

`SOURCE_ONLY → crop / translate / scale → render`

昂貴能力在正式渲染前即被排除。

### Camera Compute Map

Camera Dry Run 的核心產物是 **Camera Compute Map**。它把整個鏡頭的時間軸預先標註為 source-only、2D、depth、selective-3D、hidden、repair 或最後 fallback。

示例：

`0–6s hold → SOURCE_ONLY`  
`6–25s vertical pan → SOURCE_2D`  
`25–30s hold → SOURCE_ONLY`  
`30–37s shallow Z push → DEPTH + SELECTIVE_3D`  
`37–40s local disocclusion → LOCAL_HIDDEN / REPAIR_IF_REQUIRED`

因此節省不是 GPU 跑到一半才發現某幀不需要修，而是**讀完腳本、完成 camera compile 的瞬間就知道哪些計算永遠不應啟動。**

Camera Spine 同時提供未來位置、時間與移動方向，所以 hidden-surface preparation 也不得無方向地建立完整世界；只預備未來攝影機真正可能看見的方向與區域。

Canonical doctrine：

> **腳本不是先告訴多雷要生成什麼；腳本首先告訴多雷什麼永遠不需要生成。**

## 6. Camera-conditioned Rendering Policy

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

## 7. Doré Cinematography Capability Registry

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

每個 Capability Profile 必須記錄適用 Camera State、input/output contract、source fidelity、geometry confidence requirement、computational cost、hallucination risk、temporal/view consistency、expected generation budget，以及禁止調用條件。

多雷探索發現新技術時，先問它解決哪一種 Camera Spine 狀態、在哪個區間更輕更穩更保真，以及什麼情況絕對不應調用。

## 8. Minimum Sufficient Capability Router

Camera Core 採用 **Minimum Sufficient Capability Router** 原則。目標不是選擇「最強 expert」，而是找到完成當前鏡頭所需的最小充分能力集合。

概念評分：

`Score_i = Need_i × Confidence_i × Fidelity_i - Cost_i - HallucinationRisk_i`

全局優化方向：

`min(Generation)` subject to `CameraIntentSatisfied = true`

執行逐級停止：

1. Source-only 足夠 → 停止。
2. 2D crop / translate / scale 足夠 → 停止。
3. Reprojection + geometry 足夠 → 停止。
4. 只有真實 disocclusion 才啟動 LDI / layered representation。
5. geometry / hidden representation 仍不足才啟動局部 repair。
6. full generative NVS 永遠是最後 fallback。

**能力增加，不等於每幀成本增加。多雷越熟悉技術，就越知道什麼時候不用它。**

## 9. Generation Budget 與 Pixel Provenance

Renderer 應逐步讓每個輸出像素保留 provenance：original source、geometry-reprojected source、canonical hidden-surface、locally repaired、generatively synthesized。

Generation Budget 應成為 shot / segment / frame 的可測量指標。核心方向是在滿足 Camera Intent 前提下取得最低生成比例。

## 10. 多雷探索與 Core 的邊界

多雷探索負責發現成熟開源與新研究、理解能力邊界、建立 Capability Profile、用固定 Camera Spine 做 controlled bakeoff，並把結果回寫 Registry。

Camera Core 負責讀取 Golden Camera Spine、建立 Camera State Vector、使用確定可解釋的 Router、執行 rendering graph，並記錄 provenance、generation budget 與結果。

LLM 可以協助探索、理解、分類與 profile 建立；**正式逐幀 Camera Router 不依賴 LLM 臨場猜測。** Router 必須可重現、可測試、可解釋。

## 11. Static Cinema 的判斷準則

一個鏡頭成功，不以畫面裡有多少東西動了判斷，而以原作 authority、camera movement、必要 depth/parallax、穩定 disocclusion、最低 generation budget 與是否避免不必要 object motion 判斷。

Canonical question：

> 如果這是一個真實存在的世界，攝影機應該怎樣觀看它？

而不是：

> 怎樣讓這張圖片動起來？

## 12. 當前工程驗證線

AW-011 已把探索從 extended outside-canvas world 收斂到：

`Original Doré World → 16:9 Viewfinder → Golden Camera Spine → 2D Source Corridor → 3D Activation Boundary → Geometry / Depth → Internal Disocclusion → Minimal Completion`

V10 已證明 outside-canvas generation 可以退出主路徑。後續驗證進一步證明 residual=0 不代表視覺成功，因此修復必須通過 Fidelity Gate；同時 Camera Core 必須先消除原本不應產生的 wound，再提升 repair 能力。

後續每加入一種技術，都應以同一 Camera Spine / source authority / viewport 做 controlled comparison，只有在某類 Camera State 上帶來真實收益，才進入 Capability Registry。

---

### 核心製片法則

> **技術不決定鏡頭；鏡頭決定技術。**
>
> **技術越多，單一鏡頭真正需要啟動的技術應該越少。**
>
> **只要原作能提供下一幀，就不要建立不存在的問題。**
>
> **腳本首先告訴多雷什麼永遠不需要生成。**
>
> **原作本來就已經是一部等待攝影機進入的電影。**
