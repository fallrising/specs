---
status: draft
---

# 業務 SDD

## 文件邊界

本文件界定玩家看得見的規則與驗收入口，不定義技術架構。內容仍為 draft；所有預期結果是待驗證的規格主張，批准實作前須附參考驗證證據。

| 業務問題 | 唯一規則入口 | 資料入口 |
| --- | --- | --- |
| 哪些接點可切、切後誰相連 | REQ-SSR-01，見 [規則](requirements/rules.md) | `ship.modules`、`ship.joints` |
| 哪些模組帶電、何時可以切 | REQ-SSR-02、REQ-SSR-05，見 [規則](requirements/rules.md) | `power`、`cases.power_loop` |
| 如何牽引、容積如何計算 | REQ-SSR-03、REQ-SSR-04，見 [規則](requirements/rules.md) | `handling`、`intake` |
| 何時結束、如何脫困 | REQ-SSX-01、REQ-SSX-02，見 [體驗](requirements/experience.md) | `mission`、`cases.escape` |
| 如何辨識操作結果與重播 | REQ-SSX-03、REQ-SSQ-01，見 [體驗](requirements/experience.md)、[品質](requirements/quality.md) | `cases`、`replay` |
| 如何評估視覺與效能 | REQ-SSQ-02，見 [品質](requirements/quality.md) | `verification_profile`、`visual_checks` |

上表的資料入口全部位於 [scenarios.yaml](data/scenarios.yaml)。

## 業務狀態與邊界

模組只會處於仍在船上、已分離、回收處理中、已回收的其中一種回收狀態；供電狀態與回收狀態分開判定。結構群組依未切開的接點決定，供電依來源開關及有效供電路徑決定，不能用同一個外觀標記暗示兩者必然相同。

回收是對整個連通群組的不可重複結算。入口檢查不通過就保留原群組與分數；通過後群組中的模組一次完成結算並離開操作場景。回收艙是單批容積限制，沒有隱藏的累積倉庫上限。

暫停不是撤離；重新開始是新的任務；重播是唯讀檢視。正常撤離依任務目標判定完成或提前結束，緊急返回與逾時都保留已回收金額但不能冒稱任務完成。

## 版本與驗收

M1 使用 `power.baseline` 的樹狀路徑；M3 加入 `power.loop_extension` 的既定繞路。既有樹狀案例的資料與預期不可因新增環路而改寫。需要改規則時，先修改相應 REQ／AC 與案例，再依 repo 審核程序批准。

模型比較、規格凍結、參考驗證與證據欄位遵循 [共同評測](../../docs/model-challenge-evaluation.md)。沒有參考實作證據時只能稱「預期通過條件」，不能稱「已驗收」。
