# FDE 營運分析

> 本文件是繁體中文閱讀版；英文 [README.md](README.md) 是維護中的來源文件。

專案網站：[靜態首頁](index.html) · [案例索引](examples/README.zh-TW.md)

本專案強化 FDE（Forward Deployed Engineer）的**營運分析 skill**：把有邊界的營運問題轉成受證據限制的營運方案與下一個有責任歸屬的行動。它不是企業應用平台、交付工具箱或預設實作 roadmap。

## 預設產出

預設產出是最小充分的五段式 minimum operating solution：

1. 營運問題與預期結果。
2. 現行工作的診斷。
3. 技術中立的目標工作流程。
4. 介入方式、AI 適用性與證據限制。
5. 下一個有責任歸屬的行動。

Skill 先重整工作、責任、定義與證據流。核心原則是：**穩定規則交給軟體，語言負擔才考慮 AI。** 固定規則、計算、控制與可重複的狀態轉換交給確定性軟體；只有保留下來的工作確實具有語言理解、整合、說明或有限推理負擔，而且有證據顯示 AI 優於非 AI 流程時，才考慮 AI。`不需要 AI` 是完整的決策。

## 能力邊界

本專案的封閉能力集合是：

1. 營運問題界定。
2. 工作流程診斷與重整。
3. 介入選擇與 AI 適用性判斷。
4. 營運方案形成。
5. 只有在明確要求時才提供的條件式交付與 assurance 協助。

## 安裝與驗證

前置需求是 Git、Make 與 [uv](https://docs.astral.sh/uv/)。開發工具版本固定於 `pyproject.toml` 與 `uv.lock`。

```bash
git clone https://github.com/CarlLee1983/FDE.git
cd FDE
make verify
```

將 Skill 實體安裝到另一個 Git repository：

```bash
scripts/install-skill.sh --target /path/to/project --agent codex
scripts/install-skill.sh --target /path/to/project --agent claude
scripts/install-skill.sh --target /path/to/project --agent both
# 或
make install-skill TARGET=/path/to/project AGENT=both
```

Installer 只會寫入 `.agents/skills/fde-project-work/` 與／或 `.claude/skills/fde-project-work/`。每份副本都包含必要的方法參考、schema 與 validator，且不會把目標專案的同名檔案當成 FDE 指引。若 Skill 已存在，指令會拒絕覆寫本地變更。安裝、第一次使用、驗證、更新與移除流程見[五分鐘 Quick Start](docs/zh-TW/quickstart.md)；工作模式與封裝維護見 [Skill 操作指南](docs/zh-TW/fde-project-work-skill.md)。

## 來源階層

[CONTEXT.md](CONTEXT.md) 定義 canonical project language；已接受的 [ADR](docs/adr/) 管理難以回復的決策；[FDE 營運分析 Skill](.agents/skills/fde-project-work/SKILL.md) 管理 runtime behavior。README 是入口，supporting material 不得自行擴張這個邊界。

[FDE 情境至行動方法](FDE-Scenario-to-Action-Method.zh-TW.md) 是案例需要更深建模、assurance 或交付支援時才使用的完整參考方法。[FDE 能力強化計畫](FDE-Capability-Enhancement-Plan.zh-TW.md) 說明如何跨案例驗證分析品質。

[FDE 參考研究](docs/zh-TW/README.md)與企業架構材料是 supporting reference。情境登錄、語義定義、上下文解析、決策支援與受控行動是案例有需要時才選用的 solution patterns，不是本專案必建模組或 roadmap。

Models、schemas、artefacts、gates、research 與 implementation 都只在不確定性、風險、權限、持久性或明確要求足以支持時才使用。合成案例可以驗證推理與 repository behavior，不能證明任何目標企業的事實、接受、權限、production readiness 或價值。

## Repository 驗證

`make verify` 是本地與 CI 的單一入口。它執行根目錄與所有 examples tests、驗證所有 Git tracked `examples/**/scenario.json` 與 schema metaschema、建置 tracked-only Pages artifact、檢查 HTML、Markdown、CSS 與 local links，並驗證 Skill 結構及 frontmatter。Untracked scenario 與 Pages 檔案不屬於 release validation；要納入結果前必須先加入 Git。

```bash
make test
make validate-scenarios
make validate-pages
make verify
```

Pull Request 與 `main` push 都執行相同的 `make verify`。只有 `main` 的非 PR 執行在驗證成功後可以部署 Pages。這些結果只證明 repository behavior，不代表企業 acceptance、access、authority、production readiness 或 business value。

## 參與與授權

[貢獻指南](.github/CONTRIBUTING.md)說明邊界與驗證要求；安全問題走 GitHub 私下回報，見[安全政策](.github/SECURITY.md)，不要開公開 issue。社群行為依[行為準則](.github/CODE_OF_CONDUCT.md)，已發佈版本記於[變更紀錄](CHANGELOG.md)。

本專案採 MIT License，全文位於 repository 根目錄的 `LICENSE`，不納入靜態網站發佈內容。
