# FDE 案例索引

這些案例用來教學、壓力測試或驗證 FDE operating-analysis 方法。案例狀態描述 repository 中真正存在的交付深度，不代表任何目標企業已接受、授權、上線或取得成效。

| 案例 | 主要決策 | Repository 交付深度 | 入口 |
| --- | --- | --- | --- |
| 第三方 API 變更監測 | 如何取代被動人工檢查，AI 應介入哪一段？ | Operating analysis、scenario、HTML、development handoff；刻意不含 capability implementation、fixtures、replay 與 tests | [案例頁](third-party-api-change-monitoring/index.html) · [開發交接](third-party-api-change-monitoring/artifacts/development-handoff.md) |
| 補貨決策演進 | 如何讓建議從合成 baseline 演進，同時守住治理邊界？ | Proposal、deterministic implementation、fixtures、tests、expected output、capability-return review | [案例頁](inventory-replenishment-evolution/index.html) · [說明](inventory-replenishment-evolution/README.zh-TW.md) |
| 決策記憶與模型演進 | 如何把修正與結果變成受治理的能力候選？ | Proposal、scenario、decision episode schema、replay evidence、closure review | [案例頁](decision-memory-evolution/index.html) · [說明](decision-memory-evolution/README.zh-TW.md) |
| 客戶退款狀態 | 如何把 operating solution 轉成可驗證的多格式交付套件？ | Proposal、analysis package、HTML、presentation、DOCX 與 validation evidence | [案例頁](customer-refund-status-delivery-kit/index.html) · [說明](customer-refund-status-delivery-kit/README.md) |
| 帳務對帳 | 精準匹配是否需要 AI？ | Deterministic read-only replay、fixtures、tests、expected result；AI not needed | [說明](account-reconciliation/README.zh-TW.md) |
| 出貨延遲優先級 | 如何在 access、freshness 與語意版本下提供唯讀排序？ | Scenario、evidence、deterministic replay、tests、expected result | [說明](shipment-delay-priority/README.zh-TW.md) |
| 個人 Email 管理 | 如何先交付唯讀每日審閱，再評估 AI shadow？ | Operating proposal、scenario、HTML 尚未提供；真實信箱 access 與 baseline 缺失 | [說明](personal-email-management/README.zh-TW.md) |
| 供應商發票例外 | 例外流程應先修責任，還是先加入 AI？ | Markdown 與 HTML operating proposal | [案例頁](vendor-invoice-exception-proposal/index.html) |

## 如何閱讀狀態

- `evidenced`：有可追溯來源與新鮮度的證據。
- `proposed`：等待 accountable owner 評估的設計或判斷。
- `missing`：尚未取得，但後續決策必須補齊。
- `unverifiable`：目前可用證據無法確認，因此限制主張或行動。

Schema pass、fixture replay 或單元測試只證明 repository 行為；不能證明企業事實、權限、production readiness 或價值。
