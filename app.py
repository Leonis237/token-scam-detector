#!/usr/bin/env python3
"""Token Scam Detector — Flask web API + frontend."""

import json, time, pickle, urllib.request, os
import numpy as np
import onnxruntime as ort
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")
DIR = Path(__file__).parent

CHAIN_NAMES = {"1": "eth", "56": "bsc", "8453": "base", "42161": "arbitrum", "137": "polygon"}
LOG_TRANSFORM_COLS = [8, 9, 17]

# Load model once at startup
MODEL_PATH = DIR / "scam_detector_v3.onnx"
SCALER_PATH = DIR / "scam_detector_v3_scaler.pkl"
session = ort.InferenceSession(str(MODEL_PATH))
if SCALER_PATH.exists():
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)
else:
    scaler = None


def query_honeypot(addr, chain_id):
    url = f"https://api.honeypot.is/v2/IsHoneypot?address={addr}&chainID={chain_id}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Token-Scam-Detector/1.0")
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

    # Run inference
    x = preprocess(features)
    out = session.run(None, {"features": x})
    prob = float(out[1][0][1])

    token = hp_data.get("token", {})
    summary = hp_data.get("summary", {})
    sim = hp_data.get("simulationResult", {})
    contract = hp_data.get("contractCode", {})

    verdict = "scam" if prob > 0.7 else ("suspicious" if prob > 0.4 else "safe")

    # Build red flags
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
