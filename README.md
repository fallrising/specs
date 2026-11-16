# specs

所有項目的**業務設計（SDD／PRD）唯一來源**。多數內容由 LLM agent 撰寫，owner 審核後合併。

- 這裡寫「要做什麼、為什麼、做到怎樣算完成、分幾個里程碑」。
- 技術設計（架構、框架用法、資料結構、任務拆解）留在各項目自己的 repo。
- 進度與認領在 [fallrising/desk](https://github.com/fallrising/desk)；desk 卡的 `spec` 指向這裡的檔案。

```
需求源頭（本 repo）           進度（desk）              實作（項目 repo）
products/<slug>/  ──spec──▶  tasks/T-####/task.md ──▶  技術設計、任務、程式、測試
   REQ / AC / 里程碑            一張卡 = 一個里程碑×一個 repo   測試名稱帶 AC 編號
```

## 產品索引

| 產品 | 名稱 | 狀態 | 實作 repo | 入口 |
| --- | --- | --- | --- | --- |
| `sanguo-cards` | 群雄・三國卡牌（暫名），three.js 網頁卡牌對戰 | draft | 未建立 | [README](products/sanguo-cards/README.md) |
| `mmo-economy` | MMO 經濟危機實驗室：生產、交易、查帳與政策分支 | draft | 未指定 | [README](products/mmo-economy/README.md) |
| `space-salvage` | 太空船打撈：拆卸、供電、回收與撤離 | draft | 未指定 | [README](products/space-salvage/README.md) |
| `spellcraft` | 魔法編譯器：組合法術、交互作用與逐步解釋 | draft | 未指定 | [README](products/spellcraft/README.md) |
| `factory-resilience` | 工廠韌性：生產、物流、排程與故障回收 | draft | 未指定 | [README](products/factory-resilience/README.md) |
| `solvable-mystery` | 可解推理案件：可靠線索、唯一兇手與共謀 | draft | 未指定 | [README](products/solvable-mystery/README.md) |
| `distributed-lab` | 分散式故障實驗室：一致性、故障與恢復 | draft | 未指定 | [README](products/distributed-lab/README.md) |
| `orbital-lab` | 軌道任務實驗室：推進、預測、會合與事件 | draft | 未指定 | [README](products/orbital-lab/README.md) |

七個模型挑戰的比較方式見[共同評測規格](docs/model-challenge-evaluation.md)。每題有獨立 PRD、SDD 入口、REQ／AC、業務資料及里程碑；目前皆為草案，收錄不代表批准實作，文件檢查不代表產品驗收。

## 目錄

```
specs/
├── AGENTS.md                 agent 入口（薄入口，引用 desk 共同治理契約）
├── docs/conventions.md       撰寫規範：檔案、編號、狀態、AC、變更、項目如何取用
├── templates/product/        新產品骨架，整個目錄複製後改名
├── products/<slug>/
│   ├── README.md             產品首頁：狀態、實作 repo、desk 卡、文件索引
│   ├── prd.md                願景、對象、範圍／非目標、限制、成功指標
│   ├── sdd.md                可選的業務 SDD 導覽與規則邊界（非技術架構）
│   ├── requirements/*.md     依領域分檔的需求（REQ）與驗收案例（AC）
│   ├── data/                 機器可讀的業務資料（例如卡池），項目直接取用
│   ├── milestones.md         里程碑目標、退出條件、範圍索引（自動產生）
│   └── changelog.md          每次 SDD 變更的差異與影響
├── scripts/check_specs.py    結構驗證；CI 與提交前都跑
└── tests/                    驗證腳本的單元測試
```

## 新增產品

```sh
cp -r templates/product products/<slug>
# 改寫各檔，然後：
python3 scripts/check_specs.py --fix   # 重建里程碑範圍索引
python3 scripts/check_specs.py         # 驗證
python3 -m unittest discover -s tests
```

最後在上方「產品索引」加一列。規則見 [docs/conventions.md](docs/conventions.md)。
