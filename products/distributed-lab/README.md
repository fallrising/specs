---
product: distributed-lab
title: 分散式實驗室
status: approved
impl_repos: []
desk_cards: []
---

# 分散式實驗室

讓學習分散式系統的人在可重播的虛擬 KV 叢集中讀寫資料、施加故障，再由操作歷史與事件日誌理解哪些結果符合承諾。

| 項目 | 內容 |
| --- | --- |
| 狀態 | approved；已批准實作（desk 卡 T-0453 只做 M1） |
| 實作 repo | 未建立 |
| desk 卡 | 無 |
| 核心承諾 | 線性一致性、重試保留同一邏輯操作、已確認操作不因故障消失 |
| 可用性條件 | 網路穩定、存活多數及公平執行條件成立後才要求完成；少數分割不能確認新寫入 |

## 文件

- [PRD](prd.md)：對象、體驗、範圍、限制與成功指標。
- [業務 SDD](sdd.md)：一致性、確認、重試及故障的業務邊界。
- [里程碑](milestones.md)：可用切片、可靠品質、快照恢復變更。
- 需求：[資料與故障規則](requirements/rules.md)、[實驗體驗](requirements/experience.md)、[品質](requirements/quality.md)。
- [情境與數值](data/scenarios.yaml)：固定成員、故障情境、可知歷史及預期期望。
- [變更紀錄](changelog.md)。
- [共同模型挑戰評測](../../docs/model-challenge-evaluation.md)。

AC 與數值是草案目標，須經參考實作驗證才鎖定；靜態文件檢查不代表叢集、一致性檢查器或產品已驗收。
