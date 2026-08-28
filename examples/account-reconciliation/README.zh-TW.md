# 帳務對帳：工作流優先的最小可重播範例

> **純合成 repository 範例。** 這不是企業流程、系統連線、授權、基線、目標或驗收的證據；所有這些目標企業主張均為 `missing`、`proposed` 或 `unverifiable`。

此範例先重整對帳工作，再採用最小的確定性規則：在單一帳戶、單一幣別、單一已關帳期間的不可變新鮮快照中，依版本化 reference、幣別、整數 minor units 與日期做唯讀一對一精準比對。它不使用 AI、不寫回、不連線至任何銀行或總帳。

## 三步使用

1. 驗證情境、單元測試與 golden output：

   ```bash
   examples/account-reconciliation/scripts/validate-example.sh
   ```

2. 重播預設的合成資料：

   ```bash
   python3 examples/account-reconciliation/scripts/replay_account_reconciliation.py
   ```

3. 閱讀工作流與控制邊界：[case-analysis.md](artifacts/case-analysis.md)。

結果包含 `result`、`semanticDefinitionVersion`、`decisionServiceVersion`、`sourceEvidence`、`freshness`、`accessDecision` 與 `writeBack: false`。精準匹配會列出；多個候選會 abstain，同 reference 的金額差異會合併為一個具名例外，單邊資料也會進人工 review queue。資料過期、來源或控制總數衝突、ID 無效或重複、access 不允許／不相符，或語意與規則契約漂移時，replay fail closed，沒有結果可供採用。

所有輸入都在此目錄內，且 replay 不建立或修改檔案。若要套用至真實組織，必須由其負責人提供並驗證流程、語意、來源、身分與權限、基線與目標、驗收及 write-back 控制；不能沿用這個 fixture 當作任何一項授權。
