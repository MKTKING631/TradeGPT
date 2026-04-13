from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

# -------- STOCK ANALYSIS FUNCTION --------
def analyze_stock(symbol):
    try:
        data = yf.download(symbol, period="1mo", interval="1d")

        if data.empty:
            return None

        # Moving Average (5 days)
        data["MA5"] = data["Close"].rolling(window=5).mean()

        # RSI Calculation
        delta = data["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

        rs = gain / loss
        data["RSI"] = 100 - (100 / (1 + rs))

        latest = data.iloc[-1]

        price = latest["Close"]
        ma = latest["MA5"]
        rsi = latest["RSI"]

        # Signal logic
        if rsi > 70:
            signal = "Overbought 🔴 (Sell)"
        elif rsi < 30:
            signal = "Oversold 🟢 (Buy)"
        else:
            signal = "Neutral 🟡"

        return price, ma, rsi, signal

    except:
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
        reply = "❌ Invalid stock or error. Try: AAPL, TSLA, RELIANCE.NS"
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


# -------- RUN --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
