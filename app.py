#!/usr/bin/env python3
"""Leonis Forge — Token Scam Detector + Approval Checker + EIP-7702 Checker."""
import json, time, pickle, urllib.request, urllib.parse, urllib.error, os, re, xml.etree.ElementTree as ET
from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta
import numpy as np
import onnxruntime as ort
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory

from airdrop_safety import analyze_airdrop

app = Flask(__name__, static_folder="static")
DIR = Path(__file__).parent

# ── Analytics (in-memory) ──
analytics = {
    "started": datetime.utcnow().isoformat(),
    "total": 0,
    "endpoints": defaultdict(int),
    "ips": set(),
    "referrers": defaultdict(int),
    "daily": defaultdict(int),  # key: "YYYY-MM-DD"
}

@app.before_request
def track_request():
    analytics["total"] += 1
    path = request.path
    if path.startswith("/api/"):
        analytics["endpoints"][path] += 1
    else:
        analytics["endpoints"]["/ (pages)"] += 1
    analytics["ips"].add(request.remote_addr)
    ref = request.referrer
    if ref:
        analytics["referrers"][ref] += 1
    today = datetime.utcnow().strftime("%Y-%m-%d")
    analytics["daily"][today] += 1

# ── Stats auth (env STATS_KEY or default) ──
STATS_KEY = os.environ.get("STATS_KEY", "leonis-stats-2026")

CHAIN_NAMES = {"1": "eth", "56": "bsc", "8453": "base", "42161": "arbitrum", "137": "polygon"}

# RPC endpoints
RPC_URLS = {
    "1": "https://ethereum-rpc.publicnode.com",
    "56": "https://bsc-rpc.publicnode.com",
    "8453": "https://base-rpc.publicnode.com",
    "42161": "https://arbitrum-one-rpc.publicnode.com",
    "137": "https://polygon-bor-rpc.publicnode.com",
}

# Approval event signature: keccak256("Approval(address,address,uint256)")
APPROVAL_TOPIC = "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925"

# Known DEX/spender contracts for labeling
KNOWN_SPENDERS = {
    "0xdef1c0ded9bec7f1a1670819833240f027b25eff": "0x Protocol",
    "0x1111111254fb6c44bac0bed2854e76f90643097d": "1inch Router",
    "0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad": "Uniswap Universal Router",
    "0x881d40237659c251811cec9c364ef91dc08d300c": "Metamask Swap",
    "0x7a250d5630b4cf539739df2c5dacb4c659f2488d": "Uniswap V2 Router",
    "0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45": "Uniswap V3 Router",
    "0x6131b5fae19ea4f9d964eac0408e4408b66337b5": "KyberSwap",
    "0x216b4b4ba9f3e719726886d34a177484278bfcae": "Paraswap",
    "0x10ed43c718714eb63d5aa57b78b54704e256024e": "PancakeSwap Router",
    "0x13f4ea83d0bd40e75c8222255bc855a974568dd4": "PancakeSwap V3",
    "0xa5e0829caced8ffdd4de3c43696c57f7d7a678ff": "QuickSwap Router",
    "0x1b02da8cb0d097eb8d57a175b88c7d8b47997506": "SushiSwap Router",
    "0xe592427a0aece92de3edee1f18e0157c05861564": "Uniswap V3 Router 2",
}

MODEL_PATH = DIR / "scam_detector_v3.onnx"
SCALER_PATH = DIR / "scam_detector_v3_scaler.pkl"
session = ort.InferenceSession(str(MODEL_PATH))
if SCALER_PATH.exists():
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)
else:
    scaler = None


def rpc_call(chain_id, method, params):
    url = RPC_URLS.get(chain_id)
    if not url:
        return None
    data = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "User-Agent": "LeonisGuardian/1.0"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def get_token_info(chain_id, token_addr):
    """Get token name and symbol via eth_call."""
    # name()
    name_data = "0x06fdde03"
    name_result = rpc_call(chain_id, "eth_call", [{"to": token_addr, "data": name_data}, "latest"])
    name = "?"
    if name_result and "result" in name_result:
        try:
            decoded = bytes.fromhex(name_result["result"][2:]).decode("utf-8", errors="ignore").strip("\x00")
            if decoded:
                name = decoded[:32]
        except Exception:
            pass

    # symbol()
    sym_data = "0x95d89b41"
    sym_result = rpc_call(chain_id, "eth_call", [{"to": token_addr, "data": sym_data}, "latest"])
    symbol = "?"
    if sym_result and "result" in sym_result:
        try:
            decoded = bytes.fromhex(sym_result["result"][2:]).decode("utf-8", errors="ignore").strip("\x00")
            if decoded:
                symbol = decoded[:16]
        except Exception:
            pass

    return name, symbol


