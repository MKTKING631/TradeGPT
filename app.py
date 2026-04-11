from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    trend = ""
    signal = ""

    if request.method == "POST":
        stock = request.form["stock"]

        try:
            data = yf.Ticker(stock)
            import yfinance as yf

# inside your POST block
hist = data.history(period="1mo")

prices = list(hist["Close"])

# Moving average logic
short_avg = sum(prices[-5:]) / 5
long_avg = sum(prices[-20:]) / 20

if short_avg > long_avg:
    trend = "UPTREND 📈"
    signal = "BUY 🟢"
else:
    trend = "DOWNTREND 📉"
    signal = "SELL 🔴"

            result = f"{stock} price: {round(prices[-1],2)}"

        except:
            result = "Error ❌"

    return render_template("index.html", result=result, trend=trend, signal=signal)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
