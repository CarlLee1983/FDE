# FDE Project Work Skill 操作指南

`fde-project-work` 是可安裝至 Codex 與 Claude Code 的可攜式營運分析 Skill。它把有邊界的營運問題轉成受證據限制的營運方案與下一個有責任歸屬的行動；它不是企業平台、預設建置要求，也不證明企業已接受、授權、上線或取得價值。

安裝包可獨立使用：它攜帶必要的方法快照、scenario schema 與 validator，絕不把目標 repository 的 `README.md`、`CONTEXT.md` 或 `docs/` 當成 FDE 指引。

## 安裝與呼叫

從 FDE checkout 安裝到另一個 Git repository 的根目錄：

```bash
scripts/install-skill.sh --target /path/to/project --agent codex
scripts/install-skill.sh --target /path/to/project --agent claude
scripts/install-skill.sh --target /path/to/project --agent both
```

從 `/path/to/project` 啟動所選宿主。Codex 使用 `$fde-project-work`；Claude Code 使用 `/fde-project-work`。說明營運問題、預期結果，以及是否明確要求 proposal、scenario record、build 或 assurance review。

Installer 只會建立下列一個或兩個目錄，且會拒絕覆寫已存在的 Skill：

```text
.agents/skills/fde-project-work/  # Codex
.claude/skills/fde-project-work/  # Claude Code
```

可丟棄 repository 的完整操作、更新與移除步驟見[五分鐘 Quick Start](quickstart.md)。

## 選擇工作模式

預設是 operating analysis，完整結果固定有五部分：

1. 營運問題與預期結果。
2. 現行工作的診斷。
3. 技術中立的目標工作流程。
4. 介入方式、AI 適用性與證據限制。
5. 下一個有責任歸屬的行動。

只有明確要求才會啟用其他模式：

| 要求 | 模式 | 接著讀取 |
| --- | --- | --- |
| Proposal 或利害關係人文件 | Solution proposal | `references/solution-proposal.md` |
| Scenario record 或 preparation package | Scenario preparation | `references/task-modes.md` 與隨包 schema |
| 建置或修改可工作的 capability | Capability build | `references/agent-delivery-loop.md` 與該切片需要的方法參考 |
| Gate、control、authority、release 或持久性 action 的 review | Assurance | 對應的方法 gate 與 control 參考 |

穩定規則、計算、控制與可重複狀態轉換交給確定性軟體；只有保留下來的語言密集工作經證據顯示 AI 優於非 AI 流程時，才考慮 AI。缺少的企業證據維持 `missing`、`proposed` 或 `unverifiable`，不會被編造。

## 驗證 scenario

需要 `uv`。切換到已安裝的 Skill 目錄後，兩種宿主都執行相同指令：

```bash
./scripts/validate-scenario.sh /path/to/scenario.json
```

指令成功只證明 schema 與 record 結構，不代表企業已核准、來源可存取、已授權或已有價值。

## 安裝包結構與維護

```text
fde-project-work/
├── SKILL.md
├── references/
│   ├── source-map.md
│   ├── packaged-sources.json
│   └── canonical/             # 已同步的必要方法快照
├── schemas/fde-scenario.schema.json
└── scripts/validate-scenario.sh
```

依目前分支按需讀取 `references/source-map.md`。它定位隨包的本機參考；大型案例、翻譯與方法理由是固定版本的選讀資料。

FDE 維護者修改 `packaged-sources.json` 列出的 canonical source 後，必須在發佈前同步：

```bash
python3 scripts/sync-skill-references.py
python3 scripts/sync-skill-references.py --check
make verify
```

`make verify` 會拒絕缺少的隨包檔案、逃出 Skill 的連結、canonical／package 漂移與不完整的 snapshot manifest。