def query_approval_logs(chain_id, wallet, max_blocks=1000000):
    """Query Approval event logs for a wallet across up to max_blocks in chunks."""
    block_result = rpc_call(chain_id, "eth_blockNumber", [])
    if not block_result or "result" not in block_result:
        return []
    latest = int(block_result["result"], 16)

    owner_topic = "0x" + wallet[2:].lower().rjust(64, "0")
    all_logs = []
    seen = set()
    approvals = []

    # Scan in chunks of 100K blocks, up to max_blocks total
    chunk_size = 100000
    scanned = 0
    current_from = latest - chunk_size

    while scanned < max_blocks and current_from >= 0:
        result = rpc_call(chain_id, "eth_getLogs", [{
            "fromBlock": hex(max(0, current_from)),
            "toBlock": hex(current_from + chunk_size - 1),
            "topics": [APPROVAL_TOPIC, owner_topic],
        }])

        if result and "result" in result:
            for log in result["result"]:
                token = log["address"]
                if len(log.get("topics", [])) >= 3:
                    spender = "0x" + log["topics"][2][26:]
                else:
                    continue
                pair = (token.lower(), spender.lower())
                if pair not in seen:
                    seen.add(pair)
                    approvals.append((token, spender))

        current_from -= chunk_size
        scanned += chunk_size

        # Stop early if we found approvals and already scanned a decent range
        if approvals and scanned >= 500000:
            break

    return approvals


def check_allowance(chain_id, token_addr, wallet, spender):
    """Check ERC20 allowance via eth_call."""
    data = "0xdd62ed3e" + wallet[2:].lower().rjust(64, "0") + spender[2:].lower().rjust(64, "0")
    result = rpc_call(chain_id, "eth_call", [{"to": token_addr, "data": data}, "latest"])
    if result and "result" in result and result["result"]:
        return int(result["result"], 16)
    return 0


def query_goplus(addr, chain_id):
    """Fallback: query GoPlus Security API when Honeypot.is doesn't have the token."""
    url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_id}?contract_addresses={addr}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "LeonisGuardian/1.0")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        return {"_not_found": True, "error": str(e)}

    result = data.get("result", {}).get(addr.lower())
    if not result:
        return {"_not_found": True, "message": "Token not found in GoPlus"}

    # Map GoPlus response to Honeypot.is-like structure for extract_features
    return {
        "simulationResult": {
            "buyTax": float(result.get("buy_tax", "0") or 0) * 100,
            "sellTax": float(result.get("sell_tax", "0") or 0) * 100,
            "transferTax": 0,
        },
        "contractCode": {
            "openSource": result.get("is_open_source", "0") == "1",
            "isProxy": result.get("is_proxy", "0") == "1",
            "hasProxyCalls": False,
        },
        "holderAnalysis": {
            "holders": int(result.get("holder_count", "0") or 0),
            "failed": 0,
            "siphoned": 0,
            "averageTax": 0,
            "highestTax": 0,
            "snipersFailed": 0,
            "snipersSuccess": 0,
        },
        "summary": {
            "riskLevel": 30 if result.get("is_honeypot", "0") == "1" else 15,
            "risk": "medium" if result.get("is_honeypot", "0") == "1" else "low",
        },
        "honeypotResult": {
            "isHoneypot": result.get("is_honeypot", "0") == "1",
        },
        "simulationSuccess": True,
        "token": {
            "name": result.get("token_name", "?"),
            "symbol": result.get("token_symbol", "?"),
        },
        "flags": [{"flag": "goPlus_source"}] if result.get("is_honeypot", "0") == "1" else [],
    }


