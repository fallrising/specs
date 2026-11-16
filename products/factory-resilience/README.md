---
product: factory-resilience
title: Factory Resilience — 立體工廠排程實驗室
status: draft
impl_repos: []
desk_cards: []
---

# Factory Resilience — 立體工廠排程實驗室

讓使用者在立體小工廠中排出可執行的加工、搬運、組裝與交付計畫，再觀察故障對交期、物料與產能的影響。

| 項目 | 內容 |
| --- | --- |
| 狀態 | draft；尚未批准實作 |
| 實作 repo | 未建立 |
| desk 卡 | 無；未認領產品實作 |
| 核心評測 | 排程合法性、物料帳一致、故障重排、可解釋指標與第二輪變更 |

這份規格是供 owner 與參考實作檢視的草案。AC 與數值容差尚未鎖定；文件檢查或 fixture 計算通過，不代表產品驗收通過。共同評測方式見[模型挑戰評測](../../docs/model-challenge-evaluation.md)。

## 文件

- [PRD](prd.md)：對象、完整使用流程、範圍與非目標
- [業務 SDD](sdd.md)：需求索引、時間與物料規則摘要
- [里程碑](milestones.md)：完整切片、可靠品質、第二輪變更
- 需求：[排程與物料](requirements/rules.md)、[操作與解釋](requirements/experience.md)、[重現與品質](requirements/quality.md)
- [業務資料與 oracle](data/scenarios.yaml)：所有場景數值、可行排程、故障與回收期望的唯一來源
- [變更紀錄](changelog.md)
