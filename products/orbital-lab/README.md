---
product: orbital-lab
title: Orbital Lab — 平面軌道任務實驗室
status: draft
impl_repos: []
desk_cards: []
---

# Orbital Lab — 平面軌道任務實驗室

用立體視覺觀察平面點質量運動，規劃一次推進、比較預測軌跡與實際飛行，再完成簡化的軌道與飛越任務。

| 項目 | 內容 |
| --- | --- |
| 狀態 | draft；尚未批准實作 |
| 實作 repo | 未建立 |
| desk 卡 | 無；未認領產品實作 |
| 核心評測 | 物理基準、燃料、預測一致、重現與高速事件 |

這是有明確界線的教學與模型評測產品，物理模型採簡化假設，不承諾真實太空任務精度。AC 與容差須經參考實作確認才鎖定；數值 fixture 核對不代表產品驗收。共同評測見[模型挑戰評測](../../docs/model-challenge-evaluation.md)。

## 文件

- [PRD](prd.md)：使用者、核心流程、範圍與非目標
- [業務 SDD](sdd.md)：單位、物理假設、事件與需求索引
- [里程碑](milestones.md)
- 需求：[物理與任務](requirements/rules.md)、[操作與重現](requirements/experience.md)、[數值與可讀品質](requirements/quality.md)
- [業務資料與參考值](data/scenarios.yaml)：全部數值、容差、場景及 oracle 的唯一來源
- [變更紀錄](changelog.md)
