---
status: draft
---

# 業務 SDD

## 範圍與權威來源

本文件是業務索引與邊界說明。規則位於需求檔，內容數值與預期結果只位於 [scenarios.yaml](data/scenarios.yaml)。草案尚未批准實作，案例須先附參考驗證證據。

| 問題 | 規則入口 | 資料入口 |
| --- | --- | --- |
| 術式是否合法、花多少法力 | REQ-SPR-01，見 [規則](requirements/rules.md) | `catalog`、`composition`、`recipes` |
| 分裂、追蹤與延遲如何發射 | REQ-SPR-02，見 [規則](requirements/rules.md) | `projectile`、`cases.flight` |
| 元素先做什麼、傷害是多少 | REQ-SPR-03，見 [規則](requirements/rules.md) | `elements`、`event_order`、`cases.reactions` |
| 如何限制連鎖與新油規則 | REQ-SPR-04、REQ-SPR-05，見 [規則](requirements/rules.md) | `budgets`、`oil`、`cases.oil` |
| 玩家如何修改、看因果與保留術式 | REQ-SPX-01 至 REQ-SPX-03，見 [體驗](requirements/experience.md) | `trials`、`experience_trial` |
| 如何回歸與量測品質 | REQ-SPQ-01、REQ-SPQ-02，見 [品質](requirements/quality.md) | `replay`、`verification_profile`、`visual_checks` |

## 術式與事件邊界

術式是有限的發射分段鏈。每段從投射物開始，接元素、可選修飾及可選命中觸發；命中觸發才能接下一發射段。分裂在遊戲內產生子投射物，並不開放編輯任意分支、合流或循環。修飾順序不改變該段成本與效果；命中觸發只能在段尾。

接受施法時即預扣整份術式的最壞情況成本，之後未命中、目標死亡或預算耗盡不退款。非法術式不扣法力且不發射。每輪法力不自然回復；重置試驗場才回到初始狀態。

每次直接命中最多觸發該段的命中子段。導電、燃燒與油地面傷害不能再次觸發命中子段，不能靠間接傷害產生無限連鎖。所有傷害都必須能指出原施法與來源節點或反應；到達預算上限時記錄被抑制的結果，不得靜默截斷。

## 可觀察結果與相容性

回歸比較生命值、狀態與剩餘時間、法力、已接受或抑制的事件及試驗結果，不以粒子形狀或逐幀畫面判定規則等價。相同輸入順序、內容版本與試驗起始條件必須得到同樣結果。

M3 的油是新增元素與地面狀態，既有元素規則不能因增加油而重排。未使用油的全部舊案例必須保持成本、反應及因果順序。共同證據、參考驗證與模型比較遵循 [共同評測](../../docs/model-challenge-evaluation.md)。
