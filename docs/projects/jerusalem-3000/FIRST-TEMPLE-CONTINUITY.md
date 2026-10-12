# 第一聖殿城市鏈：共同帳本第一批

範圍：第一聖殿、早期第二聖殿、王室／大型石構爭議區、大衛城防假說。不是全城幾何或所有時代繼承完成。

| 主體 | 大衛段 | 所羅門段 | 第一聖殿晚期 | 巴比倫毀城 | 波斯 |
|---|---|---|---|---|---|
| 第一聖殿 | absent | build | transform | ruin | unresolved |
| 早期第二聖殿 | absent | absent | absent | absent | rebuild |
| 王室／大型石構爭議區 | build（爭議） | build（爭議） | unresolved | unresolved | unresolved |
| 大衛城防假說 | transform（示意體系） | transform | unresolved | unresolved | unresolved |

第一聖殿文獻建造記錄：[列王紀上 6:1–3](https://www.biblegateway.com/passage/?search=1+Kings+6%3A1-7&version=KJV)。毀壞記錄：[列王紀下 25:8–10](https://www.biblegateway.com/passage/?search=2+Kings+25%3A8-10&version=KJV)。第二聖殿建造記錄：[以斯拉記 6:14–15](https://www.biblegateway.com/passage/?search=Ezra+6%3A14-15&version=KJV)。文獻事件不核定地基、平面、埋藏深度或倒塌形態。

第一與第二聖殿是不同物件 ID。relatedObjects 表示聖區制度承接，geometryReuseVerified:false；不生成 Core 的幾何再利用連線。第一聖殿在波斯 unresolved 指特定遺存與再利用未核定，不是否定已記錄的毀壞。城防假說的 unresolved 指個別牆段去向，不是否認後期有城防。

共同契約修復：

- Core 保留事件的 offset、來源與 authority，凍結事件記錄。
- Adapter 登記相關時代、來源 URL、限制與物件關係；transform/rebuild 不自動等於可證實幾何再利用。
- 時間整合使用同一生命週期 evaluator，可在大衛—所羅門片段內取樣；0.45 是敘事界線，不是年代比例。
- unresolved 不渲染為站立、毀壞或埋藏。UI 明確顯示未核定，不默默推導不存在。
- 新物件為 ledger-only-pending-adapter，禁止舊 temporal box renderer 擅自補出幾何。PR #1249 的模型還需接到共同帳本，這一批沒有聲稱已完成。
- Evidence 面板顯示主體去向，波斯面板改用當期來源。面板可捲動，避免來源與狀態超出舞台。

驗證：Node 覆蓋前十世紀片段、毀壞／未知、反向取樣、不同聖殿 ID、來源與事件保留、未知 phase／非法 offset 拒絕、無臆造幾何再利用連線。瀏覽器核對五個時間點、倒退、UI 與帳本一致，並跑既有 18 期桌面／手機回歸、資料失敗與共享城市檢查。

下一批：將王室候選 geometry objectId 對接這些帳本 ID；建立道路／門／水系／地區共同資料契約，然後實作第一聖殿晚期與毀城的同一主體投影。保留 unresolved 項目，不能用看似完整的 模型填補證據空缺。
