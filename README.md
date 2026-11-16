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

## 目錄

```
specs/
├── AGENTS.md                 agent 入口（薄入口，引用 desk 共同治理契約）
├── docs/conventions.md       撰寫規範：檔案、編號、狀態、AC、變更、項目如何取用
├── templates/product/        新產品骨架，整個目錄複製後改名
├── products/<slug>/
│   ├── README.md             產品首頁：狀態、實作 repo、desk 卡、文件索引
│   ├── prd.md                願景、對象、範圍／非目標、限制、成功指標
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
