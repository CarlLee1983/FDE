# Forward Deployed Engineer——一手來源紀錄

> **閱讀翻譯。** 英文版為持續維護的原始文件；本文件為繁體中文閱讀譯本。

**目的。** 本備忘錄記錄擁有 Forward Deployed Engineer（FDE）這個職稱的組織，在其自己的職缺說明、部落格、文件、申報文件與公告中，實際怎麼描述這個角色。它確立了 Palantir、Anthropic 與 OpenAI 各自如何定義此角色，以及描述它所處的合作模式。本備忘錄**不**主張這些定義中的任何一個適用於本儲存庫，不建議採用這些作法，也不擴大或改變 `CONTEXT.md` 與 `docs/adr/` 所設定的能力界限。職缺公告是會過期的快照；以下每一項主張都標記為 **verified**（於本次執行期間在所引 URL 讀取）或 **inferred**（本作者跨來源綜合的解讀）。

## 來源事實

### 1. Palantir 自身對此角色的定義

Palantir 在其現行職缺說明中表示，此職稱由它首創：「At Palantir, the Forward Deployed Software Engineer (FDSE) role isn't just a job title: it's the blueprint. We pioneered this unique position, embedding talented engineers directly with our customers to tackle their most pressing challenges head-on.」同一則公告將此工作定義為「architecting and building solutions that leverage business-critical data」，並列出核心職責，包括架構與設計協作、「wrangling massive-scale data」、「developing custom applications tailored to customer needs」、「engaging directly with customer stakeholders, from technical teams to executives」，以及「shaping team strategy and driving projects from ideation to deployment」。所要求的資歷明顯不高：「1+ years of relevant, post-college work experience」，具備 Python/Java/C++/TypeScript「or similar」的紮實程式能力，以及「ability and interest to travel up to 25%」。公告載明的薪資範圍為 $135,000–$200,000/年，外加 RSU。**verified** —— [Palantir, Forward Deployed Software Engineer, New York](https://jobs.lever.co/palantir/dab396d4-2f14-4796-aac0-0d82883dccf0)。**取得日期：** 2026-08-29。

對能力界限最鮮明的陳述，來自 Palantir 自家的工程部落格。它將平台工程師（「Dev」）與前線部署工程師（「Delta」）區分開來：「Devs (Software Engineers) develop and engineer our software platforms… Deltas (Forward Deployed Software Engineers) deploy our software platforms to customers… You can think of a Dev's focus as 'one capability, many customers,' while a Delta's focus is 'one customer, many capabilities.'」該文也提到 Delta 在組織上隸屬於 Business Development，且「their mandate is to achieve technical outcomes for our customers… They measure success in terms of impact on the customer's goal.」**verified** —— [Palantir, "Dev versus Delta: Demystifying engineering roles at Palantir", 2019-04-09](https://blog.palantir.com/dev-versus-delta-demystifying-engineering-roles-at-palantir-ad44c2a6e87)。

兩份來源都明確拒絕「顧問」這種框架。Dev-versus-Delta 這篇文章引用一位具名從業者的話：「consultants generally create a one-time analysis, recommendation, or solution to a specific problem, while at Palantir we work together with our customers to build a long-term solution that allows the customer to continuously improve themselves.」在一篇姊妹文中受訪的一位 FDSE 表示，差異在於「we can pull most of the pieces together out-of-the-box, meaning we don't need to reinvent the wheel for each customer.」**verified** —— [Palantir, "A Day in the Life of a Palantir Forward Deployed Software Engineer", 2020-11-02](https://blog.palantir.com/a-day-in-the-life-of-a-palantir-forward-deployed-software-engineer-45ef2de257b1)。

**解讀。** Palantir 的 FDE 是由*槓桿方向*來定義，而不是由資深程度或某個獨立的工程學門來定義：平台已經存在，工程師的工作是針對單一客戶的營運問題去配置與擴充它。1 年以上經驗這道門檻低，也與此一致——槓桿來自平台本身，而非個人的年資。**inferred**，此判斷同時參照上述兩篇部落格文章與職缺說明。

### 2. Palantir 的建置／維運界限，以及界限兩側的角色

那篇 FDSE 訪談明確指出，維運責任並不在交付當下就結束：「I often engage in engineering reviews, code reviews, deployability optimization, maintenance and monitoring of production systems.」所列出的技術挑戰之一是：「How do I investigate a production software outage, identify a root cause of the issue, deploy a fix, and monitor the stack for stability while coordinating communication between product teams, our deployment team, and the customer?」**verified** —— 同上引 2020-11-02 貼文。

然而 Palantir 仍將維運端另外編制人力。Forward Deployed Enablement Engineer 這則職缺說明中，描述工程師「embedded with centralized customer success teams to maximize the outcomes of our deployed products and workflows」，負責分流支援請求、協助客戶端工程師排除阻礙，並參與「a 24/7 on-call rotation responsible for coordinating responses to critical customer-facing incidents」。**verified** —— [Palantir, Forward Deployed Enablement Engineer – Customer Success, New York](https://jobs.lever.co/palantir/4cba9c95-d16f-440d-83e7-2352480f689f)。**取得日期：** 2026-08-29。

非工程職的對應角色是 Deployment Strategist，其職缺說明描述要「onsite and meet[ing] with customer analysts to understand the critical questions they need to answer and locate their biggest problems」，找出相關資料集，接著「work[ing] with Forward Deployed Engineers to integrate the data into a stable and extensible pipeline」並主導使用者訓練。要求的出差比例為「25 – 75%」。**verified** —— [Palantir, Deployment Strategist, New York](https://jobs.lever.co/palantir/e0ab8226-b928-4e3a-bf87-08fe7b1ea595)。**取得日期：** 2026-08-29。

### 3. Palantir 角色家族的規模與內部區分

Palantir 公開的 Lever 職缺資料流在取得日期當天列有 307 則公開職缺，其中 68 則職稱以「Forward Deployed」開頭：50 則 Forward Deployed Software Engineer、7 則 Forward Deployed Infrastructure Engineer、3 則 Forward Deployed Enablement Engineer、2 則 Forward Deployed AI Engineer、2 則 Forward Deployed Reliability Engineer，以及各 1 則 Forward Deployed Engineer、Forward Deployed Security Engineer 與 Forward Deployed Site Reliability Engineer。**verified** —— 直接從 [Palantir 的 Lever 職缺 API](https://api.lever.co/v0/postings/palantir?mode=json) 計數所得。**取得日期：** 2026-08-29。這僅是單一招募日的快照，不構成任何趨勢主張。

Forward Deployed AI Engineer 這個變體，其描述用語更貼近本儲存庫的主題：「Forward Deployed AI Engineers work directly with customers owning Gen AI strategy and implementation. On a daily basis, you will build end-to-end workflows, take them to production, and solve real world problems at the largest scale.」其列出的價值觀包括「Solving real business problems, not academic benchmarks」，並要求「past experience building solutions with LLMs」加上「a strong foundation in Machine Learning basics (Evaluation, Training, Problem Decomposition)」。薪資範圍與 FDSE 職缺相同，同為 $135,000–$200,000。**verified** —— [Palantir, Forward Deployed AI Engineer, New York](https://jobs.lever.co/palantir/636fc05c-d348-4a06-be51-597cb9e07488)。**取得日期：** 2026-08-29。

**詞彙警告。** Palantir 現在也將「AI FDE」用作*產品*名稱，而非角色名稱：其 Foundry 文件將「AI FDE, the AI-powered forward deployed engineer」定義為「an interactive agent that operates Foundry for you through conversational commands」，它會編輯本體、撰寫函式、稽核權限，並在分支上提出變更以供審查，而非直接套用變更。**verified** —— [Palantir Foundry docs, AI FDE Overview](https://www.palantir.com/docs/foundry/ai-fde/overview)。任何人在這份文件出現之後引用 Palantir 材料中的「FDE」一詞，都必須先確認來源指的是人還是代理程式（agent）。

### 4. Palantir 對投資人陳述的合作進場模式

Palantir 最新的 Form 10-K，將標準的合作進場方式描述為免費或低成本的試用：「We often also provide our platforms to potential customers (including individual users at such customers) at no or low cost initially to them for evaluation purposes through short-term pilot deployments of our platforms, including at bootcamps, and there is no guarantee that we will be able to convert customers from these short-term pilot deployments to longer-term revenue-generating contracts.」**verified** —— [Palantir Technologies Inc., Form 10-K for FY2025, filed 2026-02-17](https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm)。

值得記下的一項負面發現：「forward deployed」這個詞在該 10-K 中完全沒有出現，「Deployment Strategist」也沒有。**verified** —— 本次執行期間對該申報文件做全文檢索所得。這個角色是 Palantir 公開文宣中招募與工程文化的構造，而不是公司在投資人揭露文件中使用的用語。任何把 FDE 當成 Palantir 官方陳述的商業模式的敘事，其依據僅在於徵才網站與部落格，而非申報文件。**inferred**。

### 5. Anthropic 的 Forward Deployed Engineer

Anthropic 現行的職缺公告將此角色放在 Applied AI 團隊之下：「you will be a Forward Deployed Engineer (FDE) who embeds directly with our most strategic customers to drive transformational AI adoption. You will collaborate closely with customer teams to ship advanced AI applications that solve real world business problems.」所列出的交付項目異常具體：「Work within customer systems to build production applications with Claude models」；「Deliver technical artifacts for customers like MCP servers, sub-agents, and agent skills that will be used in production workflows」；「Provide white glove deployment support」；「Identify and codify repeatable deployment patterns and contribute insights back to our Product and Engineering teams.」該公告也表示這批新進人員「serve as one of our founding FDEs who helps to shape our forward-deployed motion」，且 Anthropic 期望他們「to operate autonomously, thrive under ambiguity」。資格要求為 4 年以上技術性、面對客戶的職務經驗，「production experience with LLMs including advanced prompt engineering, agent development, evaluation frameworks, and deployment at scale」，以及 Python 熟練度；出差比例估計為 25%。年薪載明為 $280,000–$320,000 美元。**verified** —— [Anthropic, Forward Deployed Engineer (New York / San Francisco / Seattle)](https://job-boards.greenhouse.io/anthropic/jobs/5302966008)，公告最後更新於 2026-08-21。**取得日期：** 2026-08-29。

在取得日期當天，Anthropic 的公開職缺板列有五則以 Forward-Deployed 為職稱的職缺：上述 FDE 職缺、慕尼黑與巴黎的 FDE 職缺、倫敦的 Manager of Forward Deployed Engineering，以及 Pre-Sales Program Lead, Forward Deployed Engineering。**verified** —— [Anthropic Greenhouse board API](https://boards-api.greenhouse.io/v1/boards/anthropic/jobs?content=true)。**取得日期：** 2026-08-29。

### 6. Anthropic 如何描述圍繞 FDE 的合作模式

這兩則非 IC（individual contributor）職缺，是描述交付方式最具參考價值的來源，因為它們描述了工程師所處的介面銜接點。

Manager 職缺說明中提到，FDE 主管將「work hand-in-hand with Engagement Managers who own delivery logistics and stakeholder management」，並將以下項目列為職責之一：「Collaborate with account teams and Engagement Managers during the pre-sales process to qualify engagements, scope work, and inform statements of work.」它也要求主管「build repeatable playbooks, starter repositories, integration templates, and an internal knowledge base that captures what your team learns in the field」，並「review technical architectures and code produced by your FDEs」。出差比例為 25–50%，「particularly during engagement kickoffs」。該公告坦承此方法尚未定型：「You'll be defining what good looks like for FDE management at Anthropic — there is no existing playbook to follow.」**verified** —— [Anthropic, Manager, Forward Deployed Engineering, London](https://job-boards.greenhouse.io/anthropic/jobs/5385634008)，最後更新於 2026-08-21。**取得日期：** 2026-08-29。

Pre-sales 職缺說明直接點出生命週期的界限所在。它描述建立「the pursuit-to-signature process (including the legal and finance ways of working) that gets contracts signed quickly and cleanly」，並表示職務持有人「will work hand in glove with a Post-Sale Program Lead counterpart who owns delivery from signature onward. Together you'll define the handoff that connects your two halves of the engagement lifecycle.」它進一步要求「the prioritization heuristics that decide where a capacity-constrained team places its bets across commercial, research, and mission-oriented deals」，以及涵蓋「when we pass an opportunity to a partner, when we team, and how we run subcontract or co-delivery pursuits」的夥伴合作模式。**verified** —— [Anthropic, Pre-Sales Program Lead, Forward Deployed Engineering](https://job-boards.greenhouse.io/anthropic/jobs/5391012008)，最後更新於 2026-08-21。**取得日期：** 2026-08-29。

Anthropic 自家的公告顯示出第二種交付管道，其中前線部署工程師根本不是 Anthropic 的員工。DXC 聯盟公告將 FDE 描述為「engineers embedded directly inside customer organizations」，並表示 DXC 將培訓「tens of thousands」名 Claude 認證的 FDE，這些人選自 DXC 自己的開發團隊，並透過 Anthropic Academy 取得認證。**verified** —— [Anthropic, "DXC integrates Claude into systems regulated industries rely on", 2026-06-11](https://www.anthropic.com/news/dxc-anthropic-alliance)。另一則公告表示 Anthropic 正「scaling our partner-facing team fivefold, so that we can provide dedicated Applied AI engineers to partners working on live customer deals, technical architects to scope more complex implementations, and localized go-to-market support」。**verified** —— [Anthropic, "Anthropic invests $100 million into the Claude Partner Network", 2026-03-12](https://www.anthropic.com/news/claude-partner-network)；請注意，這第二則公告描述的是 Applied AI engineers 與 technical architects，並未使用 FDE 這個職稱。

### 7. OpenAI：兩個不同的前線部署職稱

OpenAI 官方職缺板將 Forward Deployed Engineer 與 Forward Deployed Software Engineer 區分開來，兩者的差異在於「擁有權」與「可重用性」的不同。

FDE 職缺說明表示：「Forward Deployed Engineers (FDEs) lead complex end-to-end deployments of frontier models in production alongside our most strategic customers. You will own discovery, technical scoping, system design, build, and production rollout, partnering directly with customer engineering and domain teams.」它明確定義何謂成功：「You will measure success through production adoption, measurable workflow impact, and eval-driven feedback that changes product and model roadmaps.」所列職責包括「Own technical delivery across multiple deployments from first prototype to stable production」、「Make trade-offs between scope, speed, and quality」、「Contribute directly in the code when progress or clarity depends on it」，以及「Codify working patterns into tools, playbooks, or building blocks that others can use.」它要求 5 年以上經驗，舊金山混合辦公，並「travel up to 50%」。所示薪資級距為 $162K–$280K 加股票。**verified** —— [OpenAI, Forward Deployed Engineer (FDE) – SF](https://jobs.ashbyhq.com/openai/305a4b22-7ff9-4fa5-9229-c6a22c9aa64f)，發布於 2025-08-06。**取得日期：** 2026-08-29。

FDSWE 職缺說明從平台端描述同一個團隊：「As an FDSWE, you will work with our customers and OpenAI Forward Deployed Engineers to design and implement scalable solutions… You will design abstractions to solve customer problems, and then use them to scale our speed and quality of delivery across all Forward Deployed engagements.」它也點名了範疇界定的產出物——「Prepare detailed scopes of work and project plans for both proof-of-concept prototypes and full production deployments」——以及工作姿態：「coding side-by-side to drive projects to completion on their infrastructure.」它要求 7 年以上全端經驗；所示薪資級距為 $185K–$325K 加股票。**verified** —— [OpenAI, Forward Deployed Software Engineer – SF](https://jobs.ashbyhq.com/openai/00207abc-49b7-465c-a219-f7c1140f8047)，發布於 2025-11-15。**取得日期：** 2026-08-29。

兩則職缺都以相同的團隊描述開場：「OpenAI's Forward Deployed Engineering team partners with customers to turn research breakthroughs into production systems. We operate at the intersection of customer delivery and core platform development.」在取得日期當天，OpenAI 的職缺板列有 18 則以 Forward-Deployed 為職稱的公告，橫跨舊金山、紐約、西雅圖、華盛頓特區、東京、首爾、新加坡與雪梨，其中包括醫療與法律的產業別 FDE 職缺。**verified** —— [OpenAI 職缺板 API](https://api.ashbyhq.com/posting-api/job-board/openai?includeCompensation=true)。**取得日期：** 2026-08-29。

### 8. OpenAI 陳述的交付方法

OpenAI 的前線部署工程網站給出一段精簡的方法陳述：「Forward deployed engineering (FDE) is how OpenAI brings AI into production for complex, real-world use cases. Instead of starting with a general product, FDE teams work directly with customers to solve a specific problem, validate impact, and then identify patterns that can scale.」它列出四項營運原則——「Build from first principles」、「Prioritize speed and real-world impact」、「Work directly with domain experts」、「Deliver early value, then iterate toward scale」——並將回饋迴圈命名為「build, prove, generalize」，透過此迴圈，現場工作能「identif[y] repeatable patterns that evolve into product capabilities」。**verified** —— [OpenAI, "Forward deployed engineering at OpenAI"](https://openai.com/business/the-openai-deployment-company/)（會導向 deploy.co）。**取得日期：** 2026-08-29。

OpenAI Deployment Company 的發布公告，是本次執行中找到對合作模式最明確的第一方陳述：「A typical OpenAI Deployment Company engagement will begin with a focused diagnostic of where AI can create the most value, followed by a small number of priority workflows selected with the customer's leadership and operating teams. The OpenAI Deployment Company FDEs will then work inside the organization to design, build, test, and deploy production systems, connecting OpenAI models to the customer's data, tools, controls, and business processes so teams can use them reliably in day-to-day work.」同一則公告將 FDE 的任務描述為與「business leaders, operators, and frontline teams to identify where AI can make the biggest impact, redesign organizational infrastructure and critical workflows around it, and turn those gains into durable systems」密切合作，並表示 OpenAI 已同意收購顧問公司 Tomoro，第一天即帶來「approximately 150 experienced Forward Deployed Engineers and Deployment Specialists」。**verified** —— [OpenAI, "OpenAI launches the OpenAI Deployment Company", 2026-05-11](https://openai.com/index/openai-launches-the-deployment-company/)。該收購案載明「subject to customary closing conditions… expected to close in the coming months」，因此人力規模與組織結構屬於已宣布的意向，而非已確認的事實。

### 9. 各來源分歧之處

這不是三塊招牌下的同一份工作，本備忘錄不應將它們混為一談。

**產出物不同。** Palantir 的 FDSE 是在配置與擴充 Palantir 自家的平台——「we are actually deploying existing software products to achieve the customer's outcomes」（Dev versus Delta）。OpenAI 與 Anthropic 的 FDE 則是在*客戶*自己的系統裡建置：「Work within customer systems to build production applications with Claude models」（Anthropic）、「connecting OpenAI models to the customer's data, tools, controls, and business processes」（OpenAI）。**verified** 之處在於引文本身；對比則是 **inferred**。

**資歷與價位差距甚大。** Palantir 的 FDSE 要求 1 年以上經驗，薪資 $135K–$200K；OpenAI 的 FDE 要求 5 年以上，薪資 $162K–$280K，其 FDSWE 要求 7 年以上，薪資 $185K–$325K；Anthropic 的 FDE 要求 4 年以上，薪資 $280K–$320K。**verified** 資料來自這四則職缺公告。一個合理的解讀是，Palantir 的平台吸收了 AI 實驗室仍要求個人自行吸收的那部分難度——但這是從職缺說明**inferred**而來，三家公司都沒有這樣明說。

**出差要求相差三倍。** Palantir 與 Anthropic 為 25%，OpenAI 為「up to 50%」，Palantir 的 Deployment Strategist 為 25–75%。**verified。**

**只有 Anthropic 的職缺明確點名商業生命週期的界限**（售前資格確認、工作說明書、簽約，以及「owns delivery from signature onward」的 Post-Sale Program Lead）。Palantir 與 OpenAI 面向工程師的職缺說明，都沒有描述授權從業務移交到交付端的時點。**verified** 為本次執行讀取的公告中的一項負面發現；四則公告中未提及，並不能證明這些公司沒有這道界限。**inferred。**

**沒有任何一手來源說明 FDE 何時停止寫程式或將系統交接給客戶自己的人員。** 最接近的第一方陳述是 Palantir 另設的 Enablement Engineer 角色（負責部署後支援與 24/7 事件應變）、Anthropic 另設的 Engagement Manager 與 Post-Sale Program Lead 職能，以及 OpenAI 的「deliver early value, then iterate toward scale」。在此處讀取的材料中，並無任何地方寫下退出條件。**verified** 為一項缺口。

### 10. 二手來源，已明確標示

Latent Space 發布了一篇關於前線部署工程的長文，訪談對象為 Sierra 的 Agent Engineering 負責人 Natalie Meurer，日期為 2026-07-01。Meurer 表示 Sierra 的探索工作旨在「to find the intersection between problems that are genuinely difficult… and problems that will have a meaningful business impact」，且「most customer-specific work takes place at the orchestration layer rather than in the models themselves.」被問及 Palantir 的模式是否影響了 Sierra 的作法時，她表示「somewhat」有影響，但 Sierra「intentionally called the role agent engineer, rather than forward deployed engineer.」**secondary** —— [Latent Space, "Forward Deployed Engineers and the future of software engineering", 2026-07-01](https://www.latent.space/p/forward-deployed-engineers-aiewf)；這是一篇訪談整理文章，並非 Sierra 自家的徵才或工程文件，本次執行並未查核 Sierra 的第一方材料。

## 刻意設定的界限

- 本備忘錄是三家公司對某個職稱之陳述的紀錄，並非本儲存庫所採用的定義。`CONTEXT.md` 已為本專案的用途定義了 **FDE**，本文件不對其做任何修訂。
- 以上引用的商業機制——售前資格確認、工作說明書、交易優先順序、夥伴分包——之所以被記錄下來，是因為這正是一手來源實際描述的內容。這超出本儲存庫「受治理的營運能力」這一聚焦範圍，與 [`fde-guidance-book-review.md`](../../research/fde-guidance-book-review.md) 已述明的界限一致。
- 職缺公告是為吸引應徵者而寫的招募文件。它們是能力清單最具體的公開陳述，但同時也是行銷文案。應將職責清單視為對預期範圍的主張，而非對實際觀察到之作法的證據。
- 薪資範圍、人數與職缺數量都是單日快照，應重新查核，而非直接沿用引述。

## 無法驗證的部分

- **Palantir 的 Medium 部落格無法透過一般 HTTP 擷取存取**（對 WebFetch 與 curl 皆回傳 HTTP 403）。此處引用的兩篇 Palantir 部落格文章，是在本次執行期間透過腳本化瀏覽器讀取的；日後的讀者可能會遇到相同的 403。正因如此，其內容以引述而非改寫方式呈現。
- **openai.com 同樣對一般擷取回傳 403**；OpenAI 的公告與前線部署工程頁面，也是透過腳本化瀏覽器讀取的。
- **找不到任何 Palantir 一手頁面描述 bootcamp 合作模式的可擷取內容。** `palantir.com/bootcamps/` 與 `palantir.com/bootcamp/` 僅回傳標題與網站地圖連結。本備忘錄中唯一的 bootcamp 證據，是 10-K 中的那句話，屬於風險因子揭露，而非方法描述。
- **Anthropic 的「Forward Deployed Engineer, Federal Civilian」職缺（Greenhouse job 5079562008）出現在搜尋結果中，但在取得日期當天已不在 Anthropic 現行職缺板上。** 本備忘錄未讀取也未引用此職缺。這是職缺會過期的一個具體例證。
- **找不到任何第一方的 Anthropic 或 OpenAI 工程部落格文章描述 FDE 的交付方法論。** 就 Anthropic 而言，方法論證據完全來自職缺公告與夥伴合作公告；沒有類似 Palantir 那篇 Dev-versus-Delta 論述文章的對應內容。
- **沒有任何一手來源陳述 FDE 的退出或交接標準。** 任何主張此模式包含明確交接的說法，在有這類來源出現之前，都應視為未經支持。
- **本備忘錄未引用任何 X/Twitter 貼文。** 搜尋結果浮現大量彙整站與面試準備網站上的 FDE 相關評論（Exponent、fde.academy、Paraform 及類似網站）；這些都未被採用，因為每一個案例的原始一手文件都能直接取得。
- **Tomoro 收購案與約 150 名 FDE 的數字屬於已宣布的意向**，依 OpenAI 自身文字所述須待監管核准。請勿將其引述為已完成之事實。

## 研究註記

- 本次使用的一手來源：Palantir 的 Lever 徵才公告與公開職缺 API、Palantir 的工程部落格、Palantir Foundry 文件、Palantir 的 SEC Form 10-K；Anthropic 的 Greenhouse 職缺板與職缺板 API，以及 Anthropic 的新聞頁面；OpenAI 的 Ashby 職缺板與職缺 API、openai.com，以及 deploy.co。
- 本次執行的所有擷取時間：2026-08-29。職缺數量與薪資數字僅在該日期有效。
- 第 9 節與「解讀」段落是本作者的綜合分析，標記為 **inferred**；**來源事實**中的其餘內容皆為所引頁面的引述或直接摘要，標記為 **verified**。
