// i18n — Leonis Guardian multi-language support
const I18N = {
  vi: {
    nav_scan: "Scan",
    nav_approvals: "Approvals",
    nav_features: "Tính năng",
    nav_how: "Cách dùng",
    nav_faq: "Hỏi đáp",
    nav_cta: "Scan ngay ✦",

    hero_badge: "🛡️ Miễn phí · Không cần đăng ký",
    hero_title1: "Đừng để ví ",
    hero_title_highlight: "dính chưởng",
    hero_title2: "Check trước khi quá muộn",
    hero_sub: "Dán địa chỉ token — AI quét 30+ tín hiệu scam. Dán địa chỉ ví — kiểm tra approvals nguy hiểm. Tất cả trong 1 tool.",
    hero_stat1: "30+",
    hero_stat1_label: "Tín hiệu scam",
    hero_stat2: "5",
    hero_stat2_label: "Chain",
    hero_stat3: "~81%",
    hero_stat3_label: "F1 Score",
    hero_cta: "Bắt đầu quét ngay →",

    tab_scam: "🔍 Scan Token Scam",
    tab_approval: "🛡️ Approval Checker",
    tab_eip7702: "🔐 EIP-7702 Checker",

    scam_label_addr: "Địa chỉ contract token",
    scam_placeholder: "0x87230146E138d3F296a9a77e497A2A83012e9Bc5",
    scam_label_chain: "Chain",
    scam_btn: "🔍 Scan Token",
    scam_loading: "Đang quét...",
    scam_score_label: "Xác suất scam",

    approval_label_addr: "Địa chỉ ví cần kiểm tra",
    approval_placeholder: "0x36F50C8c...",
    approval_label_chain: "Chain",
    approval_btn: "🛡️ Quét Approvals",
    approval_loading: "Đang quét approvals...",
    approval_clean: "✅ Ví sạch!",
    approval_clean_sub: "Không phát hiện approval rủi ro nào.",
    approval_summary_active: "Approvals active",
    approval_summary_risk: "Rủi ro cao",
    approval_summary_unlimited: "Không giới hạn",
    approval_note: "Quét top token + DEX phổ biến. Hỗ trợ thêm token khi có nhu cầu.",
    approval_risk_high: "⚠ Rủi ro cao",
    approval_risk_medium: "⚡ Trung bình",
    approval_risk_low: "✅ An toàn",
    approval_unlimited: "∞ Unlimited",

    info_token: "Token",
    info_chain: "Chain",
    info_risk: "Risk Level",
    info_tax: "Sell Tax",
    info_source: "Source Code",
    info_proxy: "Proxy",

    verdict_scam: "LIKELY SCAM / RUGPULL",
    verdict_suspicious: "SUSPICIOUS — DYOR",
    verdict_safe: "LIKELY SAFE",

    redflags_title: "🚩 Red Flags",
    honeypot_link: "Xem báo cáo đầy đủ trên Honeypot.is →",

    features_badge: "✨ Tại sao nên dùng?",
    features_title: "Mọi thứ để giữ ví an toàn",
    feat1_title: "30+ Tín Hiệu Scam",
    feat1_desc: "Honeypot, high tax, proxy, closed source, siphoned wallets — tất cả được AI phân tích.",
    feat2_title: "Approval Checker",
    feat2_desc: "Quét ví tìm token approvals nguy hiểm. Phát hiện unlimited allowance với DEX lạ.",
    feat3_title: "5 Chain Hỗ Trợ",
    feat3_desc: "Ethereum, BSC, Base, Arbitrum, Polygon. Nhiều chain hơn sắp ra mắt.",
    feat4_title: "Kết Quả Tức Thì",
    feat4_desc: "Dữ liệu on-chain real-time. Kết quả scam detection trong dưới 5 giây.",
    feat5_title: "AI-Powered",
    feat5_desc: "Neural network huấn luyện trên 200+ token. Cập nhật liên tục, F1 ~81%.",
    feat6_title: "Miễn Phí Mãi Mãi",
    feat6_desc: "Không cần đăng ký, không cần connect ví. Dùng public RPC — zero cost.",

    how_badge: "📋 Quy trình",
    how_title: "Cách hoạt động",
    how_step1_title: "Dán địa chỉ",
    how_step1_desc: "Copy contract token hoặc địa chỉ ví. Hỗ trợ mọi EVM chain.",
    how_step2_title: "AI Quét",
    how_step2_desc: "Model phân tích 30+ tín hiệu + on-chain data. Dưới 5 giây.",
    how_step3_title: "Nhận Kết Quả",
    how_step3_desc: "Scam score, red flags, approvals nguy hiểm — tất cả rõ ràng.",

    chains_badge: "⛓️ Networks",
    chains_title: "Multi-Chain",

    faq_badge: "❓ Hỏi đáp",
    faq_title: "Câu Hỏi Thường Gặp",
    faq_q1: "Tool này có chính xác không?",
    faq_a1: "Model neural network huấn luyện trên 200+ token với F1 score ~81% (cross-validation). Phát hiện honeypot, rug pull, high-tax tokens. Luôn luôn DYOR — đây là công cụ hỗ trợ, không phải lời khuyên tài chính.",
    faq_q2: "Có mất phí không?",
    faq_a2: "Hoàn toàn miễn phí. Dùng Honeypot.is API (free) + public RPC endpoints. Không cần đăng ký, không cần connect ví, không lưu data.",
    faq_q3: "Approval Checker quét những gì?",
    faq_a3: "Quét allowance của các token phổ biến (USDT, USDC, ETH, WBTC...) với các DEX/router lớn (Uniswap, 0x, 1inch, PancakeSwap...). Phát hiện unlimited approval với spender lạ. Hiện tại quét khoảng 8-10 token × 8 spender mỗi chain.",
    faq_q4: "Có hỗ trợ Solana không?",
    faq_a4: "Chưa. Honeypot.is chỉ hỗ trợ EVM chains. Solana sẽ được thêm khi có API phù hợp.",

    og_badge: "📋 Model on OpenGradient",
    og_desc: "Model được liệt kê trên OpenGradient Model Hub — kiếm $OPG khi người khác sử dụng model trên mạng lưới.",
    og_link: "Xem trên Hub →",

    footer_built: "Built with ✦ by",
    footer_disclaimer: "© 2026 Crypto Guardian. Không phải lời khuyên tài chính. DYOR.",

    err_no_addr: "Vui lòng nhập địa chỉ contract token",
    err_network: "Lỗi mạng. Vui lòng thử lại.",
    err_invalid_wallet: "Địa chỉ ví không hợp lệ (cần 0x + 40 ký tự hex)",
    err_rpc: "Lỗi mạng hoặc RPC không phản hồi. Thử lại sau.",

    eip7702_desc: "EIP-7702 cho phép ví EOA ủy quyền thực thi giao dịch cho smart contract. Kiểm tra ví của bạn có đang bị ủy quyền không — phát hiện sớm để ngăn chặn rủi ro.",
    eip7702_label_addr: "Địa chỉ ví cần kiểm tra",
    eip7702_btn: "🔐 Kiểm tra EIP-7702",
    eip7702_clean: "✅ Ví sạch!",
    eip7702_clean_sub: "Không phát hiện EIP-7702 delegation trên tất cả chain.",
    eip7702_found: "🚨 Phát hiện delegation!",
    eip7702_found_sub: "chain có EIP-7702 delegation đang hoạt động.",
    eip7702_clean_short: "Sạch",
    eip7702_delegated_short: "Có delegation",
    alerts_badge: "🚨 Cảnh báo",
    alerts_title: "Scam Alerts Mới Nhất",
    alerts_source: "Nguồn: Rekt.news — cập nhật tự động",

    tab_scam_desc: "<strong class=\"font-heading text-bluepen\">🔍 Token Scam Detector</strong> — Dán địa chỉ contract token để kiểm tra rủi ro: <span class=\"text-accent font-semibold\">honeypot</span> (chỉ mua được, không bán được), <span class=\"text-accent font-semibold\">thuế cao</span> (mất % lớn khi bán), <span class=\"text-accent font-semibold\">proxy ẩn</span> (owner nâng cấp logic bất kỳ lúc nào), <span class=\"text-accent font-semibold\">mã nguồn đóng</span>. AI phân tích 19 đặc điểm on-chain + Honeypot.is API. <em>Dùng cho: trader kiểm tra token trước khi mua.</em>",
    tab_approval_desc: "<strong class=\"font-heading text-greenpen\">🛡️ Approval Checker</strong> — Bạn đã từng swap trên Uniswap, PancakeSwap, hay 1inch? Mỗi lần swap bạn cấp quyền <span class=\"font-semibold\">approve</span> cho DEX rút token. Nếu quên thu hồi (revoke), hacker exploit contract DEX là <span class=\"text-accent font-semibold\">rút sạch token của bạn</span> — kể cả USDT, USDC, ETH. Quét on-chain 200K blocks + top DEX để tìm tất cả approval còn active. <em>Dùng cho: kiểm tra ví định kỳ, sau khi swap token lạ.</em>",
    tab_eip7702_desc: "<strong class=\"font-heading text-accent\">🔐 EIP-7702 Delegation Checker</strong> — Sau bản nâng cấp <span class=\"font-semibold\">Pectra</span> (2025), EIP-7702 cho phép smart contract \"mượn\" ví EOA (ví thường của bạn) để ký giao dịch thay bạn.<br><span class=\"text-accent font-semibold\">⚠️ Attack vector:</span> Bạn click \"Connect Wallet\" trên web lạ → ký 1 chữ ký trông vô hại → contract được delegate toàn quyền điều khiển ví → <span class=\"text-accent font-semibold\">rút sạch token mà không cần private key.</span><br>🧠 <em>Nhiều người không biết ví mình đang bị delegate. Checker này quét 5 chain (ETH, BSC, Base, Arbitrum, Polygon) cùng lúc — nếu thấy code <code class=\"bg-accent/20 px-1 rounded text-xs\">0xef01...</code> trong ví là có delegation.</em>",
  },

  en: {
    nav_scan: "Scan",
    nav_approvals: "Approvals",
    nav_features: "Features",
    nav_how: "How",
    nav_faq: "FAQ",
    nav_cta: "Scan now ✦",

    hero_badge: "🛡️ Free · No signup needed",
    hero_title1: "Don't let your wallet get ",
    hero_title_highlight: "rekt",
    hero_title2: "Check before it's too late",
    hero_sub: "Paste a token address — AI scans 30+ scam signals. Paste a wallet address — check for dangerous approvals. All in one tool.",
    hero_stat1: "30+",
    hero_stat1_label: "Scam Signals",
    hero_stat2: "5",
    hero_stat2_label: "Chains",
    hero_stat3: "~81%",
    hero_stat3_label: "F1 Score",
    hero_cta: "Start scanning →",

    tab_scam: "🔍 Scan Token Scam",
    tab_approval: "🛡️ Approval Checker",
    tab_eip7702: "🔐 EIP-7702 Checker",

    scam_label_addr: "Token contract address",
    scam_placeholder: "0x87230146E138d3F296a9a77e497A2A83012e9Bc5",
    scam_label_chain: "Chain",
    scam_btn: "🔍 Scan Token",
    scam_loading: "Scanning...",
    scam_score_label: "Scam Probability",

    approval_label_addr: "Wallet address to check",
    approval_placeholder: "0x36F50C8c...",
    approval_label_chain: "Chain",
    approval_btn: "🛡️ Scan Approvals",
    approval_loading: "Scanning approvals...",
    approval_clean: "✅ Wallet clean!",
    approval_clean_sub: "No risky approvals detected.",
    approval_summary_active: "Active Approvals",
    approval_summary_risk: "High Risk",
    approval_summary_unlimited: "Unlimited",
    approval_note: "Scanning top tokens + popular DEXes. More tokens on request.",
    approval_risk_high: "⚠ High Risk",
    approval_risk_medium: "⚡ Medium",
    approval_risk_low: "✅ Safe",
    approval_unlimited: "∞ Unlimited",

    info_token: "Token",
    info_chain: "Chain",
    info_risk: "Risk Level",
    info_tax: "Sell Tax",
    info_source: "Source Code",
    info_proxy: "Proxy",

    verdict_scam: "LIKELY SCAM / RUGPULL",
    verdict_suspicious: "SUSPICIOUS — DYOR",
    verdict_safe: "LIKELY SAFE",

    redflags_title: "🚩 Red Flags",
    honeypot_link: "View full report on Honeypot.is →",

    features_badge: "✨ Why use this?",
    features_title: "Everything to keep your wallet safe",
    feat1_title: "30+ Scam Signals",
    feat1_desc: "Honeypots, high taxes, proxy contracts, closed source, siphoned wallets — all analyzed by AI.",
    feat2_title: "Approval Checker",
    feat2_desc: "Scan wallets for dangerous token approvals. Detect unlimited allowances to unknown DEXes.",
    feat3_title: "5 Chains Supported",
    feat3_desc: "Ethereum, BSC, Base, Arbitrum, Polygon. More chains coming soon.",
    feat4_title: "Instant Results",
    feat4_desc: "Real-time on-chain data. Scam detection results in under 5 seconds.",
    feat5_title: "AI-Powered",
    feat5_desc: "Neural network trained on 200+ tokens. Continuously improving, F1 ~81%.",
    feat6_title: "Free Forever",
    feat6_desc: "No signup, no wallet connect required. Public RPC — zero cost.",

    how_badge: "📋 Process",
    how_title: "How It Works",
    how_step1_title: "Paste Address",
    how_step1_desc: "Copy a token contract or wallet address. All EVM chains supported.",
    how_step2_title: "AI Scan",
    how_step2_desc: "Model analyzes 30+ signals + on-chain data. Under 5 seconds.",
    how_step3_title: "Get Results",
    how_step3_desc: "Scam score, red flags, dangerous approvals — all clearly displayed.",

    chains_badge: "⛓️ Networks",
    chains_title: "Multi-Chain",

    faq_badge: "❓ FAQ",
    faq_title: "Frequently Asked Questions",
    faq_q1: "How accurate is this tool?",
    faq_a1: "Our neural network was trained on 200+ labeled tokens with ~81% cross-validation F1 score. It catches honeypots, rug pulls, and high-tax tokens. Always DYOR — this is a tool, not financial advice.",
    faq_q2: "Is it free?",
    faq_a2: "Completely free. We use the free Honeypot.is API + public RPC endpoints. No signup, no wallet connect, no data stored.",
    faq_q3: "What does Approval Checker scan?",
    faq_a3: "It checks allowances of popular tokens (USDT, USDC, ETH, WBTC...) against major DEX routers (Uniswap, 0x, 1inch, PancakeSwap...). Detects unlimited approvals to unknown spenders. Currently scans ~8-10 tokens × 8 spenders per chain.",
    faq_q4: "Does it support Solana?",
    faq_a4: "Not yet. Honeypot.is only supports EVM chains. Solana will be added when suitable APIs become available.",

    og_badge: "📋 Model on OpenGradient",
    og_desc: "Model listed on OpenGradient Model Hub — earn $OPG when others use it on the network.",
    og_link: "View on Hub →",

    footer_built: "Built with ✦ by",
    footer_disclaimer: "© 2026 Crypto Guardian. Not financial advice. DYOR.",

    err_no_addr: "Please enter a contract address",
    err_network: "Network error. Please try again.",
    err_invalid_wallet: "Invalid wallet address (needs 0x + 40 hex chars)",
    err_rpc: "Network or RPC error. Try again later.",

    eip7702_desc: "EIP-7702 allows EOA wallets to delegate transaction execution to smart contracts. Check if your wallet has any active delegations — early detection prevents risks.",
    eip7702_label_addr: "Wallet address to check",
    eip7702_btn: "🔐 Check EIP-7702",
    eip7702_clean: "✅ Wallet Clean!",
    eip7702_clean_sub: "No EIP-7702 delegations detected on any chain.",
    eip7702_found: "🚨 Delegation Detected!",
    eip7702_found_sub: "chains have active EIP-7702 delegations.",
    eip7702_clean_short: "Clean",
    eip7702_delegated_short: "Delegated",
    alerts_badge: "🚨 Alerts",
    alerts_title: "Latest Scam Alerts",
    alerts_source: "Source: Rekt.news — auto-updated",

    tab_scam_desc: "<strong class=\"font-heading text-bluepen\">🔍 Token Scam Detector</strong> — Paste a token contract address to check for risks: <span class=\"text-accent font-semibold\">honeypots</span> (buy OK, sell blocked), <span class=\"text-accent font-semibold\">high taxes</span>, <span class=\"text-accent font-semibold\">hidden proxies</span>, <span class=\"text-accent font-semibold\">closed source</span>. AI analyzes 19 on-chain features + Honeypot.is API. <em>Use for: checking tokens before buying.</em>",
    tab_approval_desc: "<strong class=\"font-heading text-greenpen\">🛡️ Approval Checker</strong> — Ever swapped on Uniswap, PancakeSwap, or 1inch? Each swap grants <span class=\"font-semibold\">approve</span> permission for the DEX to withdraw your tokens. Forgotten approvals are a <span class=\"text-accent font-semibold\">critical exploit vector</span> — if a DEX contract gets hacked, attackers drain your USDT, USDC, ETH. Scans 200K on-chain blocks + top DEXes for all active approvals. <em>Use for: periodic wallet audits, after swapping obscure tokens.</em>",
    tab_eip7702_desc: "<strong class=\"font-heading text-accent\">🔐 EIP-7702 Delegation Checker</strong> — After the <span class=\"font-semibold\">Pectra</span> upgrade (2025), EIP-7702 lets smart contracts \"borrow\" your EOA wallet to sign transactions on your behalf.<br><span class=\"text-accent font-semibold\">⚠️ Attack vector:</span> You click \"Connect Wallet\" on a shady site → sign an innocent-looking signature → the contract gets full delegation over your wallet → <span class=\"text-accent font-semibold\">drains all tokens without your private key.</span><br>🧠 <em>Many users don't know their wallet is delegated. This checker scans 5 chains (ETH, BSC, Base, Arbitrum, Polygon) simultaneously — if <code class=\"bg-accent/20 px-1 rounded text-xs\">0xef01...</code> code appears in your wallet, you have an active delegation.</em>",
  },

  zh: {
    nav_scan: "扫描",
    nav_approvals: "授权",
    nav_features: "功能",
    nav_how: "流程",
    nav_faq: "问答",
    nav_cta: "立即扫描 ✦",

    hero_badge: "🛡️ 免费 · 无需注册",
    hero_title1: "别让你的钱包",
    hero_title_highlight: "中招",
    hero_title2: "趁早检查，别等后悔",
    hero_sub: "粘贴代币地址 — AI 扫描 30+ 骗局信号。粘贴钱包地址 — 检查危险授权。一个工具全搞定。",
    hero_stat1: "30+",
    hero_stat1_label: "骗局信号",
    hero_stat2: "5",
    hero_stat2_label: "公链",
    hero_stat3: "~81%",
    hero_stat3_label: "F1 分数",
    hero_cta: "开始扫描 →",

    tab_scam: "🔍 代币骗局扫描",
    tab_approval: "🛡️ 授权检查",
    tab_eip7702: "🔐 EIP-7702 检查",

    scam_label_addr: "代币合约地址",
    scam_placeholder: "0x87230146E138d3F296a9a77e497A2A83012e9Bc5",
    scam_label_chain: "公链",
    scam_btn: "🔍 扫描代币",
    scam_loading: "扫描中...",
    scam_score_label: "骗局概率",

    approval_label_addr: "要检查的钱包地址",
    approval_placeholder: "0x36F50C8c...",
    approval_label_chain: "公链",
    approval_btn: "🛡️ 扫描授权",
    approval_loading: "扫描授权中...",
    approval_clean: "✅ 钱包安全！",
    approval_clean_sub: "未发现危险授权。",
    approval_summary_active: "活跃授权",
    approval_summary_risk: "高风险",
    approval_summary_unlimited: "无限授权",
    approval_note: "扫描热门代币 + 主流 DEX。如有需要可添加更多代币。",
    approval_risk_high: "⚠ 高风险",
    approval_risk_medium: "⚡ 中等",
    approval_risk_low: "✅ 安全",
    approval_unlimited: "∞ 无限",

    info_token: "代币",
    info_chain: "公链",
    info_risk: "风险等级",
    info_tax: "卖出税",
    info_source: "源代码",
    info_proxy: "代理",

    verdict_scam: "可能是骗局 / 貔貅盘",
    verdict_suspicious: "可疑 — 自行研究",
    verdict_safe: "可能是安全的",

    redflags_title: "🚩 危险信号",
    honeypot_link: "在 Honeypot.is 查看完整报告 →",

    features_badge: "✨ 为什么选择我们？",
    features_title: "全方位保护钱包安全",
    feat1_title: "30+ 骗局信号",
    feat1_desc: "蜜罐、高税率、代理合约、闭源、被洗劫钱包 — AI 全部分析。",
    feat2_title: "授权检查",
    feat2_desc: "扫描钱包的代币授权。检测未知 DEX 的无限授权。",
    feat3_title: "支持 5 条公链",
    feat3_desc: "以太坊、BSC、Base、Arbitrum、Polygon。更多公链即将上线。",
    feat4_title: "即时结果",
    feat4_desc: "实时链上数据。骗局检测结果不到 5 秒。",
    feat5_title: "AI 驱动",
    feat5_desc: "基于 200+ 代币训练的神经网络。持续改进，F1 ~81%。",
    feat6_title: "永久免费",
    feat6_desc: "无需注册，无需连接钱包。公共 RPC — 零成本。",

    how_badge: "📋 流程",
    how_title: "如何使用",
    how_step1_title: "粘贴地址",
    how_step1_desc: "复制代币合约或钱包地址。支持所有 EVM 链。",
    how_step2_title: "AI 扫描",
    how_step2_desc: "模型分析 30+ 信号 + 链上数据。不到 5 秒。",
    how_step3_title: "查看结果",
    how_step3_desc: "骗局分数、危险信号、可疑授权 — 清晰展示。",

    chains_badge: "⛓️ 网络",
    chains_title: "多链支持",

    faq_badge: "❓ 常见问题",
    faq_title: "常见问题",
    faq_q1: "这个工具准确吗？",
    faq_a1: "我们的神经网络在 200+ 标记代币上训练，交叉验证 F1 分数约 81%。能检测蜜罐、貔貅盘和高税率代币。请始终自行研究 — 这是工具，不是财务建议。",
    faq_q2: "免费吗？",
    faq_a2: "完全免费。使用免费的 Honeypot.is API + 公共 RPC。无需注册，无需连接钱包，不存储数据。",
    faq_q3: "授权检查扫描什么？",
    faq_a3: "检查热门代币（USDT、USDC、ETH、WBTC...）对主流 DEX（Uniswap、0x、1inch、PancakeSwap...）的授权额度。检测对未知合约的无限授权。目前每条链约扫描 8-10 个代币 × 8 个 DEX。",
    faq_q4: "支持 Solana 吗？",
    faq_a4: "暂不支持。Honeypot.is 仅支持 EVM 链。待有合适的 API 后添加 Solana。",

    og_badge: "📋 Model on OpenGradient",
    og_desc: "模型列在 OpenGradient Model Hub 上 — 当其他人在网络上使用模型时赚取 $OPG。",
    og_link: "在 Hub 上查看 →",

    footer_built: "由 ✦ 构建",
    footer_disclaimer: "© 2026 Crypto Guardian。非财务建议。DYOR。",

    err_no_addr: "请输入合约地址",
    err_network: "网络错误。请重试。",
    err_invalid_wallet: "无效的钱包地址（需要 0x + 40 个十六进制字符）",
    err_rpc: "网络或 RPC 错误。请稍后重试。",

    eip7702_desc: "EIP-7702 允许 EOA 钱包将交易执行委托给智能合约。检查您的钱包是否有活跃的委托 — 及早发现以防止风险。",
    eip7702_label_addr: "要检查的钱包地址",
    eip7702_btn: "🔐 检查 EIP-7702",
    eip7702_clean: "✅ 钱包安全！",
    eip7702_clean_sub: "所有链上未检测到 EIP-7702 委托。",
    eip7702_found: "🚨 发现委托！",
    eip7702_found_sub: "条链有活跃的 EIP-7702 委托。",
    eip7702_clean_short: "干净",
    eip7702_delegated_short: "已委托",
    alerts_badge: "🚨 警报",
    alerts_title: "最新骗局警报",
    alerts_source: "来源: Rekt.news — 自动更新",

    tab_scam_desc: "<strong class=\"font-heading text-bluepen\">🔍 代币骗局检测器</strong> — 粘贴代币合约地址以检查风险：<span class=\"text-accent font-semibold\">蜜罐</span>（只能买不能卖）、<span class=\"text-accent font-semibold\">高税率</span>、<span class=\"text-accent font-semibold\">隐藏代理</span>、<span class=\"text-accent font-semibold\">闭源代码</span>。AI分析19个链上特征 + Honeypot.is API。<em>用途：购买前检查代币。</em>",
    tab_approval_desc: "<strong class=\"font-heading text-greenpen\">🛡️ 授权检查器</strong> — 在Uniswap、PancakeSwap或1inch上交易过吗？每次交易都会授予DEX <span class=\"font-semibold\">approve</span> 权限来提取您的代币。忘记撤销（revoke）的授权是<span class=\"text-accent font-semibold\">严重的安全漏洞</span>——如果DEX合约被黑，攻击者将清空您的USDT、USDC、ETH。扫描20万区块 + 主流DEX以查找所有活跃授权。<em>用途：定期钱包审计、交易陌生代币后。</em>",
    tab_eip7702_desc: "<strong class=\"font-heading text-accent\">🔐 EIP-7702 委托检查器</strong> — <span class=\"font-semibold\">Pectra</span>升级（2025）后，EIP-7702允许智能合约\"借用\"您的EOA钱包代表您签署交易。<br><span class=\"text-accent font-semibold\">⚠️ 攻击方式：</span>您在可疑网站点击\"连接钱包\"→签署一个看似无害的签名→合约获得您钱包的完全委托权限→<span class=\"text-accent font-semibold\">无需私钥即可清空所有代币。</span><br>🧠 <em>许多用户不知道自己的钱包已被委托。此检查器同时扫描5条链（ETH、BSC、Base、Arbitrum、Polygon）——如果钱包中出现<code class=\"bg-accent/20 px-1 rounded text-xs\">0xef01...</code>代码，说明存在活跃委托。</em>",
  },

  ko: {
    nav_scan: "스캔",
    nav_approvals: "승인",
    nav_features: "기능",
    nav_how: "사용법",
    nav_faq: "FAQ",
    nav_cta: "지금 스캔 ✦",

    hero_badge: "🛡️ 무료 · 가입 불필요",
    hero_title1: "지갑 털리지 ",
    hero_title_highlight: "마세요",
    hero_title2: "늦기 전에 확인하세요",
    hero_sub: "토큰 주소 붙여넣기 — AI가 30+ 사기 신호를 스캔합니다. 지갑 주소 붙여넣기 — 위험한 승인을 확인합니다. 하나의 도구로 모두 해결.",
    hero_stat1: "30+",
    hero_stat1_label: "사기 신호",
    hero_stat2: "5",
    hero_stat2_label: "체인",
    hero_stat3: "~81%",
    hero_stat3_label: "F1 점수",
    hero_cta: "스캔 시작 →",

    tab_scam: "🔍 토큰 사기 스캔",
    tab_approval: "🛡️ 승인 확인",
    tab_eip7702: "🔐 EIP-7702 검사",

    scam_label_addr: "토큰 컨트랙트 주소",
    scam_placeholder: "0x87230146E138d3F296a9a77e497A2A83012e9Bc5",
    scam_label_chain: "체인",
    scam_btn: "🔍 토큰 스캔",
    scam_loading: "스캔 중...",
    scam_score_label: "사기 확률",

    approval_label_addr: "확인할 지갑 주소",
    approval_placeholder: "0x36F50C8c...",
    approval_label_chain: "체인",
    approval_btn: "🛡️ 승인 스캔",
    approval_loading: "승인 스캔 중...",
    approval_clean: "✅ 지갑 안전!",
    approval_clean_sub: "위험한 승인이 발견되지 않았습니다.",
    approval_summary_active: "활성 승인",
    approval_summary_risk: "고위험",
    approval_summary_unlimited: "무제한",
    approval_note: "인기 토큰 + 주요 DEX 스캔. 요청 시 더 많은 토큰 추가 가능.",
    approval_risk_high: "⚠ 고위험",
    approval_risk_medium: "⚡ 중간",
    approval_risk_low: "✅ 안전",
    approval_unlimited: "∞ 무제한",

    info_token: "토큰",
    info_chain: "체인",
    info_risk: "위험도",
    info_tax: "판매세",
    info_source: "소스코드",
    info_proxy: "프록시",

    verdict_scam: "사기 가능성 높음 / 러그풀",
    verdict_suspicious: "의심 — 직접 확인 필요",
    verdict_safe: "안전한 것으로 보임",

    redflags_title: "🚩 위험 신호",
    honeypot_link: "Honeypot.is에서 전체 보고서 보기 →",

    features_badge: "✨ 왜 사용해야 할까요?",
    features_title: "지갑을 안전하게 지키는 모든 것",
    feat1_title: "30+ 사기 신호",
    feat1_desc: "허니팟, 높은 세금, 프록시 컨트랙트, 비공개 소스, 털린 지갑 — AI가 모두 분석합니다.",
    feat2_title: "승인 확인",
    feat2_desc: "지갑의 토큰 승인을 스캔합니다. 알 수 없는 DEX에 대한 무제한 승인을 감지합니다.",
    feat3_title: "5개 체인 지원",
    feat3_desc: "이더리움, BSC, 베이스, 아비트럼, 폴리곤. 더 많은 체인 출시 예정.",
    feat4_title: "즉시 결과",
    feat4_desc: "실시간 온체인 데이터. 사기 감지 결과 5초 이내.",
    feat5_title: "AI 기반",
    feat5_desc: "200개 이상의 토큰으로 학습된 신경망. 지속적 개선, F1 ~81%.",
    feat6_title: "영원히 무료",
    feat6_desc: "가입 불필요, 지갑 연결 불필요. 공개 RPC — 비용 제로.",

    how_badge: "📋 프로세스",
    how_title: "사용 방법",
    how_step1_title: "주소 붙여넣기",
    how_step1_desc: "토큰 컨트랙트 또는 지갑 주소를 복사하세요. 모든 EVM 체인 지원.",
    how_step2_title: "AI 스캔",
    how_step2_desc: "모델이 30개 이상의 신호 + 온체인 데이터를 분석합니다. 5초 이내.",
    how_step3_title: "결과 확인",
    how_step3_desc: "사기 점수, 위험 신호, 위험한 승인 — 모두 명확하게 표시됩니다.",

    chains_badge: "⛓️ 네트워크",
    chains_title: "멀티체인",

    faq_badge: "❓ FAQ",
    faq_title: "자주 묻는 질문",
    faq_q1: "이 도구는 얼마나 정확한가요?",
    faq_a1: "저희 신경망은 200개 이상의 레이블된 토큰으로 학습되었으며 교차 검증 F1 점수 ~81%입니다. 허니팟, 러그풀, 높은 세금 토큰을 감지합니다. 항상 DYOR — 이것은 도구일 뿐 재정적 조언이 아닙니다.",
    faq_q2: "무료인가요?",
    faq_a2: "완전 무료입니다. 무료 Honeypot.is API + 공개 RPC 엔드포인트를 사용합니다. 가입 불필요, 지갑 연결 불필요, 데이터 저장 없음.",
    faq_q3: "승인 확인은 무엇을 스캔하나요?",
    faq_a3: "인기 토큰(USDT, USDC, ETH, WBTC...)의 주요 DEX 라우터(Uniswap, 0x, 1inch, PancakeSwap...)에 대한 승인 한도를 확인합니다. 알 수 없는 지출자에 대한 무제한 승인을 감지합니다. 현재 체인당 약 8-10개 토큰 × 8개 지출자를 스캔합니다.",
    faq_q4: "솔라나를 지원하나요?",
    faq_a4: "아직 아닙니다. Honeypot.is는 EVM 체인만 지원합니다. 적절한 API가 제공되면 솔라나를 추가할 예정입니다.",

    og_badge: "📋 Model on OpenGradient",
    og_desc: "모델이 OpenGradient Model Hub에 등록되어 있습니다 — 다른 사람이 네트워크에서 사용할 때 $OPG를 얻습니다.",
    og_link: "Hub에서 보기 →",

    footer_built: "✦ 제작:",
    footer_disclaimer: "© 2026 Crypto Guardian. 재정적 조언이 아닙니다. DYOR.",

    err_no_addr: "컨트랙트 주소를 입력하세요",
    err_network: "네트워크 오류. 다시 시도해주세요.",
    err_invalid_wallet: "유효하지 않은 지갑 주소 (0x + 40자 16진수 필요)",
    err_rpc: "네트워크 또는 RPC 오류. 나중에 다시 시도해주세요.",

    eip7702_desc: "EIP-7702는 EOA 지갑이 스마트 컨트랙트에 거래 실행을 위임할 수 있게 합니다. 지갑에 활성 위임이 있는지 확인하세요 — 조기 발견으로 위험을 방지합니다.",
    eip7702_label_addr: "확인할 지갑 주소",
    eip7702_btn: "🔐 EIP-7702 확인",
    eip7702_clean: "✅ 지갑 안전!",
    eip7702_clean_sub: "모든 체인에서 EIP-7702 위임이 발견되지 않았습니다.",
    eip7702_found: "🚨 위임 발견!",
    eip7702_found_sub: "개 체인에 활성 EIP-7702 위임이 있습니다.",
    eip7702_clean_short: "안전",
    eip7702_delegated_short: "위임됨",
    alerts_badge: "🚨 경고",
    alerts_title: "최신 사기 경고",
    alerts_source: "출처: Rekt.news — 자동 업데이트",

    tab_scam_desc: "<strong class=\"font-heading text-bluepen\">🔍 토큰 사기 탐지기</strong> — 토큰 컨트랙트 주소를 붙여넣어 위험을 확인하세요: <span class=\"text-accent font-semibold\">허니팟</span> (매수만 가능, 매도 불가), <span class=\"text-accent font-semibold\">높은 세금</span>, <span class=\"text-accent font-semibold\">숨겨진 프록시</span>, <span class=\"text-accent font-semibold\">비공개 소스</span>. AI가 19개 온체인 특징 + Honeypot.is API를 분석합니다. <em>용도: 구매 전 토큰 확인.</em>",
    tab_approval_desc: "<strong class=\"font-heading text-greenpen\">🛡️ 승인 검사기</strong> — Uniswap, PancakeSwap, 1inch에서 스왑한 적 있나요? 각 스왑마다 DEX가 토큰을 인출할 수 있는 <span class=\"font-semibold\">approve</span> 권한을 부여합니다. 잊혀진 승인은 <span class=\"text-accent font-semibold\">치명적인 공격 경로</span>입니다 — DEX 컨트랙트가 해킹되면 공격자가 USDT, USDC, ETH를 모두 탈취합니다. 20만 온체인 블록 + 주요 DEX를 스캔하여 모든 활성 승인을 찾습니다. <em>용도: 정기 지갑 감사, 생소한 토큰 스왑 후.</em>",
    tab_eip7702_desc: "<strong class=\"font-heading text-accent\">🔐 EIP-7702 위임 검사기</strong> — <span class=\"font-semibold\">Pectra</span> 업그레이드(2025) 이후, EIP-7702는 스마트 컨트랙트가 사용자의 EOA 지갑을 \"빌려\" 대신 거래에 서명할 수 있게 합니다.<br><span class=\"text-accent font-semibold\">⚠️ 공격 방식:</span> 수상한 사이트에서 \"지갑 연결\" 클릭 → 무해해 보이는 서명 → 컨트랙트가 지갑에 대한 완전한 위임 권한 획득 → <span class=\"text-accent font-semibold\">개인키 없이 모든 토큰 탈취.</span><br>🧠 <em>많은 사용자가 자신의 지갑이 위임되었는지 모릅니다. 이 검사기는 5개 체인(ETH, BSC, Base, Arbitrum, Polygon)을 동시에 스캔합니다 — 지갑에서 <code class=\"bg-accent/20 px-1 rounded text-xs\">0xef01...</code> 코드가 발견되면 활성 위임이 있는 것입니다.</em>",
  }
};

