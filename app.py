#!/usr/bin/env python3
"""Crypto Guardian — Token Scam Detector + Approval Checker."""
import json, time, pickle, urllib.request, os
import numpy as np
import onnxruntime as ort
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")
DIR = Path(__file__).parent

CHAIN_NAMES = {"1": "eth", "56": "bsc", "8453": "base", "42161": "arbitrum", "137": "polygon"}
LOG_TRANSFORM_COLS = [8, 9, 17]

# RPC endpoints for allowance checks
RPC_URLS = {
    "1": "https://eth.llamarpc.com",
    "56": "https://binance.llamarpc.com",
    "8453": "https://base.llamarpc.com",
    "42161": "https://arbitrum.llamarpc.com",
    "137": "https://polygon.llamarpc.com",
}

# Known DEX/spender contracts to check allowances against
KNOWN_SPENDERS = {
    "1": [
        ("0xdef1c0ded9bec7f1a1670819833240f027b25eff", "0x Protocol"),
        ("0x1111111254fb6c44bac0bed2854e76f90643097d", "1inch Router v4"),
        ("0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad", "Uniswap Universal Router"),
        ("0x881d40237659c251811cec9c364ef91dc08d300c", "Metamask Swap"),
        ("0x7a250d5630b4cf539739df2c5dacb4c659f2488d", "Uniswap V2 Router"),
        ("0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45", "Uniswap V3 Router"),
        ("0x6131b5fae19ea4f9d964eac0408e4408b66337b5", "KyberSwap"),
        ("0x216b4b4ba9f3e719726886d34a177484278bfcae", "Paraswap"),
    ],
    "56": [
        ("0x10ed43c718714eb63d5aa57b78b54704e256024e", "PancakeSwap Router"),
        ("0x13f4ea83d0bd40e75c8222255bc855a974568dd4", "PancakeSwap V3"),
        ("0xdef1c0ded9bec7f1a1670819833240f027b25eff", "0x Protocol"),
        ("0x1111111254fb6c44bac0bed2854e76f90643097d", "1inch Router"),
    ],
    "8453": [
        ("0xdef1c0ded9bec7f1a1670819833240f027b25eff", "0x Protocol"),
        ("0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad", "Uniswap Universal Router"),
    ],
    "42161": [
        ("0xdef1c0ded9bec7f1a1670819833240f027b25eff", "0x Protocol"),
        ("0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad", "Uniswap Universal Router"),
    ],
    "137": [
        ("0xdef1c0ded9bec7f1a1670819833240f027b25eff", "0x Protocol"),
        ("0xa5e0829caced8ffdd4de3c43696c57f7d7a678ff", "QuickSwap Router"),
    ],
}

# Common tokens per chain (top by TVL)
COMMON_TOKENS = {
    "1": [
        ("0xdac17f958d2ee523a2206206994597c13d831ec7", "USDT"),
        ("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "USDC"),
        ("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", "WETH"),
        ("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", "WBTC"),
        ("0x6b175474e89094c44da98b954eedeac495271d0f", "DAI"),
        ("0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce", "SHIB"),
        ("0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0", "MATIC"),
        ("0x514910771af9ca656af840dff83e8264ecf986ca", "LINK"),
    ],
    "56": [
        ("0x55d398326f99059ff775485246999027b3197955", "USDT"),
        ("0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d", "USDC"),
        ("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c", "WBNB"),
        ("0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82", "CAKE"),
        ("0x2170ed0880ac9a755fd29b2688956bd959f933f8", "ETH"),
    ],
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
    """Make a JSON-RPC call to a public RPC endpoint."""
    url = RPC_URLS.get(chain_id)
    if not url:
        return None
    data = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def check_allowance(chain_id, token_addr, wallet, spender):
    """Check ERC20 allowance via eth_call."""
    # allowance(address owner, address spender) → 0xdd62ed3e
    data = "0xdd62ed3e" + wallet[2:].lower().rjust(64, "0") + spender[2:].lower().rjust(64, "0")
    result = rpc_call(chain_id, "eth_call", [
        {"to": token_addr, "data": data}, "latest"
    ])
    if result and "result" in result and result["result"]:
        return int(result["result"], 16)
    return 0


def query_honeypot(addr, chain_id):
    url = f"https://api.honeypot.is/v2/IsHoneypot?address={addr}&chainID={chain_id}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "CryptoGuardian/1.0")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
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


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/check")
def api_check():
    addr = request.args.get("address", "").strip()
    chain_id = request.args.get("chain", "56").strip()

    if not addr:
        return jsonify({"error": "Missing address parameter"}), 400

    chain_name = CHAIN_NAMES.get(chain_id, chain_id)

    hp_data = query_honeypot(addr, chain_id)
    if "error" in hp_data:
        return jsonify({"error": f"Honeypot.is API error: {hp_data['error']}"}), 502

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
    if features[1] > 0.5:
        red_flags.append("HONEYPOT — buy OK, sell blocked")
    if features[3] > 15:
        red_flags.append(f"High sell tax: {features[3]:.0f}%")
    if features[5] < 0.5:
        red_flags.append("Contract NOT verified (closed source)")
    if features[6] > 0.5:
        red_flags.append("Proxy — owner can upgrade logic")
    if features[8] > 50:
        red_flags.append(f"{int(features[8])} failed sell txs")
    if features[9] > 0:
        red_flags.append(f"{int(features[9])} wallets siphoned")
    if features[12] > 1:
        red_flags.append(f"{int(features[12])} security flags")
    if features[18] < 7:
        red_flags.append(f"Very new: {features[18]:.0f} days")

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
        "honeypot_url": f"https://honeypot.is/{chain_name}?address={addr}",
    })


@app.route("/api/approvals")
def api_approvals():
    wallet = request.args.get("wallet", "").strip()
    chain_id = request.args.get("chain", "1").strip()

    if not wallet or not wallet.startswith("0x") or len(wallet) != 42:
        return jsonify({"error": "Invalid wallet address"}), 400

    if chain_id not in RPC_URLS:
        return jsonify({"error": f"Chain {chain_id} not supported for approval checks"}), 400

    chain_name = CHAIN_NAMES.get(chain_id, chain_id)
    spenders = KNOWN_SPENDERS.get(chain_id, [])
    tokens = COMMON_TOKENS.get(chain_id, [])

    approvals = []
    total_active = 0
    high_risk = 0
    unlimited_count = 0

    for token_addr, token_symbol in tokens:
        for spender_addr, spender_name in spenders:
            try:
                allowance = check_allowance(chain_id, token_addr, wallet, spender_addr)
            except Exception:
                continue

            if allowance is None or allowance == 0:
                continue

            total_active += 1
            is_unlimited = allowance > 10**30  # practically unlimited
            if is_unlimited:
                unlimited_count += 1

            risk = "low"
            if is_unlimited:
                risk = "high"
            elif allowance > 10**20:
                risk = "medium"

            if risk == "high":
                high_risk += 1

            approvals.append({
                "token": token_symbol,
                "token_address": token_addr,
                "spender": spender_name,
                "spender_address": spender_addr,
                "allowance": str(allowance),
                "unlimited": is_unlimited,
                "risk": risk,
            })

    return jsonify({
        "wallet": wallet,
        "chain": chain_name,
        "chain_id": chain_id,
        "total_active": total_active,
        "high_risk": high_risk,
        "unlimited": unlimited_count,
        "approvals": approvals,
        "scanned_tokens": len(tokens),
        "scanned_spenders": len(spenders),
        "note": "Scanning top tokens + known DEX contracts. Limited to {} tokens and {} spenders.".format(len(tokens), len(spenders)),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
