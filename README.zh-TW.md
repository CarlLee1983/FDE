# FDE 能力強化

> 本文件為閱讀用繁體中文譯本；英文版 [README.md](README.md) 是維護中的來源文件。

本專案專注於強化 FDE（Forward Deployed Engineer）的能力。

專案入口：[GitHub Pages 靜態首頁](index.html) · [完整案例索引](examples/README.zh-TW.md)

使用者提供的「本體論驅動 FDE」架構保留為參考模型。它協助識別 FDE 應建立的能力：共用的業務語義、具證據的上下文、受控行動與持續治理；但它不會單獨定義本專案的交付範圍。

## 目前方向

1. 定義一個可量測的業務情境。
2. 為該情境建立共用語義模型。
3. 取得具有來源血緣且符合權限的上下文。
4. 在啟用受控行動前，先交付決策支援。
5. 將可重用資產累積至下一個情境。

請從 [FDE 能力強化計畫](FDE-Capability-Enhancement-Plan.zh-TW.md) 與 [FDE 參考研究（繁中）](docs/zh-TW/README.md) 開始閱讀。

將業務情境轉為受治理 FDE 能力的工作方法，請參閱 [FDE 情境至行動方法](FDE-Scenario-to-Action-Method.zh-TW.md)。

## GitHub Pages

本 repository 已提供純靜態網站與 GitHub Actions workflow。Repository owner 在 GitHub Pages 設定中選擇 **GitHub Actions** 為發布來源後，push 到 `main` 會先組裝並驗證 artifact，再執行部署。此網站展示專案方法與合成案例，不代表任何企業已接受、授權、上線或取得成效。

## 參與與授權

[貢獻指南](.github/CONTRIBUTING.md)說明邊界檢查與三道驗證指令；安全問題走 GitHub 私下回報，見[安全政策](.github/SECURITY.md)，不要開公開 issue。社群行為依[行為準則](.github/CODE_OF_CONDUCT.md)，已發佈版本記於[變更紀錄](CHANGELOG.md)。

本專案採用 MIT License，全文位於 repository 根目錄的 `LICENSE`，不納入靜態網站發佈內容。
