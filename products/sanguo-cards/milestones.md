---
status: draft
---

# 里程碑

每個里程碑的範圍以各 REQ 的「里程碑」欄為準，文末索引由 `scripts/check_specs.py --fix` 產生。一個里程碑對應一張 desk 卡；實作 repo 只有一個時不拆子卡。

## M1 可玩切片

- 目標：在桌機瀏覽器用 three.js 沙盤打完一局蜀對魏，人對電腦，規則完整、可重現、可自動測試。
- 退出條件：範圍內每條 AC 有通過證據；`人工確認` 的 AC 由 owner 確認；可用版本（`usable/*` tag）另由 owner 決定。
- 不做：吳與群雄、自組牌組、新手教學、正式美術與音效（可用佔位美術）、換牌、本機雙人、手機版。

## M2 四國齊備

- 目標：四個陣營都可玩，玩家能自組牌組，有新手教學與兩種電腦難度，換上正式美術與音效。
- 前置：M2 開工前以 SDD PR 把吳與群雄的主公、卡池與預組牌組寫進 `data/cards.yaml`，並將本檔與相關需求轉為 `approved`。
- 退出條件：範圍內每條 AC 有通過證據；M1 的 AC 仍全部通過。
- 不做：線上對戰、帳號、抽卡、手機版。

## M3 征戰

- 目標：四章單人戰役與本機存檔，對局可中斷續玩。
- 前置：M3 開工前以 SDD PR 補齊四章的敵方牌組、特殊規則與劇情文字。
- 退出條件：範圍內每條 AC 有通過證據；M1、M2 的 AC 仍全部通過。
- 不做：多人模式、雲端存檔。

<!-- BEGIN GENERATED: scope -->

## 範圍索引（自動產生，勿手改）

**M1 可玩切片**

- REQ-AI-01 只做合法操作：AC-AI-01
- REQ-AI-02 不偷看：AC-AI-02
- REQ-AI-03 基本強度：AC-AI-03
- REQ-AI-04 思考時間：AC-AI-04
- REQ-AI-05 看得懂電腦在做什麼：AC-AI-05
- REQ-CRD-01 卡池以資料檔為準：AC-CRD-01、AC-CRD-02
- REQ-CRD-02 M1 陣營：蜀、魏：AC-CRD-03
- REQ-CRD-03 預組牌組：AC-CRD-04
- REQ-CRD-04 卡面資訊：AC-CRD-05
- REQ-CRD-05 預組牌組平衡：AC-CRD-06
- REQ-MOD-01 主選單：AC-MOD-01
- REQ-MOD-02 規則說明：AC-MOD-02
- REQ-MOD-03 設定保存：AC-MOD-03
- REQ-PRE-01 沙盤戰場：AC-PRE-01、AC-PRE-02
- REQ-PRE-02 出牌操作：AC-PRE-03、AC-PRE-04、AC-PRE-05
- REQ-PRE-03 交戰動畫：AC-PRE-06、AC-PRE-07
- REQ-PRE-04 資訊可讀：AC-PRE-08、AC-PRE-09
- REQ-PRE-05 對局紀錄：AC-PRE-10
- REQ-PRE-06 勝負畫面：AC-PRE-11
- REQ-PRE-07 動畫速度與減少動態：AC-PRE-12、AC-PRE-13
- REQ-QA-01 流暢：AC-QA-01
- REQ-QA-02 載入快：AC-QA-02、AC-QA-03
- REQ-QA-03 瀏覽器相容：AC-QA-04、AC-QA-05
- REQ-QA-04 純靜態部署：AC-QA-06
- REQ-QA-05 一局時長：AC-QA-07
- REQ-QA-06 不只靠顏色：AC-QA-08
- REQ-QA-08 素材與名稱合規：AC-QA-10
- REQ-RUL-01 對局準備：AC-RUL-01、AC-RUL-02
- REQ-RUL-02 糧：AC-RUL-03、AC-RUL-04
- REQ-RUL-03 回合流程：AC-RUL-05、AC-RUL-06
- REQ-RUL-04 出牌與格位：AC-RUL-07、AC-RUL-08
- REQ-RUL-05 交戰順序與目標：AC-RUL-09、AC-RUL-10、AC-RUL-11
- REQ-RUL-06 傷害、反擊與兵種相剋：AC-RUL-12、AC-RUL-13、AC-RUL-14
- REQ-RUL-07 關鍵字：AC-RUL-15、AC-RUL-16、AC-RUL-17、AC-RUL-18
- REQ-RUL-08 主公技：AC-RUL-19
- REQ-RUL-09 抽牌、手牌上限與疲勞：AC-RUL-20、AC-RUL-21
- REQ-RUL-10 勝負：AC-RUL-22、AC-RUL-23、AC-RUL-24
- REQ-RUL-11 對局可重現：AC-RUL-25
- REQ-RUL-12 拒絕不合法操作：AC-RUL-26

**M2 四國齊備**

- REQ-AI-06 兩種難度：AC-AI-06
- REQ-CRD-06 吳、群雄陣營：AC-CRD-07、AC-CRD-08
- REQ-MOD-04 新手教學：AC-MOD-04
- REQ-MOD-05 自組牌組：AC-MOD-05、AC-MOD-06
- REQ-PRE-08 正式美術與音效：AC-PRE-14、AC-PRE-15
- REQ-QA-07 鍵盤操作：AC-QA-09

**M3 征戰**

- REQ-MOD-06 單人戰役：AC-MOD-07、AC-MOD-08
- REQ-MOD-07 對局中斷可續：AC-MOD-09

<!-- END GENERATED: scope -->
