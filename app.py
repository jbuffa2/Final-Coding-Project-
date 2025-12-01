import pandas as pd
import plotly.express as px

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output

# ============================
# 1. LOAD CLEANED DATA
# ============================
df = pd.read_csv("london_airbnb_clean.csv")
df["room_type"] = df["room_type"].astype("category")
df["time_period"] = df["time_period"].astype("category")

# ============================
# 2. GLOBAL PLOTLY THEME
# ============================
px.defaults.template = "plotly_white"
px.defaults.width = 800
px.defaults.height = 480
px.defaults.color_discrete_sequence = ["#003688", "#E32017", "#FF8F1C"]

# ============================
# 3. SETUP APP
# ============================
app = Dash(__name__)
server = app.server

# Dropdown options
room_type_options = [{"label": rt, "value": rt} for rt in sorted(df["room_type"].unique())]
time_period_options = [{"label": tp, "value": tp} for tp in df["time_period"].cat.categories]
sat_bucket_options = [
    {"label": str(s), "value": str(s)} for s in df["satisfaction_bucket"].dropna().unique()
]

CARD = {
    "backgroundColor": "rgba(255,255,255,0.92)",
    "padding": "12px",
    "borderRadius": "10px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.15)",
}

# ============================
# 4. APP LAYOUT
# ============================
app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "padding": "30px 20px",
        "fontFamily": "Arial, sans-serif",

        # LONDON SKYLINE FULL BACKGROUND
        "backgroundImage": "url('/assets/london_sky.webp')",
        "backgroundSize": "cover",
        "backgroundRepeat": "no-repeat",
        "backgroundAttachment": "fixed",
    },
    children=[
        html.Div(
            style={
                "maxWidth": "1200px",
                "margin": "0 auto",
                "backgroundColor": "rgba(255,255,255,0.92)",
                "padding": "20px",
                "borderRadius": "14px",
                "boxShadow": "0 4px 14px rgba(0,0,0,0.35)",
            },
            children=[
                # HEADER
                html.H1(
                    "London Airbnb Price Dashboard Written By Jack Buffa, Misha Chen, and Veronica Lee",
                    style={"textAlign": "center", "marginBottom": "3px"}
                ),
                html.P(
                    "Analyzing how location, room type, and satisfaction impact pricing across London",
                    style={"textAlign": "center", "color": "#444"}
                ),

                # header skyline image
                html.Img(
                    src=app.get_asset_url("london_sky.webp"),
                    style={
                        "width": "75%",          # slightly smaller so it looks cleaner
                        "maxWidth": "900px",
                        "display": "block",
                        "margin": "0 auto",
                        "borderRadius": "12px",
                        "boxShadow": "0 3px 10px rgba(0,0,0,0.35)",
                        "marginBottom": "10px",
                    }
                ),

                # LOGOS ROW
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "gap": "40px",
                        "marginBottom": "15px"
                    },
                    children=[
                        html.Img(src=app.get_asset_url("airbnb_logo.png"), style={"height": "50px"}),
                        html.Img(src=app.get_asset_url("london_flag.png"), style={"height": "50px"}),
                        html.Img(
                            src=app.get_asset_url("bnb_collage.webp"),
                            style={"height": "50px", "borderRadius": "4px"},
                        ),
                    ],
                ),

                html.Hr(),

                # FILTERS
                html.Div(
                    style={"display": "flex", "gap": "15px", "marginBottom": "15px"},
                    children=[
                        html.Div(
                            style={"flex": "1", **CARD},
                            children=[
                                html.Label("Room Type", style={"fontWeight": "bold"}),
                                dcc.Dropdown(
                                    id="room-type-filter",
                                    options=room_type_options,
                                    multi=True,
                                    value=[o["value"] for o in room_type_options],
                                ),
                            ],
                        ),
                        html.Div(
                            style={"flex": "1", **CARD},
                            children=[
                                html.Label("Time Period", style={"fontWeight": "bold"}),
                                dcc.Checklist(
                                    id="time-period-filter",
                                    options=time_period_options,
                                    value=[o["value"] for o in time_period_options],
                                    inline=True,
                                ),
                            ],
                        ),
                        html.Div(
                            style={"flex": "1", **CARD},
                            children=[
                                html.Label("Satisfaction", style={"fontWeight": "bold"}),
                                dcc.Dropdown(
                                    id="satisfaction-filter",
                                    options=[{"label": "All", "value": "All"}] + sat_bucket_options,
                                    value="All",
                                ),
                            ],
                        ),
                    ],
                ),

                # ===== STACKED GRAPHS (NO HORIZONTAL SCROLL) =====

                # Price vs Distance
                html.Div(
                    style={**CARD, "marginBottom": "15px"},
                    children=[dcc.Graph(id="price-distance")],
                ),

                # Average Price by Distance Bucket
                html.Div(
                    style={**CARD, "marginBottom": "15px"},
                    children=[dcc.Graph(id="avg-price-distance")],
                ),

                # Attractions Index vs Price per Person
                html.Div(
                    style={**CARD, "marginBottom": "15px"},
                    children=[dcc.Graph(id="attr-price")],
                ),

                # Box Plot: Price per Person by Distance Bucket
                html.Div(
                    style={**CARD, "marginBottom": "15px"},
                    children=[dcc.Graph(id="box-distance")],
                ),

                # COLLAGE PANEL
                html.Div(
                    style={**CARD, "display": "flex", "gap": "20px"},
                    children=[
                        html.Img(
                            src=app.get_asset_url("bnb_collage.webp"),
                            style={"width": "32%", "borderRadius": "10px"}
                        ),
                        html.Div(
                            style={"flex": "1"},
                            children=[
                                html.H3("Inside London's Airbnb Market"),
                                html.P(
                                    "The collage showcases real London Airbnb interiors. "
                                    "The dashboard visualizes how these homes are priced "
                                    "based on distance, demand, and satisfaction."
                                ),
                            ],
                        ),
                    ],
                ),

                html.Br(),

                # HISTOGRAM
                html.Div(
                    style={**CARD, "marginBottom": "15px"},
                    children=[dcc.Graph(id="price-hist")],
                ),

                # TABLE
                html.Div(
                    style=CARD,
                    children=[
                        html.H3("Cleaned Airbnb Data (Preview)"),
                        dash_table.DataTable(
                            id="cleaned-table",
                            columns=[{"name": i, "id": i} for i in df.columns],
                            data=df.head(25).to_dict("records"),
                            page_size=10,
                            style_table={"overflowX": "auto"},
                            style_header={"backgroundColor": "#003688", "color": "white"},
                            style_cell={"fontSize": 12, "padding": "4px"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# ============================
# 5. FILTER FUNCTION
# ============================
def filter_df(room_types, time_periods, sat):
    d = df.copy()
    if room_types:
        d = d[d["room_type"].isin(room_types)]
    if time_periods:
        d = d[d["time_period"].isin(time_periods)]
    if sat != "All":
        d = d[d["satisfaction_bucket"].astype(str) == sat]
    return d

# ============================
# 6. CALLBACKS
# ============================

# Scatter 1: Price vs Distance
@app.callback(
    Output("price-distance", "figure"),
    Input("room-type-filter", "value"),
    Input("time-period-filter", "value"),
    Input("satisfaction-filter", "value"),
)
def update_price_dist(room, timep, sat):
    d = filter_df(room, timep, sat)

    fig = px.scatter(
        d,
        x="dist",
        y="realSum",
        color="room_type",
        size="person_capacity",
        animation_frame="satisfaction_bucket",
        facet_col="time_period",
        hover_data=["price_per_person", "host_is_superhost"],
        title="Price vs Distance to City Center",
    )

    # Airbnb watermark
    fig.add_layout_image(
        dict(
            source="/assets/airbnb_logo.png",
            xref="paper", yref="paper",
            x=1.15, y=0,
            sizex=0.32, sizey=0.32,
            xanchor="right", yanchor="bottom",
            opacity=0.15,
        )
    )

    return fig

# Avg Price Bar
@app.callback(
    Output("avg-price-distance", "figure"),
    Input("room-type-filter", "value"),
    Input("time-period-filter", "value"),
    Input("satisfaction-filter", "value"),
)
def update_avg(room, timep, sat):
    d = filter_df(room, timep, sat)
    grp = (
        d.groupby(["distance_bucket", "room_type", "time_period"], as_index=False)
        ["realSum"].mean().rename(columns={"realSum": "avg_price"})
    )

    fig = px.bar(
        grp,
        x="distance_bucket",
        y="avg_price",
        color="time_period",
        animation_frame="room_type",
        barmode="group",
        title="Average Price by Distance Bucket",
    )

    return fig

# Attr vs Price Per Person
@app.callback(
    Output("attr-price", "figure"),
    Input("room-type-filter", "value"),
    Input("time-period-filter", "value"),
    Input("satisfaction-filter", "value"),
)
def update_attr(room, timep, sat):
    d = filter_df(room, timep, sat)

    fig = px.scatter(
        d,
        x="attr_index",
        y="price_per_person",
        color="satisfaction_bucket",
        facet_col="time_period",
        hover_data=["room_type", "distance_bucket"],
        title="Attractions Index vs Price per Person",
    )
    return fig

# Box Plot
@app.callback(
    Output("box-distance", "figure"),
    Input("room-type-filter", "value"),
    Input("time-period-filter", "value"),
    Input("satisfaction-filter", "value"),
)
def update_box(room, timep, sat):
    d = filter_df(room, timep, sat)

    fig = px.box(
        d,
        x="distance_bucket",
        y="price_per_person",
        color="time_period",
        title="Price per Person by Distance Bucket",
    )
    return fig

# Histogram
@app.callback(
    Output("price-hist", "figure"),
    Input("room-type-filter", "value"),
    Input("time-period-filter", "value"),
    Input("satisfaction-filter", "value"),
)
def update_hist(room, timep, sat):
    d = filter_df(room, timep, sat)

    fig = px.histogram(
        d,
        x="realSum",
        color="satisfaction_bucket",
        nbins=40,
        opacity=0.75,
        title="Price Distribution",
    )

    # UK Flag watermark
    fig.add_layout_image(
        dict(
            source="/assets/london_flag.png",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            sizex=1.0, sizey=1.0,
            xanchor="center", yanchor="middle",
            opacity=0.09,
        )
    )

    return fig

# ============================
# 7. RUN
# ============================a
if __name__ == "__main__":
    app.run(debug=True)
