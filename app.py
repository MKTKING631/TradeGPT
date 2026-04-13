from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

# -------- STOCK ANALYSIS --------
def analyze_stock(symbol):
    try:
        data = yf.download(symbol, period="1mo", interval="1d", progress=False)

        # ✅ Fix: handle empty data
        if data is None or data.empty:
            return None

        # Moving Average (5 days)
        data["MA5"] = data["Close"].rolling(5).mean()

        # RSI Calculation (safe)
        delta = data["Close"].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        # ✅ Fix: avoid division by zero
        rs = avg_gain / (avg_loss + 1e-10)

        data["RSI"] = 100 - (100 / (1 + rs))

        latest = data.iloc[-1]

        price = float(latest["Close"])
        ma = float(latest["MA5"]) if not pd.isna(latest["MA5"]) else 0
        rsi = float(latest["RSI"]) if not pd.isna(latest["RSI"]) else 0

        # Signal
        if rsi > 70:
            signal = "Overbought 🔴 (Sell)"
        elif rsi < 30:
            signal = "Oversold 🟢 (Buy)"
        else:
            signal = "Neutral 🟡"

        return price, ma, rsi, signal

    except Exception as e:
        print("ERROR:", e)
        return None


# -------- ROUTES --------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip().upper()

    result = analyze_stock(message)

    if result is None:
        reply = "❌ Invalid stock or no data. Try: AAPL, TSLA, RELIANCE.NS"
    else:
        price, ma, rsi, signal = result

        reply = f"""
📊 Stock: {message}
💰 Price: {price:.2f}
📈 MA(5): {ma:.2f}
📉 RSI: {rsi:.2f}
🚦 Signal: {signal}
"""

    return jsonify({"reply": reply})


# -------- RUN (RENDER READY) --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