// ── Active language ──
let currentLang = localStorage.getItem('cryptoguardian_lang') || 'en';

function setLang(lang) {
  currentLang = lang;
  localStorage.setItem('cryptoguardian_lang', lang);
  applyLang();
}

function t(key) {
  return I18N[currentLang]?.[key] || I18N['en'][key] || key;
}

function applyLang() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const text = t(key);
    if (text !== undefined) {
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.placeholder = text;
      } else {
        el.textContent = text;
      }
    }
  });

  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    const key = el.getAttribute('data-i18n-html');
    const html = t(key);
    if (html !== undefined) {
      el.innerHTML = html;
    }
  });

  const hl = document.getElementById('heroHighlight');
  if (hl) hl.textContent = t('hero_title_highlight');

  document.querySelectorAll('[data-i18n-option]').forEach(opt => {
    const key = opt.getAttribute('data-i18n-option');
    opt.textContent = t(key);
  });

  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    el.placeholder = t(el.getAttribute('data-i18n-placeholder'));
  });

  const switcher = document.getElementById('langSwitcherText');
  if (switcher) switcher.textContent = currentLang.toUpperCase();

  document.documentElement.lang = currentLang === 'vi' ? 'vi' : currentLang === 'zh' ? 'zh' : currentLang === 'ko' ? 'ko' : 'en';

  if (document.getElementById('panelScam') && !document.getElementById('panelScam').classList.contains('hidden')) {
    const scoreLabel = document.querySelector('[data-i18n="scam_score_label"]');
    if (scoreLabel && document.getElementById('result').classList.contains('hidden') === false) {
      scoreLabel.textContent = t('scam_score_label');
    }
  }
}

document.addEventListener('DOMContentLoaded', applyLang);

function toggleLangMenu() {
  const menu = document.getElementById('langMenu');
  if (menu) menu.classList.toggle('hidden');
}
function closeLangMenu() {
  const menu = document.getElementById('langMenu');
  if (menu) menu.classList.add('hidden');
}
document.addEventListener('click', (e) => {
  if (!e.target.closest('#langMenu') && !e.target.closest('button[onclick*="toggleLangMenu"]')) {
    closeLangMenu();
  }
});