def query_honeypot(addr, chain_id):
    url = f"https://api.honeypot.is/v2/IsHoneypot?address={addr}&chainID={chain_id}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "LeonisGuardian/1.0")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        # 404 = token not indexed (not an API error)
        if e.code == 404:
            try:
                body = json.loads(e.read().decode())
                if "Token not found" in body.get("error", ""):
                    return {"_not_found": True, "message": "Token not yet indexed by Honeypot.is"}
            except Exception:
                pass
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def extract_features(hp_data):
    if not hp_data:
        return None
    sim = hp_data.get("simulationResult", {})
    contract = hp_data.get("contractCode", {})
    ha = hp_data.get("holderAnalysis", {})
    pair = hp_data.get("pair", {})
    summary = hp_data.get("summary", {})

    risk_level = float(summary.get("riskLevel", 0) or 0)
    is_honeypot = float(hp_data.get("honeypotResult", {}).get("isHoneypot", False))
    buy_tax = float(sim.get("buyTax", 0) or 0)
    sell_tax = float(sim.get("sellTax", 0) or 0)
    transfer_tax = float(sim.get("transferTax", 0) or 0)
    is_open_source = float(contract.get("openSource", False))
    is_proxy = float(contract.get("isProxy", False))
    has_proxy_calls = float(contract.get("hasProxyCalls", False))
    failed_sells = float(ha.get("failed", 0) or 0)
    siphoned = float(ha.get("siphoned", 0) or 0)
    avg_tax = float(ha.get("averageTax", 0) or 0)
    highest_tax = float(ha.get("highestTax", 0) or 0)
    flag_count = float(len(hp_data.get("flags", []) or []))
    holder_count = float(ha.get("holders", 0) or 0)
    snipers_failed = float(ha.get("snipersFailed", 0) or 0)
    snipers_success = float(ha.get("snipersSuccess", 0) or 0)
    fail_ratio = failed_sells / max(1.0, holder_count)
    sniper_ratio = snipers_failed / max(1.0, snipers_failed + snipers_success)
    age_days = 0.0
    created = pair.get("createdAtTimestamp")
    if created:
        age_days = max(0.0, (time.time() - float(created)) / 86400)

    return np.array([
        risk_level, is_honeypot, buy_tax, sell_tax, transfer_tax,
        is_open_source, is_proxy, has_proxy_calls, failed_sells, siphoned,
        avg_tax, highest_tax, flag_count, fail_ratio, sniper_ratio,
        snipers_failed, snipers_success, holder_count, age_days,
    ], dtype=np.float32)


def preprocess(features):
    x = features.copy().reshape(1, -1)
    for idx in LOG_TRANSFORM_COLS:
        x[0, idx] = np.log1p(np.abs(x[0, idx]))
    if scaler:
        x = scaler.transform(x)
    return x


@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/guides/<path:filename>")
def guide(filename):
    guides_dir = DIR / "static" / "guides"
    # Try the exact path first
    if (guides_dir / filename).exists():
        return send_from_directory("static/guides", filename)
    # Try with .html extension (clean URLs)
    html_name = filename + ".html"
    if (guides_dir / html_name).exists():
        return send_from_directory("static/guides", html_name)
    # Try as directory/index.html
    if (guides_dir / filename / "index.html").exists():
        return send_from_directory("static/guides", filename + "/index.html")
    return "Not Found", 404


