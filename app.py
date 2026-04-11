import yfinance as yf

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    trend = ""
    signal = ""
    prices = []   # 🔥 IMPORTANT

    if request.method == "POST":
        stock = request.form["stock"]

        try:
            data = yf.Ticker(stock)
            hist = data.history(period="7d")

            prices = list(hist["Close"])

            if len(prices) >= 2:
                if prices[-1] > prices[0]:
                    trend = "UPTREND 📈"
                    signal = "BUY 🟢"
                else:
                    trend = "DOWNTREND 📉"
                    signal = "SELL 🔴"

            result = f"{stock} price: {round(prices[-1],2)}"

        except:
            result = "Error fetching data ❌"

    return render_template(
        "index.html",
        result=result,
        trend=trend,
        signal=signal,
        prices=prices   # 🔥 MUST PASS THIS
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
