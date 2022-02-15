from dash import Dash, html, dcc, Input, Output
import altair as alt
from vega_datasets import data


# Read in global data
df = data.barley()

# Setup app and layout/frontend
app = Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

server = app.server

app.layout = html.Div(
    [
        html.Iframe(
            id="boxplot",
            style={"border-width": "0", "width": "100%", "height": "300px"},
        ),
        dcc.Dropdown(
            id="widget-site",
            value="Morris",  # REQUIRED to show the plot on the first page load
            options=[{"label": col, "value": col} for col in df.site.unique()],
        ),
    ]
)

# Set up callbacks/backend
@app.callback(Output("boxplot", "srcDoc"), Input("widget-site", "value"))
def plot_altair(site):
    df_plot = df.query(f"site == '{site}'")
    chart = (
        alt.Chart(df_plot).mark_boxplot().encode(y="variety", x="yield").interactive()
    )
    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