@app.route("/api/check")
def api_check():
    addr = request.args.get("address", "").strip()
    chain_id = request.args.get("chain", "56").strip()

    if not addr:
        return jsonify({"error": "Missing address parameter"}), 400

    chain_name = CHAIN_NAMES.get(chain_id, chain_id)

    hp_data = query_honeypot(addr, chain_id)

    # Honeypot.is doesn't have this token — try GoPlus as fallback
    if hp_data.get("_not_found"):
        hp_data = query_goplus(addr, chain_id)

    if "error" in hp_data:
        return jsonify({"error": f"Honeypot.is API error: {hp_data['error']}"}), 502

    if hp_data.get("_not_found"):
        # Neither Honeypot.is nor GoPlus has this token — basic on-chain info only
        token_name, token_symbol = get_token_info(chain_id, addr)
        return jsonify({
            "address": addr,
            "chain": chain_name,
            "token_name": token_name,
            "token_symbol": token_symbol,
            "verdict": "unknown",
            "score": 0,
            "status": "not_indexed",
            "message": "Token chưa được index bởi Honeypot.is hoặc GoPlus. Có thể là token quá mới hoặc ít người biết.",
            "red_flags": [],
            "scam_types": ["not-indexed"],
            "honeypot_url": f"https://honeypot.is/{chain_name}?address={addr}",
        })

    if hp_data.get("simulationSuccess") is False:
        return jsonify({
            "error": "Token too new or unsupported",
            "token": hp_data.get("token", {}),
            "status": "unknown"
        })

    features = extract_features(hp_data)
    if features is None:
        return jsonify({"error": "Cannot extract features"}), 500

    x = preprocess(features)
    out = session.run(None, {"features": x})
    prob = float(out[1][0][1])

    token = hp_data.get("token", {})
    summary = hp_data.get("summary", {})
    sim = hp_data.get("simulationResult", {})
    contract = hp_data.get("contractCode", {})

    verdict = "scam" if prob > 0.7 else ("suspicious" if prob > 0.4 else "safe")

    red_flags = []
    scam_types = []
    if features[1] > 0.5:
        red_flags.append("HONEYPOT — buy OK, sell blocked")
        scam_types.append("honeypot")
    if features[3] > 15:
        red_flags.append(f"High sell tax: {features[3]:.0f}%")
        scam_types.append("high-tax")
    if features[5] < 0.5:
        red_flags.append("Contract NOT verified (closed source)")
        scam_types.append("closed-source")
    if features[6] > 0.5:
        red_flags.append("Proxy — owner can upgrade logic")
        scam_types.append("proxy")
    if features[8] > 50:
        red_flags.append(f"{int(features[8])} failed sell txs")
    if features[9] > 0:
        red_flags.append(f"{int(features[9])} wallets siphoned")
    if features[12] > 1:
        red_flags.append(f"{int(features[12])} security flags")
    if features[18] < 7:
        red_flags.append(f"Very new: {features[18]:.0f} days")
        scam_types.append("new-token")

    return jsonify({
        "address": addr,
        "chain": chain_name,
        "token_name": token.get("name", "?"),
        "token_symbol": token.get("symbol", "?"),
        "risk_level": summary.get("riskLevel", 0),
        "risk_label": summary.get("risk", "?"),
        "buy_tax": sim.get("buyTax", 0),
        "sell_tax": sim.get("sellTax", 0),
        "open_source": bool(contract.get("openSource")),
        "is_proxy": bool(contract.get("isProxy")),
        "verdict": verdict,
        "score": round(prob * 100, 1),
        "red_flags": red_flags,
        "scam_types": scam_types,
        "honeypot_url": f"https://honeypot.is/{chain_name}?address={addr}",
    })


@app.route("/api/approvals")
def api_approvals():
    wallet = request.args.get("wallet", "").strip()
    chain_id = request.args.get("chain", "1").strip()

    if not wallet or not wallet.startswith("0x") or len(wallet) != 42:
        return jsonify({"error": "Invalid wallet address"}), 400

    if chain_id not in RPC_URLS:
        return jsonify({"error": f"Chain {chain_id} not supported"}), 400

    chain_name = CHAIN_NAMES.get(chain_id, chain_id)

    # Step 1: Query recent Approval logs (200K blocks)
    approval_pairs = query_approval_logs(chain_id, wallet, max_blocks=200000)

    # Step 2: Also check popular tokens against common spenders (catches old approvals)
    popular_tokens = [
        "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
        "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # WETH
        "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",  # WBTC
        "0x6b175474e89094c44da98b954eedeac495271d0f",  # DAI
        "0x6982508145454ce325ddbe47a25d4ec3d2311933",  # PEPE
        "0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce",  # SHIB
        "0x514910771af9ca656af840dff83e8264ecf986ca",  # LINK
        "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",  # UNI
    ]
    common_spenders = [
        "0xdef1c0ded9bec7f1a1670819833240f027b25eff",  # 0x Protocol
        "0x1111111254fb6c44bac0bed2854e76f90643097d",  # 1inch
        "0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad",  # Uniswap Universal
        "0x7a250d5630b4cf539739df2c5dacb4c659f2488d",  # Uniswap V2
        "0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45",  # Uniswap V3
    ]

    seen_pairs = set((t.lower(), s.lower()) for t, s in approval_pairs)
    for token_addr in popular_tokens:
        for spender_addr in common_spenders:
            pair = (token_addr.lower(), spender_addr.lower())
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            approval_pairs.append((token_addr, spender_addr))

    # Step 2: Check current allowance for each (token, spender) pair
    approvals = []
    total_active = 0
    high_risk = 0
    unlimited_count = 0

    for token_addr, spender_addr in approval_pairs:
        try:
            allowance = check_allowance(chain_id, token_addr, wallet, spender_addr)
        except Exception:
            continue

        if allowance == 0:
            continue

        total_active += 1
        is_unlimited = allowance > 10**30

        if is_unlimited:
            unlimited_count += 1

        risk = "high" if is_unlimited else "low"

        if risk == "high":
            high_risk += 1

        spender_name = KNOWN_SPENDERS.get(spender_addr.lower(), "Unknown Contract")
        token_name, token_symbol = get_token_info(chain_id, token_addr)
        if token_name == "?":
            token_name = token_symbol if token_symbol != "?" else token_addr[:10] + "..."

        approvals.append({
            "token": token_name,
            "token_symbol": token_symbol,
            "token_address": token_addr,
            "spender": spender_name,
            "spender_address": spender_addr,
            "allowance": str(allowance),
            "unlimited": is_unlimited,
            "risk": risk,
        })

    # Sort: high risk first, then by token name
    approvals.sort(key=lambda a: (0 if a["risk"] == "high" else 1, a["token"]))

    return jsonify({
        "wallet": wallet,
        "chain": chain_name,
        "chain_id": chain_id,
        "total_active": total_active,
        "high_risk": high_risk,
        "unlimited": unlimited_count,
        "approvals": approvals,
        "scanned_logs": len(approval_pairs),
        "method": "on-chain eth_getLogs + eth_call",
    })


