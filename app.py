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

        try:
            data = yf.Ticker(stock)
            hist = data.history(period="7d")

            prices = list(hist["Close"])

            if len(prices) > 1:
                if prices[-1] > prices[0]:
                    trend = "UPTREND 📈"
                    signal = "BUY 🟢"
                else:
                    trend = "DOWNTREND 📉"
                    signal = "SELL 🔴"

                result = f"{stock} price: {round(prices[-1],2)}"
            else:
                result = "No data found ❌"

        except Exception as e:
            result = "Error ❌"

    return render_template("index.html",
                           result=result,
                           trend=trend,
                           signal=signal,
                           prices=prices)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
