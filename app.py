import csv

from flask import Flask, render_template, request

from stock_api import get_stock_data
from charts import create_chart

app = Flask(__name__)

def load_symbols():

    symbols = []

    with open("stocks.csv", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            symbols.append(row["Symbol"])

    return symbols

@app.route("/", methods=["GET", "POST"])
def home():

    symbols = load_symbols()

    chart_html = None
    error_message = None

    if request.method == "POST":

        try:
            symbol = request.form["symbol"]
            chart_type = request.form["chart_type"]
            time_series = request.form["time_series"]
            start_date = request.form["start_date"]
            end_date = request.form["end_date"]

            stock_data = get_stock_data(
                symbol,
                time_series,
                start_date,
                end_date
            )

            chart_html = create_chart(
                stock_data,
                chart_type,
                symbol,
                start_date,
                end_date
            )

        except Exception as error:
            error_message = str(error)
            print("ERROR:", error)

    return render_template(
        "index.html",
        chart_html=chart_html,
        error_message=error_message,
        symbols=symbols
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True
    )
