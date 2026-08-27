# 個人 Gmail MVP 落地計畫

> 記錄日期：2026-08-27。這是由 mailbox owner 尚待確認與授權的 `proposed` 計畫，不代表 Gmail API、OAuth scope、資料保存或 AI 使用已獲准。

## 已決定的方向

- 目標信箱：Gmail。
- 執行形態：本機 Node.js／TypeScript 應用程式與本機 Web UI。
- 同步方式：使用者手動觸發，不建立背景常駐服務。
- 決策資料：本機 SQLite。
- 第一階段：Gmail mailbox metadata-only、唯讀，不使用 AI。
- 第二階段：第一階段通過後，才評估讀取正文與 AI shadow。
- 明確排除：寄信、刪信、封存、移動、標記已讀、退訂與附件下載。

## 階段一：Metadata MVP

提議 OAuth scope：

```text
https://www.googleapis.com/auth/gmail.metadata
```

此 scope 可存取 Gmail message metadata，但不能讀取正文。Google 目前將 `gmail.metadata` 與 `gmail.readonly` 都列為 restricted scopes，因此 scope 的最小化不等於免除敏感資料治理。實作前須再次核對 [Gmail API scopes](https://developers.google.com/workspace/gmail/api/auth/scopes)。

提議查詢邊界：

```text
in:inbox newer_than:7d
```

額外限制：

- 每次最多 100 個 threads。
- 不下載附件、不保存正文。
- 支援排除寄件者與 Gmail labels。
- 不處理 Spam 與 Trash。
- 每個 review item 保留 Gmail thread id 與原始連結。

第一階段可使用 From、To、Cc、Subject、Date、labels、unread status、message id 與 thread id，建立 thread 合併、確定性排序及人工 review list。

## 本機決策紀錄

提議資料欄位：

```text
review_decision
- decision_id
- gmail_thread_id
- status
- next_action
- review_after
- reason
- created_at
- updated_at
- rule_version
```

控制條件：

- OAuth credential、token 與 SQLite database 不得提交 Git。
- Token 不以明文存入 repository。
- 相同 `decision_id` 重試不得產生重複紀錄。
- 使用者可匯出並刪除所有 decision records。
- 預設不保存完整 Email 地址與主旨；需要落地時另行確認。
- Retention 提議為 30 天，最終期限為 `missing:mailbox-owner-decision`。

## Google Cloud 人工設定

由 mailbox owner 執行：

1. 建立專用 Google Cloud project。
2. 啟用 Gmail API。
3. 設定 Google Auth Platform。
4. 個人 Gmail 使用 `External` audience 與 `Testing` publishing status。
5. 將自己的 Gmail 帳號加入 Test users。
6. 建立 Desktop app OAuth client。
7. 下載 OAuth credential JSON，放在 repository 之外。

提議本機位置：

```text
~/.config/personal-email-review/google-oauth-client.json
```

Google 官方 Node.js quickstart 使用本機瀏覽器完成 Desktop app OAuth；正式實作前依最新的 [Gmail Node.js quickstart](https://developers.google.com/workspace/gmail/api/quickstart/nodejs) 執行。Testing audience 的授權可能定期失效，屆時需重新登入；不應用擴大 scope 解決此限制。

## 第一階段驗收

必須全部成立：

- Gmail API access 僅含已接受的唯讀 scope。
- 0 次 Gmail mailbox mutation。
- 100% review items 帶來源、抓取時間、規則版本與 access decision。
- 排除寄件者與 labels 的內容 0 筆進入 review list 或 decision store。
- 重複同步不產生重複 decision records。
- 使用者可撤銷 token、匯出與刪除本機衍生資料。
- 一週 shadow 期間，漏掉的 actionable threads 不高於人工 baseline。
- 每日 review time 是否下降須實測；數字目標目前為 `missing`。

## 階段二：正文與 AI shadow

只有階段一通過後，才提議升級為：

```text
https://www.googleapis.com/auth/gmail.readonly
```

條件性 AI 工作：thread 摘要、下一步候選、期限候選與回覆草稿。AI 不得寄送或改變 Gmail 狀態；輸出必須包含 source message ids、不確定性與 abstention reason。

進入此階段前仍需決定：

- 是否允許將正文送往外部模型；目前 `missing`。
- 排除哪些敏感寄件者、labels 與內容類型；目前 `missing`。
- 模型供應商、retention、訓練使用政策與地區；目前 `missing`。
- 版本化 evaluation set 與 AI 相較 metadata baseline 的增量門檻；目前 `missing`。

## 下一個工作包

在 repository 建立 Gmail metadata MVP 骨架與合成資料測試，先不需要真實 credential。完成條件是：合成 thread 可以被同步、合併、排序並產生 review list；decision records 可建立、重試、匯出與刪除；測試能證明沒有任何 Gmail mutation path。

真實 credential 只在這個合成切片通過後，由 mailbox owner 放入指定的 repository 外位置。
