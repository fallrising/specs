# 撰寫規範

本頁是 specs repo 的檔案格式與流程。`scripts/check_specs.py` 依本頁驗證；兩者不一致時以本頁為準並修腳本。

## 1. 業務與技術的界線

| 放這裡（業務） | 放項目 repo（技術） |
| --- | --- |
| 誰用、要解決什麼、為什麼現在做 | 架構、模組切分、資料結構 |
| 規則、流程、內容與數值（例如卡池） | 框架用法、渲染管線、狀態管理 |
| 可觀察的行為與驗收案例（AC） | 測試怎麼寫、放哪 |
| 里程碑與退出條件 | 技術任務、排程、組隊 |
| 業務指定的限制（平台、預算、授權、必須用的技術） | 為滿足限制所做的技術選擇 |

判斷方法：換一個技術棧重做，這句話還成立嗎？成立就屬於這裡。

## 2. 檔案

每個產品一個目錄 `products/<slug>/`，`slug` 用小寫英文與連字號，建立後不改。骨架在 [`templates/product/`](../templates/product/)。

`products/<slug>/` 下每個 `.md` 都有 frontmatter，至少含 `status`：

| status | 意思 |
| --- | --- |
| `draft` | owner 同意收錄，尚未批准實作。AC 可以再改。 |
| `approved` | 至少一個里程碑已由 owner 批准實作。哪些 REQ／AC 已鎖定，看里程碑狀態（§4）。 |
| `superseded` | 已被取代。frontmatter 加 `superseded_by: <路徑>`。 |

產品 `README.md` 的 frontmatter 另含 `product`（等於 slug）、`title`、`impl_repos`（清單）、`desk_cards`（清單）。

需求檔 `requirements/*.md` 的 frontmatter 另含 `area`：2–4 個大寫英文字母，該檔所有編號都用這個 area，同一產品內不重複。

## 3. 需求（REQ）與驗收案例（AC）

```markdown
### REQ-RUL-01 對局開始
一兩段話描述業務行為與理由。
- 里程碑：M1
- 優先：必要

#### AC-RUL-01 起手牌
- Given 雙方使用合法牌組，種子固定
- When 對局開始
- Then 先手手牌 4 張、後手 5 張加 1 張「軍糧」
- 驗證：自動
```

- 編號格式 `REQ-<AREA>-<NN>`、`AC-<AREA>-<NN>`，兩位數起跳，同產品內唯一。AC 屬於它上方最近的 REQ。
- `里程碑` 必填，值是 `milestones.md` 裡存在的 `M<n>`。`優先` 可選：`必要`／`應有`／`可選`。
- 每條 AC 必須有 `Given`、`When`、`Then`、`驗證` 四行。`驗證` 取值：
  - `自動`：項目寫成自動測試，測試名稱帶 AC 編號，進 CI。
  - `手動`：慢或依賴硬體，本地照 AC 跑，回報時附指令與結果。
  - `人工確認`：純業務判斷，owner 看過才算。寫清楚要確認什麼。
- 每條非撤回的 REQ 至少一條 AC。AC 要能判定通過或失敗；寫不出 Then 就代表需求還沒想清楚。
- **編號不重用、不改號。** 撤回時保留標題並在編號後加 `[撤回]`，正文寫原因與日期：`### REQ-RUL-07 [撤回] 換牌`。撤回的 AC 同樣處理。
- 需要內容數值時放 `data/`，REQ 引用檔名，不在正文抄一份。

## 4. 里程碑

`milestones.md` 用 `## M<n> <名稱>` 分節，每節寫：狀態、目標、退出條件、明確不做的事。

**批准以里程碑為單位。** 每節用 `- 狀態：draft` 或 `- 狀態：approved` 標示，沒寫視為 draft。里程碑 approved 之後，屬於它的 REQ 與 AC 鎖定，desk 卡可以指向它開工；同一個檔案裡屬於 draft 里程碑的 REQ 仍可修改。含有已批准里程碑 REQ 的需求檔與 `milestones.md`，檔案 `status` 寫 `approved`。
範圍以 REQ 上的 `里程碑` 欄為唯一來源；`milestones.md` 尾端的範圍索引由 `check_specs.py --fix` 產生，不手改。

一個里程碑通常對應一張 desk 卡；一張 desk 卡只對一個項目 repo（desk 運作方法 §0）。跨 repo 的里程碑由 desk 拆子卡，SDD 不用拆。

## 5. 業務資料（`data/`）

YAML，給人審也給項目直接讀取，是內容的唯一來源。項目不得自行複製後分歧；要改數值就改這裡。

宣告 `schema: card-pool/v1` 的檔案另外驗證：卡片編號唯一、牌組引用的卡存在、牌組張數與攜帶上限符合檔內 `deck_rules`。

## 6. 變更與版本

- 所有改動走 PR，owner 同意才合併。里程碑轉 `approved` 也是一個 PR：改里程碑狀態、相關檔案的 `status` 與 changelog。合併前由作者以外的 agent 獨立推導可計算的 AC 預期值，結果記在 PR（desk 運作方法 §3 驗收方式）。
- 改動已批准里程碑的 REQ／AC 時，同一 PR 在 `changelog.md` 加一筆：日期、差異、受影響的 REQ／AC、受影響的 desk 卡。項目執行中的 desk 卡依 desk 規則記一筆並停下等重審。
- 版本以 specs 的 commit SHA 識別。項目開工與交付時記下所依據的 SHA（共同治理契約「引用與依賴方向」）。

## 7. 項目如何取用

1. desk 卡 `spec:` 填產品里程碑的連結，例如 `https://github.com/fallrising/specs/blob/main/products/sanguo-cards/milestones.md#m1-可玩切片`。
2. 項目 `AGENTS.md` 寫一行需求來源：`業務需求：fallrising/specs products/<slug>/`。
3. 項目技術設計文件引用 REQ／AC 編號，不複製需求正文；`data/` 以固定 SHA 取用（git submodule、建置時下載或複製加註來源 SHA，由項目決定）。
4. 驗收回報依 desk 運作方法 §3 的表，逐條 AC 附證據。
