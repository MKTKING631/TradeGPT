from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__) 

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    import yfinance as yf
    from flask import request, jsonify

    user_input = request.json.get("message")

    try:
        data = yf.Ticker(user_input)
        hist = data.history(period="1mo")
        prices = list(hist["Close"])

        if len(prices) < 20:
            return jsonify({"reply": "Not enough data ❌"})

        # Moving Average
        short_avg = sum(prices[-5:]) / 5
        long_avg = sum(prices[-20:]) / 20

        if short_avg > long_avg:
            trend = "UPTREND 📈"
            signal = "BUY 🟢"
        else:
            trend = "DOWNTREND 📉"
            signal = "SELL 🔴"

        # RSI
        gains, losses = [], []

        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        avg_gain = sum(gains[-14:]) / 14 if len(gains) >= 14 else 0
        avg_loss = sum(losses[-14:]) / 14 if len(losses) >= 14 else 1

        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = round(100 - (100 / (1 + rs)), 2)

        reply = f"""
Stock: {user_input}
Trend: {trend}
Signal: {signal}
RSI: {rsi}
"""

    except:
        reply = "Error fetching stock ❌"

    return jsonify({"reply": reply})
