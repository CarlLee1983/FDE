# 五分鐘 Quick Start

本指南會把 FDE 營運分析 Skill 安裝到一個可丟棄的 Git repository，並完成第一次營運分析。Skill 的產出是協助決策的 minimum operating solution；它不證明企業 acceptance、authority、production readiness 或 value。

## 1. 取得 FDE

安裝 Git、Make 與 [uv](https://docs.astral.sh/uv/)，再 clone repository：

```bash
git clone https://github.com/CarlLee1983/FDE.git
cd FDE
make verify
```

也可以下載並解壓 source archive 來安裝 Skill。`make verify` 需要 Git checkout，因為正式 scenario 與 Pages 內容只從 tracked files 選取。

## 2. 安裝到測試 repository

建立一個暫時 Git repository，並各自安裝 Codex 與 Claude Code 的實體副本：

```bash
target_dir="$(mktemp -d)"
git -C "$target_dir" init
scripts/install-skill.sh --target "$target_dir" --agent both
```

安裝到正式專案時，把 `$target_dir` 換成該 repository root。也可以使用 Make：

```bash
make install-skill TARGET=/path/to/project AGENT=both
```

## 3. 確認安裝結果

```bash
test -f "$target_dir/.agents/skills/fde-project-work/SKILL.md"
test -f "$target_dir/.claude/skills/fde-project-work/SKILL.md"
test ! -L "$target_dir/.agents/skills/fde-project-work"
test ! -L "$target_dir/.claude/skills/fde-project-work"
```

Installer 不會修改目標專案的 `AGENTS.md`、`CLAUDE.md`、README 或其他設定。

每份安裝的 Skill 都包含必要的 FDE 方法快照、scenario schema 與 validator，不會把目標 repository 裡同名的檔案誤認為 FDE 指引。大型 synthetic example、翻譯與方法理由屬於已釘選版本的選讀外部參考，列在安裝包的 `references/source-map.md`；Skill 的獨立使用不依賴它們。

工作模式、安裝包結構與維護流程請見 [Skill 操作指南](fde-project-work-skill.md)。

## 4. 呼叫 Skill

從目標 repository 啟動 Codex 或 Claude Code。Codex 直接貼上完整 prompt；Claude Code 先呼叫 `/fde-project-work`，再貼上同一個營運問題。以下完整文字也已明確指定 Skill：

```text
Use $fde-project-work to analyze this operating problem:

每週五，營運人員手動下載合作商 CSV，重新命名固定欄位、
移除缺少帳號的資料、轉換日期、去除重複列後交給匯入人員。
規則已固定且有版本，這項工作每週約花二十分鐘。
請判斷下一步應該做什麼，以及是否需要 AI。
```

預期答案包含五個區段：

1. 營運問題與預期結果。
2. 現行工作的診斷。
3. 技術中立的目標工作流程。
4. 介入方式、AI 適用性與證據限制。
5. 下一個有責任歸屬的行動。

這個 prompt 中的轉換規則已固定，因此應先考慮確定性軟體，而不是 AI。Skill 應標示假設與證據缺口，不得編造企業證據。

## 5. 從任一宿主驗證 scenario

validator 唯一的工具依賴是 `uv`。從已安裝的 Skill 目錄執行，所以 Codex-only 與 Claude-only 都使用同一個命令：

```bash
cd /path/to/project/.agents/skills/fde-project-work # Codex
# 或：cd /path/to/project/.claude/skills/fde-project-work # Claude Code
./scripts/validate-scenario.sh /path/to/scenario.json
```

## 6. 更新或移除

Installer 會刻意拒絕覆寫既有 Skill。更新前先檢查或備份本地 Skill 變更，再更新 FDE checkout、只移除已安裝的 Skill 目錄，然後重新安裝：

```bash
git -C /path/to/FDE pull --ff-only
rm -r -- /path/to/project/.agents/skills/fde-project-work
rm -r -- /path/to/project/.claude/skills/fde-project-work
/path/to/FDE/scripts/install-skill.sh --target /path/to/project --agent both
```

只要執行適用的 `rm -r` 指令即可移除 Skill。Installer 不會建立或修改其他目標 repository 檔案。

專案邊界與深入參考資料見[繁中 README](../../README.zh-TW.md)。
