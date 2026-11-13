import plotly.graph_objects as go
from plotly.io import to_html

PRICE_FIELDS = [
    ("open", "Open"),
    ("high", "High"),
    ("low", "Low"),
    ("close", "Close"),
]


def build_chart(stock_data, chart_type, symbol, start_date, end_date):

    if chart_type not in ("bar", "line"):
        raise ValueError("Chart type must be 'bar' or 'line'.")

    if not stock_data:
        raise ValueError("There is no stock data to chart.")

    dates = [row["date"] for row in stock_data]

    fig = go.Figure()

    for key, label in PRICE_FIELDS:
        values = [row[key] for row in stock_data]

        if chart_type == "line":
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=values,
                    mode="lines+markers",
                    name=label
                )
            )
        else:
            fig.add_trace(
                go.Bar(
                    x=dates,
                    y=values,
                    name=label
                )
            )

    fig.update_layout(
        title=f"Stock Data for {symbol}: {start_date} to {end_date}",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        barmode="group",
        hovermode="x unified",
        legend_title="Price",
    )

    return fig


def create_chart(stock_data, chart_type, symbol, start_date, end_date):

    fig = build_chart(
        stock_data,
        chart_type,
        symbol,
        start_date,
        end_date
    )

    return to_html(fig, full_html=False)