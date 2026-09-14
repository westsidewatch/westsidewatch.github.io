# 多雷探索：全局工程索引與長線記憶

Date: 2026-09
Status: exploration record

## 問題

目前工程知識分散在產品目錄、PR、分支、聊天記錄與本機執行結果中。即使已存在 `docs/MASTER_SITE_ARCHITECTURE.md`，入口仍不夠明顯；根目錄 README 也沒有指向它。結果是人或 AI 可能知道某項工程做過，卻不能快速判斷哪一份記錄才是目前有效版本。

## 核心判斷

找到「聖經就是索引」之後，可以同時解決內容世界的索引問題，但工程記錄仍需要另一個互補索引。

兩者應區分：

- **Bible Index**：索引內容與意義。經文、事件、人物、地點、時代、主題成為書籍、影片、Moment、筆記、地圖、文章與工具的共同座標。
- **System Atlas**：索引工程本身。記錄產品、能力、代碼位置、資料權威、依賴、決策與運行邊界。

Bible Index 回答「這個資源在聖經世界的哪裡？」；System Atlas 回答「這個能力在整個工程系統的哪裡？」。

## 成熟案例帶來的啟發

### 1. Catalog as Code

Backstage Software Catalog 的核心做法，是讓每個軟體實體有穩定描述文件，包含 identity、metadata、relations 等，再由 catalog 統一發現。這類方法解決的就是大型系統中「知道有這個東西，但不知道它在哪裡、誰依賴誰」的問題。

適合多雷的不是直接引入 Backstage，而是採用同一思想建立一份極輕量 machine-readable catalog。

### 2. Docs as Code

TechDocs 的做法是讓文檔與代碼一起版本控制，而不是把文檔放在另一個知識庫。多雷目前其實已經走在這條路上，但缺少總入口與一致的記錄層級。

### 3. ADR / Decision Log

Architecture Decision Record 解決「為什麼當初這樣做」的問題。單純保留 PR 只能看到修改，不能穩定保存決策背景、替代方案與後果。多雷需要把真正跨產品的重大決策提升成 ADR，而不是散落在 PR body 或聊天。

### 4. Stable identity and semantic conventions

OpenTelemetry Semantic Conventions 的重要啟發不是 telemetry 本身，而是：大型分散系統若沒有穩定的 entity identity 和共同命名，所有下游關聯都會漂移。多雷每個產品、能力、資料集、surface 都應有穩定 ID，名稱可以變，ID 不變。

## 適合多雷的全局方案

不增加大型平台，而是在現有 GitHub repo 中建立四層：

1. **Human Entry**：根目錄 README 明確指出主站結構、全局工程索引、決策記錄、產品文檔入口。
2. **System Catalog**：一份 machine-readable JSON，記錄 stable id、kind、status、code roots、canonical docs、datasets、dependencies。
3. **ADR Log**：只記跨產品或不可輕易逆轉的架構決策。
4. **Product Contracts**：各產品保留自己的 schema、runtime boundary、acceptance tests，不把所有細節塞進總文檔。

這四層形成：

```text
Global Entry
  ↓
System Catalog
  ↓
Architecture / ADR
  ↓
Product Contract + Code + Acceptance
```

## 聖經索引與全局工程索引的關係

內容世界統一為：

```text
Bible
  → Scripture coordinate
  → Event / Person / Place / Period / Theme
  → Canonical Resource
  → ONE / 黎明書局 / 天堂影院 / 多寫 / Search / 浮現
```

工程世界統一為：

```text
System Entity ID
  → code root
  → canonical docs
  → datasets / capabilities
  → dependencies
  → ADR decisions
  → runtime / A2A execution
```

這兩張圖相互連接，但不可混為一張圖。前者是內容 ontology；後者是 engineering topology。

## 對「浮現」的意義

浮現現在第一次有確實根據：語義模型只負責找候選；Bible Coordinate Graph 提供資源為何相關的可追溯證據。當前上下文解析到經文或聖經世界座標後，才沿 canonical relation 找到資源，再決定 trace / whisper / surface / focus。

因此浮現不是推薦卡，也不是 embedding 相似度視覺化，而是「有根據的相關資源逐漸浮出水面」。

## 對 Doré Memory 的意義

Memory 應保存與召回歷史，但不能靠聊天記憶決定目前架構。正確流程應是：

```text
conversation / branch / experiment
  → durable insight or decision
  → canonical GitHub record on main
  → Memory indexes and recalls that record
```

這能避免「記得做過，但找不到現在哪個版本才對」。現有 `docs/dore-memory-core-boundary.md` 的 provider-independent 原則應繼續保持。

## 對 A2A 的意義

A2A 解決執行通路，不應承擔架構記憶。A2A 的任務、能力、local runtime、browser execution 應使用 System Catalog 中的穩定 project/capability identity。執行結果如果產生新的跨系統決策，最終仍需落回 GitHub canonical record。

## 建議下一階工程

第一階不要重做現有文檔，而是補「索引層」：

- 新增 `docs/system-catalog.v0.json`。
- 新增 `docs/adr/`，從「Bible is the Index / System Atlas is the engineering index」開始。
- 更新根 README，讓任何人或 AI 從第一屏就能找到 `MASTER_SITE_ARCHITECTURE.md`、catalog、ADR、Memory、A2A 等入口。
- 之後再建立 CI acceptance：catalog 引用的 code root / canonical doc 必須存在；新增跨產品工程若沒有 catalog/ADR 更新則不能宣稱架構完成。

這會把目前「一個工程一份記錄」改成「所有工程都掛在同一張索引上」。
