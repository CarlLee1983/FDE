# AI 數據分析師演進：用決策記憶持續打造模型工具箱

> **Synthetic demo only。** 本案例的人員、數字、資料來源、權限、基線與結果都是為了說明方法而虛構。它不能證明任何企業已經核准、上線或得到效益。

這個案例打造一位會持續擴充分析工具箱的 AI 數據分析師。它不只把每週營收數字改寫成文字，而是驗證資料、拆解變化、建立競爭性假設、尋找反證，並從人工修正與結果中提出下一個數據模型候選。

案例以 B2B 客戶訂購節奏下降為場景。決策記憶不是最終目的，而是分析師演進所需的證據機制：

```text
商業訊號 → 來源證據 → 人類解讀 → 決策與理由 → 行動 → 後續結果
```

這條決策鏈同時餵養兩條迴路：營運迴路幫助人員完成今天的審閱；演進迴路從反覆修正與結果中提出下一個能力候選。AI 可以整理與提議，但不能自行把一次成功寫成政策，也不能自行發布正式能力。

已穩定的分析方法會下沉成語意、指標、診斷、行為、決策或結果模型；AI 使用這些模型探索下一個未知問題。人類 owner 接受模型定義和商業判斷，受治理的交付流程負責測試、發布、監控與回復。

案例的核心資產是一筆不可覆寫的 `DecisionEpisode`。後續修正以新紀錄取代舊解讀的效力，但保留當時看到的證據、版本與判斷；歷史重播只能使用決策當時已存在的資料，不能偷看後來才發生的結果。

## 主要入口

- 適合展示與講解：[index.html](index.html)
- 詳細案例與交付方案：[artifacts/operating-solution-proposal.md](artifacts/operating-solution-proposal.md)
- AI 分析師與模型演進：[artifacts/analyst-model-evolution.md](artifacts/analyst-model-evolution.md)
- Append-only 決策紀錄契約：[artifacts/decision-episode.schema.json](artifacts/decision-episode.schema.json)
- 案例結案審查：[artifacts/closure-review.md](artifacts/closure-review.md)
- 三組合成 DecisionEpisode revisions：[evidence/decision-episodes.json](evidence/decision-episodes.json)
- 合成 replay report：[evidence/replay-report.json](evidence/replay-report.json)
- 原始需求：[request.md](request.md)
- 提議中的 scenario record：[scenario.json](scenario.json)

## 一分鐘理解

舊流程每週產生客戶營收報表。發現客戶 A 訂購下降後，分析人員再到訂單、客服紀錄、續約資料與業務訊息中找原因。會議最後可能決定請業務確認，但判斷理由與後續結果分散各處。三個月後遇到相似客戶，團隊又從頭查一次。

新流程先用確定性模型找出值得審閱的訂購變化並拆解頻率、單價與組合。AI 數據分析師建立採購延後、服務阻塞、需求下降與資料缺漏等競爭性假設，列出支持、反對與缺少證據，再由人類決定下一個查證。流程與 baseline 經真實 owner／使用者確認後，才以 shadow 驗證 AI 是否帶來增量價值。

當三組合成 episode 的初版與修正版都顯示分析人員反覆漏看「決策當時仍未結案的服務事件」，AI 提出新的 [context model candidate](artifacts/model-candidate.json)。合成 replay 只證明案例形狀成立；真實能力仍須 owner 接受與 shadow evidence，才能發布成版本化的 `assembleAccountReviewContext()` 工具。

## 客戶 A 的合成故事

| 項目 | 示例 | 能證明什麼 |
| --- | ---: | --- |
| 最近四週訂購金額 | 下降 24% | 有值得審閱的變化，不等於已流失 |
| 訂購頻率 | 每月 4 次降為 2 次 | 變化主要來自頻率，而非單價 |
| 平均訂單金額 | 大致持平 | 不支持「全面縮減預算」的直接結論 |
| 未結服務事件 | 1 件 | 可能相關，但尚不能證明因果 |
| 合約續約 | 45 天後 | 提高審閱時效的重要性 |
| 業務說明 | 採購排程待確認 | 是待查證敘述，不是已驗證事實 |

主管可以決定「請帳戶負責人在五個工作日內確認採購排程與服務事件」，並留下理由。三十天後若訂購恢復，這是後續觀察，不足以單獨證明原判斷正確或服務事件造成下降。

## 最重要的責任邊界

| 工作 | 最適合的負責者 |
| --- | --- |
| 排程、資料取得、權限、新鮮度與變化計算 | 確定性軟體 |
| 已發布的比較期、異常條件與診斷工具 | 版本化規則或統計工具 |
| 綜整文字脈絡、揭露矛盾、比較允許使用的過往決策 | 條件性 AI 助手 |
| 接受解讀、選擇行動、承擔客戶判斷 | 人類主管與帳戶負責人 |
| CRM 寫入、派工或客戶聯繫 | 經授權、可稽核且可復原的系統或人類行動 |

AI 不得把客戶標記為流失、自行聯繫客戶、指派任務、修改 CRM 狀態，或發布自己提出的新規則。

## 第一個真實切片

先選擇一個商業單位和 10–20 筆歷史或已獲准的帳戶審閱案例。第一版只做：

1. 使用已接受的營收與訂購頻率定義，確定性標示變化。
2. 顯示來源、資料時間、定義版本、品質與 access decision。
3. 讓主管記錄 `monitor`、`verify` 或 `escalate`，以及結構化理由。
4. 設定人工觀察期限，補記後續結果。
5. 透過具名的受控 journal action 追加決策版本，產生可重播時間線；不自動寫入 CRM 或聯繫客戶。

這個切片即使沒有 AI 仍然有價值：它先證明共同定義、證據品質與決策留痕流程可信。Journal 本身仍是持久寫入；真實環境必須另有授權、稽核、冪等、重複提交處理與復原證據，不能因為「不寫 CRM」就視為唯讀。Readiness 通過後，AI 才以 shadow 方式在相同案例上產生綜整，與人工 baseline 比較增量價值。

## 證據狀態

本案例目前是 `proposed`，AI selection 是 `deferred`。真實流程負責人、使用者驗證、資料權限、指標定義、歷史基線、CRM 控制與商業成效全部是 `missing` 或 `unverifiable`。因此它只能用來說明和演練方法，不能宣稱已能辨識流失、改善留存或直接上線。Synthetic 教學案例文件已完成，可依[結案審查](artifacts/closure-review.md)在 repository 範圍結案；企業交付不可結案。

## 下一個負責行動

由真實商業營運流程負責人召集主管、帳戶負責人、分析人員與資料 owner，確認 normal／exception／escalation／rework 路徑，選定一個商業單位與 10–20 筆可合法使用的案例，接受最小決策紀錄欄位與 shadow 比較方式。

完成條件是：技術中立的目標流程獲得負責人與使用者接受，必要來源、定義與權限有直接證據，且團隊能從原始訊號重播到人工決策及結果觀察。
