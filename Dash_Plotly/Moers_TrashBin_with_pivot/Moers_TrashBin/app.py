import dash
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from queries import *


app = dash.Dash(
    __name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width"}],
)
app.title = "Moers Trash Bins"
server = app.server


# Create app layout
app.layout = html.Div(
    [
        html.Div(
            [html.Div(
                [
                    html.H3(
                        "Moers Trash Bins",
                        style={"margin-bottom": "0px",
                               'font-weight': 'bold'},
                    ),
                ],
                className="three column",
                id="title",
            ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [html.Div(
                className="pretty_container_2 two columns"),
                html.Div(
                    [
                        dcc.RadioItems(
                            id="data_type",
                            options=[
                                # radio button #1
                                {'label': 'All ', 'value': 'all'},
                                # radio button #2
                                {'label': 'Last Measurements', 'value': 'active'},
                                # radio button #3
                                {'label': 'Sensors with Problematic Measurements',
                                    'value': 'failure'},
                            ],
                            value='all',
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        )
                    ],
                    # ==========================================
                    className="pretty_container eight columns",
                    id="cross-filter-options",
            ),
                html.Div(
                    className="pretty_container_2 two columns"),
            ],
            className="row flex-display ",
        ),
        html.Div(
            [html.Div([
                dcc.Graph(id='live-update-graph',
                          config={'displayModeBar': False, 'scrollZoom': True}),
                dcc.Interval(id='interval-component',
                             interval=10*1000,  # in milliseconds
                             n_intervals=0
                             )
            ], className="pretty_container twelve columns"),
            ],
            className="row flex-display",
        )
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


########################################################

# Start of : All, Active, In Active Display


@ app.callback(Output('live-update-graph', 'figure'), [Input('interval-component', 'n_intervals'), Input('data_type', 'value')])
def update_graph_live(n, x):
    if x == "all":
        all_trashbin_query = get_all("public", "trashbin")
        fig = px.scatter_mapbox(all_trashbin_query,
                                title="All Trash-Bins in Moers",
                                lat="latitude",
                                lon="longitude",
                                hover_name="bin_id",
                                hover_data=["number_of_container", "place"],
                                zoom=12, height=900, size_max=5,)
        fig.update_layout(mapbox_style="open-street-map", title_x=0.5,
                          title_y=0.97, font_size=16,)
        fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    if x == "active":
        df6 = get_active("public", "_dynamic_pivot")
        print(df6.columns.values.tolist())
        fig = px.scatter_mapbox(df6,
                                title="Last measurements of the devices",
                                lat="latitude",
                                lon="longitude",
                                hover_name="bin_id",
                                hover_data=
                                    df6.columns.values.tolist(),
                                color='dev_eui',
                                color_continuous_scale=px.colors.sequential.YlOrRd,
                                zoom=15,
                                height=900,
                                size_max=5,)
        fig.update_layout(mapbox_style="open-street-map",  title_x=0.5,
                          title_y=0.97, font_size=16)
        fig.update_layout(margin={
                          "r": 0, "t": 50, "l": 0, "b": 0})
    if x == "failure":
        df6 = get_failure("public", "vi_prob_meas")
        fig = px.scatter_mapbox(df6,
                                title="Devices with missing measurements",
                                lat="latitude",
                                lon="longitude",
                                hover_name="bin_id",
                                hover_data=[
                                    "last_date", "measurement"],
                                color='dev_eui',
                                color_continuous_scale=px.colors.sequential.YlOrRd,
                                zoom=15,
                                height=900,
                                size_max=5,)
        fig.update_layout(mapbox_style="open-street-map",  title_x=0.5,
                          title_y=0.97, font_size=16)
        fig.update_layout(margin={
            "r": 0, "t": 50, "l": 0, "b": 0})

    return fig


# End of : All, Active, In Active Display
########################################################
"""
@ app.callback(
    Output("line-graph_meas", "figure"),
    [Input('interval-component', 'n_intervals'), Input('channel', 'value')]
)

def update_time(n, ch):

    if ch == "distance":
        df5 = get_distance("public", "vi_last_meas")
        fig = px.scatter_mapbox(df5,
                                title="Distance",
                                lat="latitude",
                                lon="longitude",
                                hover_name="channel",
                                hover_data=["last_date", "measurement"],
                                color='dev_eui', zoom=12, height=500, size_max=5,)
        fig.update_layout(mapbox_style="open-street-map", title_x=0.5,
                          title_y=0.95, font_size=16,)
        fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

    if ch == "temperature":

        df5 = get_temperature("public", "vi_last_meas")
        fig = px.scatter_mapbox(df5,
                                title="Temperature",
                                lat="latitude",
                                lon="longitude",
                                hover_name="channel",
                                hover_data=["last_date", "measurement"],
                                color='dev_eui', zoom=12, height=500, size_max=5,)
        fig.update_layout(mapbox_style="open-street-map", title_x=0.5,
                          title_y=0.95, font_size=16,)
        fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

    return fig
"""

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
