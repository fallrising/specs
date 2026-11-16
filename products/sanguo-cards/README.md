---
product: sanguo-cards
title: 群雄・三國卡牌（暫名）
status: approved
impl_repos: []
desk_cards: [T-0453]
---

# 群雄・三國卡牌（暫名）

瀏覽器打開就能玩的三國題材卡牌對戰：雙方主公在 three.js 3D 沙盤上分三路布陣，部隊依規則自動交戰，一局 8–15 分鐘。

| 項目 | 內容 |
| --- | --- |
| 狀態 | M1 approved（2026-11-17）；M2、M3 draft |
| 實作 repo | 未建立（建議 `fallrising/sanguo-cards`） |
| desk 卡 | T-0453（M1） |
| 業務指定技術 | three.js（C-01）、純靜態網站（C-02） |

## 文件

- [PRD](prd.md)：願景、對象、範圍、非目標、限制、成功指標、待決問題
- [里程碑](milestones.md)：M1 可玩切片、M2 四國齊備、M3 征戰
- 需求
  - [對局規則](requirements/rules.md)（REQ-RUL）：規則全文與驗收
  - [卡牌、陣營與牌組](requirements/cards.md)（REQ-CRD）
  - [電腦對手](requirements/ai.md)（REQ-AI）
  - [3D 呈現與操作](requirements/presentation.md)（REQ-PRE）
  - [模式與流程](requirements/modes.md)（REQ-MOD）
  - [品質、相容與合規](requirements/quality.md)（REQ-QA）
- 業務資料：[卡池與預組牌組](data/cards.yaml)
- [變更紀錄](changelog.md)

## 給實作 repo

需求與 AC 只以本目錄為準；技術設計、任務拆解與測試放實作 repo。測試名稱帶 AC 編號（例如 `AC-RUL-12`）。規則引擎宜與 three.js 呈現分離，AC-RUL／AC-CRD／AC-AI 大多可在無瀏覽器環境自動跑——這是建議，怎麼做由實作 repo 決定。
