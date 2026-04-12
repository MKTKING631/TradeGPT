from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    trend = ""
    signal = ""
    prices = []

    if request.method == "POST":
        stock = request.form.get("stock")

        data = yf.Ticker(stock)
        hist = data.history(period="1mo")
        prices = list(hist["Close"])

        # Moving Average
        short_avg = sum(prices[-5:]) / 5
        long_avg = sum(prices[-20:]) / 20

        if short_avg > long_avg:
        trend = "UPTREND 📈"
        signal = "BUY 🟢"
        ma_signal = "Bullish"
   else:
        trend = "DOWNTREND 📉"
        signal = "SELL 🔴"
        ma_signal = "Bearish"

        # RSI
        gains = []
        losses = []
    
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

        rs =    avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = round(100 - (100 / (1 + rs)), 2)

        result = f"{stock} price: {round(prices[-1],2)}"
