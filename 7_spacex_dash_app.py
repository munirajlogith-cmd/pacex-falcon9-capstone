"""Lab 7: Plotly Dash dashboard. Run: python 7_spacex_dash_app.py  then screenshot the page."""
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from config import LAUNCH_DASH

df = pd.read_csv(LAUNCH_DASH)
min_pl, max_pl = df["Payload Mass (kg)"].min(), df["Payload Mass (kg)"].max()

app = Dash(__name__)
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={"textAlign": "center"}),
    dcc.Dropdown(
        id="site-dropdown",
        options=[{"label": "All Sites", "value": "ALL"}] +
                [{"label": s, "value": s} for s in sorted(df["Launch Site"].unique())],
        value="ALL", placeholder="Select a launch site", searchable=True),
    dcc.Graph(id="success-pie-chart"),
    html.P("Payload range (kg):"),
    dcc.RangeSlider(id="payload-slider", min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 2500)},
                    value=[min_pl, max_pl]),
    dcc.Graph(id="success-payload-scatter-chart"),
])


@app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
def update_pie(site):
    if site == "ALL":
        return px.pie(df, values="class", names="Launch Site",
                      title="Total successful launches by site")
    sub = df[df["Launch Site"] == site]
    return px.pie(sub, names="class", title=f"Success vs failure at {site}")


@app.callback(Output("success-payload-scatter-chart", "figure"),
              [Input("site-dropdown", "value"), Input("payload-slider", "value")])
def update_scatter(site, payload):
    lo, hi = payload
    sub = df[df["Payload Mass (kg)"].between(lo, hi)]
    if site != "ALL":
        sub = sub[sub["Launch Site"] == site]
    return px.scatter(sub, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                      title="Payload vs outcome by booster version")


if __name__ == "__main__":
    app.run(debug=True)