@app.route("/api/eip7702")
def api_eip7702():
    wallet = request.args.get("wallet", "").strip()

    if not wallet or not wallet.startswith("0x") or len(wallet) != 42:
        return jsonify({"error": "Invalid wallet address"}), 400

    results = []
    total_scanned = 0
    delegations_found = 0

    for chain_id, chain_name in CHAIN_NAMES.items():
        total_scanned += 1
        try:
            code_result = rpc_call(chain_id, "eth_getCode", [wallet, "latest"])
        except Exception:
            results.append({
                "chain": chain_name,
                "chain_id": chain_id,
                "status": "error",
                "delegated": False,
                "code": None,
            })
            continue

        if not code_result or "result" not in code_result:
            results.append({
                "chain": chain_name,
                "chain_id": chain_id,
                "status": "error",
                "delegated": False,
                "code": None,
            })
            continue

        code = code_result["result"]
        is_delegated = code != "0x" and len(code) > 2

        if is_delegated:
            delegations_found += 1
            delegated_to = None
            if code.startswith("0xef01"):
                # EIP-7702 delegation: 0xef01 + 20-byte address
                try:
                    delegated_to = "0x" + code[6:46]
                except Exception:
                    pass

        results.append({
            "chain": chain_name,
            "chain_id": chain_id,
            "status": "clean" if not is_delegated else "delegated",
            "delegated": is_delegated,
            "code": code if is_delegated else None,
            "delegated_to": delegated_to if is_delegated else None,
        })

    return jsonify({
        "wallet": wallet,
        "total_scanned": total_scanned,
        "delegations_found": delegations_found,
        "chains": results,
    })


@app.route("/api/alerts")
def api_alerts():
    """Return recent crypto scam alerts from Rekt.news RSS."""
    try:
        req = urllib.request.Request("https://rekt.news/feed")
        req.add_header("User-Agent", "LeonisGuardian/1.0")
        with urllib.request.urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read().decode("utf-8"))
    except Exception:
        return jsonify({"alerts": [], "error": "RSS unavailable"})

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    alerts = []
    for entry in root.findall(".//item")[:6]:
        title = entry.find("title")
        link = entry.find("link")
        desc = entry.find("description")
        date = entry.find("pubDate")
        alerts.append({
            "title": title.text.strip() if title is not None and title.text else "?",
            "url": link.text.strip() if link is not None and link.text else "#",
            "description": (desc.text or "")[:200] if desc is not None else "",
            "date": date.text if date is not None else "",
        })

    return jsonify({"alerts": alerts, "source": "Rekt.news"})


@app.route("/api/stats")
def api_stats():
    """Analytics dashboard data (key-protected)."""
    if request.args.get("key") != STATS_KEY:
        return jsonify({"error": "not found"}), 404
    daily = dict(sorted(analytics["daily"].items(), reverse=True)[:7])
    endpoints = dict(analytics["endpoints"])
    referrers = dict(
        sorted(analytics["referrers"].items(), key=lambda x: x[1], reverse=True)[:10]
    )
    return jsonify({
        "server_started": analytics["started"],
        "total_requests": analytics["total"],
        "unique_ips": len(analytics["ips"]),
        "endpoints": endpoints,
        "referrers": referrers,
        "daily": daily,
    })


