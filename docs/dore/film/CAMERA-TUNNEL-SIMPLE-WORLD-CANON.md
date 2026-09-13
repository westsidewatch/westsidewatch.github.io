# Doré Film — Simple World / Camera Tunnel Canon

Status: **PRODUCTION / ENGINEERING CANON**

## 最簡單的世界

Doré 電影的底層不是先建完整 3D 世界，而是先讓原作本身移動。

**Original Artwork + 16:9 Viewfinder + Time Curve**

只用 translate / crop / scale / hold / slow movement，就可以形成 pan、tilt、push、pull、reframe。這是 **Moving Painting / 畫動**。

**Simple World First. Complexity as Residual.**

所有複雜能力都不能取代簡單能力，只解決簡單層無法解決的剩餘問題。

**2D 拍攝，3D 知覺；知覺成立，不做 3D。**

## 鏡頭意圖前置，攝影機執行後置

製片鏈：

**Script → Shot Design → Golden Camera Spine → Trajectory Dry Run → First Moving-Painting Pass → Residual Map → Minimum Sufficient Capability Routing → Camera Run / Render**

Camera Spine 先知道未來的時間、位置、方向、FOV、速度與停留。第一批 Moving Painting 因此不是任意動畫，而是由未來鏡頭軌跡條件化的畫面準備。

先用最便宜、最忠實原作的方法滿足鏡頭；只有失敗處才加入 depth、parallax、hidden surface、repair、selective 3D 或最後的 generation。

## 16:9 時空隧道

沿 Camera Spine 的每一個時間點都有一張 16:9 frame plane：

**F0 → F1 → F2 → … → Fn**

這些平面按時間、位置、方向、尺度排列，形成蜿蜒的三維 Camera Tunnel。

**隧道是 3D 的，材料可以主要是 2D 的。**

正確拓撲：

**2D Tunnel Skeleton + Sparse Residual Volumes**

比較相鄰 `F_t → F_{t+1}`：如果 2D transform 足夠，3D 成本為零；如果不夠，只把不能由 2D 解釋的 residual 立體化。

不是先建立 3D 世界，再讓 2D 攝影機穿過它；而是先用 2D 畫面沿時間建立攝影隧道，再只把相鄰 16:9 平面之間無法由 2D 解釋的差值立體化。

## Script-to-Compute

腳本與 Camera Spine 可以在昂貴計算開始前預測可見性與能力需求。

首要問題：

**下一幀需要的像素，原作是否已經全部存在？**

若答案為是：

**SOURCE_ONLY → crop / translate / scale → render**

並保持：

**Depth OFF / 3D OFF / Hidden OFF / Repair OFF / Generation OFF**

因此：

**腳本不是先告訴多雷要生成什麼；腳本首先告訴多雷什麼永遠不需要生成。**

## 2D / 3D Activation Boundary

純 XY 位移、原作內裁切、縮放不得因 position vector 非零就啟動 3D。Depth 應只在 Z、parallax、occlusion、disocclusion 或其他真正空間需求出現時啟動，最好由明確 phase / activation scalar 控制。

每個長鏡頭預設從 source-native 原作靜幀開始；沒有敘事理由，不允許第一幀就啟動 3D。

## 長鏡頭時間語法

**Stillness → Awakening → Drift → Approach → Contemplation → Rest**

**靜觀 → 起行 → 漂移 → 進入 → 凝視 → 歸靜**

空鏡可先停留數秒，再緩慢 ease-in；中段保持平和的長時間移動，在重要節點自然停頓，再 ease-out。速度不是常數；平和才是常數。

## Style is Compute

Doré 的黑白版畫、刻線、強光暗、靜止人物、莊嚴構圖與慢長鏡頭不是工程之外的裝飾。風格本身縮小了需要求解的世界：人物可以不動，原作紋理可以直接保留，長時間 hold 不需要新世界，純 pan/scale 不需要 3D，慢 Z 運動降低 disocclusion。

**Style → Constraint → Reduced Search Space → Reduced Compute → Higher Fidelity**

「Style is Compute / Style is Algorithm」在此是製片原則，不宣稱為新的計算機科學算法。

## 長卷迭代

最簡單、永遠可播放的 V1 是把 Doré 原作按聖經時間排列為長卷，讓固定 16:9 viewfinder 以極慢速度觀看：

**Genesis → … → Gospels → Cross → Church → Revelation → New Heaven and New Earth**

先有完整長卷，再逐層把值得進入的地方變深。重要節點可停下、push-in、沿 Z 進入某幅畫，完成一段後再退出並回到時間長河。

**Long Scroll is the world’s timeline; Camera Spine is the road through which we watch that world.**

## 複雜性只能作為剩餘量

最終畫面遵循：

**Final Frame = Simple Moving Painting + Necessary Difference**

製片不預先發明算法名稱。每次實作記錄：

**camera state → how far 2D sufficed → why illusion failed → minimum added capability → fidelity / compute result**

如果未來真正形成可泛化算法，讓它從多部實際作品的結構化證據中自己浮現。
