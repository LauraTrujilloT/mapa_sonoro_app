from dash import html
from dash import dcc
from pages.hyy.hyy_data import hyy_dataframe
import dash_bootstrap_components as dbc

controls = dbc.Card(
    [
        dbc.Card(
            [
                dbc.Label("Sample"),
                dcc.Dropdown(
                    id="hyy-variable",
                    options=[
                        {"label": col, "value": col} for col in hyy_dataframe().columns
                    ],
                    value="sepal length (cm)",
                ),
            ]
        ),
        dbc.Card(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[
                        {"label": col, "value": col} for col in hyy_dataframe().columns
                    ],
                    value="sepal width (cm)",
                ),
            ]
        ),
    ],
    body=True,
)

layout = dbc.Container(
    [
        html.H1("HYY Analysis"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=3),
                dbc.Col(
                    html.Iframe(
                                id="hyy-graph", 
                                srcDoc=None,
                                style={'border-width': '5', 'width': '100%',
                                        'height': '500px'}
                            ), md=9),
            ],
            align="center",
        ),
        html.Hr(),
        dbc.Row(
            dbc.Col(
                align="center",
                id="col-hyy")
        )
    ],
    fluid=True,
)
''' 
layout = html.Div([
    html.H1("HYY Analysis"),
    html.Hr(),
    html.Iframe(
                id='hyy-graph', 
                srcDoc=None,
                style={'border-width': '5', 'width': '100%',
                       'height': '500px'}
                ),
    dcc.Slider(
        id='myy-slider',
        min=hyy_dataframe()['myy'].min(),
        max=hyy_dataframe()['myy'].max(),
        value=hyy_dataframe()['myy'].min(),
        marks={str(myy): str(myy) for myy in hyy_dataframe()['myy'].unique()},
        step=None
    )
])
'''