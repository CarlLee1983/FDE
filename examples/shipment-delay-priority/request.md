# 出貨延誤優先序參考請求

為物流團隊建立一個最小可重播的 FDE 案例：客服與物流人員每天人工掃描出貨清單，延誤、關鍵貨件與資料不完整的例外混在一起，沒有一致的優先序與升級依據。

案例必須證明一件事：一位具名的合成使用者，在具名情境與唯讀權限內，能從新鮮且語意完整的出貨快照取得確定性排序、原因與資料品質 escalation。不使用 AI、不保存人工 disposition、不執行 ERP 回寫；access、freshness 或語意版本任一不符即 fail closed。

本 repository 請求只建立 synthetic demo。所有人員、資料、授權、基線、目標與結果都是 fixture，`missing` 與 `unverifiable` 標記的項目仍需目標企業補齊。