@app.route("/stats")
def stats_page():
    if request.args.get("key") != STATS_KEY:
        return "not found", 404
    return send_from_directory("static", "stats.html")


@app.route("/api/airdrop/safety")
def api_airdrop_safety():
    """Analyze airdrop claim link for phishing, drainers, and scams."""
    url = request.args.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL required"}), 400

    try:
        report = analyze_airdrop(url)
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)[:200]}"}), 500


# ── Blog API ──
def _parse_meta(html, slug, image_dir):
    """Extract title, date, description, image from article HTML."""
    import re, html as _html
    title = ""
    date = ""
    description = ""
    image = ""

    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if m:
        title = m.group(1).strip()
        title = re.sub(r'\s*[—–-]\s*Leonis Forge\s*$', '', title).strip()
        title = _html.unescape(title)

    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
    if m:
        description = m.group(1).strip()

    m = re.search(r'class="meta"[^>]*>([^<]+)<', html)
    if not m:
        m = re.search(r'<time[^>]*>([^<]+)<', html)
    if m:
        date = _html.unescape(m.group(1).strip())

    m = re.search(r'<img\s+[^>]*src="([^"]*)"', html)
    if m:
        img_src = m.group(1).strip()
        if img_src.startswith("/"):
            image = img_src
        else:
            image = f"/{image_dir}/{img_src}"

    return {
        "title": title,
        "date": date,
        "description": description,
        "image": image,
    }


@app.route("/api/blog/list")
def api_blog_list():
    """Return all blog articles with multilingual metadata."""
    blog_root = DIR / "static" / "blog"
    articles = []

    if not blog_root.exists():
        return jsonify({"articles": []})

    for slug_dir in sorted(blog_root.iterdir(), reverse=True):
        if not slug_dir.is_dir():
            continue

        slug = slug_dir.name
        main_html = slug_dir / "index.html"

        # Must have at least the default (English) version
        if not main_html.exists():
            continue

        try:
            main_content = main_html.read_text(encoding="utf-8")
        except Exception:
            continue

        # Parse all available language versions
        languages = {}
        image_dir = f"blog/{slug}"

        # Default (English) — from index.html
        languages["en"] = _parse_meta(main_content, slug, image_dir)

        # Check for translated versions: index.vi.html, index.zh.html, index.ko.html
        for lang in ("vi", "zh", "ko"):
            lang_path = slug_dir / f"index.{lang}.html"
            if lang_path.exists():
                try:
                    lang_content = lang_path.read_text(encoding="utf-8")
                    languages[lang] = _parse_meta(lang_content, slug, image_dir)
                except Exception:
                    pass

        articles.append({
            "slug": slug,
            "url": f"/blog/{slug}",
            "languages": languages,
            "default_lang": "en",
        })

    # Sort by date, newest first
    from datetime import datetime
    def _parse_date(article):
        date_str = article.get("languages", {}).get("en", {}).get("date", "")
        # "Leonis · May 6, 2026 · Minara Strategy Studio"
        for fmt in ("%B %d, %Y", "%d/%m/%Y"):
            for part in date_str.split("·"):
                part = part.strip()
                try:
                    return datetime.strptime(part, fmt)
                except ValueError:
                    continue
        return datetime.min  # fallback: sort to the end

    articles.sort(key=_parse_date, reverse=True)

    return jsonify({"articles": articles})


# ── Blog ──
@app.route("/blog/<slug>")
def blog_article(slug):
    blog_dir = DIR / "static" / "blog" / slug
    lang = request.args.get("lang", "").lower()
    if lang and lang in ("vi", "zh", "ko"):
        lang_file = blog_dir / f"index.{lang}.html"
        if lang_file.exists():
            return send_from_directory(str(blog_dir.parent), f"{slug}/index.{lang}.html")
    if (blog_dir / "index.html").exists():
        return send_from_directory(str(blog_dir.parent), f"{slug}/index.html")
    return "Article not found", 404


@app.route("/blog/")
def blog_index():
    return "Blog coming soon", 200


@app.route("/blog/<slug>/<path:filename>")
def blog_asset(slug, filename):
    blog_dir = DIR / "static" / "blog" / slug
    return send_from_directory(str(blog_dir), filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
